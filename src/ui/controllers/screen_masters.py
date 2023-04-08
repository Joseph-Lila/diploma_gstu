import enum

from src.ui.controllers.abstract_controller import AbstractController
from src.ui.controllers.home_screen import HomeScreenController
from src.ui.controllers.loading_screen import LoadingScreenController
from src.ui.controllers.schedule_screen import ScheduleScreenController
from src.ui.views import ScreenMasterView


class ScreenMasterController(AbstractController):
    def __init__(self, bus, **kwargs):
        super().__init__(bus)
        self._view = ScreenMasterView(controller=self)

    def go_to_loading_screen(self):
        self._view.current = OuterScreens.LOADING_SCREEN.name

    def go_to_home_screen(self):
        self._view.current = OuterScreens.HOME_SCREEN.name

    def go_to_schedule_screen(self, term: str, year: int):
        self._view.get_screen(OuterScreens.SCHEDULE_SCREEN.name).term = term
        self._view.get_screen(OuterScreens.SCHEDULE_SCREEN.name).year = year
        self._view.current = OuterScreens.SCHEDULE_SCREEN.name

    def get_screen(self, key):
        return self._view.get_screen(key)


class OuterScreens(enum.Enum):
    SCREEN_MASTER = ScreenMasterController
    LOADING_SCREEN = LoadingScreenController
    HOME_SCREEN = HomeScreenController
    SCHEDULE_SCREEN = ScheduleScreenController
