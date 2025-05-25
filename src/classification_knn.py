import os
import uuid
from collections import defaultdict
from typing import List, Dict, Tuple, Counter

import attr
import cv2
import numpy as np
import torch
import torch.nn.functional as F
import torchvision
from attr import define

from utils.custom_types import BGRImageArray


@define
class Classifier:
    dataset_dir: str
    debug: bool = False
    _model: torch.nn.Module = attr.field(init=False)
    _known_classes: Dict[int, List[torch.Tensor]] = attr.field(init=False, factory=dict)
    _class_index_to_name: Dict[int, str] = attr.field(init=False, factory=dict)
    _icon_index_total: int = 0

    def __attrs_post_init__(self):
        self._model = torchvision.models.resnet18(pretrained=True)
        self._model.fc = torch.nn.Identity()
        self._model = self._model.cuda()
        self._model.eval()
        self.build_lookup()

    def build_lookup(self):
        self._known_classes = {}
        for class_folder in os.listdir(self.dataset_dir):
            class_index = int(class_folder.split('-')[0])
            class_name = class_folder.split('-')[1]
            class_path = os.path.join(self.dataset_dir, class_folder)
            self._class_index_to_name[class_index] = class_name
            for icon_name in os.listdir(class_path):
                icon_path = os.path.join(class_path, icon_name)
                icon = cv2.imread(icon_path)
                features = self.extract_features(icon)
                self._known_classes.setdefault(class_index, []).append(features)

    def extract_features(self, icon: BGRImageArray) -> torch.Tensor:
        input_tensor = self._preprocess(icon).cuda()
        with torch.no_grad():
            features = self._model(input_tensor)
        return features.squeeze()

    from collections import Counter

    def classify(self, icon: BGRImageArray, k: int = 5) -> Tuple[int, float]:
        self._icon_index_total += 1

        test_feat = self.extract_features(icon).cuda()

        all_feats = []
        all_labels = []

        for class_index, feature_list in self._known_classes.items():
            all_feats.extend(feature_list)
            all_labels.extend([class_index] * len(feature_list))

        feats_tensor = torch.stack(all_feats).cuda()
        labels_tensor = torch.tensor(all_labels).cuda()

        dists = torch.norm(feats_tensor - test_feat, dim=1)  # (N,)
        knn_indices = torch.topk(dists, k=min(k, len(dists)), largest=False).indices
        knn_labels = labels_tensor[knn_indices]
        knn_dists = dists[knn_indices]

        # Compute softmax weights (closer = higher)
        weights = torch.nn.functional.softmax(-knn_dists, dim=0)

        # Accumulate weighted votes
        class_scores = defaultdict(float)
        for label, weight in zip(knn_labels.tolist(), weights.tolist()):
            class_scores[label] += weight

        best_index = max(class_scores.items(), key=lambda x: x[1])[0]
        confidence = class_scores[best_index]

        if self.debug:
            print("This is a", self._class_index_to_name[best_index])
            print(f"Confidence (soft-kNN): {confidence:.4f}")
            print("\nNeighbor details:")
            for rank, (idx, weight) in enumerate(zip(knn_indices, weights)):
                label = labels_tensor[idx].item()
                dist = dists[idx].item()
                name = self._class_index_to_name[label]
                is_winner = "(winner)" if label == best_index else ""
                print(f"#{rank + 1}: {name:<15} dist={dist:.4f} weight={weight:.4f} {is_winner}")
        if confidence < 0.7:
            # cv2.imshow('LOW CONFIDENCE ICON', icon)
            # cv2.waitKey(0)
            frame_index = int(self._icon_index_total / 15)
            icon_index = self._icon_index_total % 15
            cv2.imwrite(f'../ambiguous/{frame_index}_{icon_index}_{self._class_index_to_name[best_index]}_{confidence:.4f}.png', icon)
            print("WARNING: LOW CONFIDENCE")
            print(f"Confidence (soft-kNN): {confidence:.4f}")
            print("\nNeighbor details:")
            for rank, (idx, weight) in enumerate(zip(knn_indices, weights)):
                label = labels_tensor[idx].item()
                dist = dists[idx].item()
                name = self._class_index_to_name[label]
                is_winner = "(winner)" if label == best_index else ""
                print(f"#{rank + 1}: {name:<15} dist={dist:.4f} weight={weight:.4f} {is_winner}")
            # raise ValueError("LOW CONFIDENCE")

        return best_index, confidence


    def _preprocess(self, icon: BGRImageArray) -> torch.Tensor:
        # Resize to 224x224
        icon = cv2.resize(icon, (224, 224))
        # BGR → RGB
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        # Normalize using ImageNet mean/std
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        icon = (icon - mean) / std
        # Convert to tensor: HWC → CHW → BCHW
        tensor = torch.from_numpy(icon).permute(2, 0, 1).unsqueeze(0).float()
        return tensor
