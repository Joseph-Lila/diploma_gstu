from kivymd.uix.screen import MDScreen
import asynckivy as ak


class LoadingScreenView(MDScreen):
    def on_enter(self, *args):
        ak.start(self.ids.progress.immediate_load(self, self.ids.progress_label))
