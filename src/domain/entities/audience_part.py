from dataclasses import dataclass
from typing import List


@dataclass
class AudiencePart:
    audience_id: int
    number: str
    total_seats: int
    free_seats: int
