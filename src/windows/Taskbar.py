import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement

class Taskbar:
    def __init__(self, theme = None) -> None:
        self.open_apps = []
        self.progress = None
        self.app_button_count = 7

        dpg.add_window(
            width=800,
            height=50,
            min_size=(800, 50),
            pos=(0, 550),
            tag="taskbar",
            menubar=False,
            no_move=True,
            no_title_bar=True,
            no_resize=True,
            no_close=True,
            no_bring_to_front_on_focus=True,
            no_focus_on_appearing=True,
            no_scrollbar=True,
            show=False)
        if theme is not None:
            dpg.bind_item_theme("taskbar", theme)

        dpg.add_image_button("taskbar.image-start", tag="taskbar.start", width=50, height=50, pos=(0,0), parent="taskbar", show=False,
                             callback=lambda: (dpg.set_item_pos("start", (0, dpg.get_viewport_client_height()-400)), dpg.hide_item("start.text2"), dpg.show_item("start")))
        with dpg.tooltip("taskbar.start", tag="taskbar.tooltip-start"):
            dpg.add_text("Menu")
        dpg.add_image_button("taskbar.image-no_internet", tag="taskbar.wifi", width=40, height=40, pos=(760,5), parent="taskbar", show=False, callback=lambda: (dpg.set_item_pos("wifi", (dpg.get_viewport_client_width(), dpg.get_viewport_client_height()-400)), dpg.show_item("wifi")))
        with dpg.tooltip("taskbar.wifi", tag="taskbar.tooltip-wifi"):
            dpg.add_text("Nastavení síťového připojení")
        dpg.add_image_button("taskbar.image-notifications", tag="taskbar.notifications", width=40, height=40, pos=(715,5), parent="taskbar", show=False, callback=lambda: (dpg.set_item_pos("notifcenter", (dpg.get_viewport_client_width(), dpg.get_viewport_client_height()-400)), dpg.set_y_scroll("notifcenter", dpg.get_y_scroll_max("notifcenter")+350), dpg.show_item("notifcenter")))
        with dpg.tooltip("taskbar.notifications", tag="taskbar.tooltip-notifications"):
            dpg.add_text("Historie oznámení", tag="taskbar.tooltip-notifications.text")
        for i in range(1,self.app_button_count+1):
            dpg.add_button(tag=f"taskbar.button{i}", width=(dpg.get_viewport_client_width()-200)/self.app_button_count, height=50, pos=((i-1)*(dpg.get_viewport_client_width()-200)/self.app_button_count + 50,0), parent="taskbar", show=False)

    def on_resize(self):
        dpg.configure_item("taskbar", width=dpg.get_viewport_client_width(), pos=(0, dpg.get_viewport_client_height()-50))
        dpg.configure_item("taskbar.wifi", pos=(dpg.get_item_width("taskbar")-45, 5))
        dpg.configure_item("taskbar.notifications", pos=(dpg.get_item_width("taskbar")-90, 5))
        for i in range(1,self.app_button_count+1):
            dpg.configure_item(f"taskbar.button{i}", width=(dpg.get_viewport_client_width()-200)/self.app_button_count, pos=((i-1)*(dpg.get_viewport_client_width()-200)/self.app_button_count + 50,0))

    def load_progress(self, progress: dict) -> None:
        self.progress = progress
        if not get_progress_requirement(self.progress["progress"], "##########3#####"):
            dpg.show_item("taskbar")
            dpg.show_item("taskbar.start")
            dpg.show_item("taskbar.wifi")
            dpg.show_item("taskbar.notifications")
        else:
            dpg.hide_item("taskbar")

    def app_opened(self, app: str, name: str) -> None:
        open_apps_without_names = [x[0] for x in self.open_apps]
        if len(self.open_apps) < self.app_button_count and app not in open_apps_without_names:
            self.open_apps.append((app, name))
            for i in range(len(self.open_apps)):
                dpg.configure_item(f"taskbar.button{i+1}", label=self.open_apps[i][1], user_data=self.open_apps[i][0], callback=lambda caller: (dpg.configure_item(dpg.get_item_user_data(caller), collapsed=False), dpg.focus_item(dpg.get_item_user_data(caller))))
                dpg.show_item(f"taskbar.button{i+1}")
        elif app in open_apps_without_names:
            dpg.configure_item(f"taskbar.button{open_apps_without_names.index(app)+1}", label=name, user_data=app, callback=lambda caller: (dpg.configure_item(dpg.get_item_user_data(caller), collapsed=False), dpg.focus_item(dpg.get_item_user_data(caller))))

    def app_closed(self, app: str) -> None:
        self.open_apps = [x for x in self.open_apps if x[0] != app]
        for i in range(len(self.open_apps)):
            dpg.configure_item(f"taskbar.button{i+1}", label=self.open_apps[i][1], user_data=self.open_apps[i][0])
        for i in range(len(self.open_apps), self.app_button_count):
            dpg.hide_item(f"taskbar.button{i+1}")
