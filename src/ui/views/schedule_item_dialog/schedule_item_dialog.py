from typing import Optional, List

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
import asynckivy as ak

from src.domain.entities import (
    CellPos,
    CellPart,
    AudiencePart,
    GroupPart,
    MentorPart,
    SubjectPart,
    AdditionalPart,
)
from src.domain.entities.schedule_item_info import ScheduleItemInfo


class ScheduleItemDialog(MDCard, ModalView):
    week_type_hint = "Выберите тип недели"
    subgroup_hint = "Выберите подгруппу"
    mentor_hint = "Выберите преподавателя"
    audience_number_hint = "Выберите аудиторию"
    subject_hint = "Выберите предмет"
    subject_type_hint = "Выберите тип предмета"

    def __init__(self, touched_slave, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.given_info_record = None
        self.touched_slave = touched_slave

        self.set_info_record()

    def on_kv_post(self, base_widget):
        self.ids.groups_cont.entity = []
        self.ids.mentor_free.entity = AdditionalPart(
            mentor_free=self.ids.mentor_free.active, schedule_record_ids=[]
        )
        self.ids.subject.entity = SubjectPart(
            subject_id=-1,
            subject="",
            subject_type_id=-1,
            subject_type="",
        )
        self.ids.subject_type.entity = SubjectPart(
            subject_id=-1,
            subject="",
            subject_type_id=-1,
            subject_type="",
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
            )
            if self.ids.subject.entity and self.ids.subject_type.entity
            else None,
            additional_part=self.ids.mentor_free.entity,
        )

    def generate_info_record(self):
        if all(
            [
                self.ids.day_of_week.text,
                self.ids.pair_number.text,
                self.ids.week_type.text,
                self.ids.subgroup.text,
                self.ids.mentor.text,
                not self.ids.mentor_free.active,
            ]
        ):
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
        elif all(
            [
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
            ]
        ):
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
            self.given_info_record: ScheduleItemInfo = (
                self.touched_slave.schedule_item_info
            )

            # tune clear btn
            self.ids.clear_button.disabled = not (
                    self.given_info_record.additional_part is not None
                    and len(self.given_info_record.additional_part.schedule_record_ids) > 0
            )

            # init required fields
            self.ids.week_type.change_text_value(
                self.touched_slave.schedule_item_info.cell_part.week_type
            )
            self.ids.subgroup.change_text_value(
                self.touched_slave.schedule_item_info.cell_part.subgroup
            )
            self.ids.day_of_week.text = (
                self.touched_slave.schedule_item_info.cell_pos.day_of_week
            )
            self.ids.pair_number.text = str(
                self.touched_slave.schedule_item_info.cell_pos.pair_number
            )

            # init additional fields
            self.ids.audience_number.entity = self.given_info_record.audience_part
            if self.given_info_record.audience_part:
                self.ids.total_seats.text = "/" + str(
                    self.given_info_record.audience_part.total_seats
                )
                self.ids.audience_number.change_text_value(
                    self.given_info_record.audience_part.number
                )
            else:
                self.ids.total_seats.text = "?"

            self.ids.groups_cont.entity = self.given_info_record.groups_part
            self.ids.actual_students.text = str(
                sum(
                    [0]
                    + [r.number_of_students for r in self.given_info_record.groups_part]
                )
            )
            # TODO: add widgets under it

            self.ids.mentor.entity = self.given_info_record.mentor_part
            if self.given_info_record.mentor_part:
                self.ids.mentor.change_text_value(
                    self.given_info_record.mentor_part.fio
                )

            if self.given_info_record.subject_part:
                self.ids.subject.entity.subject_id = (
                    self.given_info_record.subject_part.subject_id
                )
                self.ids.subject.entity.subject = (
                    self.given_info_record.subject_part.subject
                )
                self.ids.subject.change_text_value(
                    self.given_info_record.subject_part.subject
                )

                self.ids.subject_type.entity.subject_type_id = (
                    self.given_info_record.subject_part.subject_type_id
                )
                self.ids.subject_type.entity.subject_type = (
                    self.given_info_record.subject_part.subject_type
                )
                self.ids.subject_type.change_text_value(
                    self.given_info_record.subject_part.subject_type
                )
            self.ids.mentor_free.entity = self.given_info_record.additional_part
            if self.given_info_record.additional_part:
                self.ids.mentor_free.active = (
                    self.given_info_record.additional_part.mentor_free
                )
        else:
            raise ValueError

    def send_command_to_get_week_type_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_week_type_selector(self.ids.week_type)
        )

    def send_command_to_subgroup_values(self, *args):
        ak.start(
            App.get_running_app().controller.fill_subgroup_selector(self.ids.subgroup)
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
        ak.start(
            App.get_running_app().controller.delete_local_schedule_records(
                self.given_info_record.additional_part.schedule_record_ids,
                App.get_running_app().root.get_current_screen_view(),
            )
        )
        self.dismiss()
