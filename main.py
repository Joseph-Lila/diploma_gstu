from kivy.config import Config

from src.ui.model import Model

Config.set('input', 'mouse', 'mouse,disable_multitouch')

import asyncio

from kivy import Logger
from kivy.core.window import Window
from kivymd.app import MDApp

from src.bootstrap import bootstrap
from src.config import get_common_window_size
from src.ui.controller import Controller
from src.ui.screen_builder import get_main_screen


class KivyApp(MDApp):
    icon = 'assets/images/logo_new.png'
    title = 'Составитель расписания'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        Window.borderless = True
        Window.size = get_common_window_size()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.material_style = "M3"
        return get_main_screen()


async def main():
    try:
        bus = await bootstrap()
    except:
        Logger.info("Application: Can't create bus...")
        return
    app = KivyApp()
    model: Model = Model(bus, None)
    app.controller = Controller(model)
    await app.async_run(async_lib='asyncio')


if __name__ == '__main__':
    asyncio.run(main())
