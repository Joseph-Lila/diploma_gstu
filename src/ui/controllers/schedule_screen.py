from src.ui.controllers.abstract_controller import AbstractController
from src.ui.views import ScheduleScreenView


class ScheduleScreenController(AbstractController):
    def __init__(self, bus, screen_master_controller, **kwargs):
        super().__init__(bus)
        self.screen_master_controller = screen_master_controller
        self._view = ScheduleScreenView(controller=self)
