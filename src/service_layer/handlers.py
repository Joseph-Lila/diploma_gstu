from typing import Callable, Dict, List, Type

from src.adapters.orm import Schedule
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.commands import Get10Schedules, GetSchedules, GetUniqueYears
from src.domain.commands.command import Command
from src.domain.events import GotSchedules, GotUniqueYears


async def get_schedules(
        cmd: GetSchedules,
        repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_schedules(year=cmd.year, term=cmd.term)
    return GotSchedules(schedules)


async def get_10_schedules(
        cmd: Get10Schedules,
        repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_10_schedules()
    return GotSchedules(schedules)


async def get_unique_years(
        cmd: GetUniqueYears,
        repository: AbstractRepository,
) -> GotUniqueYears:
    years: List[int] = await repository.get_unique_years(term=cmd.term)
    return GotUniqueYears(years)


COMMAND_HANDLERS = {
    GetSchedules: get_schedules,
    GetUniqueYears: get_unique_years,
    Get10Schedules: get_10_schedules,
}  # type: Dict[Type[Command], Callable]
