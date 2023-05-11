from dataclasses import dataclass


@dataclass
class GroupDescription:
    group_id: int
    title: str
    faculty: str


def parse_row_data_to_group_description(row):
    group_id, title, faculty = row
    return GroupDescription(
        group_id=group_id,
        title=title,
        faculty=faculty,
    )
