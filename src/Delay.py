import dearpygui.dearpygui as dpg

class Delay:
    def __init__(self):
        self.delayed_actions = []
        self.delayed_looping_actions = []

    def add(self, action: callable, delay: float = 1.0, looping: bool = False, looping_times: int = 1):
        """Přidá funkci, která má být zavolána po určitém čase."""
        if not looping:
            self.delayed_actions.append((action, dpg.get_total_time() + delay))
        else:
            self.delayed_looping_actions.append([action, dpg.get_total_time() + delay, delay, looping_times])

    def update(self):
        """Vykoná funkce, které mají být zavolány."""
        time = dpg.get_total_time()
        for action in self.delayed_actions:
            try:
                if action[1] <= time:
                    self.delayed_actions.remove(action)
                    action[0]()
            except Exception as e:
                print("Chyba vykonávání opožděné akce", e, action)

        for i in range(len(self.delayed_looping_actions)-1, -1, -1):
            try:
                if self.delayed_looping_actions[i][1] <= time:
                    self.delayed_looping_actions[i][0]()
                    if self.delayed_looping_actions[i][3] > 1:
                        self.delayed_looping_actions[i][1] = time + self.delayed_looping_actions[i][2]
                        self.delayed_looping_actions[i][3] -= 1
                    else:
                        self.delayed_looping_actions.pop(i)
            except Exception as e:
                print("Chyba vykonávání opakované opožděné akce", e, action)

    def drop(self):
        """Zruší všechny akce."""
        self.delayed_actions = []
        self.delayed_looping_actions = []
