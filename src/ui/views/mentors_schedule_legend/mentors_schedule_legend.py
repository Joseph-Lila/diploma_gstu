from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
import asynckivy as ak
from kivy.app import App


class MentorsScheduleLegend(MDCard):
    schedule_view = ObjectProperty()
    mentor_hint_text = "Введите ФИО преподавателя"
    department_hint_text = "Введите название кафедры"

    def clear_filters(self, *args):
        self.ids.mentor.change_text_value("")
        self.ids.department.change_text_value("")

    def clear_mentor_selector_value(self, *args):
        self.ids.mentor.change_text_value("")

    def send_command_to_get_departments_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_departments_selector(
                self.ids.department,
                self.ids.department.text,
            )
        )

    def send_command_to_get_mentors_titles_depending_on_department(self, *args):
        department = (
            None if self.ids.department.text == "" else self.ids.department.text
        )
        ak.start(
            App.get_running_app().controller.fill_mentors_selector_depending_on_department(
                self.ids.mentor,
                self.ids.mentor.text,
                department,
            )
        )
