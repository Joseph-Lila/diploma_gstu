import copy
import math
from typing import List

from src.adapters.orm import Workload
from src.domain.entities import (
    CellPart,
    MentorPart,
    GroupPart,
    SubjectPart,
    AudiencePart,
)
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import Subgroup, WeekType


class ScheduleMaster:
    BOARDS_CNT = 2

    def __init__(self, model):
        self._workloads = None
        self._model = model
        self._schedule_id = None
        self._year = None
        self._term = None
        self._actual_workloads = None
        self._actual_workloads_helper = {}

    @property
    def id(self):
        return self._schedule_id

    @property
    def year(self):
        return self._year

    @property
    def term(self):
        return self._term

    @property
    def workloads(self):
        return self._workloads

    @property
    def actual_workloads(self) -> List[Workload]:
        return self._actual_workloads

    async def update_metadata(
        self,
        id_,
        year,
        term,
    ):
        # data about the schedule
        self._schedule_id = id_
        self._year = year
        self._term = term

    async def set_workloads(
        self,
        workloads: List[Workload],
    ):
        self._workloads = workloads

    async def fit_workloads_using_info_records(
        self,
        records: List[ScheduleItemInfo],
    ):
        # actualize workloads
        self._actual_workloads = copy.deepcopy(self._workloads)
        self._actual_workloads_helper.clear()

        for record in records:
            if record.additional_part.mentor_free:
                hours = await ScheduleMaster.convert_cell_part_to_hours(
                    record.cell_part
                )
                for group in record.groups_part:
                    for workload in self._actual_workloads:
                        if all(
                            [
                                workload.group_id == group.group_id,
                                workload.subject_id == record.subject_part.subject_id,
                                workload.subject_type_id
                                == record.subject_part.subject_type_id,
                                workload.mentor_id == record.mentor_part.mentor_id,
                            ]
                        ):
                            workload.hours -= hours
                            key = (
                                workload.group_id,
                                workload.subject_id,
                                workload.subject_type_id,
                                workload.mentor_id,
                            )
                            if self._actual_workloads_helper.get(key, None) is None:
                                self._actual_workloads_helper[key] = {
                                    Subgroup.FIRST.value: 0,
                                    Subgroup.SECOND.value: 0,
                                    Subgroup.BOTH.value: 0,
                                }
                            self._actual_workloads_helper[key][
                                record.cell_part.subgroup
                            ] += hours
        # clear empty workloads (where hours == 0)
        self._actual_workloads = [
            workload
            for workload in self._actual_workloads
            if not abs(workload.hours) < 1e-5
        ]

    @staticmethod
    async def check_if_groups_fit_in_the_audience(
        old_record: ScheduleItemInfo,
        groups_part: List[GroupPart],
        audience_part: AudiencePart,
        cell_part: CellPart,
    ) -> bool:
        if not all(
            [
                old_record,
                len(groups_part) > 0,
                audience_part,
                cell_part,
            ]
        ):
            return True

        # check if all the groups will fit in the provided audience
        if cell_part.subgroup in [Subgroup.FIRST.value, Subgroup.SECOND.value]:
            needed_seats = sum(
                [math.ceil(group.number_of_students / 2) for group in groups_part]
            )
        else:
            needed_seats = sum([group.number_of_students for group in groups_part])
        if needed_seats > audience_part.total_seats:
            return False

        return True

    async def check_if_groups_workloads_have_enough_hours(
        self,
        old_record: ScheduleItemInfo,
        cell_part: CellPart,
        subject_part: SubjectPart,
        groups_part: List[GroupPart],
    ):
        if cell_part and subject_part and groups_part is not None:
            hours = await self.convert_cell_part_to_hours(cell_part)
            old_hours = await self.get_old_hours(old_record)

            for group in groups_part:
                for workload in self.actual_workloads:
                    if (
                        all(
                            [
                                group.group_id == workload.group_id,
                                subject_part.subject_id == workload.subject_id,
                                subject_part.subject_type_id
                                == workload.subject_type_id,
                            ]
                        )
                        and hours > workload.hours + old_hours
                    ):
                        return False
            return True
        else:
            return False

    @staticmethod
    async def get_old_hours(
        old_record: ScheduleItemInfo,
    ) -> float:
        if old_record is not None and old_record.cell_part is not None:
            old_hours = await ScheduleMaster.convert_cell_part_to_hours(
                old_record.cell_part
            )
        else:
            old_hours = 0

        return old_hours

    @staticmethod
    async def convert_cell_part_to_hours(
        cell_part: CellPart,
    ) -> float:
        # define first coefficient
        if cell_part.subgroup == Subgroup.BOTH.value:
            a = 1
        elif cell_part.subgroup in [Subgroup.FIRST.value, Subgroup.SECOND.value]:
            a = 0.5
        else:
            raise ValueError

        # define second coefficient
        if cell_part.week_type == WeekType.BOTH.value:
            b = 1
        elif cell_part.week_type in [WeekType.UNDER.value, WeekType.ABOVE.value]:
            b = 0.5
        else:
            raise ValueError

        # by default one cell == 2 hours per week
        return 2 * a * b

    async def get_extended_actual_mentors(
        self,
        old_info: ScheduleItemInfo,
        extended_mentors: List[MentorPart],
    ) -> List[MentorPart]:
        mentor_ids = [r.mentor_id for r in self.actual_workloads]
        if old_info and old_info.mentor_part:
            mentor_ids.append(old_info.mentor_part.mentor_id)

        mentors = [
            mentor for mentor in extended_mentors if mentor.mentor_id in mentor_ids
        ]
        return mentors

    async def get_extended_actual_groups(
        self,
        old_info: ScheduleItemInfo,
        extended_groups: List[GroupPart],
    ) -> List[GroupPart]:
        group_ids = [r.group_id for r in self.actual_workloads]
        if old_info and old_info.groups_part:
            group_ids.extend([group.group_id for group in old_info.groups_part])

        groups = [
            group for group in extended_groups if group.group_id in set(group_ids)
        ]
        return groups
