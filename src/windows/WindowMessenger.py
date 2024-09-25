import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement, LEVEL_DATA
from random import uniform

from windows.Window import Window

class WindowMessenger(Window):
    def __init__(self, theme = None):
        super().__init__("msg", 850, 700, ["center", 0, 0], False, True, theme=theme, label="Datcord Messenger")
        self.conversation_data: dict = LEVEL_DATA["conversations"]
        self.shown_messages = []
        self.app_started = False
        self.defaultButton_theme = None
        self.not_an_option = False
        #offline okno
        with dpg.window(tag="msg-offline", label="Datcord Messenger Update", width=300, height=300, no_close=True, no_resize=True, show=False):
            dpg.add_image("msg.image-logo", width=150, height=150, pos=(75,30))
            dpg.add_loading_indicator(tag="msg-offline.loading", pos=(5,230), width=290, height=20, style=0, speed=1.5, color=(77,77,190,255), secondary_color=(41,40,65,255))
            dpg.add_text("Připojování...", tag="msg-offline.loadingtext", pos=(70,247), wrap=220)

        
        # nastavení
        
        with dpg.theme() as self.buttonSelected_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (51,51,84), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        
        self.settings_categories = {"Můj účet" : "my_account", "Zabezpečení": "security", "Vzhled" : "appearance", "Zvuk a Video":"voice_and_video", "Ostatní": "other"}
        categories_headline = ["Můj účet", "Zabezpečení", "Nastavení vzhledu", "Nastavení Zvuku a Videa", "Ostatní nastavení"]
        with dpg.window(tag="msg.settings", label="Datcod Messenger - Nastavení", width=800,height=600, no_resize=True, show=False, pos=(dpg.get_viewport_width()/2,(dpg.get_viewport_height()/2)-200)):
            
            count = 1
            for category, category_id in self.settings_categories.items():
                dpg.add_child_window(tag=f"msg.settings.{category_id}", label=category, width=590, height=560, pos=(200, 30), show=False)
                dpg.add_text(f"{categories_headline[count-1]}", tag=f"msg.settings.{category_id}.text", pos=(10,10), parent=f"msg.settings.{category_id}")
                dpg.add_button(tag=f"msg.settings.button.{category_id}", label=f"{category}", callback=self.show_settings_page, user_data=category_id ,pos=(15, 35*count), width=170, height=30)
                count += 1
            
            # my_account

            # profile banner
            with dpg.child_window(parent="msg.settings.my_account", tag="msg.settings.my_account.banner", pos=(285,10), width=300, height=400):
                # pfp a tag
                dpg.add_image("messenger.image-roman_big", width=120, height=120, pos=(10,20))
                dpg.add_text("R0m4n#0727", tag="msg.settings.my_account.name.text", pos=(150, 40))
                dpg.add_text('"Hackování je..."', tag="msg.settings.my_account.status", pos=(150, 60))
                # info
                
                # email
                dpg.add_input_text(readonly=True,tag="msg.settings.my_account.banner.email", pos=(10, 160), width=220, height=20, multiline=True)
                dpg.set_value("msg.settings.my_account.banner.email","E-mail: r0m4njede@post.cz")
                dpg.add_button(label="Změnit", pos=(240, 160), tag="tyhletagyjsoutotalnihovno2",callback=lambda: (dpg.set_value("msg.settings.my_account.banner.email","E-mail: skill@issue.com"), dpg.show_item("hejaledosttyhletagy2"), dpg.hide_item("tyhletagyjsoutotalnihovno2")))
                dpg.add_button(label="Odměnit", pos=(240, 160), show=False,tag="hejaledosttyhletagy2",callback=lambda: (dpg.set_value("msg.settings.my_account.banner.email","E-mail: r0m4njede@post.cz"), dpg.show_item("tyhletagyjsoutotalnihovno2"), dpg.hide_item("hejaledosttyhletagy2")))

                # telefon
                dpg.add_input_text(readonly=True,tag="msg.settings.my_account.banner.phone", pos=(10, 180), width=220, height=20, multiline=True)
                dpg.set_value("msg.settings.my_account.banner.phone","Telefon: **** *** **8 998")
                dpg.add_button(label="Odkrýt", pos=(240, 180), tag="tyhletagyjsoutotalnihovno",callback=lambda: (dpg.set_value("msg.settings.my_account.banner.phone","Telefon: +420 605 788 998"), dpg.show_item("hejaledosttyhletagy"), dpg.hide_item("tyhletagyjsoutotalnihovno")))
                dpg.add_button(label="Skrýt", pos=(240, 180), show=False,tag="hejaledosttyhletagy",callback=lambda: (dpg.set_value("msg.settings.my_account.banner.phone","Telefon: **** *** **8 998"), dpg.show_item("tyhletagyjsoutotalnihovno"), dpg.hide_item("hejaledosttyhletagy")))

                # Heslo
                self.text_created = False
                def set_err_text():
                    if not self.text_created:
                        dpg.add_text('Nelze změnit heslo "R0m4nJeNej123"\nNedostatečné oprávnení', color=(255,0,0), pos=(10, 222), parent="msg.settings.my_account.banner")
                        self.text_created = True
                
                dpg.add_input_text(readonly=True,tag="msg.settings.my_account.banner.password", pos=(10, 200), width=220, height=20, multiline=True)
                dpg.set_value("msg.settings.my_account.banner.password","Heslo: ***************")
                dpg.add_button(label="Změnit", pos=(240, 200),callback=set_err_text)
                
                # O mně    
                dpg.add_text("O mně", pos=(10, 260))
                dpg.add_text("----------------\nNadšenec do IT a hackování #L33TCREW\nJeden z TOP Hackerů ČR\nChci pracovat v: BSI\ndon't @ me", pos=(10, 270), wrap=250)

                
            # Změnit about me, už tam je vložený deep text
            dpg.add_text("Status", parent="msg.settings.my_account", pos=(10, 50))
            dpg.add_input_text(tag="msg.settings.my_account.status.input_box",hint="Zadejte nový status...", callback=self.set_status, pos=(10, 80), width=250, parent="msg.settings.my_account", on_enter=True)
            dpg.add_button(label="Změnit", callback=self.set_status, pos=(10, 100), width=250, height=30, parent="msg.settings.my_account")
            # barvičky
            
            dpg.add_text("Datcord Turbo:", parent="msg.settings.my_account", pos=(10, 150))
            dpg.add_text("Aktivní", parent="msg.settings.my_account", pos=(215, 150), color=(0,255,0))
            
            dpg.add_text("Dvoufázová autorizace:", parent="msg.settings.my_account", pos=(10, 180))
            dpg.add_text("Neaktivní", parent="msg.settings.my_account", pos=(200, 180), color=(255,0,0))
            
            dpg.add_text("Datcord věrnostní program:", parent="msg.settings.my_account", pos=(10, 210))
            dpg.add_text("Ano", parent="msg.settings.my_account", pos=(245, 210), color=(0,255,0))
            
            dpg.add_text("Zaplacené složenky:", parent="msg.settings.my_account", pos=(10, 240))
            dpg.add_text("Ne", parent="msg.settings.my_account", pos=(255, 240), color=(255,0,0))
            
            self.text_created2 = False
            def set_err_text2():
                if not self.text_created:
                    dpg.add_text('Nelze zapnout 2FA. Pro nastavení jděte do "Zabezpečení"', color=(255,0,0), pos=(80,450), parent="msg.settings.my_account")
                    self.text_created2 = True
                        
            dpg.add_button(label="Zapnout 2FA", parent="msg.settings.my_account", pos=(10, 350), width=250, height=50, callback=set_err_text2)
            
        # security
            
            # zbytečnej checkbox na poslání všech dat společnosti Datcord
            # smazat učet, request na data (GDPR)
            dpg.add_checkbox(tag="msg.settings.security.send_data", label="Poslat všechny osobní údaje společnosti Datcord",default_value=True, pos=(10, 40), parent="msg.settings.security", 
            callback=lambda: (dpg.add_text("That is not an option.", color=(255,0,0), pos=(10, 60), parent="msg.settings.security"),dpg.set_value("msg.settings.security.send_data", True), dpg.configure_item("msg.settings.security.send_data", enabled=False)))
            dpg.add_checkbox(label="Souhlasím se zpracováním dat k přeprodeji (a taky GDPR)",default_value=True, pos=(10, 80), parent="msg.settings.security")
            dpg.add_button(label="Smazat účet", parent="msg.settings.security", pos=(10, 120), width=200, height=30)
            self.text_created3 = False
            def set_err_text3():
                if not self.text_created:
                    dpg.add_text('Nelze zapnout 2FA. Pro nastavení jděte do "Můj Profil"', color=(255,0,0), pos=(80,450), parent="msg.settings.security")
                    self.text_created3 = True
                        
            dpg.add_button(label="Zapnout 2FA", parent="msg.settings.security", pos=(10, 200), width=590, height=50, callback=set_err_text3)
            
        # appearance
            dpg.add_text("Barevný režim ", tag="msg.settings.appearance.theme.text", pos=(10, 40), parent="msg.settings.appearance")
            dpg.add_combo(tag="msg.settings.appearance.theme", items=["Tmavý", "AMOLED", "10 Nit", "Světlý"], default_value="Tmavý", callback=self.check_listbox, pos=(150,40), width=250, parent="msg.settings.appearance")
            
            dpg.add_text("Moc se omlouváme, ale líní vývojáři ve společnosti Datcord tuto část nedodělali\n\nProsím nastavte si vzhled příště.",wrap=500, pos=(10, 120), parent="msg.settings.appearance")
            
        # voice_and_video
            # beep boop beep boop slidery a tlačidla
            # Zvuk
            dpg.add_text("Nastavení zvuku", pos=(10, 60), parent="msg.settings.voice_and_video")
            dpg.add_slider_int(label="Hlasitost vstupu (100%)", tag="msg.settings.inputvol",min_value=0, max_value=100,default_value=100, 
                               callback=lambda: (dpg.configure_item("msg.settings.inputvol", label=f"Hlasitost vstupu ({dpg.get_value('msg.settings.inputvol')}%)")),
                               pos=(10, 90), parent="msg.settings.voice_and_video")
            dpg.add_slider_int(label="Hlasitost výstupu (100%)", tag="msg.settings.outputvol",min_value=0, max_value=100,default_value=100, 
                               callback=lambda: (dpg.configure_item("msg.settings.outputvol", label=f"Hlasitost výstupu ({dpg.get_value('msg.settings.outputvol')}%)")),
                               pos=(10, 120), parent="msg.settings.voice_and_video")
            # bass boost mode
            dpg.add_checkbox(label="Zvýšit hlasitost mikrofonu (+30dB)",default_value=False, pos=(10, 150), parent="msg.settings.voice_and_video")
            
            dpg.add_checkbox(label="Potlačit šum",default_value=True, pos=(10, 170), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Potlačit ozvěnu",default_value=True, pos=(10, 190), parent="msg.settings.voice_and_video")
            dpg.add_text("Vstupní zařízení", parent="msg.settings.voice_and_video", pos=(10, 220))
            dpg.add_text("Výstupní zařízení", parent="msg.settings.voice_and_video", pos=(300, 220))
            dpg.add_combo(items=["Výchozí", "Vestavěný mikrofón", "OPS Virtuálné Audio"], default_value="Vestavěný mikrofón", pos=(10,240), width=250, parent="msg.settings.voice_and_video")
            dpg.add_combo(items=["Výchozí", "Vestavěné reproduktory", "OPS Virtuálné Audio"], default_value="Vestavěné reproduktory", pos=(300,240), width=250, parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Využít umělou inteligenci pro zvýšení kvality hlasu",default_value=True, pos=(10, 280), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Automaticky posílat hlasové nahrávky společnosti Datcord",default_value=True,enabled=False, pos=(10, 300), parent="msg.settings.voice_and_video")
            # video
            dpg.add_text("Nastavení videa", pos=(10, 350), parent="msg.settings.voice_and_video")
            dpg.add_text("Zdroj", parent="msg.settings.voice_and_video", pos=(10, 380))
            dpg.add_combo(items=["Výchozí", "Vestavěná kamera", "OPS Virtuálná kamera"], default_value="Výchozí", pos=(10,400), width=250, parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Automaticky vyvážit bílou",default_value=True, pos=(10, 420), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Využít umělou inteligenci pro zvýšení kvality obrazu",default_value=True, pos=(10, 440), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Posílat společnosti Datcord záznam obrazu (i když je kamera vypnuta)",default_value=True, enabled=False,pos=(10, 460), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="Zapnout hardwarovou akceleraci",default_value=True,pos=(10, 480), parent="msg.settings.voice_and_video")
            dpg.add_checkbox(label="V-Tuber filter",default_value=True, pos=(10, 500), parent="msg.settings.voice_and_video")
        # other
            
            # developer mode - on 😎
            dpg.add_checkbox(tag="msg.settings.other.developer_mode", label="Režim pro vývojáře",default_value=True, pos=(10, 40), parent="msg.settings.other")
            
            # Auto open on startup - on
            dpg.add_checkbox(tag="msg.settings.other.open_startup", label="Automaticky otevřít při spuštění Windblows",default_value=True, pos=(10, 70), parent="msg.settings.other")
            
            # language - Čeština (Pražská), Čeština (Moravská), Čeština (Ústecká), Čeština (Tradiční), Čeština (Slovenská), Čeština (Ostravská)
            dpg.add_text("Jazyk ", tag="msg.settings.other.language.text", pos=(10, 100), parent="msg.settings.other")
            
            dpg.add_combo(tag="msg.settings.other.language", items=["Čeština (Tradiční)", "Čeština (Zjednodušená)", "Čeština", "Čeština (Pražská)", "Čeština (Slovenská)", "Čeština Víno (Moravská)", "Čeština Pivo (Plzeň)", "Slovenský Jazyk (Čeština)", "Staročeština (Tradičnější)"], default_value="Čeština", callback=self.check_listbox, pos=(65,100), width=250, parent="msg.settings.other")
            
            self.show_settings_page(sender=None,app_data=None, user_data="my_account")

        #stage - zde jsou uloženy zprávy před tím, než se zobrazí
        with dpg.stage(tag="msg.stage"):
            for name, conversation in self.conversation_data.items():
                for i, message in enumerate(conversation["messages"]):
                    match message["event"]:
                        case None:
                            dpg.add_text((name if message["sender"] else "(ty)") + ": " + message["text"] + "\n ", tag=f"msg.conversation.{name}.{i}", user_data=message, color=(255,255,255) if message["sender"] else (195,255,210), wrap=630)
                        case "virus-studio-navod.txt":
                            dpg.add_button(label="Scr4per: <příloha: virus-studio-navod.txt>", tag=f"msg.conversation.{name}.{i}", height=40, user_data=message, callback=lambda: self.set_progress(1, 1))
                        case "blocked-sender":
                            dpg.add_text(f" \n[Zablokoval/a jste uživatele {name}]\n ", tag=f"msg.conversation.{name}.{i}", user_data=message, color=(255,30,30), wrap=630)
                        case "blocked":
                            dpg.add_text(f" \n[Uživatel {name} si vás zablokoval]\n ", tag=f"msg.conversation.{name}.{i}", user_data=message, color=(255,30,30), wrap=630)

        #levý panel - záhlaví
        with dpg.child_window(tag="msg.sidebartop", parent=self.tag, width=200, height=30, pos=(0,15)):
            dpg.add_text("Konverzace", tag="msg.sidebartop.text", pos=(10,5))

        #levý panel - seznam konverzací
        with dpg.child_window(tag="msg.sidebar", parent=self.tag, width=200, height=555, pos=(0,45)):
            for name, conversation in self.conversation_data.items():
                with dpg.child_window(tag=f"msg.sidebar.{name}", width=200, height=60, show=False):
                    dpg.add_image(conversation["image"], tag=f"msg.sidebar.{name}.image", width=50, height=50, pos=(5,5))
                    dpg.add_button(label=name, tag=f"msg.sidebar.{name}.name", pos=(60,0), height=60, width=140, user_data=name, callback=self.conversation_opened)

        #levý panel - profil
        with dpg.child_window(tag="msg.profile", parent=self.tag, width=200, height=100, pos=(0,600)):
            dpg.add_image_button("messenger.image-roman", tag="msg.profile.picture", width=40, height=40, pos=(10,10), callback=self.show_settings)
            dpg.add_text("R0m4n", tag="msg.profile.name", pos=(55,10))
            dpg.add_text('"Hackování je..."', tag="msg.profile.tag", pos=(55,30))
            dpg.add_image_button("messenger.image-mic0", tag="msg.profile.mic", width=30, height=30, pos=(20,60), user_data=1, callback=lambda s,a,u: dpg.configure_item(s, user_data=(u+1)%2, texture_tag=f"messenger.image-mic{u}"))
            dpg.add_image_button("messenger.image-sound0", tag="msg.profile.sound", width=30, height=30, pos=(60,60), user_data=1, callback=lambda s,a,u: dpg.configure_item(s, user_data=(u+1)%2, texture_tag=f"messenger.image-sound{u}"))
            dpg.add_image_button("messenger.image-cam1", tag="msg.profile.cam", width=30, height=30, pos=(100,60), user_data=0, callback=lambda s,a,u: dpg.configure_item(s, user_data=(u+1)%2, texture_tag=f"messenger.image-cam{u}"))
            dpg.add_image_button("messenger.image-settings", tag="msg.profile.settings", width=30, height=30, pos=(140,60), callback=self.show_settings)

        #záhlaví konverzace
        with dpg.child_window(tag="msg.topbar", parent=self.tag, width=650, height=30, pos=(200,15)):
            dpg.add_text(tag="msg.topbar.text", pos=(10,5), wrap=640)

        #obsah konverzace - každá konverzace je child okno s tagem msg.conversation.{name}
        #při přepnutí konverzace se jednoduše skryje a zobrazí se jiná
        #podobně jako u oznámení už všechny zprávy existují, ale jsou skryté
        with dpg.child_window(tag="msg.conversation", parent=self.tag, width=650, height=625, pos=(200,45)):
            for name in self.conversation_data.keys():
                dpg.add_child_window(tag=f"msg.conversation.{name}", width=650, height=625, show=False)

        #zápatí konverzace - vstupní pole a tlačítko pro odeslání zprávy
        with dpg.child_window(tag="msg.bottombar", parent=self.tag, width=650, height=30, pos=(200,670)):
            dpg.add_input_text(tag="msg.bottombar.input", hint="Zpráva", width=579, height=30, pos=(1,7), on_enter=True, callback=lambda:(dpg.set_value("msg.bottombar.input", ""), dpg.focus_item("msg.bottombar.input")))
            dpg.add_button(label="Odeslat", tag="msg.bottombar.send", width=70, height=30, pos=(580,0), callback=lambda:(dpg.set_value("msg.bottombar.input", ""), dpg.configure_item("msg.bottombar.input"), dpg.focus_item("msg.bottombar.input")))

        dpg.bind_item_theme("msg-offline", self.theme)

        with dpg.item_handler_registry(tag="msg.handler"):
            dpg.add_item_focus_handler(callback=self.focus_conversation)
        dpg.bind_item_handler_registry("msg.sidebartop", "msg.handler")
        dpg.bind_item_handler_registry("msg.sidebar", "msg.handler")
        dpg.bind_item_handler_registry("msg.profile", "msg.handler")
        dpg.bind_item_handler_registry("msg.topbar", "msg.handler")
        dpg.bind_item_handler_registry("msg.bottombar", "msg.handler")

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        #načítací okno
        if not self.app_started:
            if get_progress_requirement(self.progress["progress"], maximum_progress_string="1###############"):
                #před připojením k internetu
                self.delay(lambda: dpg.show_item("msg-offline"), 0.4)
                self.delay(lambda: (dpg.set_item_pos("msg-offline.loadingtext", (70,230)), dpg.set_value("msg-offline.loadingtext", "Načítání...\nZkontrolujte prosím\npřipojení k síti.")), 7)
            elif get_progress_requirement(self.progress["progress"], required_progress_string="1###############"):
                #po připojení k internetu (při každém startu hry, pokud je podmínka splněna - to je úmyslně)
                self.app_started = True
                dpg.show_item("msg-offline")
                dpg.set_item_pos("msg-offline.loadingtext", (70,245))
                dpg.set_value("msg-offline.loadingtext", "Vyhledávání aktualizací...")
                self.conversation_opened(None, None, "Scr4p3r")
                self.delay(lambda: (dpg.set_value("msg-offline.loadingtext", "Načítání...")), 1.1)
                self.delay(lambda: dpg.hide_item("msg-offline"), 2.6)
                self.delay(lambda: (dpg.show_item("msg"), dpg.focus_item("msg"), 
                self.taskbar_open("msg", "Datcord Messenger")), 3)

        #zobrazování zpráv v hlavním okně - vlastně je jedno, že se to děje předtím, než se připojí na net, protože se buď nic nestane, nebo to neuvidí
        messages_to_show = []
        messages_to_show_instantly = []
        for name, conversation in self.conversation_data.items():
            if get_progress_requirement(self.progress["progress"], conversation["progress"]):
                dpg.show_item(f"msg.sidebar.{name}")
                for i, message in enumerate(conversation["messages"]):
                    if f"msg.conversation.{name}.{i}" not in self.shown_messages:
                        if get_progress_requirement(self.progress["progress"], message["progressmin"], message["progressmax"]):
                            messages_to_show.append((f"msg.conversation.{name}", f"msg.conversation.{name}.{i}"))
                            self.shown_messages.append(f"msg.conversation.{name}.{i}")
                        elif get_progress_requirement(self.progress["progress"], message["progressmin"]):
                            messages_to_show_instantly.append((f"msg.conversation.{name}", f"msg.conversation.{name}.{i}"))
                            self.shown_messages.append(f"msg.conversation.{name}.{i}")

        #instantně se zobrazují zprávy pouze při prvotním spuštění hry, když byl dosažen minimální i maximální postup
        #pokud jen minimální, tak se zobrazují postupně a s oznámením
        for conversation_tag, message_tag in messages_to_show_instantly:
            dpg.move_item(message_tag, parent=conversation_tag)
        messages_to_show_ids = self.delayed_message_ids(messages_to_show)
        messages_to_show_durations = [uniform(2,2.5)]
        for i in range(len(messages_to_show)-1):
            messages_to_show_durations.append(uniform(1.5,2.1)+messages_to_show_durations[-1])
        for i in range(len(messages_to_show)):
            self.delay(lambda x=next(messages_to_show_ids): (dpg.move_item(x[1], parent=x[0]),
                       (not str(dpg.get_active_window()).startswith(".".join(x[1].split(".")[:2]))) and dpg.get_item_user_data(x[1])["sender"] and dpg.get_item_user_data(x[1])["event"] is None and self.notification("Datcord Messenger", dpg.get_value(x[1]), dpg.get_item_user_data(x[1])["progressmin"], dpg.get_item_user_data(x[1])["progressmax"], False)), messages_to_show_durations[i])

    def delayed_message_ids(self, converation_message_tags: list[tuple[str,str]]):
        for convo_tag, msg_tag in converation_message_tags:
            yield convo_tag, msg_tag

    def on_launch(self, data) -> bool:
        return self.app_started

    def on_resize(self) -> None:
        super().on_resize()
        dpg.set_item_pos("msg-offline", (dpg.get_viewport_client_width()//2-150, dpg.get_viewport_client_height()//2-150))

    def conversation_opened(self, sender, app_data, user_data) -> None:
        for item in dpg.get_item_children("msg.conversation", slot=1):
            dpg.hide_item(item)
        dpg.set_value("msg.topbar.text", user_data)
        dpg.show_item(f"msg.conversation.{user_data}")
        dpg.focus_item(f"msg.conversation.{user_data}")

    def focus_conversation(self, sender, app_data, user_data) -> None:
        for item in dpg.get_item_children("msg.conversation", slot=1):
            if dpg.is_item_shown(item):
                dpg.focus_item(item)
                break

    def check_listbox(self):
        if dpg.get_value("msg.settings.appearance.theme") == "Světlý":
            dpg.set_value("msg.settings.appearance.theme", "Tmavý")
    
    def show_settings_page(self, sender, app_data, user_data):
        for page in self.settings_categories.values():
            dpg.hide_item(f"msg.settings.{page}")
            dpg.bind_item_theme(f"msg.settings.button.{page}", self.defaultButton_theme)
        dpg.show_item(f"msg.settings.{user_data}")
        dpg.bind_item_theme(f"msg.settings.button.{user_data}", self.buttonSelected_theme)

    def show_settings(self):
        if not dpg.is_item_shown("msg.settings"):
            dpg.show_item("msg.settings")
        dpg.focus_item("msg.settings")

    def set_status(self):
        new_status = dpg.get_value("msg.settings.my_account.status.input_box")
        if new_status == None or new_status == "":
            dpg.set_value("msg.profile.tag",'"Hackování je..."')
            dpg.set_value("msg.settings.my_account.status", '"Hackování je..."')
        elif len(new_status) > 15:
            new_status = new_status[:12] + "..."
            dpg.set_value("msg.profile.tag", f'"{new_status}"')
            dpg.set_value("msg.settings.my_account.status", f'"{new_status}"')
        else:
            dpg.set_value("msg.profile.tag", f'"{new_status}"')
            dpg.set_value("msg.settings.my_account.status", f'"{new_status}"')
        dpg.set_value("msg.settings.my_account.status.input_box", "")