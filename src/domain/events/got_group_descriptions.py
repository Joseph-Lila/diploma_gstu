from dataclasses import dataclass
from typing import List

from src.domain.entities import GroupDescription
from src.domain.events.event import Event


@dataclass
class GotGroupDescriptions(Event):
    group_descriptions: List[GroupDescription]
