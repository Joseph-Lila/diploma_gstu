import enum

from kivy.core.window import Window

from src.config import get_common_window_size
from src.gui.controllers.abstract_controller import AbstractController
from src.gui.controllers.home_screen import HomeScreenController
from src.gui.controllers.loading_screen import LoadingScreenController
from src.gui.views import ScreenMasterView, InnerScreenMasterView


class ScreenMasterController(AbstractController):
    def __init__(self, bus, **kwargs):
        super().__init__(bus)
        self._view = ScreenMasterView(controller=self)

    def go_to_loading_screen(self):
        Window.size = get_common_window_size()
        self._view.manager.current = OuterScreens.LOADING_SCREEN.name

    def go_to_home_screen(self):
        Window.size = get_common_window_size()
        self._view.current = OuterScreens.HOME_SCREEN.name


class InnerScreenMasterController(AbstractController):
    def __init__(self, bus, screen_master_controller, **kwargs):
        super().__init__(bus)
        self.screen_master_controller = screen_master_controller
        self._view = InnerScreenMasterView(controller=self)


class OuterScreens(enum.Enum):
    SCREEN_MASTER = ScreenMasterController
    LOADING_SCREEN = LoadingScreenController
    HOME_SCREEN = HomeScreenController


class InnerScreens(enum.Enum):
    INNER_SCREEN_MASTER = InnerScreenMasterController
