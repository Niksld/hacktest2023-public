import dearpygui.dearpygui as dpg
from configuration import LEVEL_DATA

from windows.Window import Window

class WindowComponentXSS(Window):
    def __init__(self, theme = None):
        super().__init__("xss_exploit", 450, 480, ["center", 0, 0], False, True, theme=theme, label="XSS Exploit")
        self.maze_data: list = LEVEL_DATA["xss_mazes"]
        self.history = []
        self.lines = []
        self.current_level = 0
        self.has_loaded_level = False

        for i in range(len(self.maze_data)):
            self.maze_data[i]["correct"] = [self.maze_data[i]["correct"], list(reversed(self.maze_data[i]["correct"]))]
            self.maze_data[i]["possible"].extend(self.maze_data[i]["correct"])

        dpg.add_text(f"{0}/{len(self.maze_data)}", tag="xss_exploit.level", parent="xss_exploit", pos=(211,40))
        for i in range(36):
            id = f"{i%6}{i//6}"
            dpg.add_button(label=id, tag=f"xss_exploit.button{id}", parent="xss_exploit", width=50, height=50, pos=(50+(i%6)*60,80+(i//6)*60), user_data=id, callback=self.button_cb)

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        if not self.has_loaded_level:
            self.start_level()

    def start_level(self):
        self.has_loaded_level = True
        self.history = []

        dpg.set_value("xss_exploit.level", f"{self.current_level+1}/{len(self.maze_data)}")
        if self.current_level >= len(self.maze_data):
            for i in range(36):
                dpg.hide_item(f"xss_exploit.button{i%6}{i//6}")
            dpg.hide_item("xss_exploit.level")
            dpg.add_text("Implementace komponentu\nXSS (Cross-Site Scripting) Exploit úspěšná.", parent="xss_exploit", pos=(50,310), color=(0,255,0), wrap=450)
            self.set_progress(6, 1, "component")
            return

        maze = self.maze_data[self.current_level]
        for i in range(36):
            dpg.enable_item(f"xss_exploit.button{i%6}{i//6}")

        for tile in maze["ends"]:
            dpg.disable_item(f"xss_exploit.button{tile}")

    def button_cb(self, sender, app_data, user_data):
        self.history.append(user_data)
        dpg.disable_item(sender)

        if self.history in self.maze_data[self.current_level]["correct"]:
            self.current_level += 1
            self.delay(self.start_level, 0.5)
        else:
            l = len(self.history)
            for path in self.maze_data[self.current_level]["possible"]:
                if l <= len(path) and self.history == path[:l]:
                    return
            else:
                self.start_level()
