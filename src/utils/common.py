from typing import List, Union

import numpy as np

from fixture.predefined_slots import SlotsGame
from utils.custom_types import IconSet


def csv_row_to_icon_set(row: Union[List[str], List[int]], slots_game: SlotsGame) -> IconSet:
    icon_set_flat = np.array([int(icon) for icon in row[1:]])
    return icon_set_flat.reshape(slots_game.cols, slots_game.rows).T
