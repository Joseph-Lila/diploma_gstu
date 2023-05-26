from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class MentorPart:
    mentor_id: int
    fio: str
    scientific_degree: str


def parse_row_data_to_mentor_part(id_, fio, scientific_degree):
    return MentorPart(id_, fio, scientific_degree)
