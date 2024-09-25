import dearpygui.dearpygui as dpg
from random import sample

from configuration import get_progress_requirement
from windows.Window import Window

class WindowComponentSandbox(Window):
    def __init__(self, theme = None):
        super().__init__("sandbox_exploit", 600, 500, ["center", 0, 0], False, True, theme=theme, label="Sandbox Exploit")
        self.combination_counter = 0
        self.previous_user_data = None
        self.previous_sender = None
        self.correct_combinations = {1:10, 2:5, 3:20, 4:6, 7:11, 8:16, 9:13, 12:18, 14:19, 15:17}
        self.images = ["1", "2", "3", "4", "2", "4", "5", "6", "7", "1", "5", "8", "7", "9", "10", "6", "10", "8", "9", "3"]
        self.hidden_images = []
        self.errors = 0

        for i in range(1,21):
            dpg.add_image_button(f"sandbox_exploit.image-sbempty", tag=f"sandbox_exploit.button{i}", parent=f"sandbox_exploit", user_data=i, width=95, height=95, pos=(((i-1)%5)*100+50, ((i-1)//5)*100+50), callback=self.button_cb)

        dpg.add_text(tag="sandbox_exploit.text", parent=self.tag, pos=(200,200), show=False)
        dpg.add_input_int(tag="sandbox_exploit.input", parent=self.tag, pos=(200,250), width=200, on_enter=True, callback=self.input_cb, step=0, step_fast=0, show=False)

    def button_cb(self, sender, app_data, user_data):
        if self.combination_counter != 2:
            if self.previous_user_data != user_data:
                dpg.configure_item(f"sandbox_exploit.button{user_data}", texture_tag=f"sandbox_exploit.image-sb{self.images[user_data-1]}")
                self.combination_counter+= 1
                if self.combination_counter == 2:
                    for i in range(1,21):
                        dpg.disable_item(f"sandbox_exploit.button{i}")
                    self.delay(lambda: self.combination_delayed(sender, user_data), 3.0)
                    return
            else:
                self.previous_user_data = None
                self.previous_sender = None
                dpg.configure_item(sender, label=f"{user_data}")
                self.combination_counter = 0
                return

            self.previous_user_data = user_data
            self.previous_sender = sender

    def combination_delayed(self, sender, user_data):
        for key, val in self.correct_combinations.items():
            if (key == user_data and val == self.previous_user_data) or (key == self.previous_user_data and val == user_data):
                dpg.hide_item(self.previous_sender)
                dpg.hide_item(sender)
                self.hidden_images.append(self.previous_user_data)
                self.hidden_images.append(user_data)
                break
            else:
                for i in self.hidden_images:
                    dpg.hide_item(f"sandbox_exploit.button{i}")
        else:
            self.errors += 1
            if self.errors%6 == 2:
                self.mathematics()

        if len(self.hidden_images) == 20:
            dpg.add_text("Implementace komponentu Sandbox Exploit úspěšná", tag="sandbox_exploit.completed", parent=self.tag, pos=(50,200), color=(0,255,0))
            dpg.add_text("Doufám, že jsi použil/a kalkulačku :D", tag="sandbox_exploit.completed2", parent=self.tag, pos=(50,300), color=(40,40,40))
            self.set_progress(7, 1, "component")


        dpg.configure_item(sender, texture_tag=f"sandbox_exploit.image-sbempty")
        dpg.configure_item(self.previous_sender, texture_tag=f"sandbox_exploit.image-sbempty")
        self.combination_counter = 0
        self.previous_user_data = None
        self.previous_sender = None
        for i in range(1,21):
            dpg.enable_item(f"sandbox_exploit.button{i}")

    def mathematics(self):
        for i in range(1,21):
            dpg.hide_item(f"sandbox_exploit.button{i}")
        numbers = sample(range(-20,21), 4)
        result = sum(numbers)
        prompt = f"{numbers[0]}{' + ' if numbers[1] > 0 else ' - '}{abs(numbers[1])}{' + ' if numbers[2] > 0 else ' - '}{abs(numbers[2])}{' + ' if numbers[3] > 0 else ' - '}{abs(numbers[3])} = "

        dpg.set_value("sandbox_exploit.text", prompt)
        dpg.set_item_user_data("sandbox_exploit.input", result)
        dpg.show_item("sandbox_exploit.text")
        dpg.show_item("sandbox_exploit.input")
        if get_progress_requirement(self.progress["progress"], maximum_progress_string="###########1####"):
            self.set_progress(11, 1, "simple")

    def input_cb(self, sender, app_data, user_data):
        if user_data == dpg.get_value(sender):
            dpg.hide_item("sandbox_exploit.input")
            dpg.hide_item("sandbox_exploit.text")
            for i in range(1,21):
                if i not in self.hidden_images:
                    dpg.show_item(f"sandbox_exploit.button{i}")
        dpg.set_value(sender, 0)
