from typing import List, Union

import numpy as np

from fixture.predefined_slots import SlotsGame
from utils.custom_types import IconSet


def csv_row_to_icon_set(row: Union[List[str], List[int]], slots_game: SlotsGame) -> IconSet:
    icon_set_flat = np.array([int(icon) for icon in row[1:]])
    return icon_set_flat.reshape(slots_game.cols, slots_game.rows).T


def csv_rows_to_icon_sets_batch(rows: Union[List[List[str]], List[List[int]]], slots_game: SlotsGame) -> List[np.ndarray]:
    data = np.array(rows, dtype=int)[:, 1:]  # drop first column
    reshaped = data.reshape(-1, slots_game.cols, slots_game.rows)
    return [icon_set.T for icon_set in reshaped]


def csv_rows_to_icon_sets_batch_from_rows_cols(rows: Union[List[List[str]], List[List[int]]], r: int, c: int) -> List[np.ndarray]:
    data = np.array(rows, dtype=int)[:, 1:]  # drop first column
    reshaped = data.reshape(-1, c, r)
    return [icon_set.T for icon_set in reshaped]
