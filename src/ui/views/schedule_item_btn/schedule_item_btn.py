from typing import List
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState
from src.domain.interfaces import AbstractSizeSlave


class ScheduleItemBtn(Button, AbstractSizeSlave):
    schedule_item_info = ObjectProperty()
    cur_group = StringProperty()
    view_state = StringProperty()
    view_type = StringProperty()

    def on_press(self):
        # if (
        #     self.schedule_item_info is not None
        #     and self.view_state != ViewState.FILLED.value
        # ):
        #     # ak.start(
        #     #     App.get_running_app().controller.get_filling_variants(
        #     #         self,
        #     #         self.schedule_item_info.cell_pos,
        #     #         self.schedule_item_info.cell_part,
        #     #         self.schedule_item_info.view_type,
        #     #     )
        #     # )
        pass

    def get_minimum_width(self):
        if self.view_state != ViewState.INVISIBLE.value:
            self.texture_update()
            return self.texture.size[0] + 18
        else:
            return 0

    def set_width(self, width):
        self.size_hint_x = None
        self.size_hint_y = 1
        self.width = width

    def update_info(self, view_state: str):
        self.view_state = view_state
        if view_state == ViewState.FILLED.value:
            self.text = f"{self.schedule_item_info.subject_part.subject} a. {self.schedule_item_info.audience_part.number} {self.schedule_item_info.mentor_part.scientific_degree} {self.schedule_item_info.mentor_part.fio}"
            self.background_color = "green"  # add using config
        elif view_state == ViewState.UNAVAILABLE.value:
            """
            Make disabled=True, and add respective label
            """
        elif view_state == ViewState.EDITABLE.value:
            """
            Make disabled=False, and add respective label
            """
        elif view_state == ViewState.EMPTY.value:
            self.text = "ПУСТО"
        elif view_state == ViewState.INVISIBLE.value:
            self.text = ''
        else:
            raise

    async def get_filling_variants(self, variants: List[ScheduleItemInfo]):
        if len(variants) == 0:
            self.view_state = ViewState.UNAVAILABLE.value
        else:
            # ScheduleItemBtnDialog().open()
            pass
