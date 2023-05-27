from dataclasses import dataclass
from typing import List

from src.domain.entities import MentorPart, AudiencePart
from src.domain.events.event import Event


@dataclass
class GotAudiencesEntities(Event):
    audiences: List[AudiencePart]
