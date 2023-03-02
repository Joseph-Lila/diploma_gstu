from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class ScreenMasterView(MDScreen):
    def __draw_shadow__(self, origin, end, context=None):
        pass

    controller = ObjectProperty()
