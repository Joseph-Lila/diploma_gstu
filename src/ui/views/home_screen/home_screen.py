from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from src.ui.views.open_dialog import OpenDialog


class HomeScreenView(MDScreen):
    controller = ObjectProperty()

    def __draw_shadow__(self, origin, end, context=None):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_dialog = OpenDialog()

    def show_open_dialog(self, *args):
        self.open_dialog.open()
