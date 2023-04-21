from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class DeleteSchedule(Command):
    schedule_id: int
