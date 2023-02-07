from dataclasses import dataclass

from src.domain.events.event import Event


@dataclass
class WorkloadIsExported(Event):
    pass
