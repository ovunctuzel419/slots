from abc import abstractmethod, ABC
from typing import List, Tuple, Dict

import attrs
import numpy as np
from attrs import define

from utils.custom_types import IconSet

Line = List[int]


@define
class PayoutEstimate:
    payout: float
    free_games: int = 0
    multiplier_2x: int = 0
    mystery_multiplier_count: int = 0
    next_round_column_replace_bonus: Dict[int, int] = attrs.field(factory=dict)  # Change column [key] to [value] next round

    @classmethod
    def no_reward(cls) -> 'PayoutEstimate':
        return PayoutEstimate(payout=0)

    def __add__(self, other: 'PayoutEstimate') -> 'PayoutEstimate':
        return PayoutEstimate(
            payout=self.payout + other.payout,
            free_games=self.free_games + other.free_games,
            multiplier_2x=self.multiplier_2x + other.multiplier_2x,
            mystery_multiplier_count=self.mystery_multiplier_count + other.mystery_multiplier_count,
            next_round_column_replace_bonus=self.next_round_column_replace_bonus | other.next_round_column_replace_bonus
        )


@define(kw_only=True)
class Rule(ABC):
    symbol_index: int
    payout: float
    free_games_bonus: int = 0
    multiplier_2x_bonus: int = 0
    mystery_multiplier_count: int = 0
    next_round_column_replace_bonus: Dict[int, int] = attrs.field(factory=dict)

    @abstractmethod
    def calculate_payout(self, icon_set: IconSet, line: Line) -> PayoutEstimate:
        pass

    def scores_every_line(self) -> bool:
        return True

    def only_this_can_score(self) -> bool:
        return False

    def get_payout(self):
        return PayoutEstimate(payout=self.payout,
                              free_games=self.free_games_bonus,
                              multiplier_2x=self.multiplier_2x_bonus,
                              mystery_multiplier_count=self.mystery_multiplier_count,
                              next_round_column_replace_bonus=self.next_round_column_replace_bonus)


@define(kw_only=True)
class MatchLeftRule(Rule):
    num_matches: int = -1
    wild_symbol: int = -1

    def calculate_payout(self, icon_set: IconSet, line: Line) -> PayoutEstimate:
        icon_set = icon_set.copy()
        if self.wild_symbol != -1:
            icon_set = np.where(icon_set == self.wild_symbol, self.symbol_index, icon_set)

        symbols = icon_set[np.array(line), np.arange(len(line))]
        next_differs = (self.num_matches == len(symbols) or symbols[self.num_matches] != self.symbol_index)
        if np.all(symbols[:self.num_matches] == self.symbol_index) and next_differs:
            print(f"Matched rule {self}, iconset: {icon_set}, line: {line}, payout: {self.get_payout()}")
            return self.get_payout()
        return PayoutEstimate.no_reward()


@define(kw_only=True)
class ExistsInEveryReelRule(Rule):
    symbol_indices: List[int]
    wild_symbol: int = -1

    def calculate_payout(self, icon_set: IconSet, line: Line) -> PayoutEstimate:
        icon_set = icon_set.copy()

        # Treat wilds as matching all valid symbols
        if self.wild_symbol != -1:
            for idx in self.symbol_indices:
                icon_set = np.where(icon_set == self.wild_symbol, idx, icon_set)

        # Check each column (reel)
        for col in range(icon_set.shape[1]):
            if not np.any(np.isin(icon_set[:, col], self.symbol_indices)):
                return PayoutEstimate.no_reward()

        print(f"Matched rule {self}, iconset: {icon_set}, payout: {self.get_payout()}")
        return self.get_payout()

    def scores_every_line(self) -> bool:
        return False


@define(kw_only=True)
class MatchLeftOrRightWithWildColumnRule(Rule):
    num_matches: int = -1
    wild_symbol: int = -1
    special_wild_symbol: int = -1  # This one doesn't replace a column but counts as a match

    def calculate_payout(self, icon_set: IconSet, line: Line) -> PayoutEstimate:
        if self.wild_symbol != -1:
            icon_set = icon_set.copy()
            # Identify wild columns, replace entire wild columns with the symbol_index
            wild_cols = np.any(icon_set == self.wild_symbol, axis=0)
            special_wild_cols = np.any(icon_set == self.special_wild_symbol, axis=0)
            self.next_round_column_replace_bonus = {i: self.special_wild_symbol for i in np.where(wild_cols)[0]}
            icon_set[:, wild_cols] = self.symbol_index
            icon_set[:, special_wild_cols] = self.symbol_index

        symbols = icon_set[np.array(line), np.arange(len(line))]
        # Match left
        next_differs = (self.num_matches == len(symbols) or symbols[self.num_matches] != self.symbol_index)
        if np.all(symbols[:self.num_matches] == self.symbol_index) and next_differs:
            print(f"Matched rule {self}, iconset: {icon_set}, line: {line}, payout: {self.get_payout()}")
            return self.get_payout()

        # Match right
        next_differs = (self.num_matches == len(symbols) or symbols[len(symbols) - self.num_matches - 1] != self.symbol_index)
        if np.all(symbols[-self.num_matches:] == self.symbol_index) and next_differs:
            print(f"Matched rule {self}, iconset: {icon_set}, line: {line}, payout: {self.get_payout()}")
            return self.get_payout()

        no_payout_with_potential_bonus = PayoutEstimate.no_reward()
        no_payout_with_potential_bonus.next_round_column_replace_bonus = self.next_round_column_replace_bonus
        return no_payout_with_potential_bonus


@define(kw_only=True)
class MatchAnyPositionWithWildBonusRule(Rule):
    num_matches: int = -1
    wild_symbol: int = -1

    def calculate_payout(self, icon_set: IconSet, line: Line) -> PayoutEstimate:
        symbols = icon_set[np.array(line), np.arange(len(line))]
        for start in range(len(symbols) - self.num_matches + 1):
            window = symbols[start:start + self.num_matches]
            matches = [(s == self.symbol_index or s == self.wild_symbol) for s in window]

            if not all(matches):
                continue

            # Check if it's *exactly* num_matches (no continuation before/after)
            before_ok = (start == 0 or symbols[start - 1] not in (self.symbol_index, self.wild_symbol))
            after_ok = (start + self.num_matches == len(symbols) or symbols[start + self.num_matches] not in (self.symbol_index, self.wild_symbol))

            if before_ok and after_ok:
                used_wild = any(s == self.wild_symbol for s in window)
                payout = self.get_payout()
                payout.mystery_multiplier_count = 1 if used_wild else 0
                print(f"Matched rule {self}, symbols: {symbols}, used wild: {used_wild}, payout: {payout}")
                return payout

        return PayoutEstimate.no_reward()


@define(kw_only=True)
class FixedConfigurationRule(Rule):
    expected_icon_set: IconSet

    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.all(icon_set == self.expected_icon_set):
            return self.get_payout()
        return PayoutEstimate.no_reward()

    def only_this_can_score(self) -> bool:
        return True


@define(kw_only=True)
class AllSameRule(Rule):
    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.all(icon_set == self.symbol_index):
            return self.get_payout()
        return PayoutEstimate.no_reward()

    def only_this_can_score(self) -> bool:
        return True

@define(kw_only=True)
class ScatterRule(Rule):
    num_matches: int

    def calculate_payout(self, icon_set: IconSet, line: Line):
        if np.sum(icon_set == self.symbol_index) == self.num_matches:
            return self.get_payout()
        return PayoutEstimate.no_reward()

    def scores_every_line(self) -> bool:
        return False


@define(kw_only=True)
class Ruleset:
    lines: List[Line]
    rules: List[Rule]

    def calculate_payout(self, icon_set: IconSet) -> PayoutEstimate:
        total_payout = PayoutEstimate.no_reward()

        # Check special rules
        for rule in [rule for rule in self.rules if rule.only_this_can_score()]:
            special_payout = rule.calculate_payout(icon_set, [])
            if special_payout != PayoutEstimate.no_reward():
                return special_payout

        # For each line, calculate payout
        for line in self.lines:
            for rule in [rule for rule in self.rules if rule.scores_every_line() and not rule.only_this_can_score()]:
                total_payout += rule.calculate_payout(icon_set, line)

        for rule in [rule for rule in self.rules if not rule.scores_every_line() and not rule.only_this_can_score()]:
            total_payout += rule.calculate_payout(icon_set, [])
        return total_payout
