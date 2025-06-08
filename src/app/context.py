import os.path
from typing import List, Tuple, Optional

import numpy as np
from attrs import field, define

from app.csv_reader import CSVReader
from app.localization import PositionEstimator, PositionEstimationResult, PositionEstimationStatus
from app.payout import PayoutEstimator
from app.ruleset import PayoutEstimate
from app.strategy import OptimalStrategyFinder, Strategy
from fixture.legend import get_class_icon_paths
from fixture.predefined_slots import SlotsGame, available_games
from utils.constants import MAX_REELS_IN_GAME
from utils.custom_types import IconSet


@define
class AppContext:
    current_game: SlotsGame
    legend_icon_paths: List[str] = field(factory=list)
    legend_icon_names: List[str] = field(factory=list)
    current_icon_set: IconSet = np.zeros((3, 5), dtype=int) - 1
    current_relative_reel_index: int = 0
    current_cursor_index: int = 0
    current_payout_page_index: int = 0
    current_bet: int = 50
    csv_reader: CSVReader = CSVReader()
    payout_estimator: Optional[PayoutEstimator] = None
    _position_estimator: PositionEstimator = field(init=False)
    _optimal_strategy_finder: Optional[OptimalStrategyFinder] = field(init=False)

    def __attrs_post_init__(self):
        self._position_estimator = PositionEstimator(slots_game=self.current_game, csv_reader=self.csv_reader)

    def get_available_games(self) -> List[SlotsGame]:
        return available_games

    def on_click_load_game(self, game_name: str):
        selected_game = None
        for game in available_games:
            if game.name == game_name:
                selected_game = game
                break
        print("Selected game:", selected_game)

        self.current_game = selected_game
        self.current_icon_set = np.zeros((selected_game.rows, selected_game.cols), dtype=int) - 1
        self._position_estimator = PositionEstimator(slots_game=selected_game, csv_reader=self.csv_reader)
        self.payout_estimator = PayoutEstimator.from_game(game=selected_game, csv_reader=self.csv_reader)
        self._optimal_strategy_finder = OptimalStrategyFinder(payout_estimator=self.payout_estimator)
        self.legend_icon_paths = get_class_icon_paths(selected_game.dataset_folder_path)
        self.legend_icon_names = [f"{os.path.basename(os.path.dirname(icon_path))}" for icon_path in self.legend_icon_paths]
        self.current_relative_reel_index = 0
        self.current_payout_page_index = 0
        self.current_cursor_index = 0

    def on_click_legend_button(self, index: int):
        row = self.current_cursor_index // self.current_icon_set.shape[1]
        col = self.current_cursor_index % self.current_icon_set.shape[1]
        if row >= self.current_icon_set.shape[0] or col >= self.current_icon_set.shape[1]:
            print(f"Invalid cursor index for legend button click: {row}, {col}")
            return
        self.current_icon_set[row, col] = index
        self.current_cursor_index += 1

    def on_click_clear_all(self):
        self.current_payout_page_index = 0
        self.current_cursor_index = 0
        self.current_relative_reel_index = 0
        self.current_icon_set = np.zeros((self.current_game.rows, self.current_game.cols), dtype=int) - 1
        self._position_estimator.reset()
        self.payout_estimator.reset()

    def on_click_next_entry(self):
        self.current_cursor_index = 0
        self.current_relative_reel_index += 1
        self.current_icon_set = np.zeros((self.current_game.rows, self.current_game.cols), dtype=int) - 1

    def on_click_next_payout_page(self):
        self.current_payout_page_index = min(MAX_REELS_IN_GAME, self.current_payout_page_index + 1)

    def on_click_prev_payout_page(self):
        self.current_payout_page_index = max(0, self.current_payout_page_index - 1)

    def on_click_undo(self):
        if not np.all(self.current_icon_set == -1):
            self.current_cursor_index -= 1
            self.current_icon_set[self.current_cursor_index // self.current_icon_set.shape[1],
                                  self.current_cursor_index % self.current_icon_set.shape[1]] = -1

    def get_position_estimate(self) -> PositionEstimationResult:
        if np.any(self.current_icon_set == -1):
            return PositionEstimationResult(PositionEstimationStatus.UNKNOWN)
        self._position_estimator.update(self.current_icon_set, self.current_relative_reel_index)
        return self._position_estimator.get_position_estimate()

    def get_payout_estimate(self, position_index: int, iterations: int) -> PayoutEstimate:
        if self.payout_estimator is None:
            print("ERROR: No payout estimator available.")
            return -1

        estimate = self.payout_estimator.estimate(position_index, iterations=iterations, bet=self.current_bet)
        return estimate

    def calculate_optimal_strategy(self, start_index: int, end_index: int) -> Strategy:
        if self.payout_estimator is None:
            print("ERROR: No payout estimator available.")
            return Strategy(0, 0, 0)

        return self._optimal_strategy_finder.calculate(start_index, end_index, self.current_bet)

    def check_bonus(self, position_index: int) -> bool:
        if self.payout_estimator is None:
            print("ERROR: No payout estimator available.")
            return False

        return self.payout_estimator.check_bonus(position_index)

    def get_current_payout(self):
        position_estimate = self.get_position_estimate()
        if position_estimate.confidence < 0.7:
            return -1

        return self.payout_estimator.estimate(position_estimate.position, 1)
