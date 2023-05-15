from dataclasses import dataclass


@dataclass
class SubjectPart:
    subject_id: int
    subject_type_id: int
    subject: str
    subject_type: str
