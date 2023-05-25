from typing import Optional, List

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
import asynckivy as ak

from src.domain.entities import CellPos, CellPart, AudiencePart, GroupPart, MentorPart, SubjectPart, AdditionalPart
from src.domain.entities.schedule_item_info import ScheduleItemInfo


class ScheduleItemDialog(MDCard, ModalView):
    day_of_week_hint = 'Выберите день недели'
    pair_number_hint = 'Выберите номер пары'
    week_type_hint = 'Выберите тип недели'
    subgroup_hint = 'Выберите подгруппу'
    mentor_hint = 'Выберите преподавателя'
    audience_number_hint = 'Выберите аудиторию'
    subject_hint = 'Выберите предмет'
    subject_type_hint = 'Выберите тип предмета'

    def __init__(self, touched_slave, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.given_info_record = None
        self.touched_slave = touched_slave

        self.set_info_record()

    def on_kv_post(self, base_widget):
        self.ids.groups_cont.entity = []
        self.ids.mentor_free.entity = AdditionalPart(
            mentor_free=self.ids.mentor_free.active,
            schedule_record_ids=[]
        )

    def get_cur_info(self):
        return ScheduleItemInfo(
            cell_pos=CellPos(
                day_of_week=self.ids.day_of_week.text,
                pair_number=int(self.ids.pair_number.text),
            ),
            cell_part=CellPart(
                week_type=self.ids.week_type.text,
                subgroup=self.ids.subgroup.text,
            ),
            audience_part=self.ids.audience_number.entity,
            groups_part=self.ids.groups_cont.entity,
            mentor_part=self.ids.mentor.entity,
            subject_part=SubjectPart(
                subject_id=self.ids.subject.entity.subject_id,
                subject=self.ids.subject.entity.subject,
                subject_type_id=self.ids.subject_type.entity.subject_type_id,
                subject_type=self.ids.subject_type.entity.subject_type,
            ) if self.ids.subject.entity and self.ids.subject_type.entity
            else None,
            additional_part=self.ids.mentor_free.entity,
        )

    def generate_info_record(self):
        if all([
            self.ids.day_of_week.text,
            self.ids.pair_number.text,
            self.ids.week_type.text,
            self.ids.subgroup.text,
            self.ids.mentor.text,
            not self.ids.mentor_free.active,
        ]):
            day_of_week = self.ids.day_of_week.text
            pair_number = self.ids.pair_number.text
            week_type = self.ids.week_type.text
            subgroup = self.ids.subgroup.text
            mentor_part: MentorPart = self.ids.mentor.entity
            additional_part: AdditionalPart = self.ids.mentor_free.entity
            return ScheduleItemInfo(
                cell_pos=CellPos(
                    day_of_week=day_of_week,
                    pair_number=pair_number,
                ),
                cell_part=CellPart(
                    week_type=week_type,
                    subgroup=subgroup,
                ),
                mentor_part=mentor_part,
                additional_part=additional_part,
            )
        elif all([
            self.ids.day_of_week.text,
            self.ids.pair_number.text,
            self.ids.week_type.text,
            self.ids.subgroup.text,
            self.ids.mentor.text,
            self.ids.audience_number.text,
            len(self.ids.groups_cont.children) > 0,
            self.ids.subject.text,
            self.ids.subject_type.text,
            self.ids.mentor_free.active,
        ]):
            day_of_week = self.ids.day_of_week.text
            pair_number = self.ids.pair_number.text
            week_type = self.ids.week_type.text
            subgroup = self.ids.subgroup.text
            audience_part: Optional[AudiencePart] = self.ids.audience_number.entity
            groups_part: List[GroupPart] = self.ids.groups_cont.entity
            mentor_part: MentorPart = self.ids.mentor.entity
            subject_part: SubjectPart = SubjectPart(
                subject_id=self.ids.subject.entity.subject_id,
                subject=self.ids.subject.entity.subject,
                subject_type_id=self.ids.subject_type.entity.subject_type_id,
                subject_type=self.ids.subject_type.entity.subject_type,
            )
            additional_part: AdditionalPart = self.ids.mentor_free.entity
            return ScheduleItemInfo(
                cell_pos=CellPos(
                    day_of_week=day_of_week,
                    pair_number=pair_number,
                ),
                cell_part=CellPart(
                    week_type=week_type,
                    subgroup=subgroup,
                ),
                audience_part=audience_part,
                groups_part=groups_part,
                mentor_part=mentor_part,
                subject_part=subject_part,
                additional_part=additional_part,
            )
        else:
            raise AttributeError

    def set_info_record(self):
        if self.touched_slave.schedule_item_info is not None:
            self.given_info_record: ScheduleItemInfo = self.touched_slave.schedule_item_info

            # init required fields
            self.ids.week_type.change_text_value(self.touched_slave.schedule_item_info.cell_part.week_type)
            self.ids.subgroup.change_text_value(self.touched_slave.schedule_item_info.cell_part.subgroup)
            self.ids.day_of_week.change_text_value(self.touched_slave.schedule_item_info.cell_pos.day_of_week)
            self.ids.pair_number.change_text_value(str(self.touched_slave.schedule_item_info.cell_pos.pair_number))
        else:
            raise ValueError

    def send_command_to_get_day_of_week_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_day_of_week_selector(
                self.ids.day_of_week
            )
        )

    def send_command_to_get_pair_number_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_pair_number_selector(
                self.ids.pair_number
            )
        )

    def send_command_to_get_week_type_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_week_type_selector(
                self.ids.week_type
            )
        )

    def send_command_to_subgroup_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_subgroup_selector(
                self.ids.subgroup
            )
        )

    def send_command_to_get_mentor_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_mentors_selector_for_schedule_item(
                self.ids.mentor,
                self.given_info_record,
                self.get_cur_info(),
            )
        )

    def send_command_to_get_audience_number_values(self, *args):
        pass

    def send_command_to_get_subject_values(self, *args):
        pass

    def send_command_to_get_subject_type_values(self, *args):
        pass

    def on_save(self, *args):
        # delete existing
        # create new
        # update view
        # close dialog
        pass

    def on_clear(self, *args):
        # delete existing
        # update view
        # close dialog
        pass
