import dearpygui.dearpygui as dpg

from windows.Window import Window

class WindowInvertor(Window):
    def __init__(self, theme = None):
        super().__init__("invertor", 420, 169, ["center", 0, 0], False, True, theme=theme, no_collapse=True, label="Abode Invertor(TM) 2076 Enterprise Edition")

        dpg.configure_item("invertor", on_close=lambda: (dpg.hide_item(self.tag), self.taskbar_close(self.tag), self.hide_error()))
        self.invertor_load = 0

        dpg.add_text("Abode", tag="invertor.title", parent="invertor")
        dpg.add_text("Invertor(TM) 2076 Enterprise Edition", tag="invertor.title2", parent="invertor")
        dpg.add_progress_bar(tag="invertor.bar", parent="invertor", width=self.width-20)
        dpg.add_text("© 1895 BCE - 2066 CE Abode Systems Intergalactic", tag="invertor.text", parent="invertor", color=(70, 70, 70))

        with dpg.child_window(tag="invertor.error", parent=self.tag, height=self.height-22, width=self.width, pos=(0,13), show=False):
            dpg.add_text("Kritická chyba!",tag="invertor.error.texthead", pos=(10,10))
            dpg.add_text("Program Abode Invertor(TM) 2076 Eneterprise Edition se zhroutil.\n\nPokud se tato chyba bude opakovat, kontaktuje prosím administrátora.",tag="invertor.error.text", pos=(10,40), wrap=self.width-20)
            dpg.add_button(label="Ok", tag="invertor.error.btn", pos=((self.width/2)-30,self.height-70), width=60, height=30, callback=lambda: (dpg.hide_item(self.tag), self.taskbar_close(self.tag), self.hide_error()))

    def show_error(self):
        dpg.show_item("invertor.error")
        dpg.configure_item("invertor", height=200)
        dpg.configure_item("invertor.error", height=178)
        dpg.configure_item("invertor.error.btn", pos=((self.width/2)-30,138))

    def hide_error(self):
        dpg.hide_item("invertor.error")
        dpg.configure_item("invertor", height=169)
        dpg.configure_item("invertor.error", height=140)
        dpg.configure_item("invertor.error.btn", pos=((self.width/2)-30, self.height-70))
        self.invertor_load = 0
        dpg.set_value("invertor.bar", self.invertor_load)

    def frame_update(self):

        if dpg.is_item_shown(self.tag):

            if self.invertor_load < 1:
                # self.delay(lambda:True, 10)
                self.invertor_load += 0.0005 if self.invertor_load < 0.5 else 0.00025 if self.invertor_load < 0.75 else 0.00015
                dpg.set_value("invertor.bar",self.invertor_load)

            elif self.invertor_load >= 1:
                self.show_error()
