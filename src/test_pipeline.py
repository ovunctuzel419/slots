import os

import cv2
import numpy as np

from classification import TrainedClassifier
from fixture.predefined_extractors import extractor_map
from fixture.predefined_slots import DEMO, FRUIT, MUMMY, REELS, DRAGON, MAJESTIC, GANGSTER, BLAZINGFRUITS
from utils.visualization import visualize_icon_set


# 5535
if __name__ == '__main__':
    slots_game = BLAZINGFRUITS
    dataset_path = slots_game.dataset_folder_path
    extractor = extractor_map[slots_game.name]
    rows = extractor.icon_extractor.grid_crop.rows
    cols = extractor.icon_extractor.grid_crop.cols

    classifier = TrainedClassifier(slots_game.model_path, rows=rows, cols=cols, debug=True)
    for i, frame in enumerate(extractor.extract_frames()):
        frame_index = i + 1
        print("Processing frame: ", frame_index)

        icons = extractor.icon_extractor.extract_icons(frame)
        predictions = classifier.classify_batch(icons)
        icon_indices = [prediction[0] for prediction in predictions]
        icon_confidences = [prediction[1] for prediction in predictions]
        icon_set = np.array(icon_indices).reshape((rows, cols))
        prediction = visualize_icon_set(icon_set, dataset_path, cell_size=128)
        print(icon_set)

        cv2.putText(frame, f'frame {frame_index}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.imshow('prediction', prediction)
        key = cv2.waitKey()
