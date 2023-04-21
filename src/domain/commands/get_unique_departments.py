from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueDepartments(Command):
    title_substring: str
