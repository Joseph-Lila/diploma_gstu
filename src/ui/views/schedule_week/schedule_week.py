from typing import List

from kivy.properties import StringProperty
from kivymd.uix.card import MDCard

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import DayOfWeek, ViewType, ViewState
from src.domain.interfaces import AbstractSizeMaster
from src.domain.interfaces.abstract_tuned_by_info_records import (
    AbstractTunedByInfoRecords,
)
from src.ui.views.schedule_day import ScheduleDay


class ScheduleWeek(MDCard, AbstractSizeMaster, AbstractTunedByInfoRecords):
    view_type = StringProperty()

    def __init__(
        self,
        entity_title: str,
        view_type: str,
        pairs_quantity: int,
        context_menu,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.context_menu = context_menu
        self.slaves: List[ScheduleDay] = []
        self.update_metadata(entity_title, view_type, pairs_quantity)

    def update_metadata(
        self,
        entity_title: str,
        view_type: str,
        pairs_quantity: int,
    ):
        self.ids.entity_title.text = entity_title
        self.view_type = view_type
        self.ids.cont.clear_widgets()
        self.slaves = [
            ScheduleDay(
                pairs_quantity,
                day_of_week.value,
                view_type,
                context_menu=self.context_menu,
                cur_group=entity_title if view_type == ViewType.GROUP.value else "",
            )
            for day_of_week in DayOfWeek
        ]
        for slave in self.slaves:
            self.ids.cont.add_widget(slave)
        self.fit_slaves()

    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        for slave in self.slaves:
            # find suitable records
            fit_info_records = [
                record
                for record in info_records
                if self.ids.entity_title.text
                in [
                    record.mentor_part.fio,
                    record.audience_part.number,
                ]
                + [r.title for r in record.groups_part]
            ]
            # make copy to create new instances
            copy_of_fit_info_records = fit_info_records[:]
            # change view_state on actual
            for r in copy_of_fit_info_records:
                r.view_type = self.view_type
            await slave.tune_using_info_records(copy_of_fit_info_records)
        self.fit_slaves()

    def fit_slaves(self):
        if len(self.slaves) > 0:
            max_width = max(slave.get_minimum_width() for slave in self.slaves)
            for slave in self.slaves:
                slave.set_width(max_width)
        self.ids.entity_title.width = self.slaves[-1].width
        self.width = self.slaves[-1].width
