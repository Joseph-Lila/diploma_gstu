import asyncio

import asynckivy as ak
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard


class CreateDialog(MDCard, ModalView):
    year_hint = "Выберите год"
    term_hint = "Выберите семестр"

    def on_pre_open(self):
        self.ids.year.change_text_value("")
        self.ids.term.change_text_value("")

    def send_command_to_get_years_values(self, *args):
        term = None if self.ids.term.text == "" else self.ids.term.text
        ak.start(
            App.get_running_app().controller.fill_years_selector_depending_on_workload(
                self.ids.year,
                term,
            )
        )

    def send_command_to_get_terms_values(self, *args):
        year = None if self.ids.year.text == "" else int(self.ids.year.text)
        ak.start(
            App.get_running_app().controller.fill_terms_selector_depending_on_workload(
                self.ids.term,
                year,
            )
        )

    def send_command_to_create_schedule(self, *args):
        year = None if self.ids.year.text == "" else int(self.ids.year.text)
        term = None if self.ids.term.text == "" else self.ids.term.text
        ak.start(
            App.get_running_app().controller.try_to_create_schedule(
                self,
                year,
                term,
            )
        )

    async def check_if_new_schedule_is_created(self, new_schedule):
        if new_schedule is not None:
            self.ids.outcome_text_input.text = "Расписание успешно создано!"
            await asyncio.sleep(1)
            self.dismiss()
            App.get_running_app().root.go_to_schedule_screen(new_schedule)
        else:
            self.ids.outcome_text_input.text = (
                "Расписание с заданными параметрами уже существует."
            )
