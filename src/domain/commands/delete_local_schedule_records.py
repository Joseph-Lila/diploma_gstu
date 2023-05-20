from dataclasses import dataclass
from typing import List

from src.domain.commands.command import Command


@dataclass
class DeleteLocalScheduleRecords(Command):
    ids: List[int]
