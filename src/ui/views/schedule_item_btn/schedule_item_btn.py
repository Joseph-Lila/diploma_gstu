from typing import List, Optional
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button

from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import ViewState, SubjectColor, SubjectType, ViewType
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
        self.size_hint_x = None
        self.size_hint_y = 1
        self.width = width

    def set_invisible_width(self):
        self.size_hint = None, None
        self.size = (0, 0)
        self.opacity = 0

    def update_info(self, view_state: str, view_type: Optional[str] = None):
        self.view_state = view_state
        if view_type is not None:
            self.view_type = view_type

        if view_state == ViewState.FILLED.value:
            self.disabled = False

            if self.view_type == ViewType.MENTOR.value:
                self.text = "{subject} a. {audience_number} гр. {groups}".format(
                    subject=self.schedule_item_info.subject_part.subject,
                    audience_number=self.schedule_item_info.audience_part.number,
                    groups=", ".join(
                        [group.title for group in self.schedule_item_info.groups_part]
                    ),
                )
            elif self.view_type == ViewType.AUDIENCE.value:
                self.text = "{subject} {scientific_degree} {mentor} гр. {groups}".format(
                    subject=self.schedule_item_info.subject_part.subject,
                    scientific_degree=self.schedule_item_info.mentor_part.scientific_degree,
                    mentor=self.schedule_item_info.mentor_part.fio,
                    groups=", ".join(
                        [group.title for group in self.schedule_item_info.groups_part]
                    ),
                )
            elif self.view_type == ViewType.GROUP.value:
                self.text = "{subject} a. {audience_number} {scientific_degree} {mentor}".format(
                    subject=self.schedule_item_info.subject_part.subject,
                    audience_number=self.schedule_item_info.audience_part.number,
                    scientific_degree=self.schedule_item_info.mentor_part.scientific_degree,
                    mentor=self.schedule_item_info.mentor_part.fio,
                )
            else:
                raise ValueError

            if (
                self.schedule_item_info.subject_part.subject_type
                == SubjectType.LECTURE.value
            ):
                self.background_color = SubjectColor.LECTURE.value
            elif (
                self.schedule_item_info.subject_part.subject_type
                == SubjectType.LAB.value
            ):
                self.background_color = SubjectColor.LAB.value
            elif (
                self.schedule_item_info.subject_part.subject_type
                == SubjectType.PRACTISE.value
            ):
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
            self.background_color = "grey"
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
