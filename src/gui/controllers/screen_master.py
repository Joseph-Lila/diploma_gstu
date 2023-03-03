import enum

from kivy.core.window import Window

from src.gui.controllers.abstract_controller import AbstractController
from src.gui.controllers.home_screen import HomeScreenController
from src.gui.controllers.loading_screen import LoadingScreenController
from src.gui.views import ScreenMasterView


class ScreenMasterController(AbstractController):
    def __init__(self, bus):
        super().__init__(bus)
        self._view = ScreenMasterView(controller=self)

    def go_to_loading_screen(self):
        Window.size = (800, 550)
        self._view.manager.current = ScreenEnum.LOADING_SCREEN.name

    def go_to_home_screen(self):
        Window.maximize()
        self._view.current = ScreenEnum.HOME_SCREEN.name


class ScreenEnum(enum.Enum):
    SCREEN_MASTER_NAME = ScreenMasterController
    LOADING_SCREEN = LoadingScreenController
    HOME_SCREEN = HomeScreenController
