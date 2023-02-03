from src.bootstrap import bootstrap
from src.gui.controllers import MainScreenController

MAIN_SCREEN_KEY = "main screen"
MAIN_SCREEN_CLS = MainScreenController

SCREENS = (
    # now let's add minor screens
)


class ScreenGenerator:
    def __init__(self, screens=SCREENS):
        self.screens = screens
        self.bus = bootstrap()

    def build_app_view(self):
        app_view = self._generate_view(MAIN_SCREEN_KEY, MAIN_SCREEN_CLS)
        for key, cls in self.screens:
            if key != MAIN_SCREEN_KEY:
                view = self._generate_view(key, cls)
                view.main_controller = app_view.controller
                app_view.rail.add_widget(view)
        return app_view

    def _generate_view(self, key: str, cls):
        controller = cls(self.bus)
        view = controller.get_view()
        view.name = key
        return view
