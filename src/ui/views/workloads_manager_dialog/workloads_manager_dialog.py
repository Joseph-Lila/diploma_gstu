from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.screenmanager import MDScreenManager
import asynckivy as ak


class WorkloadsManagerDialog(MDScreenManager, ModalView):
    mentor_hint = "Выберите преподавателя"

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)

    def send_command_to_get_mentors_fios(self, *args):
        ak.start(
            App.get_running_app().controller.fill_mentors_selector(
                self.ids.mentor,
                self.ids.mentor.text,
            )
        )
