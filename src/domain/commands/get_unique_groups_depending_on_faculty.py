from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetUniqueGroupsDependingOnFaculty(Command):
    title_substring: str
    faculty: Optional[str]
