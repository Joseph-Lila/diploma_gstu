import dataclasses
from typing import Optional

from src.domain.commands.command import Command


@dataclasses.dataclass
class GetUniqueYears(Command):
    term: Optional[str]
