from typing import Callable, Dict, List, Type

from src.adapters.orm import Schedule
from src.adapters.repositories.abstract_repository import AbstractRepository
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
    GetUniqueGroupsDependingOnFaculty, GetUniqueDepartments, GetUniqueMentorsDependingOnDepartment,
)
from src.domain.commands.command import Command
from src.domain.events import (
    GotSchedules,
    GotUniqueTerms,
    GotUniqueYears,
    ScheduleIsCreated,
    GotUniqueMentors,
    GotUniqueGroups,
    ScheduleIsDeleted,
    GotUniqueFaculties,
)
from src.domain.events.got_unique_departments import GotUniqueDepartments


async def get_schedules(
    cmd: GetSchedules,
    repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_schedules(
        year=cmd.year, term=cmd.term
    )
    return GotSchedules(schedules)


async def get_10_schedules(
    cmd: Get10Schedules,
    repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_10_schedules()
    return GotSchedules(schedules)


async def get_unique_years_depending_on_workload(
    cmd: GetUniqueYearsDependingOnWorkload,
    repository: AbstractRepository,
) -> GotUniqueYears:
    years: List[int] = await repository.get_unique_years_depending_on_workload(
        term=cmd.term
    )
    return GotUniqueYears(years)


async def get_unique_years_depending_on_schedule(
    cmd: GetUniqueYearsDependingOnSchedule,
    repository: AbstractRepository,
) -> GotUniqueYears:
    years: List[int] = await repository.get_unique_years_depending_on_schedule(
        term=cmd.term
    )
    return GotUniqueYears(years)


async def get_unique_terms_depending_on_workload(
    cmd: GetUniqueTermsDependingOnWorkload,
    repository: AbstractRepository,
) -> GotUniqueTerms:
    term: List[int] = await repository.get_unique_terms_depending_on_workload(
        year=cmd.year
    )
    return GotUniqueTerms(term)


async def get_unique_terms_depending_on_schedule(
    cmd: GetUniqueTermsDependingOnSchedule,
    repository: AbstractRepository,
) -> GotUniqueTerms:
    term: List[int] = await repository.get_unique_terms_depending_on_schedule(
        year=cmd.year
    )
    return GotUniqueTerms(term)


async def create_schedule(
    cmd: CreateSchedule,
    repository: AbstractRepository,
) -> ScheduleIsCreated:
    schedule = await repository.get_schedule_by_year_and_term(
        year=cmd.year,
        term=cmd.term,
    )
    if schedule is None:
        schedule = await repository.create_schedule(
            year=cmd.year,
            term=cmd.term,
        )
        return ScheduleIsCreated(schedule)
    else:
        return ScheduleIsCreated(None)


async def delete_schedule(
    cmd: DeleteSchedule,
    repository: AbstractRepository,
) -> ScheduleIsDeleted:
    await repository.delete_schedule(
        id_=cmd.schedule_id,
    )
    return ScheduleIsDeleted(True)


async def get_unique_mentors(
    cmd: GetUniqueMentors,
    repository: AbstractRepository,
) -> GotUniqueMentors:
    mentors_fios: List[str] = await repository.get_unique_mentors_fios(
        cmd.fio_substring
    )
    return GotUniqueMentors(mentors_fios)


async def get_unique_groups(
    cmd: GetUniqueGroups,
    repository: AbstractRepository,
) -> GotUniqueGroups:
    groups_titles: List[str] = await repository.get_unique_groups_titles(
        cmd.title_substring
    )
    return GotUniqueGroups(groups_titles)


async def get_unique_groups_depending_on_faculty(
    cmd: GetUniqueGroupsDependingOnFaculty,
    repository: AbstractRepository,
) -> GotUniqueGroups:
    groups_titles: List[
        str
    ] = await repository.get_unique_groups_titles_depending_on_faculty(
        cmd.title_substring,
        cmd.faculty,
    )
    return GotUniqueGroups(groups_titles)


async def get_unique_faculties(
    cmd: GetUniqueFaculties,
    repository: AbstractRepository,
) -> GotUniqueFaculties:
    faculties_titles: List[str] = await repository.get_unique_faculties_titles(
        cmd.title_substring
    )
    return GotUniqueFaculties(faculties_titles)


async def get_unique_departments(
    cmd: GetUniqueDepartments,
    repository: AbstractRepository,
) -> GotUniqueDepartments:
    departments_titles: List[str] = await repository.get_unique_departments_titles(
        cmd.title_substring
    )
    return GotUniqueDepartments(departments_titles)


async def get_unique_mentors_depending_on_department(
    cmd: GetUniqueMentorsDependingOnDepartment,
    repository: AbstractRepository,
) -> GotUniqueMentors:
    mentors_titles: List[str] = await repository.get_unique_mentors_fios_depending_on_department(
        cmd.fio_substring,
        cmd.department,
    )
    return GotUniqueMentors(mentors_titles)


COMMAND_HANDLERS = {
    GetSchedules: get_schedules,
    GetUniqueYearsDependingOnWorkload: get_unique_years_depending_on_workload,
    GetUniqueYearsDependingOnSchedule: get_unique_years_depending_on_schedule,
    GetUniqueTermsDependingOnWorkload: get_unique_terms_depending_on_workload,
    GetUniqueTermsDependingOnSchedule: get_unique_terms_depending_on_schedule,
    Get10Schedules: get_10_schedules,
    CreateSchedule: create_schedule,
    DeleteSchedule: delete_schedule,
    GetUniqueMentors: get_unique_mentors,
    GetUniqueGroups: get_unique_groups,
    GetUniqueGroupsDependingOnFaculty: get_unique_groups_depending_on_faculty,
    GetUniqueFaculties: get_unique_faculties,
    GetUniqueDepartments: get_unique_departments,
    GetUniqueMentorsDependingOnDepartment: get_unique_mentors_depending_on_department,
}  # type: Dict[Type[Command], Callable]
