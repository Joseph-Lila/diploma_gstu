from functools import partial
from typing import List

import asynckivy as ak
from kivy.app import App
from kivymd.uix.screen import MDScreen

from src.adapters.orm import Schedule
from src.ui.controller import do_with_loading_modal_view
from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog
from src.ui.views.schedule_list_item import ScheduleListItem


class HomeScreenView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_dialog = OpenDialog()
        self.create_dialog = CreateDialog()

    def on_enter(self, *args):
        self.send_command_to_update_latest_10_schedules()

    def show_open_dialog(self, *args):
        self.open_dialog.open(self)

    def show_create_dialog(self, *args):
        self.create_dialog.open()

    async def update_latest_10_schedules(self, schedules: List[Schedule]):
        self.ids.recent_items_list_instance.clear_widgets()
        for item in schedules:
            new_item = ScheduleListItem(schedule_item=item)
            new_item.bind(
                on_press=partial(App.get_running_app().root.go_to_schedule_screen, item)
            )
            self.ids.recent_items_list_instance.add_widget(new_item)

    def send_command_to_update_latest_10_schedules(self):
        ak.start(
            App.get_running_app().controller.update_latest_10_schedules(self)
        )
