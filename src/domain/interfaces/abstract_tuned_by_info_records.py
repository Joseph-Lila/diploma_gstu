from typing import List

from src.domain.entities.schedule_item_info import ScheduleItemInfo


class AbstractTunedByInfoRecords:
    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        raise NotImplementedError
