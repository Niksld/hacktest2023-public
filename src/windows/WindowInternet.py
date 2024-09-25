import dearpygui.dearpygui as dpg
from configuration import get_progress_requirement, LEVEL_DATA

from windows.Window import Window

class WindowInternet(Window):
    def __init__(self, theme = None):
        super().__init__("internet", 900, 525, ["center", 0, 0], False, True, theme=theme, label="Webový prohlížeč WaterWhale", no_collapse=True, no_move=False)
        self.website_data = LEVEL_DATA["websites"]
        self.last_image = None

        with dpg.child_window(parent=self.tag, tag="internet.top", pos=(0,20), width=900, height=30):
            dpg.add_image_button("internet.image-home", tag="web.homepage", pos=(5,5), width=25, height=25, callback=lambda: (dpg.set_value("web.url", "gogel.gg"), self.url_callback("web.url", None, None)))
            dpg.add_input_text(tag="web.url", pos=(35, 9), width=860, callback=self.url_callback, on_enter=True, hint="URL")
            with dpg.tooltip("web.homepage", tag="web.tooltip-homepage"):
                dpg.add_text("Domovská stránka", tag="web.tooltip-homepage.text")

        #tohle by pro přehlednost mělo být v mainu, ale koho to zajímá
        #v tuhle chvíli se s barvičkami snad už nebude haprovat
        with dpg.theme() as t:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
        dpg.bind_item_theme("web.tooltip-homepage.text", t)

        with dpg.child_window(parent=self.tag, tag="internet.content", pos=(0,50), width=900, height=475):
            #gogel
            dpg.add_input_text(tag="web.gogel.search", width=400, height=33, pos=((900+400)/2-400, (550+33)/2-50), hint="Najdi tam, co neví ani Bůh sám", callback=self.gogel_search_cb, on_enter=True)
            dpg.add_button(tag="web.gogel.searchbtn", label="Hledat", width=100, height=33, pos=((900+400)/2+400-100, (550+33)/2-50))

        dpg.add_drawlist(parent=self.tag, tag="internet.drawlist", pos=(0,50), width=900, height=500)

        for item in dpg.get_item_children("internet.content")[1]:
            dpg.hide_item(item)

        dpg.set_value("web.url", "gogel.gg")
        self.load_website(**self.website_data["gogel.gg"], url="gogel.gg")

    def update_loading_text(self):
        dots = 0
        while True:
            if dots < 3:
                dots += 1
            else:
                dots = 0
            yield f"Načítání{dots*'.'} - Webový prohlížeč WaterWhale"

    def url_callback(self, sender, app_data, user_data):
        dpg.disable_item("web.url")
        dpg.disable_item("web.homepage")
        entered_url = dpg.get_value("web.url")
        for item in dpg.get_item_children("internet.content")[1]:
            dpg.hide_item(item)
        if self.last_image is not None:
            dpg.delete_item(self.last_image)
        text = self.update_loading_text()
        for i in range(12):
            self.delay(lambda: dpg.set_item_label("internet", next(text)), i*0.25)
        if entered_url in self.website_data.keys() and get_progress_requirement(self.progress["progress"], "1###############"):
            self.delay(lambda: self.load_website(**self.website_data[entered_url], url=entered_url), 3)
        else:
            self.delay(lambda: self.load_website(name=entered_url, size=[900,500], elements=[], url="null"), 3)

    def load_website(self, **kwargs):
        dpg.configure_item("internet.drawlist", width=kwargs["size"][0], height=kwargs["size"][1])
        self.last_image = dpg.draw_image(f"internet.image-{kwargs['url']}", (0,0), kwargs["size"], parent="internet.drawlist")
        for element in kwargs["elements"]:
            dpg.show_item(element)
        dpg.set_item_label("internet", kwargs["name"] + " - Webový prohlížeč WaterWhale")
        dpg.enable_item("web.url")
        dpg.enable_item("web.homepage")

    def gogel_search_cb(self, sender, app_data, user_data):
        dpg.set_value("web.url", dpg.get_value(sender))
        dpg.get_item_callback("web.url")(sender, app_data, user_data)
