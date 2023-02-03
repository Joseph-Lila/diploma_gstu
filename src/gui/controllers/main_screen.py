from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self._view = MainScreenView(controller=self)

    def get_view(self):
        return self._view
