import dearpygui.dearpygui as dpg

from windows.Window import Window
from random import randint, choice

class WindowComponentMailHandler(Window):
    def __init__(self, theme = None):
        super().__init__("mail_handler", 900, 700, ["center", 0, 0], False, True, theme=theme, label="Mail Handler")
        #  Ne, tohle určitě není backport z HT1. Why would you even think that?

        self.node_count = 12  # Toto číslo určuje počet nodes, které se vytvoří. MUSÍ být vždy sudé číslo. #proč tam nedáš prostě polovinu a pak nevynásobíš dvěma
        self.node_links = {f"mail_handler.node{i}.attr":None for i in range(self.node_count)}
        self.node_links_correct = {f"mail_handler.node{i}.attr":False for i in range(self.node_count)}
        self.operands = ['+','-','/','*']
        self.problems = {}
        self.node_config = {"x_row1": 10,
                            "x_row2": self.width-200,
                            "spacing": 120, # výška nodu je 80px
                            }


        dpg.add_text("Spoj tečky u příkladů nalevo s tečkami výsledků napravo. Pokud uděláš chybu, podrž CTRL a klikni na čáru pro její odstranění.", tag="mail_handler.guide", wrap=self.width, parent=self.tag)

        attribute_setting = dpg.mvNode_Attr_Output
        x_pos = self.node_config["x_row1"]
        y_pos = 35

        with dpg.node_editor(callback=self.link_callback, delink_callback=self.delink_callback, tag="mail_handler.nodeeditor", parent=self.tag, tracked=True, track_offset=0.5):
            for i in range(self.node_count):
                if i == int(self.node_count/2):
                    attribute_setting = dpg.mvNode_Attr_Input
                    x_pos = self.node_config["x_row2"]
                    y_pos = 35

                with dpg.node(label=f"MailHandler node {i}", tag=f"mail_handler.node{i}", pos=(x_pos, y_pos), draggable=False):
                    with dpg.node_attribute(label=f"Node A{i}" , attribute_type=attribute_setting, tag=f'mail_handler.node{i}.attr'):
                        dpg.add_text(f"Node text{i}",tag=f"mail_handler.node{i}.attr.text")
                y_pos += 100
        self.update_problems()


    def on_complete(self):
        self.update_problems()
        self.set_progress(8, 1, "component")


    def check_link(self,node1,node2):
        #  Třeba nemám páru co tohle už dělá
        key, value = None, None
        for i in range(len(self.operands)):
            if self.operands[i] in node1:
                key, value = node1, node2
        else:
            key, value = node2, node1

        if str(self.problems[dpg.get_value(f"{value}.text")]) == str(dpg.get_value(f"{key}.text")):
            self.node_links_correct[node1] = True
            self.node_links_correct[node2] = True

        dict_values = list(self.node_links_correct.values())

        count_true = 0

        for i in range(len(self.node_links_correct)):
            if dict_values[i] == True:
                count_true += 1

        if count_true == self.node_count:
            dpg.configure_item(self.tag, show=False)

            dict_keys = list(self.node_links.keys())
            for i in range(int(self.node_count/2)):
                dpg.delete_item(f"{dict_keys[i]}, {self.node_links[dict_keys[i]]}")
            for i in range(self.node_count):
                self.node_links[dict_keys[i]] = None
                self.node_links_correct[dict_keys[i]] = False

            self.on_complete()

    #  Callback na spojeni 2 node_attributů
    def link_callback(self,sender, app_data):
        # app_data -> (link_id1, link_id2)
        link_id1, link_id2 = app_data

        if self.node_links[link_id1] == None and self.node_links[link_id2] == None:
            dpg.add_node_link(link_id1, link_id2, parent=sender,tag=f"{link_id1}, {link_id2}")
            self.node_links[link_id1] = link_id2
            self.node_links[link_id2] = link_id1
            self.check_link(link_id1,link_id2)

    #  Callback na rozpojeni 2 attributů
    def delink_callback(self, sender, app_data):
        # app_data -> link_id
        prasarna = tuple(map(str, app_data.split(", "))) # :) vraci tuple
        #  If it aint broke dont fix it
        dpg.delete_item(app_data)
        self.node_links[prasarna[0]] = None
        self.node_links[prasarna[1]] = None
        self.node_links_correct[prasarna[0]] = False
        self.node_links_correct[prasarna[1]] = False

    def generate_problem(self):
        num1, num2 = randint(0,100), randint(1,100)
        operant = choice(self.operands)
        match operant:
            case "+":
                self.problems.update({f"{num1}+{num2}":(num1+num2)})
                return [f"{num1}+{num2}",(num1+num2)]
            case "-":
                self.problems.update({f"{num1}-{num2}":(num1-num2)})
                return [f"{num1}-{num2}",(num1-num2)]
            case "/":
                self.problems.update({f"{num1}/{num2}":round((num1/num2),4)})
                return [f"{num1}/{num2}",round((num1/num2),4)]
            case "*":
                self.problems.update({f"{num1}*{num2}":(num1*num2)})
                return [f"{num1}*{num2}",(num1*num2)]

    def update_problems(self):
        problems_q = []
        problems_a = []
        for i in range(int(self.node_count/2)):
            temp_problem = self.generate_problem()
            problems_q.append(temp_problem[0])
            problems_a.append(temp_problem[1])

        picking_list = problems_q
        for i in range(self.node_count):
            if i == int(self.node_count/2):
                picking_list = problems_a
            pick = choice(picking_list)
            dpg.set_value(f"mail_handler.node{i}.attr.text",pick)
            picking_list.remove(pick)
