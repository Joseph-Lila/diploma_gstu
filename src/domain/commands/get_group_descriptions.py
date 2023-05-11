from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetGroupDescriptions(Command):
    faculty_substring: str
    group_substring: str
