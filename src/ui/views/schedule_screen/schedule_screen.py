from typing import Optional, List

from kivymd.uix.screen import MDScreen

import asynckivy as ak
from kivy.app import App

from src.adapters.orm import Schedule
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.interfaces import AbstractScheduleWeeksStore
from src.ui.views import FileTabOptions
from src.ui.views.create_dialog import CreateDialog
from src.ui.views.open_dialog import OpenDialog


class ScheduleScreenView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule_weeks_stores: List[AbstractScheduleWeeksStore] = [
            self.ids.group_1,
            self.ids.mentor_1,
            self.ids.audience_1,
            self.ids.group_2,
            self.ids.mentor_2,
            self.ids.audience_2,
        ]
        self._init_file_tab_options_dialog()

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
        is_current_control_first = (
            segmented_control_instance == self.ids.first_segm_control
        )
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
            manager.current = "audiences"
        elif item_instance.text == "Нагрузка":
            manager.current = "workloads"

    def update_schedule_data(self, schedule: Schedule):
        ak.start(App.get_running_app().controller.update_schedule_metadata(schedule))
        self.ids.head_label.text = f"Расписание занятий {schedule.term.lower()} семестр {schedule.year}-{schedule.year+1} учебный год"

    def close_screen(self, *args):
        self.file_tab_options_dialog.dismiss()
        App.get_running_app().root.go_to_home_screen()

    def show_open_dialog(self, *args):
        self.file_tab_options_dialog.dismiss()
        OpenDialog().open(self)

    def show_create_dialog(self, *args):
        self.file_tab_options_dialog.dismiss()
        CreateDialog().open()

    def delete_schedule(self, *args):
        self.file_tab_options_dialog.dismiss()
        ak.start(App.get_running_app().controller.delete_schedule())
        App.get_running_app().root.go_to_home_screen()

    def save_schedule(self, *args):
        self.file_tab_options_dialog.dismiss()
        # TODO save local changes (ask before it)

    def auto_filling(self, *args):
        self.file_tab_options_dialog.dismiss()
        # TODO  save changes in database

    def generate_pdf(self, *args):
        self.file_tab_options_dialog.dismiss()

    def send_command_to_refresh_cells(self, *args):
        ak.start(
            App.get_running_app().controller.get_actual_schedule_info_records(
                self,
            )
        )

    async def refresh_cells(self, info_records: List[ScheduleItemInfo]):
        for store in self.schedule_weeks_stores:
            await store.tune_using_info_records(info_records)
