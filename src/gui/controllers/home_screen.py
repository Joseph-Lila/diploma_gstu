from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views.home_screen import HomeScreenView


class HomeScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller):
        super().__init__(bus)
        self._view = HomeScreenView(controller=self)
        self.screen_master_controller = screen_master_controller
