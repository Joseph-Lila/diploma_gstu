import asyncio
import functools

from src.domain.commands import Get10Schedules, GetSchedules, GetUniqueYears
from src.domain.events import GotSchedules, GotUniqueYears
from src.ui.views.loading_modal_dialog import LoadingModalDialog


async def do_with_loading_modal_view(func, *args, **kwargs):
    loading_modal_view = LoadingModalDialog()
    loading_modal_view.open()
    await func(*args, **kwargs)
    loading_modal_view.dismiss()


def use_loop(func):
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(func(self, *args, **kwargs))

    return wrapped


class Controller:
    def __init__(self, bus):
        self.bus = bus

    @use_loop
    async def update_open_dialog_schedules(self, open_dialog, year, term):
        event: GotSchedules = await self.bus.handle_command(
            GetSchedules(
                year=year,
                term=term,
            )
        )
        await open_dialog.update_items(event.schedules)

    @use_loop
    async def bind_dropdown_menu_for_years_selector(self, years_selector, term):
        event: GotUniqueYears = await self.bus.handle_command(
            GetUniqueYears(term=term)
        )
        await years_selector.bind_dropdown_menu(event.years)

    @use_loop
    async def update_latest_10_schedules(self, home_screen):
        event: GotSchedules = await self.bus.handle_command(
            Get10Schedules()
        )
        await home_screen.update_latest_10_schedules(event.schedules)
