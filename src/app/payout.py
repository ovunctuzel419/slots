import copy
from typing import List, Optional, Dict, Tuple

import attrs
import numpy as np
from attrs import define

from app.csv_reader import CSVReader
from app.ruleset import Ruleset, PayoutEstimate
from fixture.predefined_slots import SlotsGame, BELLS
from fixture.predefined_rulesets import predefined_rulesets
from utils.common import csv_rows_to_icon_sets_batch_from_rows_cols
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
    _csv_reader: CSVReader = CSVReader()
    _icon_sets: List[IconSet] = attrs.field(factory=list)
    _payout_cache: Dict[int, PayoutEstimate] = attrs.field(factory=dict)
    _lru_cache: Dict[Tuple[int, int], PayoutEstimate] = attrs.field(factory=dict)
    _current_free_spins: int = 0
    _multiplier_2x_remaining: int = 0

    @classmethod
    def from_game(cls, game: SlotsGame, csv_reader: Optional[CSVReader] = None) -> Optional["PayoutEstimator"]:
        if game.name not in predefined_rulesets.keys():
            return None
        return cls(
            extract_csv_path=game.get_csv_filepath(),
            ruleset=predefined_rulesets[game.name],
            rows=game.rows,
            cols=game.cols,
            csv_reader=csv_reader or CSVReader(),
        )

    def __attrs_post_init__(self):
        print("Payout cache: ", self._payout_cache)
        rows = self._csv_reader.read_lines(self.extract_csv_path, skip_header=True)
        self._icon_sets = csv_rows_to_icon_sets_batch_from_rows_cols(rows, r=self.rows, c=self.cols)

    def reset(self):
        print("Payout cache cleared.")
        self._payout_cache = {}

    def estimate(self, position: int, iterations: int, bet: int) -> PayoutEstimate:
        start_index = position - 1
        end_index = start_index + iterations

        total = copy.deepcopy(self._payout_cache[start_index - 1]) if start_index - 1 in self._payout_cache else PayoutEstimate.no_reward()

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
            # Mystery multiplier is not cumulative
            total.mystery_multiplier_count = reward.mystery_multiplier_count
            # Column replace bonus is cleared if there is no streak
            if reward.next_round_column_replace_bonus == {}:
                total.next_round_column_replace_bonus = {}

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
