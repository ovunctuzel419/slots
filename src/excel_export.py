import os
import csv
import time

from classification import TrainedClassifier
from fixture.predefined_extractors import extractor_map
from fixture.predefined_slots import BLAZINGHOT7, MUMMY, REELS, DRAGON, MAJESTIC, BELLS, GANGSTER, BLAZINGFRUITS, MEGAREELS, \
    DISCO, CRYSTALTREASURE, REELSDELUXE, VULCAN, ICEDFRUITS

if __name__ == '__main__':
    slots_game = VULCAN
    output_file = f'{slots_game.name}.csv'

    extractor = extractor_map[slots_game.name]
    num_rows = extractor.icon_extractor.grid_crop.rows
    num_cols = extractor.icon_extractor.grid_crop.cols
    classifier = TrainedClassifier(slots_game.model_path, rows=extractor.icon_extractor.grid_crop.rows, cols=extractor.icon_extractor.grid_crop.cols, debug=True)

    t = time.monotonic()
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['frame_index'] + [f'icon_c{c}_r{r}' for c in range(num_cols) for r in range(num_rows)]
        writer.writerow(header)

        initial_frame = 1
        frame_index = initial_frame
        for i, (frame, ocr_index) in enumerate(extractor.extract_frames()):
            if ocr_index and ocr_index != frame_index:
                print(f"ERROR: Recognized index ({ocr_index}) is different from calculated index ({frame_index}).")
                while frame_index < ocr_index:
                    writer.writerow([frame_index] + [-1 for _ in range(num_cols * num_rows)])
                    frame_index += 1

            print("Processing frame", frame_index)
            icons = extractor.icon_extractor.extract_icons(frame)
            predictions = classifier.classify_batch(icons)
            icon_indices = [prediction[0] for prediction in predictions]

            # Convert row-major (default) to column-major
            icon_grid = [icon_indices[r * num_cols + c] for c in range(num_cols) for r in range(num_rows)]
            writer.writerow([frame_index] + icon_grid)
            frame_index += 1


    print(f"Time taken: {(time.monotonic() - t)} seconds for 1000 frames.")

    print(f"Done. Output saved to {output_file}.")
