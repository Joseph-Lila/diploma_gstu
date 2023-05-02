from dataclasses import dataclass


@dataclass
class AudienceRecord:
    id: int
    number: str
    number_of_seats: int
