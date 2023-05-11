from typing import List
import asynckivy as ak
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState
from src.domain.interfaces import AbstractSizeSlave


class ScheduleItemBtn(Button, AbstractSizeSlave):
    schedule_item_info = ObjectProperty()
    cur_group = StringProperty()

    def on_press(self):
        if self.schedule_item_info is not None and self.schedule_item_info.view_state != ViewState.FILLED.value:
            ak.start(
                App.get_running_app().controller.get_filling_variants(
                    self,
                    self.schedule_item_info.cell_pos,
                    self.schedule_item_info.cell_part,
                    self.schedule_item_info.view_type,
                )
            )

    def get_minimum_width(self):
        self.texture_update()
        return self.texture.size[0] + 18

    def update_info(self, view_state: str, info: ScheduleItemInfo = None):
        if view_state == ViewState.FILLED.value:
            self.schedule_item_info = info
            self.text = f"{info.subject_part.subject} a. {info.audience_part.number} {info.mentor_part.scientific_degree} {info.mentor_part.fio}"
            self.background_color = 'green'  # add using config
        elif view_state == ViewState.UNAVAILABLE.value:
            """
            Make disabled=True, and add respective label
            """
        elif view_state == ViewState.EDITABLE.value:
            """
            Make disabled=False, and add respective label
            """
        elif view_state == ViewState.EMPTY.value:
            self.text = 'ПУСТО'
        elif view_state == ViewState.INVINCIBLE.value:
            """
            Make invincible
            """
        else:
            raise

    async def get_filling_variants(self, variants: List[ScheduleItemInfo]):
        if len(variants) == 0:
            self.schedule_item_info.view_state = ViewState.UNAVAILABLE.value
        else:
            # ScheduleItemBtnDialog().open()
            pass
