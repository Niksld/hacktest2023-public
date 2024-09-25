import dearpygui.dearpygui as dpg

from windows.Window import Window
from configuration import LEVEL_DATA, get_progress_requirement

class WindowStudio(Window):
    def __init__(self, theme = None):
        super().__init__("studio", 900, 600, ["center", 0, 0], False, True, theme=theme, no_collapse=True, label="Virus Studio (free trial) - Nepojmenovaný projekt*", no_scrollbar=True)

        #  Studio funguje tak, že každé tlačítko ukáže vlastní child window - pro každou úlohu tedy možno jakkoliv přizpůsobit stránku jak potřeba.

        # Je worth tohle dávat do level.json? Nikde neukládáme přesně názvy komponentů.
        # myslím že je v pohodě mít to tady --Ondra
        self.components = {"ftp_daemon" : "FTP Daemon",
                           "file_targetter" : "FileTargetter",
                           "anti_av" : "Anti-Antivir",
                           "xss_exploit" : "XSS Exploit",
                           "sandbox_exploit" : "Sandbox Exploit",
                           "mail_handler" : "Mail Handler",
                           }
        self.shown_component = None
        self.studio_data = LEVEL_DATA["studio"]

        # ---------- KOMPONENTY ----------

        for key, val in self.components.items():
            with dpg.child_window(tag=f"studio.component.{key}", parent=self.tag ,pos=(200,0), show=False, width=self.width-200, height=self.height):
                dpg.add_text(val,tag=f"studio.component.{key}.headline", pos=(10,30))
                dpg.add_text(self.studio_data['component_details'][key][0]["body"],tag=f"studio.component.{key}.body", pos=(12,60), wrap=self.width-225)

                text_offset = (self.studio_data['component_details'][key][0]["body"].count("\n")*2) * 30
                if text_offset == 0:
                    text_offset = 50
                else:
                    text_offset += 100
                dpg.add_text(self.studio_data['component_details'][key][1]["difficulty"],tag=f"studio.component.{key}.difficulty", pos=(12,text_offset), wrap=self.width-225)
                if self.studio_data['component_details'][key][2]["image"] != None:
                    dpg.add_image(self.studio_data['component_details'][key][2]["image"], tag=f"studio.component.{key}.image", pos=(12,text_offset+50), width=300, height=300)
                dpg.add_button(label="Začít", tag=f"studio.component.{key}.start_btn", user_data=key, width=70, height=50, pos=(self.width-370,self.height-250), callback=self.show_window)


        # Sidebar
        with dpg.child_window(tag="studio.sidebar", parent=self.tag, height=self.height, width=200, pos=(0,0)):
            dpg.add_text("Projekt:", tag="studio.sidebar.project", pos=(10,35))
            dpg.add_text("Nepojmenovaný projekt", tag="studio.sidebar.project_name", pos=(10,65), wrap=180)
            for i in range(len(self.components)):
                dpg.add_button(label=list(self.components.values())[i], tag=f"studio.sidebar.{list(self.components.keys())[i]}.component_btn", width=200, height=30, pos=(0,100+(i*35)), callback=self.show_component)
            dpg.add_button(label="Exportovat projekt", tag="studio.sidebar.deploybtn", width=200, height=60, pos=(0,self.height-100), enabled=False, callback=self.export_project_cb)

    def show_window(self, sender, app_data, user_data):
        if user_data in self.components.keys():
            dpg.show_item(user_data)
            dpg.focus_item(user_data)
            self.taskbar_open(user_data, self.components[user_data])

    def show_component(self, sender):
        component = sender.split(".")[2]
        if self.shown_component != None:
            dpg.hide_item(self.shown_component)
        dpg.show_item(f"studio.component.{component}")
        self.shown_component = f"studio.component.{component}"

    def export_project_cb(self, sender, app_data, user_data):
        self.set_progress(10, 1)
        with dpg.window(popup=True, width=350, height=50, min_size=(100,50), pos=(dpg.get_viewport_client_width()//2-175, dpg.get_viewport_client_height()//2-25), autosize=False):
            dpg.add_text("Projekt úspěšně exportován", wrap=340)
        #ending sequence

    def on_launch(self, data) -> bool:
        if data == "virus":
            self.delay(lambda: (dpg.hide_item(self.tag), self.taskbar_close(self.tag)), 0.1)
            if get_progress_requirement(self.progress["progress"], maximum_progress_string="##########2#####"):
                self.set_progress(10, 2)
            return False
        return True

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        p = progress["progress"]
        if get_progress_requirement(p, "###1############"):
            dpg.disable_item("studio.component.ftp_daemon.start_btn")
            dpg.disable_item("studio.sidebar.ftp_daemon.component_btn")
        if get_progress_requirement(p, "####1###########"):
            dpg.disable_item("studio.component.file_targetter.start_btn")
            dpg.disable_item("studio.sidebar.file_targetter.component_btn")
        if get_progress_requirement(p, "#####1##########"):
            dpg.disable_item("studio.component.anti_av.start_btn")
            dpg.disable_item("studio.sidebar.anti_av.component_btn")
        if get_progress_requirement(p, "######1#########"):
            dpg.disable_item("studio.component.xss_exploit.start_btn")
            dpg.disable_item("studio.sidebar.xss_exploit.component_btn")
        if get_progress_requirement(p, "#######1########"):
            dpg.disable_item("studio.component.sandbox_exploit.start_btn")
            dpg.disable_item("studio.sidebar.sandbox_exploit.component_btn")
        if get_progress_requirement(p, "########1#######"):
            dpg.disable_item("studio.component.mail_handler.start_btn")
            dpg.disable_item("studio.sidebar.mail_handler.component_btn")
        if get_progress_requirement(p, "##6#############"):
            dpg.enable_item("studio.sidebar.deploybtn")
