from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller, **kwargs):
        super().__init__(bus)
        self._view = MainScreenView(controller=self)
        self.screen_master_controller = screen_master_controller
