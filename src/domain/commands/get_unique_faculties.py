from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueFaculties(Command):
    title_substring: str
