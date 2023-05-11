from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from src.domain.interfaces import AbstractSizeMaster, AbstractSizeSlave
from src.ui.views.schedule_cell import ScheduleCell


class ScheduleDay(MDCard, AbstractSizeMaster, AbstractSizeSlave):
    def __init__(
        self, pairs_quantity: int, day_of_week: str, *args, cur_group="", **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.cur_group = cur_group
        self.slaves = []
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
