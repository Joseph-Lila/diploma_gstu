from dataclasses import dataclass

from src.adapters.orm import LocalScheduleRecord
from src.domain.commands.command import Command


@dataclass
class CreateLocalScheduleRecord(Command):
    record: LocalScheduleRecord
