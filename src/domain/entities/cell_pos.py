from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class CellPos:
    day_of_week: str
    pair_number: int
