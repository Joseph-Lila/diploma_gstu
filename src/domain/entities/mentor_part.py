from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class MentorPart:
    mentor_id: int
    fio: str
    scientific_degree: str
