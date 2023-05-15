from typing import List


class ScheduleMaster:
    BOARDS_CNT = 2

    def __init__(self, model):
        self._workloads = None
        self._model = model
        self._schedule_id = None
        self._year = None
        self._term = None

    @property
    def id(self):
        return self._schedule_id

    @property
    def year(self):
        return self._year

    @property
    def term(self):
        return self._term

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
        workloads: List[tuple],
    ):
        self._workloads = workloads
