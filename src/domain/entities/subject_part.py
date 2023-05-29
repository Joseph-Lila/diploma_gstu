from dataclasses import dataclass


@dataclass
class SubjectPart:
    subject_id: int
    subject_type_id: int
    subject: str
    subject_type: str


def parse_row_data_to_subject_part(
    subject_id,
    subject_type_id,
    subject_title,
    subject_type_title,
):
    return SubjectPart(
        subject_id,
        subject_type_id,
        subject_title,
        subject_type_title,
    )
