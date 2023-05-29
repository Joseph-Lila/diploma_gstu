from dataclasses import dataclass
from typing import List

from src.domain.entities import MentorPart, GroupPart, SubjectPart
from src.domain.events.event import Event


@dataclass
class GotSubjectsEntities(Event):
    subject_parts: List[SubjectPart]
