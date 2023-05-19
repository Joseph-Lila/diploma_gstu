from typing import List
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState, SubjectColor, SubjectType
from src.domain.interfaces import AbstractSizeSlave


class ScheduleItemBtn(Button, AbstractSizeSlave):
    schedule_item_info = ObjectProperty()
    cur_group = StringProperty()
    view_state = StringProperty()
    view_type = StringProperty()

    def get_minimum_width(self):
        if self.view_state != ViewState.INVISIBLE.value:
            self.texture_update()
            return self.texture.size[0] + 18
        else:
            return 0

    def set_width(self, width):
        self.size_hint_x = 1
        tmp_width = self.width

        self.size_hint_x = None
        self.size_hint_y = 1
        self.width = max(tmp_width, width)

    def set_invisible_width(self):
        self.size_hint = None, None
        self.size = (0, 0)
        self.opacity = 0

    def update_info(self, view_state: str):
        self.view_state = view_state

        if view_state == ViewState.FILLED.value:
            self.disabled = False
            self.text = f"{self.schedule_item_info.subject_part.subject} a. {self.schedule_item_info.audience_part.number} {self.schedule_item_info.mentor_part.scientific_degree} {self.schedule_item_info.mentor_part.fio}"

            if self.schedule_item_info.subject_part.subject_type == SubjectType.LECTURE.value:
                self.background_color = SubjectColor.LECTURE.value
            elif self.schedule_item_info.subject_part.subject_type == SubjectType.LAB.value:
                self.background_color = SubjectColor.LAB.value
            elif self.schedule_item_info.subject_part.subject_type == SubjectType.PRACTISE.value:
                self.background_color = SubjectColor.PRACTISE.value
            else:
                raise ValueError

        elif view_state == ViewState.UNAVAILABLE.value:
            self.disabled = True
            self.text = "Недоступно"
        elif view_state == ViewState.EDITABLE.value:
            self.disabled = False
            self.text = "Редактировать"
            self.background_color = SubjectColor.EDITABLE.value
        # TODO: DELETE THIS!!!
        elif view_state == ViewState.EMPTY.value:
            self.disabled = True
            self.text = "ПУСТО"
            self.background_color = 'grey'
        elif view_state == ViewState.INVISIBLE.value:
            self.disabled = True
            self.text = ""
        else:
            raise

    async def get_filling_variants(self, variants: List[ScheduleItemInfo]):
        if len(variants) == 0:
            self.view_state = ViewState.UNAVAILABLE.value
        else:
            # ScheduleItemBtnDialog().open()
            pass
