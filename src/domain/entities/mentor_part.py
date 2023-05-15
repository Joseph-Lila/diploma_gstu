from dataclasses import dataclass


@dataclass
class MentorPart:
    mentor_id: int
    fio: str
    scientific_degree: str
