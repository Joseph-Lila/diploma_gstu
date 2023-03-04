from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views import LoadingScreenView


class LoadingScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller, **kwargs):
        super().__init__(bus)
        self._view = LoadingScreenView(controller=self)
        self.screen_master_controller = screen_master_controller
        self.activate_progress_bar()

    def activate_progress_bar(self, timedelta=0.001):
        self._view.activate_progress_bar(timedelta)
