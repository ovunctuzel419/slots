import os
from functools import partial

import attr
import dearpygui.dearpygui as dpg
from attrs import define, field
from typing import List, Optional, Dict

from app.context import AppContext
from fixture.predefined_slots import GANGSTER


# Theme creation after context setup
def create_black_theme():
    with dpg.theme() as black_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 5, 5, category=dpg.mvThemeCat_Core)
    return black_theme


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


@define
class SlotPredictor:
    context: AppContext
    texture_manager: TextureManager = attr.Factory(TextureManager)
    placeholder_icon_path: str = "../assets/icon.png"

    def set_context(self, context: AppContext):
        self.context = context
        self.refresh()

    def refresh(self):
        if not self.context:
            return

        # Update grid
        for row in range(self.context.current_icon_set.shape[0]):
            for col in range(self.context.current_icon_set.shape[1]):
                icon_index = self.context.current_icon_set[row, col]
                if icon_index == -1:
                    icon_path = self.placeholder_icon_path
                else:
                    icon_path = self.context.legend_icon_paths[icon_index]
                tex_tag = self.texture_manager.get_texture_tag(icon_path)
                dpg.configure_item(f"grid_cell_{row}_{col}", texture_tag=tex_tag)

        # Update legend
        for i in range(len(self.context.legend_icon_paths)):
            tex_tag = self.texture_manager.get_texture_tag(self.context.legend_icon_paths[i])
            dpg.configure_item(f"legend_icon_{i}", texture_tag=tex_tag)
            dpg.set_value(f"legend_label_{i}", self.context.legend_icon_names[i])
        for i in range(len(self.context.legend_icon_paths), 20):
            dpg.hide_item(f"legend_icon_{i}")
            dpg.hide_item(f"legend_label_{i}")

        # Update text
        position, confidence = self.context.get_position_estimate()
        dpg.set_value("estimated_text", f"Estimated position: {position}" if position > 0 else "Please fill all slots first.")
        dpg.set_value("confidence_text", f"Confidence: {confidence}")

    def on_load_game_click(self, game_name: str):
        print("Clicked load game", game_name)
        self.context.on_click_load_game(game_name)
        self.set_context(self.context)

    def on_legend_button_click(self, index: int):
        print("Clicked legend button", index)
        self.context.on_click_legend_button(index)
        self.set_context(self.context)

    def on_clear_all_click(self):
        print("Clicked clear all")
        self.context.on_click_clear_all()
        self.set_context(self.context)

    def build_ui(self):
        black_box_theme = create_black_theme()

        with dpg.window(tag="MainWindow", label="Slot Predictor"):
            with dpg.group(horizontal=True):

                # LEFT PANEL
                with dpg.child_window(width=150, autosize_y=True):
                    dpg.add_text("Game Selection")
                    for game in self.context.get_available_games():
                        game_name = game.name
                        def make_callback(name):
                            return lambda s, a: self.on_load_game_click(name)
                        dpg.add_button(label=game_name, callback=make_callback(game_name))

                # CENTER PANEL
                with dpg.group(horizontal=False):
                    with dpg.child_window(width=390, height=256):
                        dpg.add_text("Reels")

                        with dpg.child_window(tag="GridBox", border=True, autosize_x=False, autosize_y=False):
                            dpg.bind_item_theme("GridBox", black_box_theme)

                            with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedSame,
                                           borders_innerH=True, borders_innerV=True):
                                for _ in range(5):
                                    dpg.add_table_column()
                                for r in range(3):
                                    with dpg.table_row():
                                        for c in range(5):
                                            dpg.add_image("grid_image", width=64, height=64, tag=f"grid_cell_{r}_{c}")

                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Clear", width=100, height=30, callback=self.on_clear_all_click)
                        dpg.add_button(label="Next", width=100, height=30)

                    dpg.add_spacer(height=10)
                    dpg.add_text("Estimated position:", tag="estimated_text")
                    dpg.add_text("Confidence:", tag="confidence_text")

                dpg.add_spacer(width=205)

                # RIGHT PANEL
                with dpg.child_window(width=200, autosize_y=True):
                    dpg.add_text("Legend")
                    for i in range(20):
                        with dpg.group(horizontal=True):
                            def make_callback(index: int):
                                return lambda s, a: self.on_legend_button_click(index)
                            dpg.add_image_button("grid_image", width=32, height=32, tag=f"legend_icon_{i}", callback=make_callback(i))
                            dpg.add_text("?", tag=f"legend_label_{i}")

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="Slot UI", width=1000, height=600)
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
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    app = SlotPredictor(context=AppContext(GANGSTER))
    app.run()
