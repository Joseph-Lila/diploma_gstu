import dataclasses
from typing import List

from src.domain.events.event import Event


@dataclasses.dataclass
class GotUniqueTerms(Event):
    terms: List[int]
