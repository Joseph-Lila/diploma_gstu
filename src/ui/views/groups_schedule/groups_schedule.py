from dataclasses import astuple
from typing import List

from kivymd.uix.card import MDCard

from src import config
from src.domain.entities import GroupDescription
from src.domain.enums import ViewType
from src.ui.views.schedule_week import ScheduleWeek


class GroupsSchedule(MDCard):
    GROUPS_AT_ONE_MOMENT = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = {}
        self.group_descriptions = []
        self.min_id, self.max_id = None, None

    async def add_groups(self, group_descriptions: List[GroupDescription]):
        self.groups.clear()
        self.group_descriptions.clear()
        self.ids.body_cont.clear_widgets()

        self.min_id, self.max_id = (
            0,
            min(len(group_descriptions), GroupsSchedule.GROUPS_AT_ONE_MOMENT) - 1,
        )
        self.group_descriptions = group_descriptions
        for ind, r in enumerate(group_descriptions):
            key = astuple(r)

            # create views
            self.groups[key] = ScheduleWeek(
                r.title, ViewType.GROUP.value, config.get_pairs_quantity()
            )
            if ind <= self.max_id:
                self.ids.body_cont.add_widget(self.groups[key])

    async def get_group_widget_by_id(self, id_: int):
        key = astuple(self.group_descriptions[id_])
        return self.groups[key]

    async def shift_group(self, direction: str):
        if self.min_id is None or self.max_id is None:
            return

        if direction == "r":
            if self.max_id + 1 < len(self.group_descriptions):
                widget_to_remove = await self.get_group_widget_by_id(self.min_id)
                widget_to_add = await self.get_group_widget_by_id(self.max_id + 1)
                self.ids.body_cont.remove_widget(widget_to_remove)
                self.ids.body_cont.add_widget(widget_to_add)

                self.min_id, self.max_id = self.min_id + 1, self.max_id + 1
        elif direction == "l":
            if self.min_id != 0:
                widget_to_remove = await self.get_group_widget_by_id(self.max_id)
                widget_to_add = await self.get_group_widget_by_id(self.min_id - 1)
                self.ids.body_cont.add_widget(widget_to_add)
                self.ids.body_cont.remove_widget(widget_to_remove)

                self.min_id, self.max_id = self.min_id - 1, self.max_id - 1
        else:
            raise
