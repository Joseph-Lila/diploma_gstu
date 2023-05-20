from dataclasses import dataclass
from typing import List


@dataclass
class AdditionalPart:
    mentor_free: bool
    schedule_record_ids: List[int]
