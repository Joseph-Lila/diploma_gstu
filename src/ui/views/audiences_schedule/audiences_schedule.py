from typing import List

from kivymd.uix.card import MDCard

from src import config
from src.domain.enums import ViewType
from src.domain.interfaces import AbstractScheduleWeeksStore
from src.ui.views.schedule_week.schedule_week import ScheduleWeek


class AudiencesSchedule(MDCard, AbstractScheduleWeeksStore):
    AUDIENCES_AT_ONE_MOMENT = 4

    async def add_audiences(self, audiences: List[str]):
        self.clear_audiences()

        self.min_id, self.max_id = (
            0,
            min(len(audiences), AudiencesSchedule.AUDIENCES_AT_ONE_MOMENT) - 1,
        )
        for ind, audience in enumerate(audiences):
            # create views
            self.schedule_weeks.append(
                ScheduleWeek(
                    audience,
                    ViewType.AUDIENCE.value,
                    config.get_pairs_quantity(),
                )
            )
            if ind <= self.max_id:
                self.ids.body_cont.add_widget(self.schedule_weeks[ind])
        self.master.send_command_to_refresh_cells()

    def clear_audiences(self):
        self.schedule_weeks.clear()
        self.ids.body_cont.clear_widgets()
        self.min_id, self.max_id = None, None

    async def shift_audience(self, direction: str):
        if self.min_id is None or self.max_id is None:
            return

        if direction == "r":
            if self.max_id + 1 < len(self.schedule_weeks):
                self.ids.body_cont.remove_widget(self.schedule_weeks[self.min_id])
                self.ids.body_cont.add_widget(self.schedule_weeks[self.max_id + 1])

                self.min_id, self.max_id = self.min_id + 1, self.max_id + 1
        elif direction == "l":
            if self.min_id != 0:
                self.ids.body_cont.add_widget(self.schedule_weeks[self.min_id - 1])
                self.ids.body_cont.remove_widget(self.schedule_weeks[self.max_id])

                self.min_id, self.max_id = self.min_id - 1, self.max_id - 1
        else:
            raise
