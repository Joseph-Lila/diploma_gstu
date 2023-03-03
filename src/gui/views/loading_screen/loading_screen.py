from functools import partial

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class LoadingScreenView(MDScreen):
    def __draw_shadow__(self, origin, end, context=None):
        pass

    controller = ObjectProperty()

    def activate_progress_bar(self, timedelta, *args):
        value = self.ids.progress.value
        self.ids.progress.value = value + 1
        self.ids.progress_label.text = f"{value + 1}%"
        if value + 1 < 100:
            Clock.schedule_once(partial(self.activate_progress_bar, timedelta), timedelta)
        else:
            self.controller.screen_master_controller.go_to_home_screen()
