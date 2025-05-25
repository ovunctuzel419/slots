import os.path
from typing import List, Tuple

import numpy as np
from attrs import field, define

from fixture.legend import get_class_icon_paths
from fixture.predefined_slots import SlotsGame, available_games
from utils.custom_types import IconSet


@define
class AppContext:
    current_game: SlotsGame
    legend_icon_paths: List[str] = field(factory=list)
    legend_icon_names: List[str] = field(factory=list)
    current_icon_set: IconSet = np.zeros((3, 5), dtype=int) - 1
    current_cursor_index: int = 0

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
        self.legend_icon_paths = get_class_icon_paths(selected_game.dataset_folder_path)
        self.legend_icon_names = [f"{os.path.basename(os.path.dirname(icon_path))}" for icon_path in self.legend_icon_paths]

    def on_click_legend_button(self, index: int):
        row = self.current_cursor_index // self.current_icon_set.shape[1]
        col = self.current_cursor_index % self.current_icon_set.shape[1]
        if row >= self.current_icon_set.shape[0] or col >= self.current_icon_set.shape[1]:
            print(f"Invalid cursor index for legend button click: {row}, {col}")
            return
        self.current_icon_set[row, col] = index
        self.current_cursor_index += 1

    def on_click_clear_all(self):
        self.current_cursor_index = 0
        self.current_icon_set = np.zeros((3, 5), dtype=int) - 1

    def get_position_estimate(self) -> Tuple[int, float]:
        if self.current_cursor_index < self.current_icon_set.shape[0] * self.current_icon_set.shape[1]:
            return -1, 0.0
        return 1234, 0.99
