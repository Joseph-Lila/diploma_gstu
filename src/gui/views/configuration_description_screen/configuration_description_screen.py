from datetime import date
from typing import List

from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from src.domain.entities import MentorLoadItem


class ConfigurationDescriptionScreenView(MDScreen):
    controller = ObjectProperty()

    def on_enter(self, *args):
        self.title_input.text = 'Мое расписание'
        self.year_input.text = str(date.today().year.real)
        self.author_input.text = ''
        self.update_workload()

    def update_workload(self, mentor_load_items: List[MentorLoadItem] = tuple()):
        if len(mentor_load_items) != 0:
            self.workload_title.text_color = 'black'
            self.workload_quantity.text_color = 'black'
            self.go_to_timetable_btn.disabled = False
        else:
            self.workload_title.text_color = 'red'
            self.workload_quantity.text_color = 'red'
            self.go_to_timetable_btn.disabled = True
        self.workload_quantity.text = str(len(mentor_load_items))
