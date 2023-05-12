from typing import List

from kivymd.uix.card import MDCard

from src import config
from src.domain.enums import ViewType
from src.ui.views.schedule_week import ScheduleWeek


class MentorsSchedule(MDCard):
    MENTORS_AT_ONE_MOMENT = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mentors = []
        self.min_id, self.max_id = None, None

    async def add_mentors(self, mentors: List[str]):
        self.mentors.clear()
        self.ids.body_cont.clear_widgets()

        self.min_id, self.max_id = (
            0,
            min(len(mentors), MentorsSchedule.MENTORS_AT_ONE_MOMENT) - 1,
        )
        for ind, group in enumerate(mentors):
            # create views
            self.mentors.append(
                ScheduleWeek(
                    group,
                    ViewType.GROUP.value,
                    config.get_pairs_quantity(),
                )
            )
            if ind <= self.max_id:
                self.ids.body_cont.add_widget(self.mentors[ind])

    async def shift_mentor(self, direction: str):
        if self.min_id is None or self.max_id is None:
            return

        if direction == "r":
            if self.max_id + 1 < len(self.mentors):
                self.ids.body_cont.remove_widget(self.mentors[self.min_id])
                self.ids.body_cont.add_widget(self.mentors[self.max_id + 1])

                self.min_id, self.max_id = self.min_id + 1, self.max_id + 1
        elif direction == "l":
            if self.min_id != 0:
                self.ids.body_cont.add_widget(self.mentors[self.min_id - 1])
                self.ids.body_cont.remove_widget(self.mentors[self.max_id])

                self.min_id, self.max_id = self.min_id - 1, self.max_id - 1
        else:
            raise
