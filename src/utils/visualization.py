import os

import cv2
import numpy as np

from fixture.legend import get_class_icons
from utils.custom_types import IconSet, BGRImageArray


def visualize_icon_set(icon_set: IconSet, dataset_root: str, cell_size: int = 128) -> BGRImageArray:
    class_icons = get_class_icons(dataset_root)

    canvas = np.zeros((icon_set.shape[0] * cell_size, icon_set.shape[1] * cell_size, 3), dtype=np.uint8)
    for row in range(icon_set.shape[0]):
        for col in range(icon_set.shape[1]):
            class_index = icon_set[row][col]
            icon = class_icons[class_index]
            resized_icon = cv2.resize(icon, (cell_size, cell_size))
            canvas[row * cell_size: (row + 1) * cell_size, col * cell_size: (col + 1) * cell_size] = resized_icon

    return canvas


