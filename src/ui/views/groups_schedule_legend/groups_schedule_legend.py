from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
import asynckivy as ak
from kivy.app import App


class GroupsScheduleLegend(MDCard):
    schedule_view = ObjectProperty()
    faculty_hint_text = "Введите название факультета"
    group_hint_text = "Введите название группы"

    def clear_filters(self, *args):
        self.ids.group.change_text_value("")
        self.ids.faculty.change_text_value("")

    def clear_group_selector_value(self, *args):
        self.ids.group.change_text_value("")

    def send_command_to_get_faculties_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_faculties_selector(
                self.ids.faculty,
                self.ids.faculty.text,
            )
        )

    def send_command_to_get_groups_titles_depending_on_faculty(self, *args):
        ak.start(
            App.get_running_app().controller.fill_groups_selector_depending_on_faculty(
                self.ids.group,
                self.ids.group.text,
                self.ids.faculty.text,
            )
        )

    def send_command_to_get_group_titles_depending_on_faculty(self, *args):
        ak.start(
            App.get_running_app().controller.update_schedule_view_groups(
                self.schedule_view,
                self.ids.faculty.text,
                self.ids.group.text,
            )
        )
