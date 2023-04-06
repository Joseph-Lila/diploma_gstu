from typing import Any

from src.bootstrap import bootstrap
from src.ui.controllers.screen_masters import OuterScreens


class ScreenGenerator:
    def __init__(self, outer_screens=OuterScreens):
        self.outer_screens = outer_screens
        self.bus = bootstrap()

    def build_app_view(self):
        # build outer screens
        screen_master_view = self._generate_view(self.outer_screens, OuterScreens.SCREEN_MASTER.name)
        for elem in self.outer_screens:
            if elem.name != OuterScreens.SCREEN_MASTER.name:
                view = self._generate_view(self.outer_screens, elem.name, screen_master_view)
                screen_master_view.add_widget(view)

        return screen_master_view

    def _generate_view(self, screens, key, screen_master_view: Any = None):
        controller = screens[key].value(
            self.bus,
            screen_master_controller=screen_master_view.controller if screen_master_view else screen_master_view)
        view = controller.get_view()
        view.name = key
        return view
