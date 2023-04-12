from dataclasses import dataclass
from typing import Optional

from src.adapters.orm import Schedule
from src.domain.events.event import Event


@dataclass
class ScheduleIsCreated(Event):
    schedule: Optional[Schedule]
