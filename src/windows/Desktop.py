import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement, LEVEL_DATA
from random import randint

# Struktura informací o ikonách
# {"name": "", "path": "", "app":"", "appdata":"", "unlock":"###############"}

class Desktop:
    def __init__(self, theme = None) -> None:
        self.icon_data = LEVEL_DATA["desktop_icons"]
        self.desktop_icons = []
        self.progress = None
        self.taskbar_app = None
        self.hide_all_windows = None
        self.blur = False
        self.is_blurred = False
        self.ending_sequence = False
        self.set_progress = None
        self.delay = None
        self.drop_delay = None

        dpg.add_window(
            width=800,
            height=600,
            tag="desktop",
            menubar=False,
            no_move=True,
            no_title_bar=True,
            no_resize=True,
            no_close=True,
            no_background=True,
            no_bring_to_front_on_focus=True,
            no_focus_on_appearing=True,
            show=True)
        if theme is not None:
            dpg.bind_item_theme("desktop", theme)

        dpg.add_viewport_drawlist(tag="drawlist", front=False)
        dpg.draw_image("desktop.image-wallpaper", tag="desktop.wallpaper", pmin=(0,0), pmax=(dpg.get_viewport_client_width(), dpg.get_viewport_client_height()), uv_min=(0,0), uv_max=(1,1), parent="drawlist")

        for i in range(len(self.icon_data)):
            dpg.add_image_button(f"desktop.image-{self.icon_data[i]['image']}", tag=f"desktop.icon-{self.icon_data[i]['tag']}", width=50, height=50,
                                 pos=(0,0), parent="desktop", user_data=(self.icon_data[i]), callback=self.icon_cb, show=False)
            dpg.add_text(self.icon_data[i]["name"], tag=f"desktop.text-{self.icon_data[i]['tag']}", parent="desktop", pos=(0,55), wrap=100, show=False)
            self.desktop_icons.append((f"desktop.icon-{self.icon_data[i]['tag']}",f"desktop.text-{self.icon_data[i]['tag']}"))

        self.on_resize()

    def icon_cb(self, sender, app_data, user_data):
        if dpg.does_item_exist(user_data["app"]):
            success = dpg.get_item_user_data(user_data["app"])(user_data["appdata"])
            if success is None or success is True:
                dpg.show_item(user_data["app"])
                dpg.focus_item(user_data["app"])
                self.taskbar_app(user_data["app"], user_data["name"])
        else:
            with dpg.window(width=300, height=200, pos=((dpg.get_viewport_client_width()-300)/2,(dpg.get_viewport_client_height()-200)/2), label="Problém s aplikací", no_collapse=True, no_resize=True):
                dpg.add_text(f"Nepodařilo se spustit aplikaci \"{user_data['app']}\": nedostatečné oprávnění (0xF007A785)", wrap=290)
                dpg.add_button(label="OK", callback=lambda sender: dpg.delete_item(dpg.get_item_parent(sender)))

    def wallpaper_swap(self):
        last_wallpaper = -1
        next_wallpaper = 0
        while True:
            while last_wallpaper == next_wallpaper:
                next_wallpaper = randint(0,5)
            yield dpg.delete_item("desktop.wallpaper"), dpg.draw_image(f"desktop.image-wallpaper-glitch{next_wallpaper}", tag="desktop.wallpaper", pmin=(0,0), pmax=(dpg.get_viewport_client_width(), dpg.get_viewport_client_height()), uv_min=(0,0), uv_max=(1,1), parent="drawlist")
            last_wallpaper = next_wallpaper

    def wallpaper_glitch(self):
        glitches = []
        while True:
            pmin = randint(50,dpg.get_viewport_client_width()-100), randint(50,dpg.get_viewport_client_height()-100)
            scale = randint(1,3)
            pmax = pmin[0]+scale*50, pmin[1]+scale*50
            yield glitches.append(dpg.draw_image(f"desktop.image-glitch{randint(0,5)}", pmin=pmin, pmax=pmax, uv_min=(0,0), uv_max=(1,1), parent="drawlist"))
            if randint(0,1):
                dpg.delete_item(glitches.pop(0))

    def start_ending_sequence(self):
        wallpaper_tags = self.wallpaper_swap()
        wallpaper_glitches = self.wallpaper_glitch()
        for i in range(20):
            self.delay(lambda: next(wallpaper_tags), randint(5,9)*0.1*i)
        for i in range(60):
            self.delay(lambda: next(wallpaper_glitches), randint(1,3)*0.1*i)
        self.delay(lambda: self.set_progress(10, 3), 18.1)
        self.delay(self.bsod, 18.5)

    def bsod(self):
        self.ending_sequence = True
        self.drop_delay()
        for window in dpg.get_windows():
            if not dpg.get_item_type(window).endswith("Registry"):
                try:
                    dpg.hide_item(window)
                except Exception:
                    pass
        self.on_resize()
        self.delay(lambda: (dpg.add_window(width=350, height=100, pos=(dpg.get_viewport_client_width()-400, dpg.get_viewport_client_height()-150), no_title_bar=True, no_close=True, no_collapse=True, no_move=True, no_resize=True), dpg.add_text("Tvůj postup byl uložen.\n\nStiskni Alt+F4 pro zavření okna.", parent=dpg.last_container())), 15)

    def load_progress(self, progress: dict) -> None:
        self.progress = progress
        self.blur = True
        if not self.ending_sequence:
            if self.blur != self.is_blurred:
                self.on_resize()
            for icon, label in self.desktop_icons:
                if get_progress_requirement(self.progress["progress"], dpg.get_item_user_data(icon)["unlock"]):
                    dpg.show_item(icon)
                    dpg.show_item(label)
            if get_progress_requirement(self.progress["progress"], "##########2#####", "##########3#####"):
                self.start_ending_sequence()
            elif get_progress_requirement(self.progress["progress"], "##########3#####"):
                self.bsod()

    def on_resize(self):
        dpg.configure_item("desktop", width=dpg.get_viewport_client_width(), height=dpg.get_viewport_client_height()-50)
        while True: #někdy to crashne když se to okno hodně rychle zmenšuje/zvětšuje (lol)
            try:
                dpg.delete_item("desktop.wallpaper")
                variant =  "-bsod" if self.ending_sequence else ("-blur" if self.blur else "")
                dpg.draw_image(f"desktop.image-wallpaper{variant}", tag="desktop.wallpaper", pmin=(0,0), pmax=(dpg.get_viewport_client_width(), dpg.get_viewport_client_height()), uv_min=(0,0), uv_max=(1,1), parent="drawlist")
                self.is_blurred = self.blur
                break
            except Exception as e:
                print("Chyba pozicování pozadí plochy", e)

        max_width = (dpg.get_viewport_client_width())//100
        max_height = (dpg.get_viewport_client_height()-50)//100
        for icon in self.desktop_icons:
            pos = list(dpg.get_item_user_data(icon[0])["pos"])
            if pos[0] < 0:
                pos[0] += max_width
            if pos[1] < 0:
                pos[1] += max_height
            pos[0] = pos[0] * 100 + 20
            pos[1] = pos[1] * 100 + 20
            dpg.set_item_pos(icon[0], pos)
            dpg.set_item_pos(icon[1], (pos[0], pos[1]+55))

    def set_progress_function(self, progress_function: callable) -> None:
        self.set_progress = progress_function

    def set_taskbar_app_function(self, func: callable):
        self.taskbar_app = func

    def set_hide_windows_function(self, func: callable):
        self.hide_all_windows = func

    def set_delay_function(self, func: callable):
        self.delay = func

    def set_delay_drop_function(self, func: callable):
        self.drop_delay = func
