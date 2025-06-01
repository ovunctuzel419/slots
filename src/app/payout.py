import copy
import csv
import os
from typing import List, Optional, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor
import pickle

import attrs
import numpy as np
from tqdm import tqdm
from attrs import define

from app.ruleset import Ruleset, PayoutEstimate
from fixture.predefined_slots import SlotsGame, BELLS
from fixture.predefined_rulesets import predefined_rulesets
from utils.custom_types import IconSet


def calculate_row_payout(args: Tuple[int, List[int], int, int, Ruleset]) -> Tuple[int, PayoutEstimate]:
    i, flat_row, rows, cols, ruleset = args
    print('Calculating payout for row', i)
    icon_set = np.array(flat_row).reshape(cols, rows).T
    payout = ruleset.calculate_payout(icon_set)
    return i, payout


@define
class PayoutEstimator:
    extract_csv_path: str
    ruleset: Ruleset
    rows: int
    cols: int
    use_disk_cache: bool = False
    _icon_sets: List[IconSet] = attrs.field(factory=list)
    _payout_cache: Dict[int, PayoutEstimate] = attrs.field(factory=dict)
    _lru_cache: Dict[Tuple[int, int], PayoutEstimate] = attrs.field(factory=dict)
    _current_free_spins: int = 0
    _multiplier_2x_remaining: int = 0

    @classmethod
    def from_game(cls, game: SlotsGame) -> Optional["PayoutEstimator"]:
        if game.name not in predefined_rulesets.keys():
            return None
        return cls(
            extract_csv_path=game.get_csv_filepath(),
            ruleset=predefined_rulesets[game.name],
            rows=game.rows,
            cols=game.cols,
        )

    def __attrs_post_init__(self):
        rows = list(csv.reader(open(self.extract_csv_path)))[1:]
        self._icon_sets = np.array([[int(x) for x in row[1:]] for row in rows if row]).reshape(-1, self.cols, self.rows).transpose(0, 2, 1)

    def reset(self):
        self._payout_cache = {}

    def estimate(self, position: int, iterations: int, bet: int) -> PayoutEstimate:
        start_index = position - 1
        end_index = start_index + iterations

        total = self._payout_cache.get(start_index - 1, PayoutEstimate.no_reward())

        for i in range(start_index, end_index):
            if i in self._payout_cache:
                total = copy.deepcopy(self._payout_cache[i])
                continue

            if i >= len(self._icon_sets):
                break

            icon_set_i = self._icon_sets[i].copy()

            # 1. Pay for the spin (unless free)
            if total.free_games > 0:
                total.free_games -= 1
            else:
                total.payout -= 1

            # 2. Apply column replacement bonus
            if total.next_round_column_replace_bonus:
                for col, symbol in total.next_round_column_replace_bonus.items():
                    icon_set_i[:, col] = symbol

            # 3. Get raw reward
            reward = self.ruleset.calculate_payout(icon_set_i)

            # 4. Apply multiplier
            if total.multiplier_2x > 0:
                reward.payout *= 2
                total.multiplier_2x = max(0, total.multiplier_2x - 1)

            # 5. Accumulate
            total += reward
            total.mystery_multiplier_count = reward.mystery_multiplier_count  # This is not cumulative

            # Cache total at this index
            self._payout_cache[i] = copy.deepcopy(total)

        # Scale for bet amount
        return PayoutEstimate(
            payout=int(round(total.payout * bet)),
            free_games=total.free_games,
            multiplier_2x=total.multiplier_2x,
            mystery_multiplier_count=total.mystery_multiplier_count,
            next_round_column_replace_bonus=total.next_round_column_replace_bonus
        )



if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    estimator = PayoutEstimator.from_game(BELLS)
