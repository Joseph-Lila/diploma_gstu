from dataclasses import dataclass
from typing import List


@dataclass
class Department:
    title: str
    head: str
    # mentors: List[]