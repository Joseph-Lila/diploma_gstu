from src.ui.controllers.abstract_controller import AbstractController
from src.ui.views import HomeScreenView


class HomeScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller, **kwargs):
        super().__init__(bus)
        self._view = HomeScreenView(controller=self)
        self.screen_master_controller = screen_master_controller
