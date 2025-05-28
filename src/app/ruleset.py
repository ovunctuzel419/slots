from abc import abstractmethod, ABC
from typing import List

import numpy as np
from attrs import define

from utils.custom_types import IconSet

Line = List[int]


@define
class Rule(ABC):
    symbol_index: int
    payout: int

    @abstractmethod
    def calculate_payout(self, icon_set: IconSet, line: Line):
        pass

    def scores_every_line(self) -> bool:
        return True

    def only_this_can_score(self) -> bool:
        return False


@define
class MatchLeftRule(Rule):
    num_matches: int

    def calculate_payout(self, icon_set: IconSet, line: Line):
        symbols = icon_set[np.array(line), np.arange(len(line))]
        # print(f"These are the symbols matching this line {line}: ", symbols)
        # print(f"Full icon set:\n{icon_set}")
        next_differs = (self.num_matches == len(symbols) or symbols[self.num_matches] != self.symbol_index)
        if np.all(symbols[:self.num_matches] == self.symbol_index) and next_differs:
            return self.payout
        return 0


@define
class FixedConfigurationRule(Rule):
    expected_icon_set: IconSet

    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.all(icon_set == self.expected_icon_set):
            return self.payout
        return 0

    def only_this_can_score(self) -> bool:
        return True


@define
class AllSameRule(Rule):
    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.all(icon_set == self.symbol_index):
            return self.payout
        return 0

    def only_this_can_score(self) -> bool:
        return True

@define
class ScatterRule(Rule):
    num_matches: int

    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.sum(icon_set == self.symbol_index) == self.num_matches:
            return self.payout
        return 0

    def scores_every_line(self) -> bool:
        return False


@define
class Ruleset:
    lines: List[Line]
    rules: List[Rule]

    def calculate_payout(self, icon_set: IconSet):
        total_payout = 0
        # Check special rules
        for rule in [rule for rule in self.rules if rule.only_this_can_score()]:
            total_payout += rule.calculate_payout(icon_set, [])
            if total_payout > 0:
                return total_payout

        # For each line, calculate payout
        for line in self.lines:
            for rule in [rule for rule in self.rules if rule.scores_every_line() and not rule.only_this_can_score()]:
                total_payout += rule.calculate_payout(icon_set, line)

        for rule in [rule for rule in self.rules if not rule.scores_every_line() and not rule.only_this_can_score()]:
            total_payout += rule.calculate_payout(icon_set, [])
        print("Total payout: ", total_payout)
        return total_payout
