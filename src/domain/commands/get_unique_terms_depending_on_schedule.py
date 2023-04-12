import dataclasses
from typing import Optional

from src.domain.commands.command import Command


@dataclasses.dataclass
class GetUniqueTermsDependingOnSchedule(Command):
    year: Optional[str]
