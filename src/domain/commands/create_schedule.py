from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class CreateSchedule(Command):
    year: int
    term: str
