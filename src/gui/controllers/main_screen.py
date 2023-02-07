from src.gui.controllers.abstract_controller import AbstractController, use_loop
from src.gui.views import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self._view = MainScreenView(controller=self)

    def get_view(self):
        return self._view

    @use_loop
    async def create_configuration(self):
        await self._view.set_configuration_screen()
