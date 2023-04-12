from kivymd.uix.list import TwoLineAvatarListItem

from src.adapters.orm import Schedule


class ScheduleListItem(TwoLineAvatarListItem):
    def __init__(self, schedule_item: Schedule, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule_item = schedule_item
        self.text = f"Расписание занятий {self.schedule_item.year}-{self.schedule_item.year + 1} учебный год"
        self.secondary_text = f"Семестр: {self.schedule_item.term}"
