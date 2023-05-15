from dataclasses import dataclass
from typing import List

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.events.event import Event


@dataclass
class GotExtendedScheduleRecords(Event):
    records: List[ScheduleItemInfo]
