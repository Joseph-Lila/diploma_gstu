from src.bootstrap import bootstrap
from src.gui.controllers.screen_master import ScreenEnum


class ScreenGenerator:
    def __init__(self, screens=ScreenEnum):
        self.screens = screens
        self.bus = bootstrap()

    def build_app_view(self):
        screen_master_view = self._generate_view(ScreenEnum.SCREEN_MASTER_NAME.name, None)
        for elem in self.screens:
            if elem.name != ScreenEnum.SCREEN_MASTER_NAME.name:
                view = self._generate_view(elem.name, screen_master_view)
                screen_master_view.add_widget(view)
        return screen_master_view

    def _generate_view(self, key, screen_master_view):
        if screen_master_view:
            controller = self.screens[key].value(self.bus, screen_master_controller=screen_master_view.controller)
        else:
            controller = self.screens[key].value(self.bus)
        view = controller.get_view()
        view.name = key
        return view
