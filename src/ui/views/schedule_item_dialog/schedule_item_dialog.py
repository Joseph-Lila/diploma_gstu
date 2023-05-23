from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
import asynckivy as ak


class ScheduleItemDialog(MDCard, ModalView):
    day_of_week_hint = 'Выберите день недели'

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
