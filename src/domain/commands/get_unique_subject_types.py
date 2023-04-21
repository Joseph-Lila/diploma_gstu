from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueSubjectTypes(Command):
    title_substring: str
