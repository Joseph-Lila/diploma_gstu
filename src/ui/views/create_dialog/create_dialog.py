import asyncio

import asynckivy as ak
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard

from src.ui.controller import do_with_loading_modal_view


class CreateDialog(MDCard, ModalView):
    default_year_menu_value = "Выберите год"
    default_term_menu_value = "Выберите семестр"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.year.ids.right_icon_button.bind(
            on_press=self.send_command_to_get_years_values
        )
        self.ids.term.ids.right_icon_button.bind(
            on_press=self.send_command_to_get_terms_values
        )

    def send_command_to_get_years_values(self, *args):
        term = (
            None
            if self.ids.term.text == self.default_term_menu_value
            else self.ids.term.text
        )
        ak.start(
            do_with_loading_modal_view(
                App.get_running_app().controller.fill_years_selector_depending_on_workload,
                self.ids.year,
                term,
            )
        )

    def send_command_to_get_terms_values(self, *args):
        year = (
            None
            if self.ids.year.text == self.default_year_menu_value
            else int(self.ids.year.text)
        )
        ak.start(
            do_with_loading_modal_view(
                App.get_running_app().controller.fill_terms_selector_depending_on_workload,
                self.ids.term,
                year,
            )
        )

    def send_command_to_create_schedule(self, *args):
        year = (
            None
            if self.ids.year.text == self.default_year_menu_value
            else int(self.ids.year.text)
        )
        term = (
            None
            if self.ids.term.text == self.default_term_menu_value
            else self.ids.term.text
        )
        ak.start(
            do_with_loading_modal_view(
                App.get_running_app().controller.try_to_create_schedule,
                self,
                year,
                term,
            )
        )

    async def check_if_new_schedule_is_created(self, new_schedule):
        if new_schedule is not None:
            self.ids.outcome_text_input.text = "Расписание успешно создано!"
            await asyncio.sleep(1)
            App.get_running_app().root.go_to_schedule_screen(new_schedule)
            self.dismiss()
        else:
            self.ids.outcome_text_input.text = (
                "Расписание с заданными параметрами уже существует."
            )
