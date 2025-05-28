import csv
import pickle
from random import random
from typing import List, Optional, Dict

import attrs
import numpy as np
from attrs import define

from app.ruleset import Ruleset
from fixture.predefined_rulesets import predefined_rulesets
from fixture.predefined_slots import SlotsGame
from utils.custom_types import IconSet


@define
class PayoutEstimator:
    extract_csv_path: str
    ruleset: Ruleset
    rows: int
    cols: int
    use_disk_cache: bool = True
    _icon_sets: List[IconSet] = attrs.field(factory=list)
    _payout_cache: Dict[int, int] = attrs.field(factory=dict)


    @classmethod
    def from_game(cls, game: SlotsGame) -> Optional["PayoutEstimator"]:
        if game.name not in predefined_rulesets.keys():
            return None
        return PayoutEstimator(extract_csv_path=game.get_csv_filepath(),
                               ruleset=predefined_rulesets[game.name],
                               rows=game.rows,
                               cols=game.cols)

    def __attrs_post_init__(self):
        # Skip the first header row
        rows = list(csv.reader(open(self.extract_csv_path)))[1:]
        # Skip the first column and convert to int
        self._icon_sets = np.array([[int(x) for x in row[1:]] for row in rows if row]).reshape(-1, self.cols, self.rows).transpose(0, 2, 1)
        self._load_payouts()

    def _load_payouts(self):
        if self.use_disk_cache:
            self._payout_cache = pickle.load(open(f"{self.extract_csv_path}.payouts", "rb"))
            return

        for i, icon_set in enumerate(self._icon_sets):
            self._payout_cache[i] = self.ruleset.calculate_payout(icon_set)

        if self.use_disk_cache:
            pickle.dumps(self._payout_cache, open(f"{self.extract_csv_path}.payouts", "wb"))

    def estimate(self, position: int, iterations: int) -> int:
        # Position is zero-indexed, but slots are 1-indexed
        total_payout = 0
        for i in range(iterations):
            total_payout += self._payout_cache[position + i - 1]
        return total_payout

    def check_bonus(self, position: int) -> bool:
        return random() < 0.1  # TODO: implement this
