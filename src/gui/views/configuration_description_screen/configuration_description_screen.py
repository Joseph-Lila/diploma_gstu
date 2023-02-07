from datetime import date

from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class ConfigurationDescriptionScreenView(MDScreen):
    controller = ObjectProperty()

    def on_enter(self, *args):
        self.title_input.text = 'Мое расписание'
        self.year_input.text = str(date.today().year.real)
        self.author_input.text = ''
