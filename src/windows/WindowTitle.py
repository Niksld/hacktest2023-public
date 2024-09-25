import dearpygui.dearpygui as dpg
from re import compile as regexcompile
from configuration import DEBUG

from windows.Window import Window

class WindowTitle(Window):
    def __init__(self, theme = None):
        super().__init__("title", 350, 270, ["center", 0, 0], theme=theme, no_title_bar=True, no_move=True, no_collapse=True, pos=(250,175))
        self.login_session = None
        self.test_account_pat = regexcompile(r"^((test)[0-9]{2}|\w)$")
        self.replacement_account_pat = regexcompile(r"^nahradni[0-9]{2}$")

        dpg.add_text("Vítej v\u00a0Hacktestu!\n\nTvým úkolem bude sestavit vir z\u00a0různých komponentů.\nOvěříš své hackerské schopnosti: v\u00a0počítači hledej, jak\u00a0postupovat.", tag="title.text", parent=self.tag, wrap=dpg.get_item_width(self.tag) - 20)
        dpg.add_spacer(height=10, parent=self.tag)
        with dpg.group(horizontal=True, parent=self.tag):
            dpg.add_button(tag="title.fullscreenbtn", label="F11", callback=dpg.toggle_viewport_fullscreen)
            dpg.add_text("pro přepnutí na celou obrazovku", tag="title.fullscreentext", color=(180,180,180))
        dpg.add_spacer(height=20, parent=self.tag)
        dpg.add_button(tag="title.btn", label="Začít", height=50, parent=self.tag)
        with dpg.stage(tag="title.stage"):
            dpg.add_text("Uživatelské jméno", tag="title.username.text")
            dpg.add_input_text(tag="title.username.input", on_enter=True, callback=lambda: dpg.focus_item("title.password.input"), width=275)
            dpg.add_text("Heslo", tag="title.password.text")
            dpg.add_input_text(tag="title.password.input", password=True, on_enter=True, callback=self.login_cb, width=275)
            dpg.add_spacer(height=10)
            dpg.add_button(tag="title.btnlogin", label="Přihlásit se", callback=self.login_cb, height=40)
            dpg.add_text("", tag="title.error", color=(255, 0, 0), wrap=250)
        dpg.draw_image("title.image-logo", tag="title.logo", pmin=(0,0), pmax=(447, 88), uv_min=(0,0), uv_max=(1,1), parent="drawlist")

    def login_window(self, error: str | None = None) -> None:
        for item in dpg.get_item_children("title", 1):
            if dpg.get_item_type(item) != "mvAppItemType::mvSpacer":
                dpg.hide_item(item)
            else:
                dpg.delete_item(item)
        for item in dpg.get_item_children("title.stage", 1):
            dpg.move_item(item, parent=self.tag)
        if error is not None:
            dpg.set_value("title.error", error)
            dpg.focus_item("title.password.input")

    def set_login_session(self, fun: callable) -> None:
        def f(*args, **kwargs):
            dpg.disable_item("title.btnlogin")
            dpg.disable_item("title.username.input")
            dpg.disable_item("title.password.input")
            dpg.configure_item("title.btnlogin", label="Přihlašování...")
            dpg.set_value("title.error", "")
            value = fun(*args, **kwargs)
            dpg.enable_item("title.btnlogin")
            dpg.enable_item("title.username.input")
            dpg.enable_item("title.password.input")
            dpg.configure_item("title.btnlogin", label="Přihlásit se")
            return value
        self.login_session = f

    def login_cb(self, sender, app_data, user_data) -> None:
        """Callback pro tlačítko přihlášení. Získá přihlašovací údaje z okna, vytvoří nový lokální soubor a zahájí synchronizaci, tím spustí hru."""
        username = dpg.get_value("title.username.input")
        password = dpg.get_value("title.password.input")
        if self.login_session(username, password):
            # self.no_login_window()
            if not DEBUG and self.test_account_pat.match(username):
                with dpg.window(width=500, height=150, label="Testovací účet", no_move=True, no_collapse=True, no_resize=True, pos=(250,175)):
                    dpg.add_text("VAROVÁNÍ: Používáš testovací účet! Jakýkoliv postup nebude při hodnocení brán v\u00a0úvahu.\n\nPokud tuto zprávu vidíš, nahlaš to pořadatelům.", color=(255, 0, 0), wrap=490)
            elif self.replacement_account_pat.match(username):
                with dpg.window(width=500, height=150, label="Náhradní účet", no_move=True, no_collapse=True, no_resize=True, pos=(250,175)):
                    dpg.add_text("VAROVÁNÍ: Používáš náhradní účet.\n\nUjisti se, že pořadatelé ví, komu výsledky z tohoto náhradního účtu přiřadit.", color=(255,255,100), wrap=490)
        else:
            dpg.set_value("title.error", "Nesprávné přihlašovací údaje. V\u00a0případě potíží se\u00a0zeptej pořadatelů.")

    def on_resize(self):
        super().on_resize()
        while True: #někdy to crashne když se to okno hodně rychle zmenšuje/zvětšuje (lol)
            try:
                shown = dpg.is_item_shown("title.logo")
                dpg.delete_item("title.logo")
                pos = ((dpg.get_viewport_client_width()-447)//2,((dpg.get_viewport_client_height()-88)//2)-200)
                dpg.draw_image("title.image-logo", tag="title.logo", pmin=pos, pmax=(pos[0]+447,pos[1]+88), uv_min=(0,0), uv_max=(1,1), parent="drawlist", show=shown)
                break
            except Exception as e:
                print("Chyba pozicování loga", e)

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        dpg.hide_item(self.tag)
        dpg.hide_item("title.logo")
