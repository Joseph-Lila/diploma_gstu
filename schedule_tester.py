import asyncio
from kivy.lang import Builder
from kivymd.app import MDApp

from src.ui.views.schedule_cell import ScheduleCell
from src.ui.views.schedule_item_btn.schedule_item_btn import ScheduleItemBtn

KV = '''
MDScreen:
    MDGridLayout:
        id: grid
        cols: 2
        rows: 1

'''


class HiApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.material_style = "M3"
        cont = Builder.load_string(KV)
        cell_1 = ScheduleCell()
        cell_2 = ScheduleCell()
        btn = ScheduleItemBtn()
        cell_1.add_widget(btn)
        cont.ids.grid.add_widget(cell_1)
        cont.ids.grid.add_widget(cell_2)
        return cont


async def main():
    app = HiApp()
    await app.async_run(async_lib='asyncio')


if __name__ == '__main__':
    asyncio.run(main())
