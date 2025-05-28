import os

import cv2
import numpy as np

from classification import TrainedClassifier
from fixture.predefined_rulesets import predefined_rulesets
from fixture.predefined_slots import BLAZINGFRUITS
from fixture.predefined_extractors import extractor_map
from utils.visualization import visualize_icon_set


if __name__ == "__main__":
    slots_game = BLAZINGFRUITS
    ruleset = predefined_rulesets[slots_game.name]
    bet = 50
    extractor = extractor_map[slots_game.name]
    rows = extractor.icon_extractor.grid_crop.rows
    cols = extractor.icon_extractor.grid_crop.cols

    classifier = TrainedClassifier(slots_game.model_path, rows=rows, cols=cols, debug=True)
    for i, frame in enumerate(extractor.extract_frames()):
        frame_index = i + 1

        icons = extractor.icon_extractor.extract_icons(frame)
        predictions = classifier.classify_batch(icons)
        icon_indices = [prediction[0] for prediction in predictions]
        icon_confidences = [prediction[1] for prediction in predictions]
        icon_set = np.array(icon_indices).reshape((rows, cols))
        prediction = visualize_icon_set(icon_set, slots_game.dataset_folder_path, cell_size=128)
        payout = ruleset.calculate_payout(icon_set) * bet

        viz = np.vstack((np.zeros((100, prediction.shape[1], 3), dtype=np.uint8), prediction))
        cv2.putText(viz, f'Frame {frame_index}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, lineType=cv2.LINE_AA)
        cv2.putText(viz, f'Bet: {bet}  Payout: {payout}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, lineType=cv2.LINE_AA)

        cv2.imshow('Payout', viz)

        key = cv2.waitKey()
