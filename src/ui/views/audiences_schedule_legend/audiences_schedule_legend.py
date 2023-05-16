from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
import asynckivy as ak
from kivy.app import App


class AudiencesScheduleLegend(MDCard):
    schedule_view = ObjectProperty()
    department_hint_text = "Введите название кафедры"
    audience_hint_text = "Введите номер аудитории"

    def clear_results(self, *args):
        self.ids.audience.change_text_value("")
        self.ids.department.change_text_value("")
        self.schedule_view.clear_audiences()

    def clear_audience_selector_value(self, *args):
        self.ids.audience.change_text_value("")

    def send_command_to_get_departments_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_departments_selector(
                self.ids.department,
                self.ids.department.text,
            )
        )

    def send_command_to_get_audiences_numbers_depending_on_department(self, *args):
        ak.start(
            App.get_running_app().controller.fill_audiences_selector_depending_on_department(
                self.ids.audience,
                self.ids.audience.text,
                self.ids.department.text,
            )
        )

    def send_command_to_get_audience_numbers_depending_on_department(self, *args):
        ak.start(
            App.get_running_app().controller.update_schedule_view_audiences(
                self.schedule_view,
                self.ids.audience.text,
                self.ids.department.text,
            )
        )