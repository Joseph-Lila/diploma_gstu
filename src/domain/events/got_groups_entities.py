from dataclasses import dataclass
from typing import List

from src.domain.entities import MentorPart, GroupPart
from src.domain.events.event import Event


@dataclass
class GotGroupsEntities(Event):
    groups: List[GroupPart]
