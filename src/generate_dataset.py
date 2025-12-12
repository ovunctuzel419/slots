import os
import random
import sys
from operator import index

import cv2
import numpy as np

from classification import TrainedClassifier
from fixture.predefined_classes import predefined_classes
from fixture.predefined_extractors import extractor_map
from fixture.predefined_slots import DEMO, MUMMY, REELS, DRAGON, MAJESTIC, BELLS, GANGSTER, BLAZINGFRUITS, MEGAREELS, \
    DISCO, CRYSTALTREASURE, REELSDELUXE, VULCAN, ICEDFRUITS
from utils.custom_types import BGRImageArray


def save_icon(dataset_dir: str, icon: BGRImageArray, class_index: int, class_name: str) -> None:
    path_for_class = f'{dataset_dir}/{str(class_index).zfill(3)}-{class_name}'
    os.makedirs(path_for_class, exist_ok=True)
    existing_indices = [index.split('.')[0] for index in os.listdir(path_for_class)]
    max_index = max(int(index) for index in existing_indices) if existing_indices else 0
    sample_index = max_index + 1
    cv2.imwrite(f'{path_for_class}/{sample_index}.png', icon)


def augment_icon(icon: BGRImageArray) -> BGRImageArray:
    return icon


key_to_index = {ord('0'): 0,
                ord('1'): 1,
                ord('2'): 2,
                ord('3'): 3,
                ord('4'): 4,
                ord('5'): 5,
                ord('6'): 6,
                ord('7'): 7,
                ord('8'): 8,
                ord('9'): 9,
                ord('q'): 10,
                ord('w'): 11,
                ord('e'): 12,
                ord('r'): 13,
                ord('t'): 14,
                ord('y'): 15,
                ord('u'): 16,
                ord('i'): 17,
                ord('o'): 18,
            }
index_to_key = {value: key for key, value in key_to_index.items()}

if __name__ == '__main__':
    game = REELS
    video_path = game.video_folder_path
    extractor = extractor_map[game.name]
    # Optionally defined a classifier for active learning
    classifier = TrainedClassifier(game.model_path, rows=extractor.icon_extractor.grid_crop.rows, cols=extractor.icon_extractor.grid_crop.cols)

    classes = predefined_classes[game.name]
    print(f'Classes:\n' + str.join('\n', [f'{chr(index_to_key[index])}: {class_name}' for index, class_name in classes.items()]))
    sample_count_per_class = 20
    samples_per_class = {key: 0 for key in classes}
    for i, subframe in enumerate(extractor.extract_frames()):
        print(i)
        for j, icon in enumerate(extractor.icon_extractor.extract_icons(subframe)):
            # Active learning (Optional)
            if classifier:
                prediction, confidence = classifier.classify(icon)
                if confidence > 0.8:
                    # print(f"Already confident that this is a {classes[prediction]} ({confidence}). Skipping.")
                    continue

            # Sample difficult examples more
            # difficult_frame_indices = 3, 5
            # difficult_icon_indices = 5, 9, 10, 14, 15, 19
            # is_difficult_frame = any([(i % 9) in difficult_frame_indices])
            # is_difficult_icon = j in difficult_icon_indices
            # if not (is_difficult_icon and is_difficult_frame) and random.random() < 0.9:
            #     continue

            print(f'Frame {i}, Icon {j}')

            cv2.imshow('icon', icon)
            key = cv2.waitKey()
            print(f'Pressed {key}')
            cv2.imshow('icon', np.zeros(icon.shape, dtype=np.uint8))  # Clear canvas
            cv2.waitKey(1)

            if key == 27:
                break
            if key == ord('s'):
                continue
            elif key in key_to_index and key_to_index[key] in classes:
                key = key_to_index[key]
                print('Pressed', key, 'for', classes[key])
                samples_per_class[key] += 1
                if samples_per_class[key] >= sample_count_per_class:
                    print('Already have enough samples for', classes[key])
                    continue
                if all(samples_per_class[key] >= sample_count_per_class for key in classes):
                    print('Already have enough samples for all classes')
                    sys.exit(0)
                save_icon(f'../dataset/{os.path.basename(video_path)}', icon, key, classes[key])
