from src.ui.screens_enum import Screens
from src.ui.views.screen_master import ScreenMasterView


def get_main_screen():
    screen_master = get_screen_master()
    screens = get_screens()
    for screen in screens:
        screen_master.add_widget(screen)
    return screen_master


def get_screen_master():
    screen_master = ScreenMasterView()
    return screen_master


def get_screens():
    screens = [
        screen.value(name=screen.name)
        for screen in Screens
    ]
    return screens
