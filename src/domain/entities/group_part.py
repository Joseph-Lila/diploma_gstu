from dataclasses import dataclass
from typing import List


@dataclass
class GroupPart:
    group_id: int
    title: str
    number_of_students: int
