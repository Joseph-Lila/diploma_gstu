from dataclasses import dataclass, field
from typing import List, Optional

from src.domain.entities import (
    AdditionalPart,
    AudiencePart,
    CellPart,
    CellPos,
    GroupPart,
    MentorPart,
    SubjectPart,
)


@dataclass
class ScheduleItemInfo:
    cell_pos: Optional[CellPos] = None
    cell_part: Optional[CellPart] = None
    audience_part: Optional[AudiencePart] = None
    groups_part: List[GroupPart] = field(default_factory=lambda: [])
    mentor_part: Optional[MentorPart] = None
    subject_part: Optional[SubjectPart] = None
    additional_part: Optional[AdditionalPart] = None


def build_schedule_item_info_from_raw_data(
    day_of_week,
    pair_number,
    week_type,
    subgroup,
    audience_id,
    audience_number,
    number_of_seats,
    group_id,
    group_title,
    number_of_students,
    mentor_id,
    mentor_fio,
    scientific_degree,
    subject_id,
    subject_type_id,
    subject_title,
    subject_type_title,
    mentor_free,
    schedule_record_id,
):
    return ScheduleItemInfo(
        cell_pos=CellPos(
            day_of_week=day_of_week,
            pair_number=pair_number,
        ),
        cell_part=CellPart(
            subgroup=subgroup,
            week_type=week_type,
        ),
        audience_part=AudiencePart(
            audience_id=audience_id,
            number=audience_number,
            total_seats=number_of_seats,
        ),
        groups_part=[
            GroupPart(
                group_id=group_id,
                title=group_title,
                number_of_students=number_of_students,
            )
        ],
        mentor_part=MentorPart(
            fio=mentor_fio,
            mentor_id=mentor_id,
            scientific_degree=scientific_degree,
        ),
        subject_part=SubjectPart(
            subject=subject_title,
            subject_id=subject_id,
            subject_type=subject_type_title,
            subject_type_id=subject_type_id,
        ),
        additional_part=AdditionalPart(
            mentor_free=mentor_free,
            schedule_record_id=schedule_record_id,
        ),
    )
