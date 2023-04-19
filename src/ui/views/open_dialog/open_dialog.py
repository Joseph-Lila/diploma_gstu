from functools import partial
from typing import List

import asynckivy as ak
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard

from src.adapters.orm import Schedule
from src.ui.views.schedule_list_item import ScheduleListItem


class OpenDialog(MDCard, ModalView):
    year_hint = "Выберите год"
    term_hint = "Выберите семестр"

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.send_command_to_update_schedule_items()

    def clear_filters(self, *args):
        self.ids.year.change_text_value("")
        self.ids.term.change_text_value("")

    def send_command_to_get_years_values(self, *args):
        term = None if self.ids.term.text == "" else self.ids.term.text
        ak.start(
            App.get_running_app().controller.fill_years_selector_depending_on_schedule(
                self.ids.year,
                term,
            )
        )

    def send_command_to_get_terms_values(self, *args):
        year = None if self.ids.year.text == "" else int(self.ids.year.text)
        ak.start(
            App.get_running_app().controller.fill_terms_selector_depending_on_schedule(
                self.ids.term,
                year,
            )
        )

    def send_command_to_update_schedule_items(self):
        year = None if self.ids.year.text == "" else int(self.ids.year.text)
        term = None if self.ids.term.text == "" else self.ids.term.text
        ak.start(
            App.get_running_app().controller.update_open_dialog_schedules(
                self,
                year,
                term,
            )
        )

    async def update_items(self, new_items: List[Schedule]):
        self.ids.list_container.clear_widgets()
        for item in new_items:
            new_item = ScheduleListItem(schedule_item=item)
            new_item.bind(
                on_press=partial(App.get_running_app().root.go_to_schedule_screen, item)
            )
            new_item.bind(on_release=self.dismiss)
            self.ids.list_container.add_widget(new_item)
