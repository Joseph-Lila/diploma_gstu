from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueAudiencesDependingOnDepartment(Command):
    number_substring: str
    department: str
