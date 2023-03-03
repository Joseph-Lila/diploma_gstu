import asyncio

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '550')

from kivy.core.window import Window
from kivymd.app import MDApp
from src.gui.screens import ScreenGenerator


class KivyApp(MDApp):
    icon = 'assets/images/logo_new.png'
    title = 'Составитель расписания'

    def build(self):
        Window.borderless = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
