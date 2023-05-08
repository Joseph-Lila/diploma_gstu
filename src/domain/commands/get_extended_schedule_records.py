from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetExtendedScheduleRecords(Command):
    schedule_id: int
