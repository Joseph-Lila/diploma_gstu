from dataclasses import dataclass, field
from typing import List, Optional

from src.domain.entities import AdditionalPart, AudiencePart, CellPart, CellPos, GroupPart, MentorPart, SubjectPart
from src.domain.enums import ViewState, ViewType


@dataclass
class ScheduleItemInfo:
    cell_pos: Optional[CellPos] = None
    cell_part: Optional[CellPart] = None
    audience_part: Optional[AudiencePart] = None
    groups_part: List[GroupPart] = field(default_factory=lambda: [])
    mentor_part: Optional[MentorPart] = None
    subject_part: Optional[SubjectPart] = None
    additional_part: Optional[AdditionalPart] = None
    view_state: str = ViewState.UNAVAILABLE.value
    view_type: str = ViewType.GROUP.value
