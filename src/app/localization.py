import csv
import os
import time
from enum import Enum
from typing import Tuple, List, Dict

import attrs
import numpy as np
from attrs import define

from app.csv_reader import CSVReader
from fixture.predefined_slots import SlotsGame, GANGSTER
from utils.common import csv_row_to_icon_set, csv_rows_to_icon_sets_batch
from utils.custom_types import IconSet


class PositionEstimationStatus(str, Enum):
    CONFIDENT = "CONFIDENT"
    UNCERTAIN = "UNCERTAIN"
    UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"


@define
class PositionEstimationResult:
    status: PositionEstimationStatus
    position: int = -1
    confidence: float = 0.0


@define
class PositionEstimator:
    slots_game: SlotsGame
    _csv_reader: CSVReader = CSVReader()
    _information: List[IconSet] = attrs.field(factory=list)
    _icon_sets: List[IconSet] = attrs.field(factory=list)
    _last_update_relative_reel_index: int = 0
    _cache: Dict[int, List[int]] = attrs.field(factory=dict)

    def __attrs_post_init__(self):
        # Skip the first header row
        rows = self._csv_reader.read_lines(self.slots_game.get_csv_filepath(), skip_header=True)
        # Skip the first column and convert to int
        self._icon_sets = csv_rows_to_icon_sets_batch(rows, slots_game=self.slots_game)

    def reset(self):
        self._information = []
        self._last_update_relative_reel_index = 0
        self._cache = {}

    def update(self, current_icon_set: IconSet, current_relative_reel_index: int) -> None:
        if np.any(current_icon_set == -1):
            return

        self._last_update_relative_reel_index = current_relative_reel_index
        if len(self._information) < current_relative_reel_index + 1:
            self._information.append(current_icon_set)
        elif len(self._information) > current_relative_reel_index + 1:
            print(f"Overwriting information {current_relative_reel_index}")
            self._information[current_relative_reel_index] = current_icon_set
        else:
            print(f"WARNING: Unexpected current_relative_reel_index {current_relative_reel_index}")

    def get_position_estimate(self) -> PositionEstimationResult:
        if self._last_update_relative_reel_index in self._cache:
            # Cache hit
            candidates = self._cache[self._last_update_relative_reel_index]
        else:
            # Cache miss
            candidates = []
            information_len = len(self._information)
            for i in range(len(self._icon_sets) - information_len + 1):
                match = True
                for j in range(information_len):
                    if not np.array_equal(self._information[j], self._icon_sets[i + j]):
                        match = False
                        break
                if match:
                    candidates.append(i + information_len - 1 + 1)  # The final +1 is due to the reels being 1-indexed
            self._cache[self._last_update_relative_reel_index] = candidates

        if len(candidates) == 0:
            print("No match found. Position estimation failed.")
            return PositionEstimationResult(PositionEstimationStatus.ERROR)
        if len(candidates) > 1:
            return PositionEstimationResult(PositionEstimationStatus.UNCERTAIN, candidates[0], 1.0 / len(candidates))
        return PositionEstimationResult(PositionEstimationStatus.CONFIDENT, candidates[0], 1.0)


if __name__ == '__main__':
    game = GANGSTER
    estimator = PositionEstimator(game)

    test_input_1 = csv_row_to_icon_set([20, 7, 7, 7, 4, 8, 9, 10, 2, 5, 2, 10, 7, 4, 1, 10], game)
    test_input_2 = csv_row_to_icon_set([21, 7, 10, 2, 3, 5, 7, 4, 3, 5, 8, 6, 3, 3, 4, 1], game)
    test_input_3 = csv_row_to_icon_set([22, 8, 9, 0, 7, 7, 7, 6, 7, 9, 2, 10, 3, 7, 7, 7], game)

    estimator.update(test_input_1, 0)
    print(estimator.get_position_estimate())

    estimator.update(test_input_1, 5)
    print(estimator.get_position_estimate())

    estimator.update(test_input_2, 1)
    print(estimator.get_position_estimate())

    estimator.update(test_input_3, 2)
    print(estimator.get_position_estimate())
