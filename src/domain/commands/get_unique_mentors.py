from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueMentors(Command):
    fio_substring: str
