import dearpygui.dearpygui as dpg

from configuration import *
from GameSession import GameSession
from windows.Desktop import Desktop
from windows.Taskbar import Taskbar
from windows.WindowCrash import WindowCrash
from windows.WindowTitle import WindowTitle
from windows.WindowDebug import WindowDebug
from windows.WindowNotification import WindowNotification
from windows.WindowText import WindowText
from windows.WindowWifi import WindowWifi
from windows.WindowStart import WindowStart
from windows.WindowInvertor import WindowInvertor
from windows.WindowTerminal import WindowTerminal
from windows.WindowMessenger import WindowMessenger
from windows.WindowPaint import WindowPaint
from windows.WindowInternet import WindowInternet
from windows.WindowStudio import WindowStudio
from windows.WindowComponentSandbox import WindowComponentSandbox
from windows.WindowComponentFileTargetter import WindowComponentFileTargetter
from windows.WindowComponentXSS import WindowComponentXSS
from windows.WindowComponentFTP import WindowComponentFTP
from windows.WindowComponentMailHandler import WindowComponentMailHandler
from windows.WindowComponentAntiAV import WindowComponentAntiAV
from windows.WindowCalc import WindowCalc

dpg.create_context()

#font
with dpg.font_registry():
    with dpg.font(relpath("fonts/RobotoMono-Regular.ttf"), 19) as roboto:
        dpg.add_font_range(0x0100, 0x25FF)
    with dpg.font(relpath("fonts/RedHatMono-Regular.ttf"), 19) as redhat:
        dpg.add_font_range(0x0100, 0x017F)
    with dpg.font(relpath("fonts/RobotoMono-Regular.ttf"), 25) as roboto_large:
        dpg.add_font_range(0x0100, 0x017F)

    dpg.bind_font(roboto)

# globalni theme
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (14,10,12), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (14,10,12), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (43,0,45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (100,0,99), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (153,0,36), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (199,0,44), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (206,15,50), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20,24,22), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (153,0,36), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (109,109,109), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (109,109,109), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (109,109,109), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvImageButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (109,109,109), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (109,109,109), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (109,109,109), category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)
with dpg.theme() as Desktop_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)

# themes oken
with dpg.theme() as Taskbar_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (45,20,20), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Border, (40,15,15), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (40,15,15), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvImageButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowCrash_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200,20,20), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowDebug_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240,240,240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (170,170,170), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200,200,220), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200,200,240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (5,5,5), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (180,180,180), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (200,200,200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240,240,240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (225,225,225), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (240,240,240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (225,225,225), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowNotification_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (250,250,197), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (250,250,197), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (250,250,197), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (5,5,5), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 15, category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowMessenger_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (31,30,55), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 15, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (32,32,52), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (51,51,84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (61,61,99), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (83,82,102), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (88,87,107), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (93,92,112), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowMessengerSettings_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 29, 47), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 15, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        
with dpg.theme() as WindowMessengerSettingsContainer_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 29, 47), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (31,30,55), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 15, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (32,32,52), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (51,51,84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (61,61,99), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (83,82,102), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (88,87,107), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (93,92,112), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowMessengerSettingsBanner_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 29, 47), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (31,30,55), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41,40,65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 15, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (32,32,52), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (51,51,84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (61,61,99), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (83,82,102), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (88,87,107), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (93,92,112), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowTerminal_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0,0,0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0,255,0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35,35,35), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (55,55,55), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (35,35,35), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowPaint_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255,255,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (20, 24, 22), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 136, 227), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (80, 146, 237), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowInternet_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (160,160,160), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (160,160,160), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200,200,200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (200,200,200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240,240,240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (76,146,172), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (106,176,202), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (116,186,212), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (150,150,150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (76,146,172), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (150,150,150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0,0,0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowStudio_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowComponentFTP_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_IndentSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (62, 71, 92), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (124, 144, 191), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (134, 154, 201), category=dpg.mvThemeCat_Core)

with dpg.theme() as WindowComponentSandbox_theme:
    with dpg.theme_component(dpg.mvImageButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (153,0,36), category=dpg.mvThemeCat_Core)
        
with dpg.theme() as WindowCalc_theme:
    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (153,0,36), category=dpg.mvThemeCat_Core)

        

#debug okno se všemi stylovými prvky
# dpg.show_style_editor()

#obrázky
with dpg.texture_registry():
    for device in set([x["image"] for x in LEVEL_DATA["desktop_icons"]]):
        imagedata = dpg.load_image(relpath(f"images/{device}.png")) #0: width, 1: height, 2: channels, 3: data
        dpg.add_static_texture(imagedata[0], imagedata[1], imagedata[3], tag=f"desktop.image-{device}")
    for image in LEVEL_DATA["images"]:
        imagedata = dpg.load_image(relpath(f"images/{image['image']}.png"))
        dpg.add_static_texture(imagedata[0], imagedata[1], imagedata[3], tag=image['parent'] + ("." if image['parent'] != "" else "") + f"image-{image['name']}")


#viewport, ve kterém se zobrazují okna
dpg.create_viewport(
    title=f"Hacktest 2023 {RELEASE_VERSION}"
         + (" (offline)" if OFFLINE_MODE else f" ({SERVER_IP}:{SERVER_PORT}"
         + ("*)" if DEFAULT_SERVER_IP != SERVER_IP or DEFAULT_SERVER_PORT != SERVER_PORT else ")")),
    width=1000,
    height=750,
    min_width=1000,
    min_height=750,
    resizable=True,
    small_icon=relpath("images/hacker.ico"),
    large_icon=relpath("images/hacker.ico"))

session = GameSession()

# vytvoření všech oken
session.add_desktop(Desktop(Desktop_theme))

session.add_taskbar(Taskbar(Taskbar_theme))
session.desktop.set_taskbar_app_function(session.taskbar.app_opened)

session.add_window(WindowNotification(theme_notification=WindowNotification_theme))
session.windows["notifcenter"].set_notification_disable_function(session.get_disabled_notifications)


session.add_window(WindowStart())
session.windows["start"].set_notification_disable_function(session.set_disabled_notifications)

session.add_window(WindowWifi())

session.add_window(WindowCrash(WindowCrash_theme))

session.add_window(WindowTitle())
dpg.set_item_callback("title.btn", session.start_title_screen)
if USERFILE_RESET:
    dpg.set_value("title.error", "Soubor s lokálně uloženými daty byl odstraněn.")

session.add_window(WindowDebug(WindowDebug_theme))

session.add_window(WindowText())

session.add_window(WindowInvertor())
session.add_frame_update_function(session.windows["invertor"].frame_update)

session.add_window(WindowInternet(WindowInternet_theme))

session.add_window(WindowTerminal(WindowTerminal_theme))

session.add_window(WindowMessenger(WindowMessenger_theme))
dpg.bind_item_theme("msg.settings", WindowMessenger_theme)
dpg.bind_item_font("msg", redhat)
dpg.bind_item_font("msg-offline", redhat)
for category in session.windows["msg"].settings_categories.values():
    dpg.bind_item_font(f"msg.settings.{category}.text", roboto_large)
    dpg.bind_item_theme(f"msg.settings.{category}", WindowMessengerSettings_theme)
    dpg.bind_item_theme(f"msg.settings.button.{category}", WindowMessengerSettings_theme)
    dpg.bind_item_font(f"msg.settings.button.{category}", roboto_large)
session.windows["msg"].defaultButton_theme = WindowMessengerSettings_theme
dpg.bind_item_theme("msg.settings", WindowMessengerSettingsContainer_theme)
dpg.bind_item_theme("msg.settings.my_account.banner", WindowMessengerSettingsBanner_theme)

# Nejde to po dobrým tak to půjde po zlým >:(
dpg.bind_item_theme("msg.settings.button.my_account", session.windows["msg"].buttonSelected_theme)


session.add_window(WindowPaint(WindowPaint_theme))
session.add_frame_update_function(session.windows["paint"].frame_update)

session.add_window(WindowStudio(WindowStudio_theme))
dpg.bind_item_font("studio.sidebar.project", roboto_large)
for component in session.windows["studio"].components:
    dpg.bind_item_font(f"studio.component.{component}.headline", roboto_large)

session.add_window(WindowComponentSandbox(WindowComponentSandbox_theme))

session.add_window(WindowComponentFileTargetter())
session.add_frame_update_function(session.windows["file_targetter"].frame_update)

session.add_window(WindowComponentXSS())

session.add_window(WindowComponentFTP(WindowComponentFTP_theme))

session.add_window(WindowComponentMailHandler())

session.add_window(WindowComponentAntiAV())
session.add_frame_update_function(session.windows["anti_av"].frame_update)

session.add_window(WindowCalc(WindowCalc_theme))


# fullscreen
dpg.set_viewport_resize_callback(session.on_resize)
with dpg.handler_registry():
    dpg.add_key_press_handler(dpg.mvKey_F11, callback=lambda: dpg.toggle_viewport_fullscreen())

# render loop
dpg.show_item("title")
dpg.setup_dearpygui()
dpg.maximize_viewport() if DEBUG else dpg.toggle_viewport_fullscreen()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    session.frame_update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
