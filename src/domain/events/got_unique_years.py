import dataclasses
from typing import List

from src.domain.events.event import Event


@dataclasses.dataclass
class GotUniqueYears(Event):
    years: List[int]
