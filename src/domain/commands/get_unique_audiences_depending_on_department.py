from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetUniqueAudiencesDependingOnDepartment(Command):
    number_substring: str
    department: Optional[str]
