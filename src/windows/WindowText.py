import dearpygui.dearpygui as dpg
from configuration import LEVEL_DATA, relpath
from textwrap import fill

from windows.Window import Window

class WindowText(Window):
    def __init__(self, theme = None):
        super().__init__("text", 400, 400, ["center", 0, 0], False, True, theme=theme, autosize=True, min_size=(400,400), label="Bez názvu (4)")

        dpg.add_input_text(tag="text.content", parent=self.tag, width=390, height=380, multiline=True, readonly=True)
        self.text_data = LEVEL_DATA["text_files"]

    def on_launch(self, data: str) -> None:
        if not data.endswith("LICENCE.txt"):
            content = [file["content"] for file in self.text_data if file["name"] == data][0].splitlines()
        else:
            with open(relpath(f"licences/{data}"), "r") as file:
                content = file.read().splitlines()

        content = "\n".join([fill(line, 43, break_long_words=True, break_on_hyphens=True) for line in content])
        dpg.set_item_label(self.tag, data)
        dpg.set_value("text.content", content)
