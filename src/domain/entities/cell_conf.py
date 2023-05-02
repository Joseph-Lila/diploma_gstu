from dataclasses import dataclass


@dataclass
class CellConf:
    day_of_week: str
    pair_number: int
    week_type: str
    subgroup: str
