from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class MakeLocalScheduleRecordsLikeGlobal(Command):
    schedule_id: int
