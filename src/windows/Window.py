import dearpygui.dearpygui as dpg

class Window:
    def __init__(self, tag: str, width: int, height: int, sticky: list = ["none", 0, 0], no_close: bool = True, hide_on_close: bool = False, theme = None, **kwargs) -> None:
        dpg.add_window(
            width=width,
            height=height,
            tag=tag,
            show=False,
            no_resize=True,
            no_close=no_close,
            on_close=lambda: (dpg.hide_item(tag), self.taskbar_close(self.tag)) if (not no_close) and hide_on_close else lambda: dpg.delete_item(tag),
            user_data=self.on_launch,
            **kwargs)
        self.tag = tag
        self.width = width
        self.height = height
        self.sticky = sticky
        self.theme = theme
        self.progress = None
        self.set_progress = None
        """Volá se z okna při postupu uživatelem. Aktualizuje postup v relaci a synchronizuje jej s lokálním souborem i serverem. Následně aktualizuje postup ve všech oknech.
        \nParametry:\n
            index:  index pro přepis
            value:  hodnota pro přepis, pouze pokud je větší než aktuální hodnota
            mode:   simple - přepis na určeném indexu (výchozí)
                    component - přepis jednoho indexu + součet všech komponent"""
        self.taskbar_open = None
        self.taskbar_close = None
        self.delay = None
        self.notification = None

        if self.theme is not None:
            dpg.bind_item_theme(self.tag, self.theme)

    #pozicování okna při změně velikosti viewportu
    #lze predefinovat v případě, že jedna třída obsahuje více oken, stále by se ale měl odkázat na super()
    def on_resize(self):
        match self.sticky[0]:
            case "topleft" | "none" | "":
                pass
            case "bottomleft":
                dpg.configure_item(self.tag, pos=(0, dpg.get_viewport_client_height()-self.height+self.sticky[2]))
            case "topright":
                dpg.configure_item(self.tag, pos=(dpg.get_viewport_client_width()-self.width-self.sticky[1], 0))
            case "bottomright":
                dpg.configure_item(self.tag, pos=(dpg.get_viewport_client_width()-self.width+self.sticky[1], dpg.get_viewport_client_height()-self.height+self.sticky[2]))
            case "center":
                dpg.configure_item(self.tag, pos=(dpg.get_viewport_client_width()//2-self.width//2+self.sticky[1], dpg.get_viewport_client_height()//2-self.height//2+self.sticky[2]))
            case _:
                raise ValueError(f"Neplatný parametr \"{self.sticky[0]}\" pozicování okna \"{self.tag}\"")


    #odkaz na funkci z GameSession, kterou lze zapsat progress, nemělo by se předefinovávat
    def set_progress_function(self, progress_function: callable) -> None:
        self.set_progress = progress_function

    #vytvoření a zavření okna na liště
    def set_taskbar_app_functions(self, taskbar_open_function: callable, taskbar_close_function: callable) -> None:
        self.taskbar_open = taskbar_open_function
        self.taskbar_close = taskbar_close_function

    #odkaz na funkci z GameSession, slouží k opoždění vykonání akcí
    #pozor, obsah fstringů apod. se vyhodnotí až po uplynutí času, takže pokud se v něm nachází proměnná, která se mění (for cyklus), může dojít k chybě
    def set_delay_function(self, delay_function: callable) -> None:
        self.delay = delay_function

    #odkaz na funkci z GameSession pro vytvoření oznámení
    def set_notification_function(self, notification_function: callable) -> None:
        self.notification = notification_function

    #volá se při každé změně progressu, i když pochází z tohoto okna, předefinovat jak je potřeba
    def load_progress(self, progress: dict) -> None:
        self.progress = progress

    #volá se při spuštění okna z ikony na ploše, předefinovat jak je potřeba
    def on_launch(self, data) -> bool|None:
        pass
