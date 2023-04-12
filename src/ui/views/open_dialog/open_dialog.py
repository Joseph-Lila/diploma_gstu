from typing import List

import asynckivy as ak
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard

from src.adapters.orm import Schedule
from src.ui.controller import do_with_loading_modal_view
from src.ui.views.schedule_list_item import ScheduleListItem


class OpenDialog(MDCard, ModalView):
    default_year_menu_value = 'Выберите год'
    default_term_menu_value = 'Выберите семестр'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.year.ids.right_icon_button.bind(on_press=self.send_command_to_get_years_values)

    def clear_filters(self, *args):
        self.ids.year.text = self.default_year_menu_value
        self.ids.term.text = self.default_term_menu_value

    def send_command_to_get_years_values(self, *args):
        term = None if self.ids.term.text == self.default_term_menu_value else self.ids.term.text
        ak.start(
            do_with_loading_modal_view(
                App.get_running_app().controller.bind_dropdown_menu_for_years_selector,
                self.ids.year,
                term,
            )
        )

    def send_command_to_update_schedule_items(self):
        year = None if self.ids.year.text == self.default_year_menu_value else int(self.ids.year.text)
        term = None if self.ids.term.text == self.default_term_menu_value else self.ids.term.text
        ak.start(
            do_with_loading_modal_view(
                App.get_running_app().controller.update_open_dialog_schedules,
                self,
                year,
                term,
            )
        )

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.send_command_to_update_schedule_items()

    async def update_items(self, new_items: List[Schedule]):
        self.ids.list_container.clear_widgets()
        for item in new_items:
            self.ids.list_container.add_widget(
                ScheduleListItem(schedule_item=item)
            )
