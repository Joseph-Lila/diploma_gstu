from dataclasses import dataclass
from typing import List

from src.domain.commands.command import Command


@dataclass
class GetSubjectTypesForScheduleItem(Command):
    mentor_id: int
    audience_id: int
