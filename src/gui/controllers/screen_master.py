from src.gui.controllers.abstract_controller import AbstractController
from src.gui.views import ScreenMasterView


class ScreenMasterController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self._view = ScreenMasterView(controller=self)
