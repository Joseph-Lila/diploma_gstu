import asyncio
import functools
from typing import Optional

from src.domain.commands import (
    CreateSchedule,
    Get10Schedules,
    GetSchedules,
    GetUniqueTermsDependingOnSchedule,
    GetUniqueTermsDependingOnWorkload,
    GetUniqueYearsDependingOnSchedule,
    GetUniqueYearsDependingOnWorkload,
    GetUniqueMentors,
    GetUniqueGroups,
    DeleteSchedule,
    GetUniqueFaculties,
    GetUniqueGroupsDependingOnFaculty,
    GetUniqueDepartments,
    GetUniqueMentorsDependingOnDepartment,
    GetUniqueAudiencesDependingOnDepartment,
)
from src.domain.events import (
    GotSchedules,
    GotUniqueTerms,
    GotUniqueYears,
    ScheduleIsCreated,
    GotUniqueMentors,
    GotUniqueGroups,
    ScheduleIsDeleted,
    GotUniqueFaculties,
    GotUniqueAudiences,
)
from src.domain.events.got_unique_departments import GotUniqueDepartments
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
    async def fill_years_selector_depending_on_workload(self, years_selector, term):
        event: GotUniqueYears = await self.bus.handle_command(
            GetUniqueYearsDependingOnWorkload(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop
    async def fill_years_selector_depending_on_schedule(self, years_selector, term):
        event: GotUniqueYears = await self.bus.handle_command(
            GetUniqueYearsDependingOnSchedule(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop
    async def fill_terms_selector_depending_on_workload(self, terms_selector, year):
        event: GotUniqueTerms = await self.bus.handle_command(
            GetUniqueTermsDependingOnWorkload(year=year)
        )
        await terms_selector.update_variants(event.terms)

    @use_loop
    async def fill_terms_selector_depending_on_schedule(self, terms_selector, year):
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
    async def delete_schedule(self, schedule_id: int):
        event: ScheduleIsDeleted = await self.bus.handle_command(
            DeleteSchedule(schedule_id=schedule_id)
        )
        return event.success

    @use_loop
    async def fill_faculties_selector(self, faculties_selector, title_substring):
        event: GotUniqueFaculties = await self.bus.handle_command(
            GetUniqueFaculties(title_substring)
        )
        await faculties_selector.update_variants(event.faculties)

    @use_loop
    async def fill_mentors_selector(self, mentors_selector, fio_substring):
        event: GotUniqueMentors = await self.bus.handle_command(
            GetUniqueMentors(fio_substring)
        )
        await mentors_selector.update_variants(event.mentors)

    @use_loop
    async def fill_groups_selector(self, groups_selector, title_substring):
        event: GotUniqueGroups = await self.bus.handle_command(
            GetUniqueGroups(title_substring)
        )
        await groups_selector.update_variants(event.groups)

    @use_loop
    async def fill_groups_selector_depending_on_faculty(
        self, groups_selector, title_substring, faculty: Optional[str]
    ):
        event: GotUniqueGroups = await self.bus.handle_command(
            GetUniqueGroupsDependingOnFaculty(
                title_substring,
                faculty,
            )
        )
        await groups_selector.update_variants(event.groups)

    @use_loop
    async def fill_departments_selector(self, departments_selector, title_substring):
        event: GotUniqueDepartments = await self.bus.handle_command(
            GetUniqueDepartments(title_substring)
        )
        await departments_selector.update_variants(event.departments)

    @use_loop
    async def fill_mentors_selector_depending_on_department(
        self, mentors_selector, title_substring, department: Optional[str]
    ):
        event: GotUniqueMentors = await self.bus.handle_command(
            GetUniqueMentorsDependingOnDepartment(
                title_substring,
                department,
            )
        )
        await mentors_selector.update_variants(event.mentors)

    @use_loop
    async def fill_audiences_selector_depending_on_department(
        self, audiences_selector, number_substring, department: Optional[str]
    ):
        event: GotUniqueAudiences = await self.bus.handle_command(
            GetUniqueAudiencesDependingOnDepartment(
                number_substring,
                department,
            )
        )
        await audiences_selector.update_variants(event.audiences)
