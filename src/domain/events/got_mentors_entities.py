from dataclasses import dataclass
from typing import List

from src.domain.entities import MentorPart
from src.domain.events.event import Event


@dataclass
class GotMentorsEntities(Event):
    mentors: List[MentorPart]
