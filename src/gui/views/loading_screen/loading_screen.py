import asyncio
import time
from functools import partial

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
import asynckivy as ak


class LoadingScreenView(MDScreen):
    def __draw_shadow__(self, origin, end, context=None):
        pass

    controller = ObjectProperty()

    def on_kv_post(self, base_widget):
        self.increment_progress_value()

    def increment_progress_value(self, *args):
        value = self.ids.progress.value
        self.ids.progress.value = value + 1
        self.ids.progress_label.text = f"{value + 1}%"
        if value + 1 < 100:
            Clock.schedule_once(self.increment_progress_value, 0.01)
