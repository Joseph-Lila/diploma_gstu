import asynckivy as ak
from kivymd.uix.screen import MDScreen


class LoadingScreenView(MDScreen):
    def on_enter(self, *args):
        ak.start(self.ids.progress.linear_load(self, self.ids.progress_label))
