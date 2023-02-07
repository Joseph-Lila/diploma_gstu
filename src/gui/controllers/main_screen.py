from src.domain.entities import Configuration
from src.gui.controllers.abstract_controller import AbstractController, use_loop
from src.gui.views import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self._view = MainScreenView(controller=self)
        self.configuration = None

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
