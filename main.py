import asyncio

from kivymd.app import MDApp


class KivyApp(MDApp):
    title = 'Scheduler'


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
