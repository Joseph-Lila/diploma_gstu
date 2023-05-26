from dataclasses import dataclass


@dataclass
class GroupPart:
    group_id: int
    title: str
    number_of_students: int


def parse_row_data_to_group_part(row_data: tuple):
    return GroupPart(*row_data)
