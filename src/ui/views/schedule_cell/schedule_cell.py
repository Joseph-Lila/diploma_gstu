from dataclasses import astuple
from typing import List, Any, Tuple
import asynckivy as ak
from kivy.app import App
from kivy.core.window import Window
from kivymd.uix.card import MDCard

from src.domain.entities import CellPart, CellPos
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState, Subgroup, WeekType
from src.domain.interfaces import (
    AbstractSizeMaster,
    AbstractSizeSlave,
)
from src.domain.interfaces.abstract_tuned_by_info_records import (
    AbstractTunedByInfoRecords,
)
from src.service_layer.handlers import convert_pos_into_pos_hint
from src.ui.views.schedule_cell_configuration_type_dialog import (
    ScheduleCellConfigurationTypeDialog,
)
from src.ui.views.schedule_item_btn import ScheduleItemBtn
from src.ui.views.schedule_item_dialog import ScheduleItemDialog


class ScheduleCell(
    MDCard, AbstractSizeMaster, AbstractSizeSlave, AbstractTunedByInfoRecords
):
    SLAVES_CNT = 4
    CONDITIONS = (
        {
            (WeekType.ABOVE.value, Subgroup.FIRST.value): [],
            (WeekType.ABOVE.value, Subgroup.BOTH.value): [1],
            (WeekType.BOTH.value, Subgroup.FIRST.value): [],
            (WeekType.BOTH.value, Subgroup.BOTH.value): [1, 2, 3],
        },
        {
            (WeekType.ABOVE.value, Subgroup.SECOND.value): [],
            (WeekType.BOTH.value, Subgroup.SECOND.value): [],
        },
        {
            (WeekType.UNDER.value, Subgroup.FIRST.value): [],
            (WeekType.BOTH.value, Subgroup.FIRST.value): [],
            (WeekType.UNDER.value, Subgroup.BOTH.value): [3],
        },
        {
            (WeekType.UNDER.value, Subgroup.SECOND.value): [],
            (WeekType.BOTH.value, Subgroup.SECOND.value): [],
        },
    )

    def __init__(
        self,
        day_of_week,
        pair_number,
        view_type,
        context_menu,
        *args,
        cur_group="",
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.context_menu = context_menu
        self.cur_group = cur_group
        self.slaves: List[ScheduleItemBtn] = [
            ScheduleItemBtn(
                cur_group=cur_group,
                view_state=ViewState.EMPTY.value,
                schedule_item_info=ScheduleItemInfo(
                    cell_part=CellPart(
                        week_type=WeekType.UNDEFINED.value,
                        subgroup=Subgroup.UNDEFINED.value,
                    ),
                    cell_pos=CellPos(day_of_week, pair_number),
                ),
            )
            for _ in range(ScheduleCell.SLAVES_CNT)
        ]
        for slave in self.slaves:
            slave.update_view_metadata(ViewState.EMPTY.value, view_type)
        if ScheduleCell.SLAVES_CNT < 4:
            raise
        self.ids.top_cont.add_widget(self.slaves[0])
        self.ids.top_cont.add_widget(self.slaves[1])
        self.ids.bottom_cont.add_widget(self.slaves[2])
        self.ids.bottom_cont.add_widget(self.slaves[3])
        self.fit_slaves()

    def open_dialog(self, *args):
        self.context_menu.dismiss()
        ScheduleCellConfigurationTypeDialog(self.slaves).open()

    def clear(self, *args):
        self.context_menu.dismiss()

        ids_to_delete = []
        for slave in self.slaves:
            if (
                slave.schedule_item_info is not None
                and slave.schedule_item_info.additional_part is not None
            ):
                if self.cur_group != "":
                    for i, group in enumerate(slave.schedule_item_info.groups_part):
                        if group.title == self.cur_group:
                            ids_to_delete.append(
                                slave.schedule_item_info.additional_part.schedule_record_ids[
                                    i
                                ]
                            )
                else:
                    for (
                        schedule_record_id
                    ) in slave.schedule_item_info.additional_part.schedule_record_ids:
                        ids_to_delete.append(schedule_record_id)

        ak.start(
            App.get_running_app().controller.delete_local_schedule_records(
                ids_to_delete,
                App.get_running_app().root.get_current_screen_view(),
            )
        )

    def check_if_clearable(self):
        for slave in self.slaves:
            if slave.view_state in [
                ViewState.FILLED.value,
            ]:
                return True
        return False

    def check_if_configuration_can_be_tuned(self):
        for slave in self.slaves:
            if slave.view_state not in [
                ViewState.EDITABLE.value,
                ViewState.INVISIBLE.value,
                ViewState.UNAVAILABLE.value,
            ]:
                return False
        return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and touch.button == "right":
            pos = self.to_window(*touch.pos)
            pos_hint = convert_pos_into_pos_hint(
                Window.size,
                pos,
            )
            self.context_menu.set_data(
                pos,
                pos_hint,
                self.open_dialog,
                self.clear,
                self.check_if_clearable(),
                self.check_if_configuration_can_be_tuned(),
            )
            self.context_menu.open()
        elif (
            self.collide_point(*touch.pos)
            and touch.button == "left"
            and not self.context_menu._is_open
        ):
            self.context_menu.dismiss()
            [touched_slave] = [
                slave for slave in self.slaves if slave.collide_point(*touch.pos)
            ]
            if touched_slave.view_state in [
                ViewState.FILLED.value,
                ViewState.EDITABLE.value,
            ]:
                ScheduleItemDialog(touched_slave).open()

    def fit_slaves(self):
        if len(self.slaves) > 0:
            max_width = max(slave.get_minimum_width() for slave in self.slaves)
            for slave in self.slaves:
                if slave.view_state == ViewState.INVISIBLE.value:
                    slave.set_invisible_width()
                else:
                    slave.set_width(max_width)

            # tune containers
            if (
                self.slaves[0].view_state
                == self.slaves[1].view_state
                == ViewState.INVISIBLE.value
            ):
                self.ids.top_cont.size_hint_y = None
                self.ids.top_cont.height = 0
            else:
                self.ids.top_cont.size_hint_y = 1
            if (
                self.slaves[2].view_state
                == self.slaves[3].view_state
                == ViewState.INVISIBLE.value
            ):
                self.ids.bottom_cont.size_hint_y = None
                self.ids.bottom_cont.height = 0
            else:
                self.ids.bottom_cont.size_hint_y = 1

    def set_width(self, width):
        super().set_width(width)

    def expand_slaves_on_all_width(self):
        self.ids.top_cont.size_hint_x = 1
        self.ids.bottom_cont.size_hint_x = 1
        for slave in self.slaves:
            if slave.view_state != ViewState.INVISIBLE.value:
                slave.size_hint_x = 1

    def get_minimum_width(self):
        return (
            max(
                [
                    self.slaves[0].width + self.slaves[1].width,
                    self.slaves[2].width + self.slaves[3].width,
                ]
            )
            + 2 * self.padding[-1]
            + self.spacing
        )

    async def tune_using_info_records(self, info_records: List[ScheduleItemInfo]):
        slave_results: List[Any] = [None for _ in range(len(self.slaves))]

        parsed_info_records = [astuple(record.cell_part) for record in info_records]

        for i, parsed_info_record in enumerate(parsed_info_records):
            for j, condition in enumerate(self.CONDITIONS):
                if parsed_info_record in condition:
                    res = ViewState.FILLED.value \
                        if info_records[i].additional_part.mentor_free else ViewState.MENTOR_IS_BUSY.value
                    slave_results[j] = (res, info_records[i])
                    for ind in condition[parsed_info_record]:
                        slave_results[ind] = (ViewState.INVISIBLE.value, None)

        for i, res in enumerate(slave_results):
            if res is not None:
                state, info = res
                if info is not None:
                    self.slaves[i].schedule_item_info = info
                self.slaves[i].update_view_metadata(state)
            else:
                # TODO: find actual state
                state = ViewState.EDITABLE.value
                self.slaves[i].schedule_item_info.cell_part = CellPart(
                    week_type=WeekType.ABOVE.value if i < 2 else WeekType.UNDER.value,
                    subgroup=Subgroup.FIRST.value if i % 2 == 0 else Subgroup.SECOND.value,
                )
                self.slaves[i].update_view_metadata(state)

        self.fit_slaves()
