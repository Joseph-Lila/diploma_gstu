from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetSchedules(Command):
    year: Optional[int]
    term: Optional[str]
