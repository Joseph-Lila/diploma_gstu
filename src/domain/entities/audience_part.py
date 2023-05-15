from dataclasses import dataclass


@dataclass
class AudiencePart:
    audience_id: int
    number: str
    total_seats: int
