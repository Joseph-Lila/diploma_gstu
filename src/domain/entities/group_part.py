from dataclasses import dataclass


@dataclass
class GroupPart:
    group_id: int
    title: str
    number_of_students: int


def parse_row_data_to_group_part(id_, title, number_of_students):
    return GroupPart(id_, title, number_of_students)
