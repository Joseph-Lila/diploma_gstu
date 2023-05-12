from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetGroupTitlesDependingOnFaculty(Command):
    faculty_substring: str
    group_substring: str
