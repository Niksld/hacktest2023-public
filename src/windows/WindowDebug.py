import dearpygui.dearpygui as dpg
from configuration import DEBUG

from windows.Window import Window

class WindowDebug(Window):
    def __init__(self, theme = None):
        super().__init__("debug", 170, 110, ["topright", 0, 0], theme=theme, no_title_bar=True, no_collapse=True, no_move=True)
        dpg.add_text("", tag="debug.guide", parent="debug")
        dpg.add_input_int(label="Index", width=100, min_value=0, max_value=1, step=1, min_clamped=True, max_clamped=True, tag="debug.index", parent="debug")
        dpg.add_button(tag="debug.increment", label="Přidat bod", height=30, parent="debug", callback=self.progress_increment_cb)

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        if DEBUG:
            dpg.show_item("debug")
        dpg.set_value("debug.guide", progress["progress"])
        dpg.configure_item("debug.index", max_value=len(progress["progress"])-1)

    def progress_increment_cb(self, sender, app_data, user_data) -> None:
        index = dpg.get_value("debug.index")
        if int(self.progress["progress"][index]) < 9:
            self.set_progress(index, int(self.progress["progress"][index]) + 1)
        else:
            dpg.set_value("debug.guide", self.progress["progress"][:index] + "!" + self.progress["progress"][index+1:])
