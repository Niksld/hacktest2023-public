import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement, LEVEL_DATA

from windows.Window import Window

class WindowWifi(Window):
    def __init__(self, theme = None):
        super().__init__("wifi", 250, 350, ["bottomright", 0, -50], False, True, theme=theme, no_collapse=True, no_move=True, popup=True, min_size=(250, 350), max_size=(250, 350))
        self.connected = None
        self.networks = LEVEL_DATA["networks"]

        dpg.add_text("Připojení není dostupné", tag="wifi.status", parent="wifi", color=(255,0,0), wrap=240)
        for i in range(len(self.networks)):
            dpg.add_child_window(label=self.networks[i]["name"], tag=f"wifi.section{i}", parent="wifi", height=75, autosize_x=True, menubar=False)
            dpg.add_text(self.networks[i]["name"], tag=f"wifi.name{i}", parent=f"wifi.section{i}", wrap=190)
            dpg.add_button(label="Připojit", tag=f"wifi.connect{i}", parent=f"wifi.section{i}", user_data=i, callback=(lambda sender, app_data, user_data: self.connect_cb(sender, app_data, user_data)))
            dpg.add_text("Připojování", tag=f"wifi.connecting{i}", parent=f"wifi.section{i}", show=False)
            dpg.add_input_text(tag=f"wifi.password{i}", parent=f"wifi.section{i}", password=True, no_spaces=True, hint="Zadejte heslo", on_enter=True, user_data=(i, self.networks[i]), callback=self.password_input_cb, show=False)
            dpg.add_image(f"wifi.image-wifi/{self.networks[i]['strength']}", tag=f"wifi.icon{i}", parent=f"wifi.section{i}", width=30, height=30, pos=(175,32))

    def connect_cb(self, sender, app_data, user_data):
        dpg.hide_item(sender)
        dpg.show_item(f"wifi.connecting{user_data}")
        text = self.update_connection_text()
        for i in range(12):
            self.delay(lambda: dpg.configure_item(f"wifi.connecting{user_data}", default_value=next(text)), 0.2*i)
        self.delay(lambda: (dpg.hide_item(f"wifi.connecting{user_data}"),
                   dpg.show_item(f"wifi.password{user_data}"),
                   dpg.focus_item(f"wifi.password{user_data}")), 2.5)

    def update_connection_text(self):
        dots = 0
        while True:
            if dots < 3:
                dots += 1
            else:
                dots = 0
            yield "Připojování" + dots*"."

    def password_input_cb(self, sender, app_data, user_data):
        user_input = dpg.get_value(sender)
        dpg.hide_item(sender)
        dpg.configure_item(f"wifi.connecting{user_data[0]}", default_value="Ověřování")
        dpg.show_item(f"wifi.connecting{user_data[0]}")

        if user_input == user_data[1]["password"]:
            self.connected = user_data
            for i in [n for n in range(len(self.networks)) if n != user_data[0]]:
                dpg.hide_item(f"wifi.section{i}")
            self.delay(lambda: dpg.configure_item(f"wifi.connecting{user_data[0]}", default_value="Získávání IP adresy"), 0.1)
            self.delay(lambda: dpg.configure_item("wifi.status", default_value="Připojeno k " + user_data[1]["name"], color=(0,255,0)), 1.0)
            self.delay(lambda: (dpg.configure_item(f"wifi.connecting{user_data[0]}", default_value="Připojeno"),
                       self.set_progress(0, 1)), 1.3)
            self.delay(lambda: dpg.hide_item("wifi"), 2.5)

        else:
            self.delay(lambda: (dpg.hide_item(f"wifi.connecting{user_data[0]}"),
            dpg.set_value(f"wifi.password{user_data[0]}", ""),
            dpg.configure_item(f"wifi.password{user_data[0]}", hint="Chybné heslo"),
            dpg.show_item(f"wifi.password{user_data[0]}")), 2.5)

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        if get_progress_requirement(self.progress["progress"], "1###############"):
            if self.connected is not None:
                dpg.configure_item("taskbar.wifi", texture_tag=f"wifi.image-wifi/{self.connected[1]['strength']}")
            else:
                dpg.configure_item("taskbar.wifi", texture_tag="wifi.image-ethernet")
                dpg.configure_item("wifi.status", default_value="Připojeno k síti Ethernet", color=(0,255,0))
