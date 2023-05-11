from typing import List

from kivymd.uix.card import MDCard

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState
from src.domain.interfaces import AbstractSizeMaster, AbstractSizeSlave
from src.ui.views.schedule_item_btn import ScheduleItemBtn


class ScheduleCell(MDCard, AbstractSizeMaster, AbstractSizeSlave):
    SLAVES_CNT = 4

    def __init__(self, *args, cur_group='', **kwargs):
        super().__init__(*args, **kwargs)
        self.slaves = [ScheduleItemBtn(cur_group=cur_group) for _ in range(ScheduleCell.SLAVES_CNT)]
        for slave in self.slaves:
            slave.update_info(ViewState.EMPTY.value)
        if ScheduleCell.SLAVES_CNT < 4:
            raise
        self.ids.top_cont.add_widget(self.slaves[0])
        self.ids.top_cont.add_widget(self.slaves[1])
        self.ids.bottom_cont.add_widget(self.slaves[2])
        self.ids.bottom_cont.add_widget(self.slaves[3])
        self.fit_slaves()

    def get_minimum_width(self):
        return self.slaves[-1].width * 2 + 2 * self.padding[-1] + self.spacing

    async def tune_slaves_using_info_records(self, info_records: List[ScheduleItemInfo]):
        print(f"{info_records = }")
