from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, WipeTransition


class InnerScreenMasterView(ScreenManager):
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = WipeTransition()
