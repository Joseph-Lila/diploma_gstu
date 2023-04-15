from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetUniqueGroups(Command):
    title_substring: str
