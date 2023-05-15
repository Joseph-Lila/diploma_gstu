from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class MakeGlobalScheduleRecordsLikeLocal(Command):
    schedule_id: int
