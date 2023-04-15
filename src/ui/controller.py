import asyncio
import functools

from src.domain.commands import (CreateSchedule, Get10Schedules, GetSchedules,
                                 GetUniqueTermsDependingOnSchedule,
                                 GetUniqueTermsDependingOnWorkload,
                                 GetUniqueYearsDependingOnSchedule,
                                 GetUniqueYearsDependingOnWorkload, GetUniqueMentors)
from src.domain.events import (GotSchedules, GotUniqueTerms, GotUniqueYears,
                               ScheduleIsCreated, GotUniqueMentors)
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
    async def fill_years_selector_depending_on_workload(
        self, years_selector, term
    ):
        event: GotUniqueYears = await self.bus.handle_command(
            GetUniqueYearsDependingOnWorkload(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop
    async def fill_years_selector_depending_on_schedule(
        self, years_selector, term
    ):
        event: GotUniqueYears = await self.bus.handle_command(
            GetUniqueYearsDependingOnSchedule(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop
    async def fill_terms_selector_depending_on_workload(
        self, terms_selector, year
    ):
        event: GotUniqueTerms = await self.bus.handle_command(
            GetUniqueTermsDependingOnWorkload(year=year)
        )
        await terms_selector.update_variants(event.terms)

    @use_loop
    async def fill_terms_selector_depending_on_schedule(
        self, terms_selector, year
    ):
        event: GotUniqueTerms = await self.bus.handle_command(
            GetUniqueTermsDependingOnSchedule(year=year)
        )
        await terms_selector.update_variants(event.terms)

    @use_loop
    async def update_latest_10_schedules(self, home_screen):
        event: GotSchedules = await self.bus.handle_command(Get10Schedules())
        await home_screen.update_latest_10_schedules(event.schedules)

    @use_loop
    async def try_to_create_schedule(self, create_dialog, year: int, term: str):
        event: ScheduleIsCreated = await self.bus.handle_command(
            CreateSchedule(year=year, term=term)
        )
        await create_dialog.check_if_new_schedule_is_created(event.schedule)

    @use_loop
    async def fill_mentors_selector(
            self, mentors_selector, fio_substring
    ):
        event: GotUniqueMentors = await self.bus.handle_command(
            GetUniqueMentors(fio_substring)
        )
        await mentors_selector.update_variants(event.mentors)