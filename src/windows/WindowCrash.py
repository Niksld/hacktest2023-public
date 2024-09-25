import dearpygui.dearpygui as dpg

from windows.Window import Window

class WindowCrash(Window):
    def __init__(self, theme = None):
        super().__init__("crash", 500, 500, ["center", 0, 0], theme=theme, label="Kritická chyba", modal=True, no_move=True)
        dpg.add_text("", tag="crash.text", parent="crash", wrap=dpg.get_item_width("crash") - 20)

    def show(self, error: str) -> None:
        dpg.set_value("crash.text", "Pokud toto vidíš, oznam to.\n\n" + error)
        dpg.show_item("crash")
