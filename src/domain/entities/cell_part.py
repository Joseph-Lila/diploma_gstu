from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class CellPart:
    week_type: str
    subgroup: str
