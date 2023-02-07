from src.domain.commands import ExportWorkload, ImportWorkload
from src.domain.entities import Configuration
from src.domain.events import WorkloadIsExported, WorkloadIsImported
from src.domain.utils import FileManagerOpeningMods
from src.gui.controllers.abstract_controller import (AbstractController,
                                                     use_loop)
from src.gui.views import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self.configuration = None
        self._view = MainScreenView(controller=self)

    def get_view(self):
        return self._view

    @use_loop
    async def create_configuration(self):
        await self._view.set_configuration_screen()
        self.configuration = Configuration()

    @use_loop
    async def close_configuration(self):
        await self._view.set_start_screen()
        self.configuration = None

    @use_loop
    async def update_workload(self, path, mode):
        if mode == FileManagerOpeningMods.IMPORT:
            event: WorkloadIsImported = await self.bus.handle_command(
                ImportWorkload(path)
            )
            self.configuration.mentor_load_items = event.mentor_load_items
            await self._view.update_workload(event.mentor_load_items, show_message=True)
        elif mode == FileManagerOpeningMods.EXPORT and self.configuration:
            event: WorkloadIsExported = await self.bus.handle_command(
                ExportWorkload(path, self.configuration.mentor_load_items)
            )
            await self._view.show_success_export_message()
