from dataclasses import dataclass
from typing import List

from src.domain.events.event import Event


@dataclass
class GotUniqueMentors(Event):
    mentors: List[str]
