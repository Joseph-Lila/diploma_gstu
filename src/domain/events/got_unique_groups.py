from dataclasses import dataclass
from typing import List

from src.domain.events.event import Event


@dataclass
class GotUniqueGroups(Event):
    groups: List[str]
