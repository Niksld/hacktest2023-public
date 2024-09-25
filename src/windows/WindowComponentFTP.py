import dearpygui.dearpygui as dpg
from configuration import LEVEL_DATA

from windows.Window import Window

class WindowComponentFTP(Window):
    def __init__(self, theme = None):
        super().__init__("ftp_daemon", 200, 200, ["center", 0, 0], False, True, theme=theme, label="FTP Daemon")
        self.levels = LEVEL_DATA["ftp_daemon"]
        self.current_level = 0
        self.has_loaded_level = False
        #rovná: 0 - nahoru+dolů, 1 - vlevo+vpravo
        #zatáčka: 0 - nahoru+vpravo, 1 - vpravo+dolů, 2 - dolů+vlevo, 3 - vlevo+nahoru
        dpg.add_text("1/5", parent="ftp_daemon", tag="ftp_daemon.level")
        dpg.add_button(label="Pokračovat", parent="ftp_daemon", tag="ftp_daemon.next_level", height=50, width=150, callback=self.next_level_cb, show=False)

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        if not self.has_loaded_level:
            self.start_level()

    def on_resize(self):
        super().on_resize()
        dpg.configure_item("ftp_daemon.level", pos=((self.width/2)-12, 45))
        dpg.configure_item("ftp_daemon.next_level", pos=((self.width/2)-75, self.height-65))

    def start_level(self):
        rows = self.levels[self.current_level]["rows"]
        columns = self.levels[self.current_level]["columns"]
        self.width = (columns+2)*76
        self.height = 170+rows*75
        dpg.configure_item("ftp_daemon", width=self.width, height=self.height)
        self.on_resize()
        dpg.set_value("ftp_daemon.level", f"{self.current_level+1}/{len(self.levels)}")

        for item in dpg.get_item_children("ftp_daemon", slot=1):
            if dpg.get_item_type(item) in ("mvAppItemType::mvImageButton", "mvAppItemType::mvImage"):
                dpg.delete_item(item)

        for row in range(rows):
            for column in range(columns):
                orientation = self.levels[self.current_level]["content"][row][column]
                if self.levels[self.current_level]["content"][row][column] >= 2:
                    #turn
                    dpg.add_image_button(f"ftp_daemon.image-turn{orientation-2}e", tag=f"ftp_daemon.button{column}-{row}", parent="ftp_daemon", user_data=[orientation, 0, column, row], width=75,height=75,pos=(76+column*76,95+row*75), callback=self.button_cb)
                else:
                    dpg.add_image_button(f"ftp_daemon.image-straight{orientation}e", tag=f"ftp_daemon.button{column}-{row}", parent="ftp_daemon", user_data=[orientation, 0, column, row], width=75,height=75,pos=(76+column*76,95+row*75), callback=self.button_cb)
        dpg.add_image("ftp_daemon.image-source", tag="ftp_daemon.source", parent="ftp_daemon", width=75,height=75,pos=(0, 95+self.levels[self.current_level]["source"]*75))
        dpg.add_image("ftp_daemon.image-destinatione", tag="ftp_daemon.destination", parent="ftp_daemon", width=75,height=75,pos=(76+columns*76, 95+self.levels[self.current_level]["destination"]*75))

        self.update()
        self.has_loaded_level = True

    def button_cb(self, sender, app_data, user_data):
        user_data=[(user_data[0]+1)%2 if user_data[0] < 2 else ((user_data[0]-1)%4)+2, user_data[1:]]
        dpg.configure_item(sender, texture_tag=f"ftp_daemon.image-{'straight' if user_data[0] < 2 else 'turn'}{user_data[0] if user_data[0] < 2 else user_data[0]-2}e", user_data=user_data)
        #nemusi se checkovat, pokud policko samo neni aktivni a nesousedi s aktivnim polickem
        self.update()

    def next_level_cb(self, sender, app_data, user_data):
        dpg.hide_item("ftp_daemon.next_level")
        if self.current_level < len(self.levels)-1:
            self.current_level += 1
            self.start_level()
        else:
            for item in dpg.get_item_children(self.tag, slot=1):
                dpg.hide_item(item)
            dpg.add_text("Implementace komponentu FTP Daemon úspěšná!", parent=self.tag, pos=((self.width/2)-175, (self.height/2)-10), color=(0, 255, 0))
            self.set_progress(3, 1, "component")


    def update(self):
        #deaktivace vsech policek
        try:
            for i in range(self.levels[self.current_level]["rows"]):
                for j in range(self.levels[self.current_level]["columns"]):
                    u = dpg.get_item_user_data(f"ftp_daemon.button{j}-{i}")
                    t = dpg.get_item_configuration(f"ftp_daemon.button{j}-{i}")["texture_tag"][:-1] + "e"
                    dpg.configure_item(f"ftp_daemon.button{j}-{i}", user_data=[u[0], 0, u[2:]], texture_tag=t)
        except:
            pass
        #urceni aktualni pozice a orientace
        curr_ori = dpg.get_item_user_data(f"ftp_daemon.button0-{self.levels[self.current_level]['source']}")[0]
        if curr_ori in (1,4,5):
            curr_pos = (0, self.levels[self.current_level]["source"])
            found = True

            while found:
                u = dpg.get_item_user_data(f"ftp_daemon.button{curr_pos[0]}-{curr_pos[1]}")
                t = dpg.get_item_configuration(f"ftp_daemon.button{curr_pos[0]}-{curr_pos[1]}")["texture_tag"][:-1] + "f"
                dpg.configure_item(f"ftp_daemon.button{curr_pos[0]}-{curr_pos[1]}", user_data=[u[0], 1, u[2:]], texture_tag=t)
                new_pos_options = self.get_next(curr_ori, *curr_pos)
                for i in range(2):
                    #kontrolovana pozice - nesmi byt mimo hraci plochu, nesmi byt predchozi pozice a musi byt navazujici na aktualni
                    new_pos = new_pos_options[i]
                    if new_pos != curr_pos and new_pos[0] >= 0 and new_pos[0] < self.levels[self.current_level]["columns"] and new_pos[1] >= 0 and new_pos[1] < self.levels[self.current_level]["rows"]:

                        new_ori = dpg.get_item_user_data(f"ftp_daemon.button{new_pos[0]}-{new_pos[1]}")[0]
                        if new_ori in new_pos_options[i+2] and dpg.get_item_user_data(f"ftp_daemon.button{new_pos[0]}-{new_pos[1]}")[1] == 0:
                            #nalezeno navazujici policko
                            curr_pos = new_pos
                            curr_ori = new_ori
                            break
                else:
                    break
        last_item = dpg.get_item_user_data(f"ftp_daemon.button{self.levels[self.current_level]['columns']-1}-{self.levels[self.current_level]['destination']}")
        if last_item[0] in (1,2,3) and last_item[1] == 1:
            dpg.configure_item("ftp_daemon.destination", texture_tag="ftp_daemon.image-destinationf")
            for item in dpg.get_item_children(self.tag, slot=1):
                if dpg.get_item_type(item) == "mvAppItemType::mvImageButton":
                    dpg.disable_item(item)
            dpg.show_item("ftp_daemon.next_level")
        else:

            dpg.configure_item("ftp_daemon.destination", texture_tag="ftp_daemon.image-destinatione")


    def get_next(self, orientation: int, x: int, y: int) -> tuple:
        match orientation:
            case 0:
                return (x,y-1), (x,y+1), (0,3,4), (0,2,5)
            case 1:
                return (x+1,y), (x-1,y), (1,4,5), (1,2,3)
            case 2:
                return (x,y-1), (x+1,y), (0,3,4), (1,4,5)
            case 3:
                return (x+1,y), (x,y+1), (1,4,5), (0,2,5)
            case 4:
                return (x,y+1), (x-1,y), (0,2,5), (1,2,3)
            case 5:
                return (x,y-1), (x-1,y), (0,3,4), (1,2,3)
        return (x,y), (x,y)
