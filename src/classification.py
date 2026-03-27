import os
import time
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
class TrainedClassifier:
    model_path: str
    rows: int
    cols: int
    debug: bool = False
    _model: torch.nn.Module = attr.field(init=False)
    _class_index_to_name: Dict[int, str] = attr.field(init=False)
    _icon_index_total: int = 0
    _imagenet_mean: torch.Tensor = torch.tensor([0.485, 0.456, 0.406], device="cuda").view(1, 3, 1, 1) * 255
    _imagenet_std: torch.Tensor = torch.tensor([0.229, 0.224, 0.225], device="cuda").view(1, 3, 1, 1) * 255


    def __attrs_post_init__(self):
        checkpoint = torch.load(self.model_path)
        self._class_index_to_name = {i: name for i, name in enumerate(checkpoint['classes'])}

        # Resnet
        model = torchvision.models.resnet18(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, len(self._class_index_to_name))

        # Mobilenet
        # model = torchvision.models.mobilenet_v2(pretrained=False)
        # model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(self._class_index_to_name))

        model.load_state_dict(checkpoint['model'])
        self._model = model.cuda().eval()
        self._model = self._model.half()

    def classify(self, icon: BGRImageArray) -> Tuple[int, float]:
        self._icon_index_total += 1

        input_tensor = self._preprocess(icon).cuda().half()
        with torch.no_grad():
            logits = self._model(input_tensor)
            probs = F.softmax(logits, dim=1).squeeze()
            pred_index = torch.argmax(probs).item()
            confidence = probs[pred_index].item()

        if self.debug:
            print("This is a", self._class_index_to_name[pred_index])
            print(f"Confidence: {confidence:.4f}")

        if confidence < 0.85:
            model_suffix = os.path.basename(self.model_path).split(".")[0]
            os.makedirs('../ambiguous', exist_ok=True)
            os.makedirs(f'../ambiguous/{model_suffix}', exist_ok=True)

            filename = f"../ambiguous/{model_suffix}/{self._icon_index_total}_{self._class_index_to_name[pred_index]}.png"
            cv2.imwrite(filename, icon)
            print("WARNING: LOW CONFIDENCE")
            print(f"Confidence: {confidence:.4f}")
        return pred_index, confidence

    def classify_batch(self, icon_list: List[BGRImageArray]) -> List[Tuple[int, float]]:
        # GPU friendly preprocessing
        resized = [cv2.resize(cv2.cvtColor(icon, cv2.COLOR_BGR2RGB), (224, 224)) for icon in icon_list]
        batch = np.stack(resized)  # (N, H, W, C)
        tensor = torch.from_numpy(batch).cuda().float()  # (N, H, W, C)
        tensor = tensor.permute(0, 3, 1, 2)  # (N, C, H, W)
        tensor = (tensor - self._imagenet_mean) / self._imagenet_std
        input_tensor = tensor.half()

        with torch.no_grad():
            logits = self._model(input_tensor)
            probs = F.softmax(logits, dim=1).squeeze()
            pred_indices = torch.argmax(probs, dim=1)
            confidences = probs[torch.arange(len(icon_list)), pred_indices]

        for i in range(len(icon_list)):
            frame_index = int(self._icon_index_total / (self.rows * self.cols))
            icon_index = self._icon_index_total % (self.rows * self.cols)
            if confidences[i] < 0.85:
                model_suffix = os.path.basename(self.model_path).split(".")[0]
                os.makedirs(f'../ambiguous/{model_suffix}', exist_ok=True)
                filename = f"../ambiguous/{model_suffix}/{frame_index}_{icon_index}_{self._class_index_to_name[pred_indices[i].item()]}.png"
                cv2.imwrite(filename, icon_list[i])
                print("WARNING: LOW CONFIDENCE")
                print(f"Confidence: {confidences[i]:.4f}")
            self._icon_index_total += 1

        return list(zip(pred_indices.tolist(), confidences.tolist()))


    def _preprocess(self, icon: BGRImageArray) -> torch.Tensor:
        icon = cv2.resize(icon, (224, 224))
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        icon = (icon - mean) / std
        tensor = torch.from_numpy(icon).permute(2, 0, 1).unsqueeze(0).float()
        return tensor
