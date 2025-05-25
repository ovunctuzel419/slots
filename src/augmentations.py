import os
import random
import shutil

import cv2
import numpy as np

from fixture.predefined_slots import MUMMY, REELS, DRAGON, MAJESTIC, BELLS, GANGSTER, BLAZINGFRUITS
from utils.custom_types import BGRImageArray


def paste_augment(image: BGRImageArray, image_to_paste: BGRImageArray):
    h, w = image.shape[:2]

    # Randomly flip the image
    if random.random() < 0.5:
        image_to_paste = cv2.flip(image_to_paste, 1)

    # Random scale factor
    scale = random.uniform(2.0, 5.0)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image_to_paste, (new_w, new_h))

    # Ensure 3 channels
    if resized.shape[2] == 4:
        resized = cv2.cvtColor(resized, cv2.COLOR_BGRA2BGR)

    # Crop to match original image size
    x_offset = random.randint(0, new_w - w)
    y_offset = random.randint(0, new_h - h)
    cropped = resized[y_offset:y_offset + h, x_offset:x_offset + w]

    # Blend
    alpha = random.uniform(0.1, 0.65)
    blended = cv2.addWeighted(image, 1 - alpha, cropped, alpha, 0)
    return blended


def blur_augment(image: BGRImageArray):
    strength = random.uniform(0.1, 5.0)
    return cv2.GaussianBlur(image, (0, 0), strength)


def translate_augment(image: BGRImageArray):
    x_offset = random.randint(-10, 10)
    y_offset = random.randint(-10, 10)
    return cv2.warpAffine(image, np.float32([[1, 0, x_offset], [0, 1, y_offset]]), (image.shape[1], image.shape[0]))


def brightness_augment(image: BGRImageArray):
    brightness = random.uniform(0.5, 1.5)
    return cv2.convertScaleAbs(image, alpha=brightness, beta=0)


def augment_dataset(dataset_path: str, iters: int = 1):
    augmented_dataset_path = dataset_path + '_augmented'
    shutil.rmtree(augmented_dataset_path, ignore_errors=True)
    shutil.copytree(dataset_path, augmented_dataset_path)
    circle = cv2.imread('../assets/circlearrow.png', cv2.IMREAD_UNCHANGED)

    for class_name in os.listdir(augmented_dataset_path):
        class_dir = os.path.join(augmented_dataset_path, class_name)

        max_sample_index = max(int(file_name.split('.')[0]) for file_name in os.listdir(class_dir))
        new_index = max_sample_index + 1
        for file_name in os.listdir(class_dir):
            for _ in range(iters):
                file_path = os.path.join(class_dir, file_name)
                image = cv2.imread(file_path)
                augmented_image = random.choice([paste_augment(image, circle),
                                                 blur_augment(image),
                                                 translate_augment(image),
                                                 brightness_augment(image)])
                augmented_file_path = os.path.join(class_dir, f'{new_index}.png')
                cv2.imwrite(augmented_file_path, augmented_image)
                new_index += 1


# if __name__ == '__main__':
#     icon = cv2.imread('../dataset/GX010010.MP4/0-cherry/1.png')
#     circle = cv2.imread('../assets/circlearrow.png', cv2.IMREAD_UNCHANGED)  # preserve alpha if any
#
#     before = icon.copy()
#     for i in range(100):
#
#         cv2.imshow('augmentation', np.hstack((before, paste_augment(icon, circle))))
#         cv2.waitKey()
#         cv2.imshow('augmentation', np.hstack((before, blur_augment(icon))))
#         cv2.waitKey()
#         cv2.imshow('augmentation', np.hstack((before, translate_augment(icon))))
#         cv2.waitKey()
#         cv2.imshow('augmentation', np.hstack((before, brightness_augment(icon))))
#         cv2.waitKey()

if __name__ == '__main__':
    augment_dataset(BLAZINGFRUITS.dataset_folder_path.replace('_augmented', ''), 9)
