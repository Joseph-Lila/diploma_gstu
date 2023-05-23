from kivy.properties import ObjectProperty

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from typing import List

from src.ui.views.schedule_week.schedule_week import ScheduleWeek


class AbstractScheduleWeeksStore:
    master = ObjectProperty()

    def __init__(self):
        self.schedule_weeks: List[ScheduleWeek] = []
        self.min_id, self.max_id = None, None

    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        for schedule_week in self.schedule_weeks:
            await schedule_week.tune_using_info_records(info_records)

    def fit_widgets(self):
        for schedule_week in self.schedule_weeks:
            schedule_week.fit_slaves()
