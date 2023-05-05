from dataclasses import dataclass
from typing import List


@dataclass
class MentorPart:
    mentor_id: int
    fio: str
    scientific_degree: str
