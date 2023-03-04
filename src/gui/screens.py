from typing import Any

from src.bootstrap import bootstrap
from src.gui.controllers.screen_masters import OuterScreens, InnerScreens


class ScreenGenerator:
    def __init__(self, outer_screens=OuterScreens, inner_screens=InnerScreens):
        self.outer_screens = outer_screens
        self.inner_screens = inner_screens
        self.bus = bootstrap()

    def build_app_view(self):
        # build outer screens
        screen_master_view = self._generate_view(self.outer_screens, OuterScreens.SCREEN_MASTER.name)
        home_screen_view = None
        for elem in self.outer_screens:
            if elem.name != OuterScreens.SCREEN_MASTER.name:
                view = self._generate_view(self.outer_screens, elem.name, screen_master_view)
                screen_master_view.add_widget(view)
                if elem.name == OuterScreens.HOME_SCREEN.name:
                    home_screen_view = view

        # build inner screens
        inner_screen_master_view = self._generate_view(self.inner_screens, InnerScreens.INNER_SCREEN_MASTER.name, screen_master_view)
        for elem in self.inner_screens:
            if elem.name != InnerScreens.INNER_SCREEN_MASTER.name:
                view = self._generate_view(self.inner_screens, elem.name, inner_screen_master_view)
                inner_screen_master_view.add_widget(view)

        # attach inner screen master to outer screen master
        if home_screen_view:
            home_screen_view.nav_layout.add_widget(inner_screen_master_view)
        return screen_master_view

    def _generate_view(self, screens, key, screen_master_view: Any = None):
        controller = screens[key].value(
            self.bus,
            screen_master_controller=screen_master_view.controller if screen_master_view else screen_master_view)
        view = controller.get_view()
        view.name = key
        return view
