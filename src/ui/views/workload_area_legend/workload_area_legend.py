from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivy.app import App
import asynckivy as ak

from src.adapters.orm import Schedule


class WorkloadAreaLegend(MDCard):
    schedule_view = ObjectProperty()

    mentor_hint_text = "Преподаватель"
    group_hint_text = "Группа"
    subject_type_hint_text = "Тип занятия"
    subject_hint_text = "Предмет"

    def clear_filters(self, *args):
        self.ids.mentor.change_text_value("")
        self.ids.group.change_text_value("")
        self.ids.subject_type.change_text_value("")
        self.ids.subject.change_text_value("")

    def send_command_to_get_mentors_fios(self, *args):
        ak.start(
            App.get_running_app().controller.fill_mentors_selector(
                self.ids.mentor,
                self.ids.mentor.text,
            )
        )

    def send_command_to_get_groups_titles(self, *args):
        ak.start(
            App.get_running_app().controller.fill_groups_selector(
                self.ids.group,
                self.ids.group.text,
            )
        )

    def send_command_to_get_subjects_titles(self, *args):
        ak.start(
            App.get_running_app().controller.fill_subjects_selector(
                self.ids.subject,
                self.ids.subject.text,
            )
        )

    def send_command_to_get_subject_types_titles(self, *args):
        ak.start(
            App.get_running_app().controller.fill_subject_types_selector(
                self.ids.subject_type,
                self.ids.subject_type.text,
            )
        )

    def send_command_to_get_workload_data(self, *args):
        schedule: Schedule = App.get_running_app().controller.model.schedule_master
        if schedule is None:
            raise

        year = schedule.year
        term = schedule.term
        ak.start(
            App.get_running_app().controller.get_workloads(
                self.schedule_view,
                self.ids.group.text,
                self.ids.subject.text,
                self.ids.subject_type.text,
                self.ids.mentor.text,
                year,
                term,
            )
        )
