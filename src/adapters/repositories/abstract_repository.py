import abc
from typing import Optional, List

from src.domain.entities.schedule_item_info import ScheduleItemInfo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_schedules(
        self,
        year: Optional[int],
        term: Optional[str],
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_workloads(
        self,
        year: int,
        term: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_years_depending_on_workload(
        self,
        term: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_years_depending_on_schedule(
        self,
        term: Optional[str],
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_terms_depending_on_workload(
        self,
        year: Optional[str],
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_terms_depending_on_schedule(
        self,
        year: Optional[str],
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_mentors_fios(
        self,
        fio_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_groups_titles(
        self,
        title_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_subjects_titles(
        self,
        title_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_subject_types_titles(
        self,
        title_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_groups_titles_depending_on_faculty(
        self,
        title_substring: str,
        faculty_title: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_audiences_numbers_depending_on_department(
        self,
        number_substring: str,
        department_title: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_mentors_fios_depending_on_department(
        self,
        fio_substring: str,
        department_title: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_faculties_titles(
        self,
        title_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_departments_titles(
        self,
        title_substring: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_10_schedules(
        self,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_schedule_by_year_and_term(
        self,
        year,
        term,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_schedule(
        self,
        year,
        term,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_schedule(
        self,
        id_,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_row_workloads(
        self,
        group_substring,
        subject_substring,
        subject_type_substring,
        mentor_substring,
        year,
        term,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_extended_local_schedule_records(
        self,
        schedule_id: int,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_group_titles_depending_on_faculty(
        self,
        group_substring,
        faculty_substring,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_global_schedule_records(
        self,
        schedule_id: int,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_local_schedule_records(
        self,
        schedule_id: int,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def clear_local_schedule_record(
        self,
        id_=None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def clear_global_schedule_record(
        self,
        schedule_id: int,
        id_=None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_local_schedule_record(
        self,
        schedule_id: int,
        day_of_week: str,
        pair_number: int,
        subject_id: int,
        subject_type_id: int,
        mentor_id: int,
        audience_id: int,
        group_id: int,
        week_type: str,
        subgroup: str,
        mentor_free: bool,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_global_schedule_record(
        self,
        schedule_id: int,
        day_of_week: str,
        pair_number: int,
        subject_id: int,
        subject_type_id: int,
        mentor_id: int,
        audience_id: int,
        group_id: int,
        week_type: str,
        subgroup: str,
        mentor_free: bool,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def make_global_schedule_records_like_local(
        self,
        schedule_id: int,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def make_local_schedule_records_like_global(
        self,
        schedule_id: int,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_mentors_for_schedule_item(
            self,
            info_record: ScheduleItemInfo,
    ):
        raise NotImplementedError
