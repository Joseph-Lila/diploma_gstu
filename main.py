import asyncio

from kivy.core.window import Window

from src.config import get_common_window_size

from kivymd.app import MDApp
from src.ui.screens import ScreenGenerator


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
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
