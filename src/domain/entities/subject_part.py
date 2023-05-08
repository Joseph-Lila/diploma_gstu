from dataclasses import dataclass, field
from typing import List


@dataclass
class SubjectPart:
    subject_id: int
    subject_type_id: int
    subject: str
    subject_type: str
