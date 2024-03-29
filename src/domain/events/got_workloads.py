from dataclasses import dataclass
from typing import List

from src.adapters.orm import Workload
from src.domain.events.event import Event


@dataclass
class GotWorkloads(Event):
    data: List[Workload]
