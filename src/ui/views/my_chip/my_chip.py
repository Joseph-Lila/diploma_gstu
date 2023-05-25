from kivy.properties import ObjectProperty
from kivymd.uix.chip import MDChip


class MyChip(MDChip):
    icon_check_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 1)
    entity = ObjectProperty()
    _no_ripple_effect = True
    master = ObjectProperty()

    def __init__(self, entity, students_cnt_label, master, **kwargs):
        super().__init__(**kwargs)
        self.entity = entity
        self.students_cnt_label = students_cnt_label
        self.master = master
        self.bind(active=self.put_entity_to_parent)
        self.bind(active=self.change_students_cnt_label_value)

    def put_entity_to_parent(self, instance_chip, active_value: int):
        if self.master:
            if active_value:
                self.master.entity.append(self.entity)
            else:
                self.master.entity.remove(self.entity)

    def change_students_cnt_label_value(self, instance_chip, active_value: int):
        students_cnt = int(self.students_cnt_label.text)

        if active_value:
            students_cnt += self.entity.number_of_students
        else:
            students_cnt -= self.entity.number_of_students

        self.students_cnt_label.text = str(students_cnt)
