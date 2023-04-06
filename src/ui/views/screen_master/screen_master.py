from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition


class ScreenMasterView(ScreenManager):
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
