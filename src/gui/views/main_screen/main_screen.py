from typing import List

import asynckivy as ak
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen

from src.config import ROOT_DIR
from src.domain.entities import MentorLoadItem
from src.domain.utils import FileManagerOpeningMods


class MainScreenView(MDScreen):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path_using_file_manager,
            ext=['.csv'],
            selector='file',
        )
        self._file_manager_opening_mode = FileManagerOpeningMods.IMPORT
        self._success_import_dialog = self.__init_success_import_dialog()
        self._success_export_dialog = self.__init_success_export_dialog()

    @staticmethod
    def __init_success_import_dialog():
        dialog = ModalView(size_hint=(None, None), size=(390, 240), auto_dismiss=False)
        content = Factory.SuccessImportDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.add_widget(content)
        return dialog

    @staticmethod
    def __init_success_export_dialog():
        dialog = ModalView(size_hint=(None, None), size=(390, 240), auto_dismiss=False)
        content = Factory.SuccessExportDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.add_widget(content)
        return dialog

    async def set_configuration_screen(self):
        self.content_manager.current = 'configuration_description_screen'

    async def set_start_screen(self):
        self.content_manager.current = 'start_screen'

    def open_file_manager_for_importing(self, *args):
        self._file_manager_opening_mode = FileManagerOpeningMods.IMPORT
        # self._file_manager.show_disks()
        self._file_manager.show(str(ROOT_DIR))

    def open_file_manager_for_exporting(self, *args):
        self._file_manager_opening_mode = FileManagerOpeningMods.EXPORT
        # self._file_manager.show_disks()
        self._file_manager.show(str(ROOT_DIR))

    def select_path_using_file_manager(self, path):
        ak.start(self.controller.update_workload(path, self._file_manager_opening_mode))
        self._file_manager.close()

    def exit_file_manager(self, *args):
        self._file_manager.close()

    async def update_workload(self, mentor_load_items: List[MentorLoadItem], show_message=False):
        self.configuration_description_screen.update_workload(mentor_load_items)
        if show_message:
            self._success_import_dialog.open()

    async def show_success_export_message(self):
        self._success_export_dialog.open()
