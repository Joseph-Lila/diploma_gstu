import copy
from typing import List

from src.adapters.orm import Workload
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import Subgroup
from src.service_layer.handlers import convert_cell_part_to_hours


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
    def actual_workloads(self):
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
                hours = await convert_cell_part_to_hours(record.cell_part)
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
