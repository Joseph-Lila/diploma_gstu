from dataclasses import dataclass
from typing import List

from src.domain.commands.command import Command
from src.domain.entities.schedule_item_info import ScheduleItemInfo


@dataclass
class GetGroupsForScheduleItem(Command):
    subject_id: int
    subject_type_id: int
    mentor_id: int
