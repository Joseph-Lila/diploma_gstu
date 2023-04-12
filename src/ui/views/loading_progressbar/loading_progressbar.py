import asynckivy as ak
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar


class LoadingProgressBar(ProgressBar):
    async def immediate_load(self, sender, progress_label, *args):
        self.value = 100
        progress_label.text = '100%'
        await ak.sleep(.001)
        Window.maximize()
        sender.manager.go_to_home_screen()

    async def linear_load(self, sender, progress_label, timedelta=.001, *args):
        for i in range(1, 101):
            await ak.sleep(timedelta)
            self.value = i
            progress_label.text = f'{i}%'
        Window.maximize()
        sender.manager.go_to_home_screen()
