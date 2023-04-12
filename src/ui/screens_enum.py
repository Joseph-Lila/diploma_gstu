import enum

from src.ui.views import HomeScreenView, LoadingScreenView, ScheduleScreenView


class Screens(enum.Enum):
    LOADING_SCREEN = LoadingScreenView
    HOME_SCREEN = HomeScreenView
    SCHEDULE_SCREEN = ScheduleScreenView
