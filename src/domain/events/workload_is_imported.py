from dataclasses import dataclass
from typing import List

from src.domain.entities import MentorLoadItem
from src.domain.events.event import Event


@dataclass
class WorkloadIsImported(Event):
    mentor_load_items: List[MentorLoadItem]
