from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views import LoadingScreenView


class LoadingScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller):
        super().__init__(bus)
        self._view = LoadingScreenView(controller=self)
        self.screen_master_controller = screen_master_controller
