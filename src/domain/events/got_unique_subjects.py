from dataclasses import dataclass
from typing import List

from src.domain.events.event import Event


@dataclass
class GotUniqueSubjects(Event):
    subjects: List[str]
