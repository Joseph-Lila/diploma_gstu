from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class MainScreenView(MDScreen):
    controller = ObjectProperty()

    async def set_configuration_screen(self):
        self.content_manager.current = 'configuration screen'
