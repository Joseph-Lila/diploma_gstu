import math

from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty
from kivymd.uix.chip import MDChip
from kivymd.uix.snackbar import Snackbar

from src.domain.enums import Subgroup


class MyChip(MDChip):
    icon_check_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 1)
    entity = ObjectProperty()
    _no_ripple_effect = True
    master = ObjectProperty()

    def __init__(
        self,
        entity,
        students_cnt_label,
        audience_widget,
        subgroup_widget,
        master,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.entity = entity
        self.students_cnt_label = students_cnt_label
        self.audience_widget = audience_widget
        self.subgroup_widget = subgroup_widget
        self.master = master
        self.bind(active=self.active_event)

    def active_event(self, instance_chip, active_value: int):
        self.put_entity_to_parent(active_value)
        self.change_students_cnt_label_value(active_value)

        if (
            self.students_cnt_label.text.isnumeric()
            and self.audience_widget.text.isnumeric()
            and int(self.students_cnt_label.text) > int(self.audience_widget.text)
        ):
            self.active = False
            Snackbar(
                text="Недостаточно свободных мест в аудитории!",
                snackbar_animation_dir="Right",
                bg_color="pink",
                font_size=sp(18),
            ).open()

    def put_entity_to_parent(self, active_value: int):
        if self.master:
            if active_value:
                self.master.entity.append(self.entity)
            else:
                self.master.entity.remove(self.entity)

    def change_students_cnt_label_value(self, active_value: int):
        students_cnt = int(self.students_cnt_label.text)

        # depending on subgroup type we have different students quantity
        if self.subgroup_widget.text in [Subgroup.FIRST.value, Subgroup.SECOND.value]:
            number_of_students = math.ceil(self.entity.number_of_students / 2)
        else:
            number_of_students = self.entity.number_of_students

        if active_value:
            students_cnt += number_of_students
        else:
            students_cnt -= number_of_students

        self.students_cnt_label.text = str(students_cnt)
