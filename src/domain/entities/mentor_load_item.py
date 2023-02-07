from dataclasses import dataclass


@dataclass
class MentorLoadItem:
    mentor: str
    group: str
    subject: str
    subject_type: str
    hours: int
