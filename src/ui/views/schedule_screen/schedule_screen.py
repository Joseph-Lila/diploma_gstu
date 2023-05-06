from dataclasses import astuple
from typing import Optional

from kivymd.uix.screen import MDScreen

import asynckivy as ak
from kivy.app import App

from src.adapters.orm import Schedule
from src.domain.enums import ViewType
from src.ui.schedule_master import ScheduleMaster
from src.ui.views import FileTabOptions, GroupsSchedule, AuditoriesSchedule, MentorsSchedule
from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog


class ScheduleScreenView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups_schedule: Optional[GroupsSchedule] = None
        self.audiences_schedule: Optional[AuditoriesSchedule] = None
        self.mentors_schedule: Optional[MentorsSchedule] = None
        self._init_file_tab_options_dialog()
        self.open_dialog = OpenDialog()
        self.create_dialog = CreateDialog()

    def _init_file_tab_options_dialog(self):
        self.file_tab_options_dialog = FileTabOptions()
        self.file_tab_options_dialog.ids.create_btn.bind(
            on_press=self.show_create_dialog
        )
        self.file_tab_options_dialog.ids.open_btn.bind(on_press=self.show_open_dialog)
        self.file_tab_options_dialog.ids.save_btn.bind(on_press=self.save_schedule)
        self.file_tab_options_dialog.ids.delete_btn.bind(on_press=self.delete_schedule)
        self.file_tab_options_dialog.ids.autocomplete_btn.bind(
            on_press=self.auto_filling
        )
        self.file_tab_options_dialog.ids.get_pdf_btn.bind(on_press=self.generate_pdf)
        self.file_tab_options_dialog.ids.close_btn.bind(on_press=self.close_screen)

    def change_schedule_view(self, segmented_control_instance, item_instance):
        is_current_control_first = segmented_control_instance == self.ids.first_segm_control
        manager = (
            self.ids.first_scr_mng
            if is_current_control_first
            else self.ids.second_scr_mng
        )
        if item_instance.text == "Группы":
            manager.current = "groups"
        elif item_instance.text == "Преподаватели":
            manager.current = "mentors"
        elif item_instance.text == "Аудитории":
            manager.current = "auditories"
        elif item_instance.text == "Нагрузка":
            manager.current = "workloads"

    def update_schedule_data(self, schedule: Schedule):
        ak.start(
            App.get_running_app().controller.update_schedule_metadata(schedule)
        )
        self.ids.head_label.text = f"Расписание занятий {schedule.term.lower()} семестр {schedule.year}-{schedule.year+1} учебный год"

    def move_specific_view_to_schedule_view(self, schedule_view_instance, view_type: ViewType):
        if view_type == ViewType.GROUP:
            # remove needed widget from its parent
            pass

    def close_screen(self, *args):
        self.file_tab_options_dialog.dismiss()
        App.get_running_app().root.go_to_home_screen()

    def show_open_dialog(self, *args):
        self.file_tab_options_dialog.dismiss()
        self.open_dialog.open(self)

    def show_create_dialog(self, *args):
        self.file_tab_options_dialog.dismiss()
        self.create_dialog.open()

    def delete_schedule(self, *args):
        self.file_tab_options_dialog.dismiss()
        ak.start(
            App.get_running_app().controller.delete_schedule()
        )
        App.get_running_app().root.go_to_home_screen()

    def save_schedule(self, *args):
        self.file_tab_options_dialog.dismiss()

    def auto_filling(self, *args):
        self.file_tab_options_dialog.dismiss()
        # TODO  save changes in database

    def generate_pdf(self, *args):
        self.file_tab_options_dialog.dismiss()
