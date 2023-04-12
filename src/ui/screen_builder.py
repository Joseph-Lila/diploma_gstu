from src.ui.screens_enum import Screens
from src.ui.views.screen_master import ScreenMasterView


def get_main_screen(controller):
    screen_master = get_screen_master(controller)
    screens = get_screens(controller)
    for screen in screens:
        screen_master.add_widget(screen)
    return screen_master


def get_screen_master(controller):
    screen_master = ScreenMasterView()
    screen_master.controller = controller
    return screen_master


def get_screens(controller):
    screens = [
        screen.value(name=screen.name)
        for screen in Screens
    ]
    for screen in screens:
        screen.controller = controller
    return screens
