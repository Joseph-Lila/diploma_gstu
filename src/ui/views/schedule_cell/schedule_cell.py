from typing import List

from kivymd.uix.card import MDCard

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState, Subgroup, WeekType
from src.domain.interfaces import (
    AbstractSizeMaster,
    AbstractSizeSlave,
)
from src.domain.interfaces.abstract_tuned_by_info_records import (
    AbstractTunedByInfoRecords,
)
from src.ui.views.schedule_item_btn import ScheduleItemBtn


class ScheduleCell(
    MDCard, AbstractSizeMaster, AbstractSizeSlave, AbstractTunedByInfoRecords
):
    SLAVES_CNT = 4
    CONDITIONS = (
        {
            (Subgroup.FIRST.value, WeekType.ABOVE.value): [],
            (Subgroup.BOTH.value, WeekType.ABOVE.value): [1],
            (Subgroup.FIRST.value, WeekType.BOTH.value): [],
            (Subgroup.BOTH.value, WeekType.BOTH.value): [1, 2, 3],
        },
        {
            (Subgroup.SECOND.value, WeekType.ABOVE.value): [],
            (Subgroup.SECOND.value, WeekType.BOTH.value): [],
        },
        {
            (Subgroup.FIRST.value, WeekType.UNDER.value): [],
            (Subgroup.FIRST.value, WeekType.BOTH.value): [],
            (Subgroup.BOTH.value, WeekType.UNDER.value): [3],
        },
        {
            (Subgroup.SECOND.value, WeekType.UNDER.value): [],
            (Subgroup.SECOND.value, WeekType.BOTH.value): [],
        },
    )

    def __init__(self, *args, cur_group="", **kwargs):
        super().__init__(*args, **kwargs)
        self.slaves: List[ScheduleItemBtn] = [
            ScheduleItemBtn(
                cur_group=cur_group,
                view_state=ViewState.EMPTY.value,
            ) for _ in range(ScheduleCell.SLAVES_CNT)
        ]
        for slave in self.slaves:
            slave.update_info(ViewState.EMPTY.value)
        if ScheduleCell.SLAVES_CNT < 4:
            raise
        self.ids.top_cont.add_widget(self.slaves[0])
        self.ids.top_cont.add_widget(self.slaves[1])
        self.ids.bottom_cont.add_widget(self.slaves[2])
        self.ids.bottom_cont.add_widget(self.slaves[3])
        self.fit_slaves()

    def fit_slaves(self):
        if len(self.slaves) > 0:
            max_width = max(slave.get_minimum_width() for slave in self.slaves)
            for slave in self.slaves:
                if slave.view_state == ViewState.INVISIBLE.value:
                    slave.set_invisible_width()
                else:
                    slave.set_width(max_width)

            # tune containers
            if self.slaves[0].view_state == self.slaves[1].view_state == ViewState.INVISIBLE.value:
                self.ids.top_cont.size_hint_y = None
                self.ids.top_cont.height = 0
            else:
                self.ids.top_cont.size_hint_y = 1
            if self.slaves[2].view_state == self.slaves[3].view_state == ViewState.INVISIBLE.value:
                self.ids.bottom_cont.size_hint_y = None
                self.ids.bottom_cont.height = 0
            else:
                self.ids.bottom_cont.size_hint_y = 1

    def set_width(self, width):
        self.size_hint_x = None
        self.size_hint_y = 1
        self.width = width

    def expand_slaves_on_all_width(self):
        self.ids.top_cont.size_hint_x = 1
        self.ids.bottom_cont.size_hint_x = 1
        for slave in self.slaves:
            if slave.view_state != ViewState.INVISIBLE.value:
                slave.size_hint_x = 1

    def get_minimum_width(self):
        return max(
            [
                self.slaves[0].width + self.slaves[1].width,
                self.slaves[2].width + self.slaves[3].width,
            ]
        ) + 2 * self.padding[-1] + self.spacing

    @staticmethod
    def parse_info(info_record: ScheduleItemInfo):
        return info_record.cell_part.subgroup, info_record.cell_part.week_type

    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        slave_states = [ViewState.EMPTY.value for _ in self.slaves]

        if len(info_records) == 0:
            slave_states = [
                ViewState.EMPTY.value,
                ViewState.INVISIBLE.value,
                ViewState.INVISIBLE.value,
                ViewState.INVISIBLE.value,
            ]
        else:
            parsed_info_records = [ScheduleCell.parse_info(record) for record in info_records]

            for i, parsed_info_record in enumerate(parsed_info_records):
                for j, condition in enumerate(self.CONDITIONS):
                    if parsed_info_record in condition:
                        self.slaves[j].schedule_item_info = info_records[i]
                        slave_states[j] = ViewState.FILLED.value
                        for ind in condition[parsed_info_record]:
                            slave_states[ind] = ViewState.INVISIBLE.value

        for i, state in enumerate(slave_states):
            if state != ViewState.EMPTY.value:
                self.slaves[i].update_info(state)
            else:
                # define real state
                # TODO: find actual state
                self.slaves[i].update_info(state)

        self.fit_slaves()
