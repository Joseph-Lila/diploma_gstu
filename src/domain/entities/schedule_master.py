from typing import Dict, List

from src.adapters.orm import Workload, ScheduleRecord
from src.domain.entities.audience_record import AudienceRecord
from src.domain.entities.cell_conf import CellConf
from src.domain.entities.cell_pos import CellPos
from src.domain.enums import WeekType, Subgroup


class ScheduleMaster:
    def __init__(self):
        self._id = None
        self._year = None
        self._term = None

        self._audience_records: List[AudienceRecord] = []

        self._workloads_remainder: List[Workload] = []
        self._schedule_records: Dict[CellPos, List[ScheduleRecord]] = {}
        self._filling_conditions = {
            "day_of_week": None,
            "pair_number": None,
            "week_type": None,
            "subgroup": None,
            "subject_id": None,
            "subject_type_id": None,
            "hours": None,
        }

    @property
    def id(self):
        return self._id

    def update_metadata(
            self,
            id_,
            year,
            term,
            audience_records,
            workloads_remainder,
            old_schedule_records,
    ):
        self._id = id_
        self._year = year
        self._term = term
        self._audience_records = audience_records
        self._workloads_remainder = workloads_remainder

    def must_condition(self, workload: Workload, cell_conf: CellConf):
        cell_pos = CellPos(
            day_of_week=cell_conf.day_of_week,
            pair_number=cell_conf.pair_number,
        )

        # check if mentor is busy
        if not len(
            [
                r for r in self._schedule_records[cell_pos]
                if r.mentor_id == workload.mentor_id
                and r.week_type in [cell_conf.week_type, WeekType.BOTH.value]
                and r.subgroup in [cell_conf.subgroup, Subgroup.BOTH.value]
            ]
        ) == 0:
            return False

        # check if there is a free audience
        if len(
            [
                r for r in self._audience_records
                if r not in
                [
                    record for record in
                    self._schedule_records[cell_pos]
                    if record.audience_id == r.id
                ]
            ]
        ) == 0:
            return False
