from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetUniqueMentorsDependingOnDepartment(Command):
    fio_substring: str
    department: str
