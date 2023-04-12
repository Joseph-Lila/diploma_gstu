import dataclasses
from typing import Optional

from src.domain.commands.command import Command


@dataclasses.dataclass
class GetUniqueYearsDependingOnSchedule(Command):
    term: Optional[str]
