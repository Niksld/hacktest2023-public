import dearpygui.dearpygui as dpg
from configuration import LEVEL_DATA
from random import choice, uniform

from windows.Window import Window

class WindowComponentFileTargetter(Window):
    def __init__(self, theme = None):
        super().__init__("file_targetter", 500, 700, ["center", 0, 0], False, True, theme=theme, label="FileTargetter", no_collapse=True)
        self.words = LEVEL_DATA["file_targetter_words"]
        self.paused = True
        self.shown_words = {}
        self.correct = 0
        self.errors = 0
        self.last_update_time = dpg.get_total_time()

        dpg.add_text("Proces učení můžeš zahájit tlačítkem níže.\n\nPro úspěch je potřeba zadat 15 slov, tolerují se maximálně 3 chyby. Při selhání můžeš proces opakovat.", tag="file_targetter.info", parent="file_targetter", pos=(50, 100), wrap=390)
        dpg.add_button(label="Začít", tag="file_targetter.start", parent="file_targetter", width=400, height=50, pos=(50, 500), callback=self.start)
        dpg.add_text("Správně: 0/15", tag="file_targetter.correct", parent="file_targetter", pos=(50, 600))
        dpg.add_text("Chyby: 0/4", tag="file_targetter.errors", parent="file_targetter", pos=(370, 600))
        dpg.add_input_text(tag="file_targetter.input", parent="file_targetter", width=400, height=50, pos=(50, 650), no_spaces=True, hint="Zadej slova...", on_enter=True, callback=self.input_cb, enabled=False)

    def place_word(self):
        word = choice([x for x in self.words if x not in self.shown_words.keys()])
        self.shown_words[word] = (dpg.add_text(word, parent="file_targetter", pos=(uniform(50, 485-(len(word)*7)), uniform(20, 200))))

    def start(self, sender, app_data, user_data):
        dpg.hide_item("file_targetter.start")
        dpg.hide_item("file_targetter.info")
        dpg.set_value("file_targetter.correct", f"Správně: {self.correct}/15")
        dpg.set_value("file_targetter.errors", f"Chyby: {self.errors}/4")
        dpg.enable_item("file_targetter.input")
        dpg.focus_item("file_targetter.input")
        self.place_word()
        self.place_word()
        self.paused = False

    def input_cb(self, sender, app_data, user_data):
        user_input = dpg.get_value(sender)
        if user_input in self.shown_words.keys():
            dpg.delete_item(self.shown_words[user_input])
            del self.shown_words[user_input]
            self.correct += 1
            dpg.set_value("file_targetter.correct", f"Správně: {self.correct}/15")
        dpg.set_value(sender, "")
        dpg.focus_item(sender)

    def frame_update(self):
        if dpg.is_item_shown(self.tag) and not self.paused:
            delta_time = dpg.get_total_time() - self.last_update_time
            if delta_time > 0.05:
                self.last_update_time = dpg.get_total_time()
                if len(self.shown_words) == 0:
                    self.place_word()
                picked_text_word = choice(list(self.shown_words.keys()))
                picked_text = self.shown_words[picked_text_word]
                picked_text_coords = dpg.get_item_pos(picked_text)
                if picked_text_coords[1] > 550:
                    del self.shown_words[picked_text_word]
                    dpg.delete_item(picked_text)
                    self.errors += 1
                    dpg.set_value("file_targetter.errors", f"Chyby: {self.errors}/4")
                    self.place_word()
                else:
                    not_red = int(255 - ((picked_text_coords[1] - 200)/350 * 200)) if picked_text_coords[1] > 300 else 255
                    dpg.configure_item(picked_text, color=(255, not_red, not_red), pos=(picked_text_coords[0], picked_text_coords[1] + 4))

                if uniform(0,1) < 0.04 and len(self.shown_words) < 5:
                    self.place_word()

                if self.errors >= 4:
                    self.paused = True
                    for item in self.shown_words.values():
                        dpg.delete_item(item)
                    dpg.disable_item("file_targetter.input")
                    dpg.set_value("file_targetter.input", "")
                    dpg.set_value("file_targetter.info", f"Kritická chyba: proces učení AI selhal.\nOpakuj prosím pokus.\n\nSprávně: {self.correct}/15\nChyby: {self.errors}/4")
                    dpg.show_item("file_targetter.info")
                    dpg.configure_item("file_targetter.start", label="Zkusit znovu")
                    dpg.show_item("file_targetter.start")
                    self.shown_words = {}
                    self.correct = 0
                    self.errors = 0

                elif self.correct >= 15:
                    self.paused = True
                    for item in dpg.get_item_children("file_targetter", slot=1):
                        dpg.hide_item(item)
                    dpg.add_text("Implementace komponentu FileTargetter úspěšná.", tag="file_targetter.info2", parent="file_targetter", pos=(50, 100), wrap=390, color=(0,255,0))
                    self.set_progress(4, 1, "component")
