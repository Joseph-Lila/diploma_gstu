from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetMentorsForScheduleItem(Command):
    day_of_week: str
    pair_number: int
    week_type: str
    subgroup: str
    subject_id: int
    subject_type_id: int
