import dearpygui.dearpygui as dpg
from random import uniform
from configuration import get_progress_requirement, LEVEL_DATA

from windows.Window import Window

class WindowNotification(Window):
    def __init__(self, theme_menu = None, theme_notification = None):
        super().__init__("notifcenter", 400, 350, ["bottomright", 0, -50], False, True, theme=theme_menu, no_collapse=True, no_move=True, popup=True, min_size=(400, 350), max_size=(400, 350), no_scrollbar=False, autosize=False)
        self.notification_data = LEVEL_DATA["notifications"]
        self.theme_notification = theme_notification
        self.history: list[str] = []
        self.currently_shown: list[str] = []
        self.external_notifications = 0
        self.limit = 5
        self.are_notifications_disabled = None

        #vytvoření všech "interních" oznámení určených v level.json, které se zobrazují po dosažení určitého postupu
        for i in range(len(self.notification_data)):
            with dpg.window(tag=f"notification{i}", label=self.notification_data[i]["app"], width=300, height=100, no_collapse=True, no_move=True, no_resize=True,
                            no_focus_on_appearing=True, no_scrollbar=True, no_close=self.notification_data[i]["important"], on_close=self.notification_closed_cb, user_data=self.notification_data[i], show=False):
                dpg.add_text(self.notification_data[i]["content"], wrap=290, indent=10)
        dpg.add_text("Historie oznámení", parent=self.tag)
        #to stejné, ale místo samostatných oken oznámení to jsou záznamy v historii
        for i in range(len(self.notification_data)):
            with dpg.child_window(parent=self.tag, tag=f"notifcenter.history{i}", autosize_x=True, height=110, show=False):
                dpg.add_text(self.notification_data[i]["app"], wrap=350)
                dpg.add_text(self.notification_data[i]["content"], wrap=350)

        if self.theme_notification is not None:
            for i in range(len(self.notification_data)):
                dpg.bind_item_theme(f"notification{i}", self.theme_notification)

        with dpg.item_handler_registry(tag=f"notification.handler-Datcord Messenger"):
            dpg.add_item_clicked_handler(callback=lambda: (dpg.show_item("msg"), dpg.focus_item("msg"), self.taskbar_open("msg", "Datcord Messenger")))
        with dpg.item_handler_registry(tag=f"notification.handler-Virus Studio"):
            dpg.add_item_clicked_handler(callback=lambda: (dpg.show_item("studio"), dpg.focus_item("studio"), self.taskbar_open("studio", "Virus Studio")))

    def set_notification_disable_function(self, fun: callable):
        self.are_notifications_disabled = fun

    def load_progress(self, progress: dict) -> None:
        super().load_progress(progress)
        #zavřít zobrazená oznámení, která nejdou zavřít křížkem, pokud byl dosažen maximální postup
        for notification in self.currently_shown:
            if dpg.get_item_user_data(notification)["important"] and not get_progress_requirement(progress["progress"], maximum_progress_string=dpg.get_item_user_data(notification)["progressmax"]):
                self.notification_closed_cb(notification, None, None)

        if self.are_notifications_disabled():
            return
        #zobrazit oznámení, která jsou v level.json a splňují podmínky pro zobrazení
        notifications_to_show = []
        for i in range(len(self.notification_data)):
            if f"notification{i}" not in self.history and get_progress_requirement(progress["progress"], self.notification_data[i]["progressmin"], self.notification_data[i]["progressmax"]):
                self.history.append(f"notification{i}")
                self.currently_shown.append(f"notification{i}")
                self.reposition_notifications()
                notifications_to_show.append(i)
        notifications_to_show_ids = self.delayed_notification_ids(notifications_to_show)
        notifications_to_show_durations = [uniform(0.5,2)]
        for i in range(len(notifications_to_show)-1):
            notifications_to_show_durations.append(uniform(1.5,3)+notifications_to_show_durations[-1])
        for i in range(len(notifications_to_show)):
            self.delay(lambda x=next(notifications_to_show_ids): (self.show_notification(f"notification{x}"), dpg.show_item(f"notifcenter.history{x}")), notifications_to_show_durations[i])

    #generátor pro delay: postupné předávání tagů oznámení, která se mají zobrazit
    def delayed_notification_ids(self, notification_tags: list) -> str:
        for tag in notification_tags:
            yield tag

    #vytvoření "externího" oznámení z jiného okna
    def external_notification(self, app: str, content: str, progressmin: str, progressmax: str, important: bool = False):
        if self.are_notifications_disabled():
            return
        external_notification_id = self.external_notifications
        self.external_notifications += 1
        with dpg.window(tag=f"notification{external_notification_id}e", label=app, width=300, height=100, no_collapse=True, no_move=True, no_resize=True,
                        no_focus_on_appearing=True, no_scrollbar=True, no_close=important, on_close=self.notification_closed_cb, user_data={"app": app, "content": content,
                        "progressmin": progressmin, "progressmax": progressmax, "important": important}, show=False):
            dpg.add_text(content, wrap=290, indent=10)

        with dpg.child_window(parent=self.tag, tag=f"notifcenter.history{external_notification_id}e", autosize_x=True, height=110):
            dpg.add_text(app, wrap=350)
            dpg.add_text(content, wrap=350)
        self.currently_shown.append(f"notification{external_notification_id}e")
        self.reposition_notifications()
        dpg.bind_item_theme(f"notification{external_notification_id}e", self.theme_notification)
        self.show_notification(f"notification{external_notification_id}e")

    #zobrazení oznámení, kontrola počtu zobrazených oznámení, přidání handleru pro otevření aplikace
    def show_notification(self, tag: str) -> None:
        if len(self.currently_shown) > self.limit:
            for notification in self.currently_shown:
                if not dpg.get_item_user_data(notification)["important"]:
                    self.notification_closed_cb(notification, None, None)
                    break

        app_on_click = dpg.get_item_user_data(tag)["app"]
        if app_on_click == "Datcord Messenger" or app_on_click == "Virus Studio":
            dpg.bind_item_handler_registry(dpg.get_item_children(tag, slot=1)[0], f"notification.handler-{app_on_click}")

        dpg.show_item(tag)
        if not dpg.get_item_user_data(tag)["important"]:
            self.delay(lambda: (tag in self.currently_shown and self.notification_closed_cb(tag, None, None)), 30)

        #callback při zavření oznámení, křížkem i automaticky
    def notification_closed_cb(self, sender, app_data, user_data) -> None:
        self.currently_shown.remove(sender)
        dpg.hide_item(sender)
        self.delay(self.reposition_notifications, 0.2)

    def reposition_notifications(self) -> None:
        for i, tag in enumerate(self.currently_shown):
            dpg.set_item_pos(tag, (dpg.get_viewport_client_width()-300, dpg.get_viewport_client_height()-160-105*i))

    def on_resize(self):
        super().on_resize()
        self.limit = int((dpg.get_viewport_client_height()-160)/105)
        self.reposition_notifications()
