import asyncio
import functools
from dataclasses import astuple
from typing import Optional, List

from src import config
from src.adapters.orm import Schedule, LocalScheduleRecord
from src.domain.commands import (
    CreateSchedule,
    Get10Schedules,
    GetSchedules,
    GetUniqueTermsDependingOnSchedule,
    GetUniqueTermsDependingOnWorkload,
    GetUniqueYearsDependingOnSchedule,
    GetUniqueYearsDependingOnWorkload,
    GetUniqueMentors,
    GetUniqueGroups,
    DeleteSchedule,
    GetUniqueFaculties,
    GetUniqueGroupsDependingOnFaculty,
    GetUniqueDepartments,
    GetUniqueMentorsDependingOnDepartment,
    GetUniqueAudiencesDependingOnDepartment,
    GetUniqueSubjects,
    GetUniqueSubjectTypes,
    GetRowWorkloads,
    MakeGlobalScheduleRecordsLikeLocal,
    GetExtendedScheduleRecords,
    DeleteLocalScheduleRecords,
    CreateLocalScheduleRecord,
    GetMentorsForScheduleItem,
    CheckIfMentorNotOnOtherClassAndFree,
)
from src.domain.commands import GetWorkloads
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import WeekType, DayOfWeek, Subgroup
from src.domain.events import (
    GotSchedules,
    GotUniqueTerms,
    GotUniqueYears,
    ScheduleIsCreated,
    GotUniqueMentors,
    GotUniqueGroups,
    ScheduleIsDeleted,
    GotUniqueFaculties,
    GotUniqueAudiences,
    GotUniqueSubjects,
    GotUniqueSubjectTypes,
    GotRowWorkloads,
    GotExtendedScheduleRecords,
    GotWorkloads,
    GotMentorsEntities,
)
from src.domain.events.got_unique_departments import GotUniqueDepartments
from src.service_layer.handlers import convert_cell_part_to_hours
from src.ui.views.loading_modal_dialog import LoadingModalDialog


def do_with_loading_modal_view(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        loading_modal_view = LoadingModalDialog()
        loading_modal_view.open()
        await func(*args, **kwargs)
        loading_modal_view.dismiss()

    return wrapped


def use_loop(use_loading_modal_view=False):
    def _use_loop(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                if use_loading_modal_view:
                    loop.create_task(do_with_loading_modal_view(func)(*args, **kwargs))
                else:
                    loop.create_task(func(*args, **kwargs))

        return wrapped

    return _use_loop


class Controller:
    def __init__(self, model):
        self.model = model

    @use_loop(use_loading_modal_view=True)
    async def update_open_dialog_schedules(self, open_dialog, year, term):
        event: GotSchedules = await self.model.bus.handle_command(
            GetSchedules(
                year=year,
                term=term,
            )
        )
        await open_dialog.update_items(event.schedules)

    @use_loop(use_loading_modal_view=False)
    async def fill_years_selector_depending_on_workload(self, years_selector, term):
        event: GotUniqueYears = await self.model.bus.handle_command(
            GetUniqueYearsDependingOnWorkload(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop(use_loading_modal_view=False)
    async def fill_years_selector_depending_on_schedule(self, years_selector, term):
        event: GotUniqueYears = await self.model.bus.handle_command(
            GetUniqueYearsDependingOnSchedule(term=term)
        )
        await years_selector.update_variants([str(year) for year in event.years])

    @use_loop(use_loading_modal_view=False)
    async def fill_terms_selector_depending_on_workload(self, terms_selector, year):
        event: GotUniqueTerms = await self.model.bus.handle_command(
            GetUniqueTermsDependingOnWorkload(year=year)
        )
        await terms_selector.update_variants(event.terms)

    @use_loop(use_loading_modal_view=False)
    async def fill_terms_selector_depending_on_schedule(self, terms_selector, year):
        event: GotUniqueTerms = await self.model.bus.handle_command(
            GetUniqueTermsDependingOnSchedule(year=year)
        )
        await terms_selector.update_variants(event.terms)

    @use_loop(use_loading_modal_view=True)
    async def update_latest_10_schedules(self, home_screen):
        event: GotSchedules = await self.model.bus.handle_command(Get10Schedules())
        await home_screen.update_latest_10_schedules(event.schedules)

    @use_loop(use_loading_modal_view=True)
    async def try_to_create_schedule(self, create_dialog, year: int, term: str):
        event: ScheduleIsCreated = await self.model.bus.handle_command(
            CreateSchedule(year=year, term=term)
        )
        await create_dialog.check_if_new_schedule_is_created(event.schedule)

    @use_loop(use_loading_modal_view=True)
    async def delete_schedule(self):
        if self.model.schedule_master is None:
            return
        event: ScheduleIsDeleted = await self.model.bus.handle_command(
            DeleteSchedule(schedule_id=self.model.schedule_master.id)
        )
        return event.success

    @use_loop(use_loading_modal_view=False)
    async def fill_faculties_selector(self, faculties_selector, title_substring):
        event: GotUniqueFaculties = await self.model.bus.handle_command(
            GetUniqueFaculties(title_substring)
        )
        await faculties_selector.update_variants(event.faculties)

    @use_loop(use_loading_modal_view=False)
    async def fill_mentors_selector(self, mentors_selector, fio_substring):
        event: GotUniqueMentors = await self.model.bus.handle_command(
            GetUniqueMentors(fio_substring)
        )
        await mentors_selector.update_variants(event.mentors)

    @use_loop(use_loading_modal_view=False)
    async def fill_groups_selector(self, groups_selector, title_substring):
        event: GotUniqueGroups = await self.model.bus.handle_command(
            GetUniqueGroups(title_substring)
        )
        await groups_selector.update_variants(event.groups)

    @use_loop(use_loading_modal_view=False)
    async def fill_groups_selector_depending_on_faculty(
        self, groups_selector, title_substring, faculty: str
    ):
        event: GotUniqueGroups = await self.model.bus.handle_command(
            GetUniqueGroupsDependingOnFaculty(
                title_substring,
                faculty,
            )
        )
        await groups_selector.update_variants(event.groups)

    @use_loop(use_loading_modal_view=False)
    async def fill_departments_selector(self, departments_selector, title_substring):
        event: GotUniqueDepartments = await self.model.bus.handle_command(
            GetUniqueDepartments(title_substring)
        )
        await departments_selector.update_variants(event.departments)

    @use_loop(use_loading_modal_view=False)
    async def fill_subjects_selector(self, subjects_selector, title_substring):
        event: GotUniqueSubjects = await self.model.bus.handle_command(
            GetUniqueSubjects(title_substring)
        )
        await subjects_selector.update_variants(event.subjects)

    @use_loop(use_loading_modal_view=False)
    async def fill_subject_types_selector(
        self, subject_types_selector, title_substring
    ):
        event: GotUniqueSubjectTypes = await self.model.bus.handle_command(
            GetUniqueSubjectTypes(title_substring)
        )
        await subject_types_selector.update_variants(event.subject_types)

    @use_loop(use_loading_modal_view=False)
    async def fill_mentors_selector_depending_on_department(
        self, mentors_selector, title_substring, department: Optional[str]
    ):
        event: GotUniqueMentors = await self.model.bus.handle_command(
            GetUniqueMentorsDependingOnDepartment(
                title_substring,
                department,
            )
        )
        await mentors_selector.update_variants(event.mentors)

    @use_loop(use_loading_modal_view=False)
    async def fill_audiences_selector_depending_on_department(
        self, audiences_selector, number_substring, department: Optional[str]
    ):
        event: GotUniqueAudiences = await self.model.bus.handle_command(
            GetUniqueAudiencesDependingOnDepartment(
                number_substring,
                department,
            )
        )
        await audiences_selector.update_variants(event.audiences)

    @use_loop(use_loading_modal_view=True)
    async def get_workloads(
        self,
        sender,
        group_substring,
        subject_substring,
        subject_type_substring,
        mentor_substring,
        year,
        term,
    ):
        event: GotRowWorkloads = await self.model.bus.handle_command(
            GetRowWorkloads(
                group_substring,
                subject_substring,
                subject_type_substring,
                mentor_substring,
                year,
                term,
            )
        )
        await sender.update_data(event.data)

    @use_loop(use_loading_modal_view=True)
    async def update_schedule_view_groups(
        self,
        sender,
        faculty_substring,
        group_substring,
    ):
        event: GotUniqueGroups = await self.model.bus.handle_command(
            GetUniqueGroupsDependingOnFaculty(
                group_substring,
                faculty_substring,
            )
        )
        await sender.add_groups(event.groups)

    @use_loop(use_loading_modal_view=True)
    async def update_schedule_view_mentors(
        self,
        sender,
        mentor_fio_substring,
        department_substring,
    ):
        event: GotUniqueMentors = await self.model.bus.handle_command(
            GetUniqueMentorsDependingOnDepartment(
                mentor_fio_substring,
                department_substring,
            )
        )
        await sender.add_mentors(event.mentors)

    @use_loop(use_loading_modal_view=True)
    async def update_schedule_view_audiences(
        self,
        sender,
        audience_number_substring,
        department_substring,
    ):
        event: GotUniqueAudiences = await self.model.bus.handle_command(
            GetUniqueAudiencesDependingOnDepartment(
                audience_number_substring,
                department_substring,
            )
        )
        await sender.add_audiences(event.audiences)

    @use_loop(use_loading_modal_view=True)
    async def update_schedule_metadata(self, schedule: Schedule):
        self.model.create_schedule_master()
        await self.model.schedule_master.update_metadata(*astuple(schedule))
        await self.model.bus.handle_command(
            MakeGlobalScheduleRecordsLikeLocal(self.model.schedule_master.id)
        )
        event: GotWorkloads = await self.model.bus.handle_command(
            GetWorkloads(
                self.model.schedule_master.year,
                self.model.schedule_master.term,
            )
        )
        await self.model.schedule_master.set_workloads(event.data)

    @use_loop(use_loading_modal_view=True)
    async def get_actual_schedule_info_records(
        self,
        sender,
    ):
        event: GotExtendedScheduleRecords = await self.model.bus.handle_command(
            GetExtendedScheduleRecords(self.model.schedule_master.id)
        )
        await self.model.schedule_master.fit_workloads_using_info_records(event.records)
        await sender.refresh_cells(event.records)

    @use_loop(use_loading_modal_view=True)
    async def delete_local_schedule_records(
        self,
        ids: List[int],
        schedule_screen_view,
    ):
        await self.model.bus.handle_command(DeleteLocalScheduleRecords(ids=ids))
        event: GotExtendedScheduleRecords = await self.model.bus.handle_command(
            GetExtendedScheduleRecords(self.model.schedule_master.id)
        )
        await self.model.schedule_master.fit_workloads_using_info_records(event.records)
        await schedule_screen_view.refresh_cells(event.records)

    @use_loop(use_loading_modal_view=True)
    async def add_local_schedule_records(
        self,
        record: ScheduleItemInfo,
    ):
        local_records = []
        for i, group in enumerate(record.groups_part):
            local_records.append(
                LocalScheduleRecord(
                    schedule_id=self.model.schedule_master.id,
                    day_of_week=record.cell_pos.day_of_week,
                    pair_number=record.cell_pos.pair_number,
                    subject_id=record.subject_part.subject_id,
                    subject_type_id=record.subject_part.subject_type_id,
                    mentor_id=record.mentor_part.mentor_id,
                    audience_id=record.audience_part.audience_id,
                    group_id=group.group_id,
                    week_type=record.cell_part.week_type,
                    subgroup=record.cell_part.subgroup,
                    mentor_free=True,
                )
            )
        for record in local_records:
            await self.model.bus.handle_command(CreateLocalScheduleRecord(record))

    @use_loop(use_loading_modal_view=False)
    async def fill_week_type_selector(
        self,
        selector,
    ):
        await selector.update_variants([r.value for r in WeekType])

    @use_loop(use_loading_modal_view=False)
    async def fill_subgroup_selector(
        self,
        selector,
    ):
        await selector.update_variants([r.value for r in Subgroup])

    @use_loop(use_loading_modal_view=False)
    async def fill_mentors_selector_for_schedule_item(
        self,
        selector,
        old_info_record: ScheduleItemInfo,
        info_record: ScheduleItemInfo,
    ):
        if old_info_record is not None and old_info_record.cell_part is not None:
            old_hours = await convert_cell_part_to_hours(old_info_record.cell_part)
        else:
            old_hours = 0
        # check that hours are good for all the groups and groups fit in audience
        if len(info_record.groups_part) > 0:
            for group in info_record.groups_part:
                for workload in self.model.schedule_master.actual_workloads:
                    hours = await convert_cell_part_to_hours(info_record.cell_part)
                    if (
                        all(
                            [
                                group.group_id == workload.group_id,
                                info_record.subject_part.subject_id
                                == workload.subject_id,
                                info_record.subject_part.subject_type_id
                                == workload.subject_type_id,
                            ]
                        )
                        and hours < workload.hours + old_hours
                    ):
                        await selector.update_variants([])
                        return

            # check if all the groups will fit in the provided audience
            if (
                sum([group.number_of_students for group in info_record.groups_part])
                > info_record.audience_part.total_seats
            ):
                await selector.update_variants([])
                return
        event: GotMentorsEntities = await self.model.bus.handle_command(
            GetMentorsForScheduleItem(
                info_record,
            )
        )
        # we grab only mentors who are in actual_workloads or old_info
        actual_mentor_ids = [
            r.mentor_id for r in self.model.schedule_master.actual_workloads
        ]
        existing_id = (
            [old_info_record.mentor_part.mentor_id]
            if old_info_record.mentor_part is not None
            else []
        )
        mentors = [
            mentor
            for mentor in event.mentors
            if mentor.mentor_id in actual_mentor_ids + existing_id
        ]
        conclusions = []
        for i in range(len(mentors)):
            # check that mentor is really free
            conclusion: bool = await self.model.bus.handle_command(
                CheckIfMentorNotOnOtherClassAndFree(
                    mentors[i].mentor_id,
                    info_record.cell_pos.day_of_week,
                    info_record.cell_pos.pair_number,
                    info_record.cell_part.week_type,
                    info_record.cell_part.subgroup,
                    info_record.subject_part.subject_id
                    if info_record.subject_part
                    else -1,
                    info_record.subject_part.subject_type_id
                    if info_record.subject_part
                    else -1,
                )
            )
            conclusions.append(conclusion)
        mentors_to_remove = [
            mentor for i, mentor in enumerate(mentors) if not conclusions[i]
        ]
        for mentor in mentors_to_remove:
            mentors.remove(mentor)
        await selector.update_entities(mentors, "fio")
