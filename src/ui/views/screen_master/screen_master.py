from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import NoTransition, ScreenManager

from src.ui import Screens


class ScreenMasterView(ScreenManager):
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()

    def go_to_home_screen(self):
        self.current = Screens.HOME_SCREEN.name
