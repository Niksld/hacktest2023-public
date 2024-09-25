import dearpygui.dearpygui as dpg

from windows.Window import Window

class WindowPaint(Window):
    def __init__(self, theme = None):
        super().__init__("paint", 800, 600, ["center", 0, 0], False, True, theme=theme, no_collapse=True, label="Kreslení", no_scrollbar=True)

        self.last_position = None
        self.tool = "point"
        self.tool_names = {"point": "Tečka", "squarepoint": "Čtverec", "eraser": "Guma"}

        # tool variables
        self.tool_size = 3
        self.tool_radius = self.tool_size/2
        self.tool_color = (0,0,0)

        with dpg.child_window(tag="paint.sidebar", parent=self.tag, height=self.height, width=100, pos=(0,0)):
            # sidebar elementy
            dpg.add_image_button("paint.image-dot", label="Tečka", tag="paint.sidebar.point", callback=self.set_tool, pos=(0,30), width=50, height=50)
            with dpg.tooltip("paint.sidebar.point", tag="paint.tooltip-point"):
                dpg.add_text("Tečka")
            dpg.add_image_button("paint.image-square",label="Čtverec", tag="paint.sidebar.squarepoint", callback=self.set_tool, pos=(50,30), width=50, height=50)
            with dpg.tooltip("paint.sidebar.squarepoint", tag="paint.tooltip-squarepoint"):
                dpg.add_text("Čtverec")
            dpg.add_image_button("paint.image-erase",label="Guma", tag="paint.sidebar.eraser", callback=self.set_tool, pos=(0,80), width=50, height=50)
            with dpg.tooltip("paint.sidebar.eraser", tag="paint.tooltip-eraser"):
                dpg.add_text("Guma")
            dpg.add_image_button("paint.image-clear",label="RESET", tag="paint.sidebar.clear", callback=self.clear, pos=(50,80), width=50, height=50)
            with dpg.tooltip("paint.sidebar.clear", tag="paint.tooltip-clear"):
                dpg.add_text("Resetovat")
            dpg.add_text("Velikost", tag="paint.sidebar.size_text", pos=(20,self.height-135))
            dpg.add_slider_int(label="Velikost", width=100, pos=(0,self.height-115), max_value=150, min_value=1,default_value=self.tool_size , callback=self.set_size)
            dpg.add_text("Nástroj:\nTečka", tag="paint.sidebar.mode_text", pos=(2,self.height-175),wrap=100)
            dpg.add_color_picker(tag="paint.sidebar.colorpicker",default_value=self.tool_color,pos=(0,self.height-90), width=100, no_inputs=True, callback=self.set_color)
        dpg.add_drawlist(tag="paint.drawlist", parent=self.tag, width=self.width, height=self.height-20, pos=(100,0))

    def set_tool(self, sender):
        tool = sender.split(".")[2]
        self.tool = tool
        dpg.set_value("paint.sidebar.mode_text", value=f"Nástroj:\n{self.tool_names[tool]}")

    def set_color(self, sender):
        self.tool_color = dpg.get_value(sender)

    def set_size(self, sender):
        self.tool_size = dpg.get_value(sender)
        self.tool_radius = self.tool_size/2

    def clear(self):
        dpg.draw_rectangle((100,0),(self.width,self.height),parent="paint.drawlist", color=(255,255,255),fill=(255,255,255))

    def draw_point(self, coordinates: list or tuple, is_erasing=False):
        """Vykreslí tečku na pozici kurzoru"""

        if is_erasing:
            temp_color_storage = self.tool_color
            self.tool_color = (255,255,255)

        dpg.draw_circle(parent="paint.drawlist",center=(coordinates[0], coordinates[1]),radius=self.tool_radius, color=self.tool_color, fill=self.tool_color)

        # Rozdíl minulé pozice x,y od aktuální
        if self.last_position != None:
            position_delta = [max(self.last_position[0], coordinates[0]) - min(self.last_position[0], coordinates[0]),
                            max(self.last_position[1], coordinates[1]) - min(self.last_position[1], coordinates[1])]

        #  Pokud je rozdíl moc velký, dokreslí čáru -> plynulá čára
            if position_delta[0] > self.tool_radius or position_delta[1] > self.tool_radius:
                dpg.draw_line(self.last_position, coordinates, parent="paint.drawlist", thickness=self.tool_size, color=self.tool_color)

        self.last_position = coordinates
        if is_erasing:
            self.tool_color = temp_color_storage

    def draw_squarepoint(self, coordinates: list or tuple):
        """Vykreslí čtverec na pozici kurzoru"""

        dpg.draw_rectangle((coordinates[0],coordinates[1]),(coordinates[0]+self.tool_size,coordinates[1]+self.tool_size) ,parent="paint.drawlist", color=self.tool_color, fill=self.tool_color)

        if self.last_position != None:
        # Rozdíl minulé pozice x,y od aktuální
            position_delta = [max(self.last_position[0], coordinates[0]) - min(self.last_position[0], coordinates[0]),
                            max(self.last_position[1], coordinates[1]) - min(self.last_position[1], coordinates[1])]

        #  Pokud je rozdil moc velký dokreslí čáru -> plynulá čára
            if position_delta[0] > self.tool_radius or position_delta[1] > self.tool_radius:
                dpg.draw_line((self.last_position[0]+self.tool_radius, self.last_position[1]+self.tool_radius), (coordinates[0]+self.tool_radius, coordinates[1]+self.tool_radius), parent="paint.drawlist", thickness=self.tool_size, color=self.tool_color)

        self.last_position = coordinates

    def draw_cursor(self):
        # Tato funkce bude mít nastarosti udělat kurzor u myši, aby člověk viděl kam kreslí/maže.
        pass

    def draw(self, coordinates: tuple or list):
        match self.tool:
            case "point":
                self.draw_point(coordinates)
            case "squarepoint":
                self.draw_squarepoint(coordinates)
            case "eraser":
                self.draw_point(coordinates, is_erasing=True)

    def frame_update(self):
        if dpg.is_item_shown("paint"):

            mouse_pos = dpg.get_mouse_pos()

            if mouse_pos[0] > self.width-2 or mouse_pos[1] > 580 or mouse_pos[0] < 105 or mouse_pos[1] < -10:
                self.last_position = None
            elif not dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
                    self.last_position = dpg.get_drawing_mouse_pos()
            elif dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
                self.draw(dpg.get_drawing_mouse_pos())
                # BUGFIX: Při větších velikostech toolů se překresluje jakoby i na taskbar. (Jak overspray irl) - pos nechce posunout element doprava.
                # Vzhledem k tomu, že drawlist nejde posunout doprava přes pos, tak prostě přemalovávám při každým kreslení sekci screenu, kde je sidebar.
                # Elementy jsou nad ním, child window se z nějakýho důvodu nechá překreslit. Takže ho malujem na základní barvu okna a nikdo nic netuší :)
                # - Matry (no kdo jinej by to sem takhle napsal že xd)
                # "Nemusíte psát dokumentaci, pokud je váš kód sebedokumentující" - Lenka Hrušková
                dpg.draw_rectangle((0,0),(100,self.height), parent="paint.drawlist", color=(20, 24, 22), fill=(20, 24, 22))
