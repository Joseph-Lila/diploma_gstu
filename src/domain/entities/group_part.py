from dataclasses import dataclass


@dataclass
class GroupPart:
    group_id: int
    title: str
    number_of_students: int
