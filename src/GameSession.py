from configuration import get_progress_highest, set_progress_index, OFFLINE_MODE, SERVER_IP, SERVER_PORT, ATTENDEES
from local_save import local_get, local_set, local_set_progress, local_check
from server_save import server_get, server_set
from Delay import Delay

class GameSession:
    """Relace hry, nadřazená oknům. Zajišťuje postup mezi okny, relací, lokálním souborem a serverem."""
    def __init__(self):
        self.offline_mode = True
        self.attendees = ATTENDEES

        self.windows = {}
        self.desktop = None
        self.taskbar = None
        self.userdata = {
            "username": "",
            "password": "",
            "progress": "0000000000000000"
        }

        self.delay = Delay()
        self.frame_update_functions = []

        self.disabled_notifications = False

    def add_desktop(self, desktop: object) -> None:
        """Přidá instanci plochy do relace."""
        self.desktop = desktop
        self.desktop.set_progress_function(self.set_progress)
        self.desktop.set_delay_function(self.delay.add)
        self.desktop.set_delay_drop_function(self.delay.drop)

    def add_taskbar(self, taskbar: object) -> None:
        """Přidá instanci lišty úloh do relace."""
        self.taskbar = taskbar

    def add_window(self, window: object) -> None:
        """Přidá instanci okna do slovníku oken."""
        name = window.tag
        self.windows[name] = window
        self.windows[name].set_progress_function(self.set_progress)
        self.windows[name].set_taskbar_app_functions(self.taskbar.app_opened, self.taskbar.app_closed)
        self.windows[name].set_delay_function(self.add_delayed_action)
        self.windows[name].set_notification_function(self.windows["notifcenter"].external_notification)

    def set_progress(self, index: int, value: int, mode: str|None = "simple") -> None:
        """Volá se z okna při postupu uživatelem. Aktualizuje postup v relaci a synchronizuje jej s lokálním souborem i serverem. Následně aktualizuje postup ve všech oknech.
        \nParametry:\n
            index:  index pro přepis
            value:  hodnota pro přepis, pouze pokud je větší než aktuální hodnota
            mode:   simple - přepis na určeném indexu (výchozí)
                    component - přepis jednoho indexu + součet všech komponent"""

        self.userdata["progress"] = set_progress_index(self.userdata["progress"], index, value)
        if mode == "component":
            self.userdata["progress"] = get_progress_highest(self.userdata["progress"], "00" + str(sum([int(x) for x in self.userdata["progress"]][3:10])) + "0000000000000")
        elif mode != None and mode != "simple":
            raise ValueError(f"Neznámý režim přepisu postupu: {mode}")

        self.sync_progress(True)

    def crash(self, text: str) -> None:
        """Zobrazí hlášku o chybě."""
        self.windows["crash"].show(text)

    def on_resize(self) -> None:
        self.desktop.on_resize()
        self.taskbar.on_resize()
        for window in self.windows:
            self.windows[window].on_resize()

    def sync_progress(self, force_load: bool = False) -> str:
        """Synchronizuje postup uživatele relace <-> lokální soubor <-> server."""
        local_progress = None
        server_progress = None
        best_progress = None
        #Ziskani progressu z lokalniho souboru, porovnani s relaci a ulozeni
        local_progress = local_get()["progress"]
        best_progress = get_progress_highest(self.userdata["progress"], local_progress)
        if local_progress != best_progress:
            local_set_progress(best_progress)
            local_progress = best_progress

        #Jestlize je appka v online modu, pokracovat v porovnani se serverem
        if not self.offline_mode:
            #Stazeni dat ze serveru; pokud je odpoved None, stazeni selhalo -> crash
            server_progress, server_error = server_get(self.userdata["username"])
            if server_progress is not None and len(server_progress) == len(local_progress):
                #Porovnani postupu se serverem, stazeni dat ze serveru
                best_progress = get_progress_highest(best_progress, server_progress)
                if local_progress != best_progress:
                    local_set_progress(best_progress)
                #Pokud nejsou data stazena ze serveru ten nejvyssi postup, odeslat zpet
                if server_progress != best_progress:
                    server_response, server_error = server_set(self.userdata["username"], best_progress)
                    if server_progress != best_progress and (not server_response):
                        self.crash(f"Odeslání postupu na\u00a0server selhalo.\n\n{server_error}\n\ns: {SERVER_IP}:{SERVER_PORT}\nu: {self.userdata['username']}\nR: {self.userdata['progress']}\nL: {local_progress}\nS: {server_progress}\nB: {best_progress}")
                        return
            else:
                self.crash(f"Stáhnutí postupu ze\u00a0serveru selhalo.\n\n{server_error}\n\ns: {SERVER_IP}:{SERVER_PORT}\nu: {self.userdata['username']}\nR: {self.userdata['progress']}\nL: {local_progress}\nS: {server_progress}")
                return

        #Propagace noveho progressu do oken
        if self.userdata["progress"] != best_progress or self.userdata["progress"] == "0000000000000000" or force_load:
            self.userdata["progress"] = best_progress
            for window in self.windows.values():
                window.load_progress(self.userdata)
            self.desktop.load_progress(self.userdata)
            self.taskbar.load_progress(self.userdata)

        return best_progress

    def start_title_screen(self) -> None:
        #prvotní načtení postupu
        local_check_status = local_check()
        if local_check_status == 1:
            self.userdata = local_get()
            self.userdata["progress"] = "0000000000000000"
            self.sync_progress()
        else:
            #hra se spouští bez lokálního souboru, titulní obrazovka
            self.windows["title"].login_window("Soubor s\u00a0lokálně uloženými daty je poškozen. Pokud toto vidíš, oznam\u00a0to prosím." if local_check_status == -1 else None)
            self.windows["title"].set_login_session(self.new_local_login)

    def new_local_login(self, username: str, password: str) -> bool:
        """Vytvoří nový lokální soubor se zadanými přihlašovacími údaji."""
        if username in self.attendees:
            if self.attendees[username] == password:
                self.userdata = {
                    "username": username,
                    "password": password,
                    "progress": "0000000000000000"
                }
                local_set(self.userdata)
                self.sync_progress()
                return True
        return False

    def add_delayed_action(self, action: callable, delay: float = 1.0, looping: bool = False, looping_times: int = 1) -> None:
        """Přidá akci do seznamu akcí, které se mají spustit po určité době."""
        self.delay.add(action, delay, looping, looping_times)

    def add_frame_update_function(self, function: callable) -> None:
        """Přidá funkci, která se má spustit každý frame"""
        self.frame_update_functions.append(function)

    def frame_update(self) -> None:
        """Spouští se každý frame v render loopu."""
        self.delay.update()
        for fun in self.frame_update_functions:
            fun()

    def set_disabled_notifications(self, enabled: bool) -> None:
        self.disabled_notifications = enabled

    def get_disabled_notifications(self) -> bool:
        return self.disabled_notifications
