from typing import Callable, Dict, List, Type

from src.adapters.orm import Schedule
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.commands import (CreateSchedule, Get10Schedules, GetSchedules,
                                 GetUniqueTermsDependingOnSchedule,
                                 GetUniqueTermsDependingOnWorkload,
                                 GetUniqueYearsDependingOnSchedule,
                                 GetUniqueYearsDependingOnWorkload)
from src.domain.commands.command import Command
from src.domain.events import (GotSchedules, GotUniqueTerms, GotUniqueYears,
                               ScheduleIsCreated)


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


COMMAND_HANDLERS = {
    GetSchedules: get_schedules,
    GetUniqueYearsDependingOnWorkload: get_unique_years_depending_on_workload,
    GetUniqueYearsDependingOnSchedule: get_unique_years_depending_on_schedule,
    GetUniqueTermsDependingOnWorkload: get_unique_terms_depending_on_workload,
    GetUniqueTermsDependingOnSchedule: get_unique_terms_depending_on_schedule,
    Get10Schedules: get_10_schedules,
    CreateSchedule: create_schedule,
}  # type: Dict[Type[Command], Callable]
