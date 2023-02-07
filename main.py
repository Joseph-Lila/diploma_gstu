from kivy.config import Config
Config.set("graphics", "window_state", "maximized")

from kivy.core.window import Window

Window.minimum_width, Window.minimum_height = (1200, 600)

import asyncio
from kivy.loader import Loader
from src.gui.screens import ScreenGenerator
from kivymd.app import MDApp
from kivymd import images_path

Loader.loading_image = f"{images_path}transparent.png"


class KivyApp(MDApp):
    title = 'Составитель расписания'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
