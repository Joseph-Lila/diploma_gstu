from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog


class HomeScreenView(MDScreen):
    controller = ObjectProperty()

    def __draw_shadow__(self, origin, end, context=None):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_dialog = OpenDialog()
        self.create_dialog = CreateDialog()

    def show_open_dialog(self, *args):
        self.open_dialog.open()

    def show_create_dialog(self, *args):
        self.create_dialog.open()
