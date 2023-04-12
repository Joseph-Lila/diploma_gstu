from dataclasses import dataclass
from typing import List

from src.adapters.orm import Schedule
from src.domain.events.event import Event


@dataclass
class GotSchedules(Event):
    schedules: List[Schedule]
