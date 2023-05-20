from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class AudiencePart:
    audience_id: int
    number: str
    total_seats: int
