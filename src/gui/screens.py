from src.bootstrap import bootstrap
from src.gui.controllers import MainScreenController

MAIN_SCREEN_KEY = "main screen"
MAIN_SCREEN_CLS = MainScreenController


class ScreenGenerator:
    def __init__(self):
        self.bus = bootstrap()

    def build_app_view(self):
        app_view = self._generate_view(MAIN_SCREEN_KEY, MAIN_SCREEN_CLS)
        minor_view_pairs = app_view.controller.get_minor_view_pairs()
        for name, view in minor_view_pairs:
            view.name = name
            view.controller = app_view.controller
            app_view.content_manager.add_widget(view)
        return app_view

    def _generate_view(self, key: str, cls):
        controller = cls(self.bus)
        view = controller.get_view()
        view.name = key
        return view
