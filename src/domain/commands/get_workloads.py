from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetWorkloads(Command):
    year: int
    term: str
