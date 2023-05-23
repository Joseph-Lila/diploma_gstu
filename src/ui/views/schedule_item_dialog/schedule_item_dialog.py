from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
import asynckivy as ak


class ScheduleItemDialog(MDCard, ModalView):
    day_of_week_hint = 'Выберите день недели'
    pair_number_hint = 'Выберите номер пары'
    week_type_hint = 'Выберите тип недели'
    subgroup_hint = 'Выберите подгруппу'
    mentor_hint = 'Выберите преподавателя'
    audience_number_hint = 'Выберите аудиторию'
    subject_hint = 'Выберите предмет'
    subject_type_hint = 'Выберите тип предмета'

    def __init__(self, touched_slave, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.touched_slave = touched_slave

        self.set_info_records()

    def get_info_records(self):
        pass

    def set_info_records(self):
        pass

    def send_command_to_get_day_of_week_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_day_of_week_selector(
                self.ids.day_of_week
            )
        )

    def send_command_to_get_pair_number_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_pair_number_selector(
                self.ids.pair_number
            )
        )

    def send_command_to_get_week_type_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_week_type_selector(
                self.ids.week_type
            )
        )

    def send_command_to_subgroup_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_subgroup_selector(
                self.ids.subgroup
            )
        )

    def send_command_to_get_mentor_values(self, *args):
        pass

    def send_command_to_get_audience_number_values(self, *args):
        pass

    def send_command_to_get_subject_values(self, *args):
        pass

    def send_command_to_get_subject_type_values(self, *args):
        pass
