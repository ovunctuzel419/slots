import hashlib
from contextlib import contextmanager

import attr
import dearpygui.dearpygui as dpg
import numpy as np
from attrs import define
from typing import Dict

from app.auth import verify_otp
from app.context import AppContext
from app.localization import PositionEstimationStatus, PositionEstimationResult
from app.ruleset import PayoutEstimate
from fixture.predefined_slots import GANGSTER
from utils.constants import MAX_REELS_IN_GAME
from utils.paths import resource_path


# Theme creation after context setup
def create_black_theme():
    with dpg.theme() as black_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 5, 5, category=dpg.mvThemeCat_Core)
    return black_theme


def create_white_text_theme():
    white_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvText, parent=white_theme):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])
    return white_theme


def create_green_text_theme():
    green_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvText, parent=green_theme):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [180, 255, 160, 255])
    return green_theme


@contextmanager
def loading_bar():
    dpg.hide_item("OptimalStrategyParentBox")
    dpg.show_item("loading_bar")
    try:
        yield
    finally:
        dpg.hide_item("loading_bar")
        dpg.show_item("OptimalStrategyParentBox")


@define
class TextureManager:
    cache: Dict[str, str] = {}

    def get_texture_tag(self, filepath: str) -> str:
        if filepath in self.cache:
            return self.cache[filepath]

        width, height, channels, data = dpg.load_image(filepath)
        tag = f"tex_{len(self.cache)}"
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag=tag)
        self.cache[filepath] = tag
        return tag

    def get_texture_tag_from_array(self, array: np.ndarray) -> str:
        import cv2

        # Convert to RGBA
        if array.ndim == 2:
            rgba = cv2.cvtColor(array, cv2.COLOR_GRAY2RGBA)
        elif array.shape[2] == 3:
            rgba = cv2.cvtColor(array, cv2.COLOR_BGR2RGBA)
        elif array.shape[2] == 4:
            rgba = array.copy()
        else:
            raise ValueError("Unsupported array shape for texture input")

        rgba = rgba.astype(np.float32) / 255.0
        height, width = rgba.shape[:2]
        data = rgba.flatten().tolist()

        tag = f"tex_arr_{len(self.cache)}"
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag=tag)

        self.cache[tag] = tag
        return tag


@define
class SlotPredictor:
    context: AppContext
    texture_manager: TextureManager = attr.Factory(TextureManager)
    placeholder_icon_path: str = resource_path("assets/icon.png")
    payout_page_size: int = 20
    max_cols_in_grid: int = 5
    max_rows_in_grid: int = 5

    def set_context(self, context: AppContext):
        self.context = context
        self.refresh()

    def refresh(self):
        if not self.context:
            return

        dpg.show_item("CenterPanel")
        dpg.show_item("PayoutsPanel")
        dpg.show_item("RightPanel")

        self.refresh_grid()
        self.refresh_legend()

        with loading_bar():
            position_estimate = self.context.get_position_estimate()
        with loading_bar():
            self.refresh_payouts_panel(position_estimate)
            self.refresh_estimation_panel(position_estimate)
            self.refresh_optimal_strategy(position_estimate)

        if position_estimate.status != PositionEstimationStatus.CONFIDENT:
            dpg.hide_item("OptimalStrategyParentBox")

    def refresh_legend(self):
        # Update legend
        for i in range(len(self.context.legend_icon_paths)):
            tex_tag = self.texture_manager.get_texture_tag(self.context.legend_icon_paths[i])
            dpg.show_item(f"legend_icon_{i}")
            dpg.show_item(f"legend_label_{i}")
            dpg.configure_item(f"legend_icon_{i}", texture_tag=tex_tag)
            dpg.set_value(f"legend_label_{i}", self.context.legend_icon_names[i])
        for i in range(len(self.context.legend_icon_paths), 20):
            dpg.hide_item(f"legend_icon_{i}")
            dpg.hide_item(f"legend_label_{i}")

    def refresh_payouts_panel(self, position_estimate: PositionEstimationResult):
        # - Payouts
        if position_estimate.position > 0:
            # Current payout
            current_payout_index = position_estimate.position
            current_payout = self.context.get_payout_estimate(current_payout_index, iterations=1)
            current_payout_text = self.build_payout_string(current_payout_index, current_payout)
            current_payout_text = "Payout: " + current_payout_text[current_payout_text.find(":"):]
            dpg.set_value("payout_text", current_payout_text)

            # Future payouts
            for i in range(self.payout_page_size):
                page_index = self.context.current_payout_page_index
                payout_index = page_index * self.payout_page_size + position_estimate.position + i + 1
                payout_index = payout_index % MAX_REELS_IN_GAME
                if position_estimate.status == PositionEstimationStatus.CONFIDENT:
                    dpg.show_item(f"payout_row_{i}")
                    payout = self.context.get_payout_estimate(payout_index - i, iterations=i + 1)

                    # Previous payout, for green text
                    if i == 0:
                        if page_index == 0:
                            prev_payout = current_payout
                        else:
                            prev_payout = self.context.get_payout_estimate(payout_index - i - self.payout_page_size, iterations=self.payout_page_size)
                    else:
                        prev_payout = self.context.get_payout_estimate(payout_index - i, iterations=i)

                    payout_row_text = self.build_payout_string(payout_index, payout)
                    dpg.set_value(f"payout_row_{i}", payout_row_text)

                    # Make positive payouts green
                    if payout.payout - prev_payout.payout > -self.context.current_bet:
                        dpg.bind_item_theme(f"payout_row_{i}", create_green_text_theme())
                    else:
                        dpg.bind_item_theme(f"payout_row_{i}", create_white_text_theme())

                    self.refresh_hover_image(payout_index, i)
                else:
                    dpg.hide_item(f"payout_row_{i}")
        else:
            for i in range(self.payout_page_size):
                dpg.hide_item(f"payout_row_{i}")
        dpg.set_value("payout_page_text", f"Page {str(self.context.current_payout_page_index + 1).zfill(3)}")

    def build_payout_string(self, payout_index: int, payout_estimate: PayoutEstimate) -> str:
        payout = payout_estimate.payout
        multiplier_2x = payout_estimate.multiplier_2x
        free_games = payout_estimate.free_games
        mystery_mult_ct = payout_estimate.mystery_multiplier_count
        multiplier_text = "" if multiplier_2x <= 0 else f" [x2 ({multiplier_2x})]"
        free_games_text = "" if free_games <= 0 else f" [FREE {free_games}x] "
        mystery_bonus_text = "" if mystery_mult_ct <= 0 else f" [MULT {mystery_mult_ct}x]"
        return f"{payout_index}: {payout}" + multiplier_text + free_games_text + mystery_bonus_text

    def refresh_bet_options(self):
        dpg.configure_item("bet_options", items=self.context.current_game.bets)
        self.context.current_bet = self.context.current_game.bets[0]

    def refresh_hover_image(self, position_index: int, payout_row_index: int):
        icon_set = self.context._position_estimator._icon_sets[position_index - 1]
        for r in range(self.max_rows_in_grid):
            for c in range(self.max_cols_in_grid):
                if r >= icon_set.shape[0] or c >= icon_set.shape[1]:
                    dpg.hide_item(f"tooltip_{payout_row_index}_{r}_{c}")
                    continue
                icon_index = icon_set[r, c]
                # print(f"ICON SET FOR {position_index}: {icon_set} - (This is payout row {payout_row_index})")
                texture_tag = self.texture_manager.get_texture_tag(self.context.legend_icon_paths[icon_index])
                dpg.show_item(f"tooltip_{payout_row_index}_{r}_{c}")
                dpg.configure_item(f"tooltip_{payout_row_index}_{r}_{c}", texture_tag=texture_tag)

    def refresh_estimation_panel(self, position_estimate: PositionEstimationResult):
        dpg.set_value("estimated_text", f"Estimated position: {position_estimate.position}" if position_estimate.status != PositionEstimationStatus.UNKNOWN else "Please fill all slots first.")
        confidence_text = ""
        if position_estimate.status in [PositionEstimationStatus.CONFIDENT, PositionEstimationStatus.UNCERTAIN]:
            confidence_text = f"{int(position_estimate.confidence * 100)}%"
        elif position_estimate.status == PositionEstimationStatus.ERROR:
            confidence_text = "ERROR - No match found"
        elif position_estimate.status == PositionEstimationStatus.UNKNOWN:
            confidence_text = "???"
        self._toggle_visibility("next_entry_button", position_estimate.status == PositionEstimationStatus.UNCERTAIN)
        self._toggle_visibility("undo_button", position_estimate.status == PositionEstimationStatus.UNKNOWN)
        dpg.set_value("confidence_text", f"Confidence: {confidence_text}")

    def refresh_grid(self):
        for row in range(self.max_rows_in_grid):
            self._toggle_visibility(f"grid_row_{row}", row < self.context.current_icon_set.shape[0])
            for col in range(self.max_cols_in_grid):
                self._toggle_visibility(f"grid_cell_{row}_{col}", col < self.context.current_icon_set.shape[1])

        for row in range(self.context.current_icon_set.shape[0]):
            for col in range(self.context.current_icon_set.shape[1]):
                icon_index = self.context.current_icon_set[row, col]
                if icon_index == -1:
                    icon_path = self.placeholder_icon_path
                else:
                    icon_path = self.context.legend_icon_paths[icon_index]
                tex_tag = self.texture_manager.get_texture_tag(icon_path)
                nominal_height = 64
                height = int(3 / self.context.current_icon_set.shape[0] * nominal_height)
                dpg.configure_item(f"grid_cell_{row}_{col}", texture_tag=tex_tag, height=height)

    def refresh_optimal_strategy(self, position_estimate: PositionEstimationResult):
        if position_estimate.status != PositionEstimationStatus.CONFIDENT:
            dpg.hide_item("OptimalStrategyBox")
            return

        dpg.show_item("OptimalStrategyBox")
        strategy = self.context.calculate_optimal_strategy(
            start_index=position_estimate.position + 1,
            end_index=position_estimate.position + 1 + self.payout_page_size * (self.context.current_payout_page_index + 1))
        dpg.set_value("strategy_max_loss_text", f"Maximum Loss: {strategy.max_loss}")
        dpg.set_value("strategy_gains_text", f"Potential Gains: {strategy.gains}")
        dpg.set_value("strategy_stop_play_text", f"Spin {(strategy.position_to_stop - position_estimate.position) % MAX_REELS_IN_GAME} times."
                                                            f"\nStop playing at: {strategy.position_to_stop}")

        for r in range(self.max_rows_in_grid):
            for c in range(self.max_cols_in_grid):
                icon_set = self.context._position_estimator._icon_sets[strategy.position_to_stop - 1]
                within_bounds = r < icon_set.shape[0] and c < icon_set.shape[1]
                self._toggle_visibility(f"strategy_cell_{r}_{c}", within_bounds)
                if within_bounds:
                    icon_index = icon_set[r, c]
                    texture_tag = self.texture_manager.get_texture_tag(self.context.legend_icon_paths[icon_index])
                    dpg.show_item(f"strategy_cell_{r}_{c}")
                    dpg.configure_item(f"strategy_cell_{r}_{c}", texture_tag=texture_tag)


    def on_load_game_click(self, game_name: str):
        print("Clicked load game", game_name)
        with loading_bar():
            self.context.on_click_load_game(game_name)

        self.refresh_bet_options()
        self.set_context(self.context)

    def on_legend_button_click(self, index: int):
        print("Clicked legend button", index)
        self.context.on_click_legend_button(index)
        self.set_context(self.context)

    def on_clear_all_click(self):
        print("Clicked clear all")
        self.context.on_click_clear_all()
        self.set_context(self.context)

    def on_next_entry_click(self):
        print("Clicked next entry")
        self.context.on_click_next_entry()
        self.set_context(self.context)

    def on_next_payout_page_click(self):
        print("Clicked next payout page")
        self.context.on_click_next_payout_page()
        self.set_context(self.context)

    def on_prev_payout_page_click(self):
        print("Clicked prev payout page")
        self.context.on_click_prev_payout_page()
        self.set_context(self.context)

    def on_next_payout_multipage_click(self):
        print("Clicked next payout page")
        for i in range(10):
            self.context.on_click_next_payout_page()
            self.set_context(self.context)

    def on_prev_payout_multipage_click(self):
        print("Clicked prev payout page")
        for i in range(10):
            self.context.on_click_prev_payout_page()
            self.set_context(self.context)

    def on_bet_click(self, bet: int):
        print("Bet set to", bet)
        self.context.current_bet = int(bet)
        self.set_context(self.context)

    def on_undo_click(self):
        print("Clicked undo button")
        self.context.on_click_undo()
        self.set_context(self.context)

    def on_debug_click(self):
        print("Clicked debug button")
        # self.context.current_icon_set = np.array(([0, 5, 0, 11, 1],
        #                                           [7, 15, 12, 5, 2],
        #                                           [1, 0, 1, 0, 12],
        #                                           [15, 6, 8, 15, 1]))
        self.context.current_icon_set = np.array(([6, 0, 5, 11, 10],
                                                  [10, 10, 6, 4, 0],
                                                  [5, 3, 0, 6, 5],
                                                  [2, 7, 9, 1, 4]))
        # self.context.current_icon_set = np.array(([3, 10, 8, 5, 0],
        #                                           [8, 1, 8, 2, 7],
        #                                           [9, 4, 8, 10, 10]))
        self.set_context(self.context)

    def check_password(self):
        plain_text_password = dpg.get_value("PasswordInput")
        password_hash = hashlib.sha256(plain_text_password.encode('utf-8')).hexdigest()
        if password_hash == 'fe9128409048f02b5e2f0ffc5387feb8fa4229ac7947e3128b2689d3e6a65469':
            dpg.hide_item("PasswordWindow")
            dpg.show_item("MainWindow")
        else:
            dpg.set_value("PasswordStatus", "Wrong password!")

    def check_double_otp(self):
        otp1 = dpg.get_value("OTP1")
        otp2 = dpg.get_value("OTP2")
        if verify_otp(otp1, otp2, known_secrets_json_path=resource_path("auth_codes/secrets.json")):
            dpg.hide_item("OTP1")
            dpg.hide_item("PasswordWindow")
            dpg.show_item("MainWindow")
        else:
            dpg.set_value("PasswordStatus", "Wrong password combination, try again.")

    def build_ui(self):
        black_box_theme = create_black_theme()

        with dpg.window(tag="PasswordWindow", no_title_bar=True, no_close=True, no_move=True, width=300, height=130, no_collapse=True, no_resize=True, pos=[(dpg.get_viewport_width() - 300) / 2, (dpg.get_viewport_height() - 180) / 2]):
            dpg.add_text("Enter one-time passwords to unlock")
            dpg.add_input_text(label="User 1", tag="OTP1", password=True)
            dpg.add_input_text(label="User 2", tag="OTP2", password=True)
            dpg.add_button(label="Submit", callback=self.check_double_otp)
            dpg.add_text("", tag="PasswordStatus")

        with dpg.window(tag="MainWindow", label="Slot Predictor"):
            with dpg.group(horizontal=True):

                # LEFT PANEL
                with dpg.child_window(width=150, autosize_y=True, tag="LeftPanel"):
                    dpg.add_text("Game Selection")
                    for game in self.context.get_available_games():
                        game_name = game.name
                        def make_callback(name):
                            return lambda s, a: self.on_load_game_click(name)
                        dpg.add_button(label=game_name, callback=make_callback(game_name))

                # CENTER PANEL
                with dpg.group(horizontal=False):
                    with dpg.group(horizontal=False, tag="CenterPanel"):
                        with dpg.child_window(width=390, height=258):
                            dpg.add_text("Reels")

                            with dpg.child_window(tag="GridBox", border=True, autosize_x=False, autosize_y=False):
                                dpg.bind_item_theme("GridBox", black_box_theme)

                                with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedSame,
                                               borders_innerH=True, borders_innerV=True):
                                    for _ in range(self.max_rows_in_grid):
                                        dpg.add_table_column(tag=f"grid_col_{_}")
                                    for r in range(self.max_cols_in_grid):
                                        with dpg.table_row(tag=f"grid_row_{r}"):
                                            for c in range(self.max_rows_in_grid):
                                                dpg.add_image("grid_image", width=64, height=64, tag=f"grid_cell_{r}_{c}")

                        dpg.add_spacer(height=5)
                        with dpg.group(horizontal=True):
                            with dpg.group(horizontal=False):
                                dpg.add_spacer(height=7)
                                with dpg.group(horizontal=True):
                                    dpg.add_button(label="Clear", width=100, height=30, callback=self.on_clear_all_click, tag="clear_all_button")
                                    dpg.add_button(label="Next", width=100, height=30, callback=self.on_next_entry_click, tag="next_entry_button")
                                    dpg.add_button(label="Undo", width=60, height=30, callback=self.on_undo_click, tag="undo_button")
                                    # dpg.add_button(label="Debug", width=40, height=30, callback=self.on_debug_click, tag="debug_button")
                                    dpg.hide_item("next_entry_button")
                            dpg.add_spacer(width=10)
                            # Bet selection
                            with dpg.group(horizontal=False):
                                dpg.add_text("Choose bet:")
                                dpg.add_radio_button(
                                    items=["50", "100", "200"],
                                    default_value="50",
                                    horizontal=True,  # or False for vertical layout
                                    tag="bet_options",
                                    callback=lambda s, a: self.on_bet_click(int(a))
                                )

                        dpg.add_spacer(height=5)
                        dpg.add_text("Estimated position:", tag="estimated_text")
                        dpg.add_text("Confidence:", tag="confidence_text")
                        dpg.add_spacer(height=13)

                        # Optimal strategy window
                        with dpg.child_window(width=390, height=176, no_scrollbar=True, no_scroll_with_mouse=True, tag="OptimalStrategyParentBox"):
                            with dpg.group(tag="OptimalStrategyBox"):
                                dpg.add_text("Optimal Strategy")
                                dpg.add_spacer(height=3)
                                with dpg.group(horizontal=True, tag="strategy_group"):
                                    cell_size = 32
                                    with dpg.drawlist(width=self.max_cols_in_grid * cell_size, height=self.max_rows_in_grid * cell_size) as drawlist:
                                        for r in range(self.max_rows_in_grid):
                                            for c in range(self.max_cols_in_grid):
                                                x = c * cell_size
                                                y = r * cell_size
                                                dpg.draw_image("grid_image",
                                                               (x, y),
                                                               (x + cell_size, y + cell_size),
                                                               parent=drawlist,
                                                               tag=f"strategy_cell_{r}_{c}")
                                    with dpg.group(horizontal=False):
                                        dpg.add_text("Maximum Loss: 12345", tag="strategy_max_loss_text")
                                        dpg.add_text("Potential Gains: 12345", tag="strategy_gains_text")
                                        dpg.add_spacer(height=45)
                                        dpg.add_text("Stop playing at: 12345", tag="strategy_stop_play_text")

                    # Loading indicator for long operations
                    with dpg.group(horizontal=False, tag="loading_bar"):
                        dpg.add_spacer(height=120)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=5)
                            dpg.add_loading_indicator(tag="spinner", style=1)
                            dpg.add_spacer(width=5)
                            with dpg.group(horizontal=False):
                                dpg.add_spacer(height=10)
                                dpg.add_text("Please Wait...", tag="loading_text")
                    dpg.hide_item("loading_bar")

                # PAYOUTS PANEL
                with dpg.child_window(width=260, autosize_y=True, tag="PayoutsPanel"):
                    dpg.add_text("Payout:", tag="payout_text")
                    dpg.add_text("Future payouts:", tag="payout_future_text")
                    for i in range(self.payout_page_size):
                        dpg.add_text("", tag=f"payout_row_{i}")

                        # Payout tooltip on hover
                        with dpg.tooltip(parent=f"payout_row_{i}"):
                            with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedSame,
                                           borders_innerH=True, borders_innerV=True):
                                for _ in range(self.max_rows_in_grid):
                                    dpg.add_table_column(tag=f"tooltip_{i}_col_{_}")
                                for r in range(self.max_cols_in_grid):
                                    with dpg.table_row(tag=f"tooltip_{i}_row_{r}"):
                                        for c in range(self.max_rows_in_grid):
                                            dpg.add_image("grid_image", width=32, height=32, tag=f"tooltip_{i}_{r}_{c}")

                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="<<", width=30, height=25, callback=self.on_prev_payout_multipage_click)
                        dpg.add_button(label="<", width=38, height=25, callback=self.on_prev_payout_page_click)
                        dpg.add_spacer(width=2)
                        dpg.add_text("Page 001", tag=f"payout_page_text")
                        dpg.add_spacer(width=2)
                        dpg.add_button(label=">", width=38, height=25, callback=self.on_next_payout_page_click)
                        dpg.add_button(label=">>", width=30, height=25, callback=self.on_next_payout_multipage_click)

                # RIGHT PANEL
                with dpg.child_window(width=220, autosize_y=True, tag="RightPanel"):
                    dpg.add_text("Legend")
                    for i in range(20):
                        with dpg.group(horizontal=True):
                            def make_callback(index: int):
                                return lambda s, a: self.on_legend_button_click(index)
                            dpg.add_image_button("grid_image", width=32, height=32, tag=f"legend_icon_{i}", callback=make_callback(i))
                            dpg.add_text("?", tag=f"legend_label_{i}")

                # Hide all panels except game selection
                dpg.hide_item("CenterPanel")
                dpg.hide_item("PayoutsPanel")
                dpg.hide_item("RightPanel")

                # Hide main window until password is entered
                dpg.hide_item("MainWindow")

    @staticmethod
    def _toggle_visibility(tag: str, visible: bool):
        if visible:
            dpg.show_item(tag)
        else:
            dpg.hide_item(tag)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="UI", width=1080, height=620)
        dpg.setup_dearpygui()

        # Load default texture
        width, height, channels, data = dpg.load_image(self.placeholder_icon_path)
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="grid_image")

        self.build_ui()
        dpg.set_primary_window("MainWindow", True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == '__main__':
    app = SlotPredictor(context=AppContext(current_game=GANGSTER))
    app.run()
