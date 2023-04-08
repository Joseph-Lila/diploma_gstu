from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog


class ScheduleScreenView(MDScreen):
    controller = ObjectProperty()
    term = StringProperty()
    year = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tabs_menu_items()
        self._init_tab_menus()
        self.open_dialog = OpenDialog()
        self.create_dialog = CreateDialog()

    def __draw_shadow__(self, origin, end, context=None):
        pass

    def _init_tabs_menu_items(self):
        self.file_tab_menu_items = [
            {
                "text": "Создать",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._show_create_dialog(),
            },
            {
                "text": "Открыть",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._show_open_dialog(),
            },
            {
                "text": "Удалить",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._delete_schedule(),
            },
            {
                "viewclass": "MDSeparator",
                "orientation": 'horizontal',
                "color": 'black',
                "height": 2,
            },
            {
                "text": "Автозаполнение",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._autofilling(),
            },
            {
                "viewclass": "MDSeparator",
                "orientation": 'horizontal',
                "color": 'black',
                "height": 2,
            },
            {
                "text": "Закрыть",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._close_screen(),
            }
        ]

    def _init_tab_menus(self):
        self.file_tab_menu = MDDropdownMenu(
            caller=self.ids.file_tab,
            items=self.file_tab_menu_items,
            width_mult=4,
            max_height=250,
        )

    def _close_screen(self, *args):
        self.file_tab_menu.dismiss()
        self.controller.screen_master_controller.go_to_home_screen()

    def _show_open_dialog(self, *args):
        self.file_tab_menu.dismiss()
        self.open_dialog.open()

    def _show_create_dialog(self, *args):
        self.file_tab_menu.dismiss()
        self.create_dialog.open()

    def _delete_schedule(self, *args):
        self.file_tab_menu.dismiss()
        # TODO  save changes in database

    def _autofilling(self, *args):
        self.file_tab_menu.dismiss()
        # TODO  save changes in database
