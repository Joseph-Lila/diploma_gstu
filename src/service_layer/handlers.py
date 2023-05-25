from typing import Callable, Dict, List, Type, Tuple

from src.adapters.orm import Schedule, Workload
from src.adapters.repositories.abstract_repository import AbstractRepository
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
    GetUniqueSubjectTypes,
    GetUniqueSubjects,
    GetRowWorkloads,
    GetExtendedScheduleRecords,
    MakeGlobalScheduleRecordsLikeLocal,
    MakeLocalScheduleRecordsLikeGlobal,
    DeleteLocalScheduleRecords, CreateLocalScheduleRecord, GetMentorsForScheduleItem,
    CheckIfMentorNotOnOtherClassAndFree,
)
from src.domain.commands.command import Command
from src.domain.commands import GetWorkloads
from src.domain.entities import CellPart
from src.domain.entities.mentor_part import parse_row_data_to_mentor_part
from src.domain.entities.schedule_item_info import (
    build_schedule_item_info_from_raw_data,
)
from src.domain.enums import Subgroup, WeekType
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
    GotUniqueSubjectTypes,
    GotUniqueSubjects,
    GotRowWorkloads,
    GotExtendedScheduleRecords, GotWorkloads, GotMentorsEntities,
)
from src.domain.events.got_unique_departments import GotUniqueDepartments


async def get_schedules(
    cmd: GetSchedules,
    repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_schedules(
        year=cmd.year, term=cmd.term
    )
    return GotSchedules(schedules)


def convert_pos_into_pos_hint(window_pos: tuple, pos: tuple) -> dict:
    window_x, window_y = window_pos
    x, y = pos
    return {
        "x": x / window_x,
        "y": y / window_y,
    }


async def convert_cell_part_to_hours(cell_part: CellPart):
    # define first coefficient
    if cell_part.subgroup == Subgroup.BOTH.value:
        a = 1
    elif cell_part.subgroup in [Subgroup.FIRST.value, Subgroup.SECOND.value]:
        a = .5
    else:
        raise ValueError

    # define second coefficient
    if cell_part.week_type == WeekType.BOTH.value:
        b = 1
    elif cell_part.week_type in [WeekType.UNDER.value, WeekType.ABOVE.value]:
        b = .5
    else:
        raise ValueError

    # by default one cell == 2 hours per week
    return 2 * a * b


async def get_10_schedules(
    cmd: Get10Schedules,
    repository: AbstractRepository,
) -> GotSchedules:
    schedules: List[Schedule] = await repository.get_10_schedules()
    return GotSchedules(schedules)


async def get_unique_years_depending_on_workload(
    cmd: GetUniqueYearsDependingOnWorkload,
    repository: AbstractRepository,
) -> GotUniqueYears:
    years: List[int] = await repository.get_unique_years_depending_on_workload(
        term=cmd.term
    )
    return GotUniqueYears(years)


async def get_unique_years_depending_on_schedule(
    cmd: GetUniqueYearsDependingOnSchedule,
    repository: AbstractRepository,
) -> GotUniqueYears:
    years: List[int] = await repository.get_unique_years_depending_on_schedule(
        term=cmd.term
    )
    return GotUniqueYears(years)


async def get_unique_terms_depending_on_workload(
    cmd: GetUniqueTermsDependingOnWorkload,
    repository: AbstractRepository,
) -> GotUniqueTerms:
    term: List[int] = await repository.get_unique_terms_depending_on_workload(
        year=cmd.year
    )
    return GotUniqueTerms(term)


async def get_unique_terms_depending_on_schedule(
    cmd: GetUniqueTermsDependingOnSchedule,
    repository: AbstractRepository,
) -> GotUniqueTerms:
    term: List[int] = await repository.get_unique_terms_depending_on_schedule(
        year=cmd.year
    )
    return GotUniqueTerms(term)


async def create_schedule(
    cmd: CreateSchedule,
    repository: AbstractRepository,
) -> ScheduleIsCreated:
    schedule = await repository.get_schedule_by_year_and_term(
        year=cmd.year,
        term=cmd.term,
    )
    if schedule is None:
        schedule = await repository.create_schedule(
            year=cmd.year,
            term=cmd.term,
        )
        return ScheduleIsCreated(schedule)
    else:
        return ScheduleIsCreated(None)


async def create_local_schedule_record(
    cmd: CreateLocalScheduleRecord,
    repository: AbstractRepository,
):
    await repository.create_local_schedule_record(
        schedule_id=cmd.record.schedule_id,
        day_of_week=cmd.record.day_of_week,
        pair_number=cmd.record.pair_number,
        subject_id=cmd.record.subject_id,
        subject_type_id=cmd.record.subject_type_id,
        mentor_id=cmd.record.mentor_id,
        audience_id=cmd.record.audience_id,
        group_id=cmd.record.group_id,
        week_type=cmd.record.week_type,
        subgroup=cmd.record.subgroup,
        mentor_free=cmd.record.mentor_free,
    )


async def delete_schedule(
    cmd: DeleteSchedule,
    repository: AbstractRepository,
) -> ScheduleIsDeleted:
    await repository.delete_schedule(
        id_=cmd.schedule_id,
    )
    return ScheduleIsDeleted(True)


async def get_unique_mentors(
    cmd: GetUniqueMentors,
    repository: AbstractRepository,
) -> GotUniqueMentors:
    mentors_fios: List[str] = await repository.get_unique_mentors_fios(
        cmd.fio_substring
    )
    return GotUniqueMentors(mentors_fios)


async def get_unique_groups(
    cmd: GetUniqueGroups,
    repository: AbstractRepository,
) -> GotUniqueGroups:
    groups_titles: List[str] = await repository.get_unique_groups_titles(
        cmd.title_substring
    )
    return GotUniqueGroups(groups_titles)


async def get_unique_groups_depending_on_faculty(
    cmd: GetUniqueGroupsDependingOnFaculty,
    repository: AbstractRepository,
) -> GotUniqueGroups:
    groups_titles: List[
        str
    ] = await repository.get_unique_groups_titles_depending_on_faculty(
        cmd.title_substring,
        cmd.faculty,
    )
    return GotUniqueGroups(groups_titles)


async def get_unique_faculties(
    cmd: GetUniqueFaculties,
    repository: AbstractRepository,
) -> GotUniqueFaculties:
    faculties_titles: List[str] = await repository.get_unique_faculties_titles(
        cmd.title_substring
    )
    return GotUniqueFaculties(faculties_titles)


async def get_unique_departments(
    cmd: GetUniqueDepartments,
    repository: AbstractRepository,
) -> GotUniqueDepartments:
    departments_titles: List[str] = await repository.get_unique_departments_titles(
        cmd.title_substring
    )
    return GotUniqueDepartments(departments_titles)


async def get_unique_subjects(
    cmd: GetUniqueSubjects,
    repository: AbstractRepository,
) -> GotUniqueSubjects:
    subjects_titles: List[str] = await repository.get_unique_subjects_titles(
        cmd.title_substring
    )
    return GotUniqueSubjects(subjects_titles)


async def get_unique_subject_types(
    cmd: GetUniqueSubjectTypes,
    repository: AbstractRepository,
) -> GotUniqueSubjectTypes:
    subject_types_titles: List[str] = await repository.get_unique_subject_types_titles(
        cmd.title_substring
    )
    return GotUniqueSubjectTypes(subject_types_titles)


async def get_unique_mentors_depending_on_department(
    cmd: GetUniqueMentorsDependingOnDepartment,
    repository: AbstractRepository,
) -> GotUniqueMentors:
    mentors_titles: List[
        str
    ] = await repository.get_unique_mentors_fios_depending_on_department(
        cmd.fio_substring,
        cmd.department,
    )
    return GotUniqueMentors(mentors_titles)


async def get_unique_audiences_depending_on_department(
    cmd: GetUniqueAudiencesDependingOnDepartment,
    repository: AbstractRepository,
) -> GotUniqueAudiences:
    audiences_numbers: List[
        str
    ] = await repository.get_unique_audiences_numbers_depending_on_department(
        cmd.number_substring,
        cmd.department,
    )
    return GotUniqueAudiences(audiences_numbers)


async def get_row_workloads(
    cmd: GetRowWorkloads,
    repository: AbstractRepository,
) -> GotRowWorkloads:
    data: List[tuple] = await repository.get_row_workloads(
        cmd.group_substring,
        cmd.subject_substring,
        cmd.subject_type_substring,
        cmd.mentor_substring,
        cmd.year,
        cmd.term,
    )
    return GotRowWorkloads(data)


async def get_workloads(
    cmd: GetWorkloads,
    repository: AbstractRepository,
) -> GotWorkloads:
    workloads: List[Workload] = await repository.get_workloads(
        cmd.year,
        cmd.term,
    )
    return GotWorkloads(workloads)


async def get_extended_schedule_records(
    cmd: GetExtendedScheduleRecords,
    repository: AbstractRepository,
) -> GotExtendedScheduleRecords:
    data: Tuple[tuple] = await repository.get_extended_local_schedule_records(
        cmd.schedule_id,
    )
    records = {}
    for item in data:
        record = build_schedule_item_info_from_raw_data(*item)
        if (
            record.cell_pos,
            record.cell_part,
            record.audience_part,
            record.mentor_part,
        ) in records:
            records[
                (
                    record.cell_pos,
                    record.cell_part,
                    record.audience_part,
                    record.mentor_part,
                )
            ].groups_part.extend(record.groups_part)
            records[
                (
                    record.cell_pos,
                    record.cell_part,
                    record.audience_part,
                    record.mentor_part,
                )
            ].additional_part.schedule_record_ids.extend(
                record.additional_part.schedule_record_ids
            )
        else:
            records[
                (
                    record.cell_pos,
                    record.cell_part,
                    record.audience_part,
                    record.mentor_part,
                )
            ] = record
    return GotExtendedScheduleRecords(list(records.values()))


async def make_local_schedule_records_like_global(
    cmd: MakeLocalScheduleRecordsLikeGlobal,
    repository: AbstractRepository,
):
    await repository.make_local_schedule_records_like_global(cmd.schedule_id)


async def make_global_schedule_records_like_local(
    cmd: MakeGlobalScheduleRecordsLikeLocal,
    repository: AbstractRepository,
):
    await repository.make_global_schedule_records_like_local(cmd.schedule_id)


async def delete_local_schedule_records(
    cmd: DeleteLocalScheduleRecords,
    repository: AbstractRepository,
):
    for id_ in cmd.ids:
        await repository.clear_local_schedule_record(id_=id_)


async def get_mentors_for_schedule_item(
    cmd: GetMentorsForScheduleItem,
    repository: AbstractRepository,
) -> GotMentorsEntities:
    mentor_records = await repository.get_mentors_for_schedule_item(
        info_record=cmd.info_record
    )
    mentors = [parse_row_data_to_mentor_part(r) for r in mentor_records]
    return GotMentorsEntities(mentors)


async def check_if_mentor_not_on_other_class_and_free(
    cmd: CheckIfMentorNotOnOtherClassAndFree,
    repository: AbstractRepository,
) -> bool:
    conclusion: bool = await repository.get_free_mentors_at_the_moment(
        cmd.mentor_id,
        cmd.day_of_week,
        cmd.pair_number,
        cmd.week_type,
        cmd.subgroup,
        cmd.subject_id,
        cmd.subject_type_id,
    )
    return conclusion


COMMAND_HANDLERS = {
    CheckIfMentorNotOnOtherClassAndFree: check_if_mentor_not_on_other_class_and_free,
    DeleteLocalScheduleRecords: delete_local_schedule_records,
    MakeLocalScheduleRecordsLikeGlobal: make_local_schedule_records_like_global,
    MakeGlobalScheduleRecordsLikeLocal: make_global_schedule_records_like_local,
    GetSchedules: get_schedules,
    GetExtendedScheduleRecords: get_extended_schedule_records,
    GetUniqueYearsDependingOnWorkload: get_unique_years_depending_on_workload,
    GetUniqueYearsDependingOnSchedule: get_unique_years_depending_on_schedule,
    GetUniqueTermsDependingOnWorkload: get_unique_terms_depending_on_workload,
    GetUniqueTermsDependingOnSchedule: get_unique_terms_depending_on_schedule,
    Get10Schedules: get_10_schedules,
    CreateSchedule: create_schedule,
    CreateLocalScheduleRecord: create_local_schedule_record,
    DeleteSchedule: delete_schedule,
    GetUniqueMentors: get_unique_mentors,
    GetUniqueGroups: get_unique_groups,
    GetUniqueGroupsDependingOnFaculty: get_unique_groups_depending_on_faculty,
    GetUniqueFaculties: get_unique_faculties,
    GetUniqueDepartments: get_unique_departments,
    GetUniqueMentorsDependingOnDepartment: get_unique_mentors_depending_on_department,
    GetUniqueAudiencesDependingOnDepartment: get_unique_audiences_depending_on_department,
    GetUniqueSubjects: get_unique_subjects,
    GetUniqueSubjectTypes: get_unique_subject_types,
    GetRowWorkloads: get_row_workloads,
    GetWorkloads: get_workloads,
    GetMentorsForScheduleItem: get_mentors_for_schedule_item,
}  # type: Dict[Type[Command], Callable]
