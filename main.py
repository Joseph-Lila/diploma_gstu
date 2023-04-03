import asyncio

from kivy.config import Config

from src.config import get_common_window_size

new_window_size_x, new_window_size_y = get_common_window_size()
Config.set('graphics', 'width', f'{new_window_size_x}')
Config.set('graphics', 'height', f'{new_window_size_y}')
Config.set('graphics', 'borderless', '1')

from kivymd.app import MDApp
from src.gui.screens import ScreenGenerator


class KivyApp(MDApp):
    icon = 'assets/images/logo_new.png'
    title = 'Составитель расписания'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
