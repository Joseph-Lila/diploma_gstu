from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueSubjects(Command):
    title_substring: str
