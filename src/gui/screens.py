from src.bootstrap import bootstrap
from src.gui.controllers import ScreenMasterController
from src.gui.controllers.loading_screen import LoadingScreenController

SCREEN_MASTER_NAME = 'screen master'


SCREENS = {
    SCREEN_MASTER_NAME: ScreenMasterController,
    "loading screen": LoadingScreenController,
}


class ScreenGenerator:
    def __init__(self, screens=SCREENS):
        self.screens = screens
        self.bus = bootstrap()

    def build_app_view(self):
        screen_master_view = self._generate_view(SCREEN_MASTER_NAME, None)
        for key in self.screens.keys():
            if key != SCREEN_MASTER_NAME:
                view = self._generate_view(key, screen_master_view)
                screen_master_view.add_widget(view)
        return screen_master_view

    def _generate_view(self, key, screen_master_view):
        if screen_master_view:
            controller = self.screens[key](self.bus, screen_master_controller=screen_master_view.controller)
        else:
            controller = self.screens[key](self.bus)
        view = controller.get_view()
        view.name = key
        return view
