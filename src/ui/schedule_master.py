from typing import Optional, List

from pandas import DataFrame

from src.domain.commands import GetExtendedScheduleRecords
from src.domain.entities import GroupPart
from src.domain.entities.schedule_item_info import ScheduleItemInfo, build_from_raw_data
from src.domain.enums import ViewType, ViewState
from src.domain.events import GotDataFrame
from src.ui.controller import use_loop


class ScheduleMaster:
    BOARDS_CNT = 2

    def __init__(self, model):
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

    @use_loop
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
