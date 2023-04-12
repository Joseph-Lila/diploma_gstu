from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from src.adapters.orm import Schedule
from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog


class ScheduleScreenView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule = None
        self._init_tabs_menu_items()
        self._init_tab_menus()
        self.open_dialog = OpenDialog()
        self.create_dialog = CreateDialog()

    def update_metadata(self, schedule: Schedule):
        self.schedule = schedule
        self.ids.head_label.text = f"Расписание занятий {schedule.term.lower()} семестр {schedule.year}-{schedule.year+1} учебный год"

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
                "orientation": "horizontal",
                "color": "black",
                "height": 2,
            },
            {
                "text": "Автозаполнение",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._autofilling(),
            },
            {
                "viewclass": "MDSeparator",
                "orientation": "horizontal",
                "color": "black",
                "height": 2,
            },
            {
                "text": "Закрыть",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self._close_screen(),
            },
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
        App.get_running_app().root.go_to_home_screen()

    def _show_open_dialog(self, *args):
        self.file_tab_menu.dismiss()
        self.open_dialog.open(self)

    def _show_create_dialog(self, *args):
        self.file_tab_menu.dismiss()
        self.create_dialog.open()

    def _delete_schedule(self, *args):
        self.file_tab_menu.dismiss()
        # TODO  save changes in database

    def _autofilling(self, *args):
        self.file_tab_menu.dismiss()
        # TODO  save changes in database
