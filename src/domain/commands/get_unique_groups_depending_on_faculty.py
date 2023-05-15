from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueGroupsDependingOnFaculty(Command):
    title_substring: str
    faculty: str
