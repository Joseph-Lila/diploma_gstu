from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class Get10Schedules(Command):
    pass
