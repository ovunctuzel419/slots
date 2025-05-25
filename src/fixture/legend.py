import os
from typing import List

import cv2
import numpy as np

from fixture.predefined_slots import SlotsGame, DEMO, FRUIT, MUMMY, REELS
from utils.custom_types import BGRImageArray


def black_frame(image: BGRImageArray, frame_thickness: int = 4) -> BGRImageArray:
    image[:frame_thickness, :] = (0, 0, 0)
    image[-frame_thickness:, :] = (0, 0, 0)
    image[:, :frame_thickness] = (0, 0, 0)
    image[:, -frame_thickness:] = (0, 0, 0)
    return image


def get_class_icons(dataset_root: str) -> List[BGRImageArray]:
    return [cv2.imread(icon_path) for icon_path in get_class_icon_paths(dataset_root)]


def get_class_icon_paths(dataset_root: str) -> List[str]:
    print(os.getcwd())
    classes = os.listdir(dataset_root)
    paths = []
    for klass in classes:
        first_icon_in_folder = os.listdir(os.path.join(dataset_root, klass))[0]
        icon_path = os.path.join(dataset_root, klass, first_icon_in_folder)
        paths.append(icon_path)

    return paths


def create_legend(slots_game: SlotsGame) -> BGRImageArray:
    os.chdir('../')
    dataset_root = slots_game.dataset_folder_path
    classes = os.listdir(dataset_root)
    class_icons = get_class_icons(slots_game, dataset_root)

    row_h = 32
    w = 320
    canvas = np.zeros((row_h * len(class_icons), w, 3), dtype=np.uint8)
    for i, icon in enumerate(class_icons):
        icon = cv2.resize(icon, (row_h, row_h))
        icon = black_frame(icon, frame_thickness=3)
        canvas[row_h * i:row_h * (i + 1), :row_h] = icon
        cv2.putText(canvas, classes[i], (row_h + 16, row_h * i + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2, lineType=cv2.LINE_AA)

    # Add title
    title_card = np.zeros((64, w, 3), dtype=np.uint8)
    cv2.putText(title_card, slots_game.name, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, lineType=cv2.LINE_AA)
    cv2.line(title_card, (0, 48), (w, 48), (100, 100, 100), 2)
    canvas = np.vstack((title_card, canvas))

    return canvas


if __name__ == '__main__':
    slots_game = FRUIT
    legend = create_legend(slots_game)
    cv2.imshow('legend', legend)
    cv2.waitKey()
    os.makedirs('../legends', exist_ok=True)
    cv2.imwrite(f'../legends/legend_{slots_game.name}.png', legend)
