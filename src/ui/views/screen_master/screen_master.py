from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import NoTransition, ScreenManager

from src.adapters.orm import Schedule
from src.ui import Screens
from src.ui.views import ScheduleScreenView


class ScreenMasterView(ScreenManager):
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()

    def get_current_screen_view(self, *args):
        return self.current_screen

    def go_to_home_screen(self):
        self.current = Screens.HOME_SCREEN.name

    def go_to_schedule_screen(self, schedule: Schedule, *args):
        screen: ScheduleScreenView = self.get_screen(Screens.SCHEDULE_SCREEN.name)
        screen.update_schedule_data(schedule)
        self.current = Screens.SCHEDULE_SCREEN.name
