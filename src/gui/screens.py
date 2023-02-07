from src.bootstrap import bootstrap
from src.gui.controllers import MainScreenController
from src.gui.views import ConfigurationDescriptionScreenView, StartScreenView

MAIN_SCREEN_KEY = "main_screen"
MAIN_SCREEN_CLS = MainScreenController

SCREENS = (
    ('start_screen', StartScreenView),
    ('configuration_description_screen', ConfigurationDescriptionScreenView),
)


class ScreenGenerator:
    def __init__(self, screens=SCREENS):
        self.screens = screens
        self.bus = bootstrap()

    def build_app_view(self):
        controller = MAIN_SCREEN_CLS(self.bus)
        app_view = controller.get_view()
        for key, cls in self.screens:
            if key != MAIN_SCREEN_KEY:
                view = self._generate_view(key, cls, controller)
                app_view.content_manager.add_widget(view)
                setattr(app_view, key, view)
        return app_view

    @staticmethod
    def _generate_view(key: str, cls, controller):
        view = cls(controller=controller)
        view.name = key
        return view
