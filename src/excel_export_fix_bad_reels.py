import os
import csv
import time

from classification import TrainedClassifier
from fixture.predefined_extractors import extractor_map
from fixture.predefined_slots import FRUIT, MUMMY, REELS

if __name__ == '__main__':
    slots_game = REELS
    output_file = f'{slots_game.name}.csv'
    num_rows = 3
    num_cols = 5
    extractor = extractor_map[slots_game.name]
    classifier = TrainedClassifier(slots_game.model_path)

    t = time.monotonic()
    with open(output_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['frame_index'] + [f'icon_c{c}_r{r}' for c in range(num_cols) for r in range(num_rows)]
        writer.writerow(header)

        for i, frame in enumerate(extractor.extract_frames()):
            frame_index = i + 1 + 411570
            print("Processing frame", frame_index)
            icons = extractor.icon_extractor.extract_icons(frame)
            predictions = classifier.classify_batch(icons)
            icon_indices = [prediction[0] for prediction in predictions]

            # Convert row-major (default) to column-major
            icon_grid = [icon_indices[r * num_cols + c] for c in range(num_cols) for r in range(num_rows)]
            writer.writerow([frame_index] + icon_grid)

    print(f"Time taken: {(time.monotonic() - t)} seconds for 1000 frames.")

    print(f"Done. Output saved to {output_file}.")
