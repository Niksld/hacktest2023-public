import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement
from random import random, choice

from windows.Window import Window

class WindowStart(Window):
    def __init__(self, theme = None):
        super().__init__("start", 250, 350, ["bottomleft", 0, -50], False, True, theme=theme, no_collapse=True, no_move=True, popup=True, min_size=(250, 350))
        self.points = 0
        self.update_size = 0
        self.settings_system_notifications_cb = None

        dpg.add_text("R0m4n", tag="start.username", parent="start")
        dpg.add_progress_bar(tag="start.progressbar", parent="start", width=200, overlay="Postup: 0% (0 bodů)")
        dpg.add_text(tag="start.guide", parent="start", wrap=220, color=(110,110,110))

        dpg.add_text("Windblows 2064", tag="start.text1", parent="start", pos=(8,300), color=(110,110,110))
        dpg.add_text(tag="start.text2", parent="start", color=(255,0,0), pos=(8,100), wrap=220, show=False)
        dpg.add_button(tag="start.button-settings", label="Nastavení", parent="start", pos=(160,240), width=90, callback=lambda: dpg.show_item("settings"))
        dpg.add_button(tag="start.button-about", label="O systému", parent="start", pos=(160,270), width=90, callback=lambda: dpg.show_item("about"))
        dpg.add_button(tag="start.button-shutdown", label="Vypnout", parent="start", callback=lambda: (self.calculate_update_size(), dpg.show_item("start.text2")), pos=(160,300), width=90)

        # O systému
        with dpg.window(tag="about", label="O produktu Windblows", width=400, height=500, pos=(100,100), on_close=lambda: dpg.hide_item("about"), no_collapse=True, no_resize=True, show=False):
            dpg.add_spacer(height=60)
            dpg.add_image("start.image-windblows", height=53, width=240, pos=(80,33))
            dpg.draw_line((8,65),(378,65), color=(180,180,180,255))
            dpg.add_text("WindBlows\nVerze 75H2 (Hacktest 2023)\nVšechna práva vyhrazena.", wrap=390)
            dpg.add_spacer(height=10)
            dpg.add_text("Windblows 2064 je základní programové vybavení počítače, které umožňuje běh programů a\u00A0ovlivňuje, jak bude počítačový systém komunikovat s\u00A0uživatelem.", wrap=390)
            dpg.add_spacer(height=35)
            dpg.add_text("Tento produkt používá licencované produkty, převážně fonty, licence níže:", wrap=390)
            dpg.add_button(label="Roboto Mono Font", user_data="RobotoMono", callback=self.licence_cb)
            dpg.add_button(label="Red Hat Mono Font", user_data="RedHatMono", callback=self.licence_cb)
            dpg.add_button(label="Hacked Font", user_data="HackedFont", callback=self.licence_cb)
            dpg.add_spacer(height=10)
            dpg.add_text("Vývojáři: Niksld, Ondrejtra, MichaelCZE, GrimReapTM", wrap=390)

        # Nastavení
        with dpg.window(tag="settings", label="Nastavení", width=650, height=300, pos=(100,100), no_collapse=True, no_resize=True, on_close=lambda: dpg.hide_item("settings"), show=False):
            with dpg.tab_bar(tag="settings.tabs"):
                # Síť
                with dpg.tab(tag="settings.network", label="Síť"):
                    dpg.add_text("Nejste připojeni k internetu", tag="settings.network.status", color=(255,0,0))
                    dpg.add_spacer(height=10)
                    dpg.add_button(tag="settings.network.networkbtn", label="Otevřít nastavení síťového připojení", callback=lambda: dpg.get_item_callback("taskbar.wifi")(), width=300, height=40)
                    dpg.add_button(tag="settings.network.helpbtn", label="Otevřít poradce při potížích", callback=lambda: (dpg.set_item_pos("settings-network-help", (dpg.get_item_pos("settings")[0]+125,dpg.get_item_pos("settings")[1]+100)), dpg.show_item("settings-network-help"), dpg.focus_item("settings-network-help")), width=300, height=40)
                    dpg.add_spacer(height=15)
                    dpg.add_text("MAC adresa zařízení: 1E-C4-67-D5-EB-96")
                    dpg.add_checkbox(tag="settings.network.mac-checkbox", label="Používat náhodnou MAC adresu při připojení k\u00A0síti", default_value=True)

                # Zařízení
                with dpg.tab(tag="settings.devices", label="Zařízení"):
                    dpg.add_checkbox(tag="settings.devices.keyboard-checkbox", label="Povolit vstup z klávesnice", default_value=True, enabled=False)
                    dpg.add_checkbox(tag="settings.devices.mouse-checkbox", label="Povolit vstup z myši", default_value=True, enabled=False)
                    dpg.add_checkbox(tag="settings.devices.trackpad-checkbox", label="Povolit vstup z dotykové plochy", default_value=True, enabled=False)
                    dpg.add_checkbox(tag="settings.devices.touch-checkbox", label="Povolit vstup z dotykové obrazovky", default_value=True)
                    dpg.add_checkbox(tag="settings.devices.gamepad-checkbox", label="Povolit vstup z herního ovladače")
                    dpg.add_checkbox(tag="settings.devices.pen-checkbox", label="Povolit vstup z pera")
                    dpg.add_checkbox(tag="settings.devices.camera-checkbox", label="Povolit vstup z kamery", default_value=True)
                    dpg.add_checkbox(tag="settings.devices.microphone-checkbox", label="Povolit vstup z mikrofonu", default_value=True)
                    dpg.add_checkbox(tag="settings.devices.motion-checkbox", label="Povolit vstup z pohybového senzoru", default_value=True)
                    dpg.add_checkbox(tag="settings.devices.motion-neuralink", label="Povolit vstup z aparatury pro komunikaci s lidským mozkem")
                    # idk Ondro pomoc

                # Hraní
                with dpg.tab(tag="settings.gaming", label="Hraní"):
                    dpg.add_checkbox(tag="settings.gaming.notifications-checkbox", label="Ztišit oznámení", callback=lambda s,a,u:(self.settings_system_notifications_cb(dpg.get_value(s)), dpg.configure_item("taskbar.notifications", texture_tag=f"taskbar.image-notifications{'-disabled' if dpg.get_value(s) else ''}"), dpg.configure_item("taskbar.tooltip-notifications.text", default_value="Historie oznámení" if not dpg.get_value(s) else "Oznámení jsou ztišená")))
                    dpg.add_checkbox(tag="settings.gaming.gaming-checkbox", label="Herní režim")
                    dpg.add_checkbox(tag="settings.gaming.hardware-checkbox", label="Povolit hardwarovou akceleraci")
                    dpg.add_checkbox(tag="settings.gaming.color-checkbox", label="Režim vysokého kontrastu", callback=self.settings_gaming_color_cb)
                    # Gaming😎

                # Aktualizace a zabezpečení
                with dpg.tab(tag="settings.update", label="Aktualizace a zabezpečení"):
                    #stahujeme 50 z 12231 aktualizací, prosím restartujte počítač
                        dpg.add_text("Jsou k dispozici aktualizace", tag="settings.update.text1", color=(0,255,0), show=False)
                        dpg.add_progress_bar(tag="settings.update.progressbar", overlay="Stahování aktualizací: 0% (0/2)", show=False)
                        dpg.add_button(tag="settings.update.button", label="Vyhledat aktualizace", callback=self.calculate_update_size, show=False)
                        dpg.add_text("Chyba: připojení k aktualizační službě selhalo (0xfa147b02)\nZkontrolujte připojení k internetu.", tag="settings.update.text2", color=(255,0,0))
                        dpg.add_spacer(height=30)
                        with dpg.child_window(tag="settings.update.promo", autosize_x=True, height=100, show=False):
                            dpg.add_image("paint.image-clear", height=50, width=50, pos=(25,25))
                            dpg.add_text("Upgradujte na Windblows 2064.0.0.1", pos=(100,5))
                            dpg.add_text("Aktualizace Windblows 2064.0.0.1 přináší nové funkce a opravy chyb.", pos=(100,25))
                            dpg.add_text("Tento počítač momentálně nesplňuje minimální požadavky\npro spuštění Windblows 2064.0.0.1", pos=(100,50), color=(255,0,0))
                # Účty
                with dpg.tab(tag="settings.accounts", label="Účty"):
                    
                    dpg.add_image("messenger.image-roman_big", height=125, width=125, pos=(25,75))
                    dpg.add_text("ROMANEK", pos=(160,95))
                    dpg.add_text("r0m4njede@post.cz",color=(150,150,150) ,pos=(160,115))
                    dpg.add_text("Administrátor",color=(150,150,150), pos=(160,135))
                    
                    dpg.add_image("start.image-cloud", height=64, width=64, pos=(340,70))
                    dpg.add_text("SheepDrive", pos=(420,75))
                    dpg.add_text("Skoro plný",color=(150,150,150), pos=(420,95))
                    
                    dpg.add_image("start.image-web-browsing", height=64, width=64, pos=(330,125))
                    dpg.add_text("Webové Prohlížedí", pos=(420,140))
                    dpg.add_text("Vždy tě sleduje",color=(201,8,37), pos=(420,160))
                    
                    dpg.add_image("start.image-update", height=64, width=64, pos=(330,195))
                    dpg.add_text("Windblows Update", pos=(420,205))
                    dpg.add_text("Naposledy kontrolováno:",color=(150,150,150), pos=(420,225))
                    dpg.add_text("teď",color=(200,0,0), pos=(420,245))
                    
        #Poradce při potížích (sítě 💀)
        with dpg.window(tag="settings-network-help", label="Poradce při potížích", pos=(200,200), width=400, height=100, no_resize=True, no_collapse=True, show=False, on_close=lambda: dpg.hide_item("settings-network-help")):
            dpg.add_text("Poradce při potížích nenalezl žádné problémy.", color=(0,255,0), pos=(5,40), wrap=390)

    def licence_cb(self, sender, app_data, user_data):
        filename = f"{user_data}-LICENCE.txt"
        dpg.get_item_user_data("text")(filename)
        self.taskbar_open("text", filename)
        dpg.show_item("text")

    def settings_gaming_color_cb(self, sender, app_data, user_data):
        for item in dpg.get_all_items():
            if dpg.get_item_type(item) == "mvAppItemType::mvText":
                dpg.configure_item(item, color=choice(((255, 0, 179), (245,245,10))))

    def set_notification_disable_function(self, fun: callable):
        self.settings_system_notifications_cb = fun

    def calculate_update_size(self):
        if get_progress_requirement(self.progress["progress"], "1###############"):
            self.update_size += random()*random()*10
            self.update_size = round(self.update_size, 2)
            update_count = (self.update_size**0.2)
            dpg.set_value("start.text2", f"Před vypnutím systému prosím nainstalujte veškeré dostupné aktualizace\n(celkem {self.update_size} TB)")
            dpg.set_value("settings.update.progressbar", (update_count)/10.0)
            dpg.configure_item("settings.update.progressbar", overlay=f"Stahování aktualizací: {round(15*(update_count))}/{round(self.update_size*15, None)}")
        else:
            dpg.set_value("start.text2", f"\n\nKritická chyba:\nnedostatečné oprávnění")

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        dpg.set_value("start.username", progress["username"])
        dpg.set_value("start.guide", progress["progress"])

        if get_progress_requirement(self.progress["progress"], "1###############"):
            dpg.configure_item("settings.network.status", default_value="Jste připojeni k internetu", color=(0,255,0))
            dpg.show_item("settings.update.text1")
            dpg.show_item("settings.update.progressbar")
            dpg.show_item("settings.update.button")
            dpg.show_item("settings.update.promo")
            dpg.hide_item("settings.update.text2")

        self.points = 0

        # 0. - internet; 1. virus studio (stažení souboru, instalace); 2. počet dokončených součástí, 3.-9. součásti (poslední je nepoužitá), 10. ending sequence (spuštění)

        #připojení k internetu
        if get_progress_requirement(progress["progress"], "1###############"):
            self.points += 1
        #stažení souboru o instalaci Virus Studia z Datcordu
        #instalace Virus Studia
        if get_progress_requirement(progress["progress"], "#2##############"):
            self.points += 2
        #FTP Daemon - trubky
        if get_progress_requirement(progress["progress"], "###1############"):
            self.points += 3
        #FileTargetter - ATF
        if get_progress_requirement(progress["progress"], "####1###########"):
            self.points += 2
        #Anti-Antivir - shooter
        if get_progress_requirement(progress["progress"], "#####1##########"):
            self.points += 1
        #XSS Exploit - bludiště
        if get_progress_requirement(progress["progress"], "######1#########"):
            self.points += 3
        #Sandbox Exploit - pexeso
        if get_progress_requirement(progress["progress"], "#######1########"):
            self.points += 2
        #Mail Handler - spojovačka
        if get_progress_requirement(progress["progress"], "########1#######"):
            self.points += 1
        #TBD --- odstraněno - rezerovaný index 9
        #všechny součásti
        if get_progress_requirement(progress["progress"], "##6#############"):
            self.points += 2
        #export viru
        #spuštění ending sequence
        if get_progress_requirement(progress["progress"], "##########2#####"):
            self.points += 1
        #bsod

        dpg.set_value("start.progressbar", self.points/18)
        dpg.configure_item("start.progressbar", overlay=f"Postup: {round((self.points/18)*100, None)}% ({self.points} bod{'ů' if self.points >= 5 or self.points == 0 else ('y' if self.points >= 2 else '')})")
