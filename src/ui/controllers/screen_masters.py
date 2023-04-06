import enum

from kivy.core.window import Window

from src.config import get_common_window_size
from src.ui.controllers.abstract_controller import AbstractController
from src.ui.controllers.home_screen import HomeScreenController
from src.ui.controllers.loading_screen import LoadingScreenController
from src.ui.views import ScreenMasterView


class ScreenMasterController(AbstractController):
    def __init__(self, bus, **kwargs):
        super().__init__(bus)
        self._view = ScreenMasterView(controller=self)

    def go_to_loading_screen(self):
        Window.size = get_common_window_size()
        self._view.manager.current = OuterScreens.LOADING_SCREEN.name

    def go_to_home_screen(self):
        Window.maximize()
        self._view.current = OuterScreens.HOME_SCREEN.name


class OuterScreens(enum.Enum):
    SCREEN_MASTER = ScreenMasterController
    LOADING_SCREEN = LoadingScreenController
    HOME_SCREEN = HomeScreenController

