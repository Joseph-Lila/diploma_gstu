from typing import List

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.interfaces import (
    AbstractSizeMaster,
    AbstractSizeSlave,
)
from src.domain.interfaces.abstract_tuned_by_info_records import (
    AbstractTunedByInfoRecords,
)
from src.ui.views.schedule_cell import ScheduleCell


class ScheduleDay(
    MDCard, AbstractSizeMaster, AbstractSizeSlave, AbstractTunedByInfoRecords
):
    def __init__(
        self, pairs_quantity: int, day_of_week: str, *args, cur_group="", **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.cur_group = cur_group
        self.slaves: List[ScheduleCell] = []
        self.update_metadata(pairs_quantity, day_of_week)

    def get_minimum_width(self):
        return (
            self.padding[-1] * 2
            + self.ids.day_of_week_lbl.width
            + self.ids.pairs_cells_cont.width
            + self.slaves[-1].width
        )

    def update_metadata(
        self,
        pairs_quantity: int,
        day_of_week: str,
    ):
        self.ids.day_of_week_lbl.text = day_of_week

        self.ids.content.clear_widgets()
        self.ids.pairs_cells_cont.clear_widgets()
        self.slaves = [
            ScheduleCell(cur_group=self.cur_group) for _ in range(1, pairs_quantity + 1)
        ]

        for i in range(1, pairs_quantity + 1):
            self.ids.pairs_cells_cont.add_widget(
                MDLabel(
                    font_size=11,
                    text=str(i),
                    halign="center",
                    valign="center",
                    outline_color=(1, 0, 0, 1),
                ),
            )
            self.ids.content.add_widget(self.slaves[i - 1])
        self.fit_slaves()

    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        for i, slave in enumerate(self.slaves, start=1):
            await slave.tune_using_info_records(
                [
                    record
                    for record in info_records
                    if self.ids.day_of_week_lbl.text == record.cell_pos.day_of_week
                    and i == record.cell_pos.pair_number
                ]
            )
