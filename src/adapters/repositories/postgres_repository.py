from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.orm import (
    Schedule,
    Workload,
    async_session_factory,
    Mentor,
    Group,
    Faculty,
    Department,
    Audience,
    Subject,
    SubjectType,
    ScheduleRecord,
    LocalScheduleRecord,
)
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.entities.schedule_item_info import ScheduleItemInfo
from src.domain.enums import WeekType, Subgroup


class PostgresRepository(AbstractRepository):
    def __init__(
        self,
        async_session_factory_: async_sessionmaker[
            AsyncSession
        ] = async_session_factory,
    ):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_schedules(
        self,
        year: Optional[int],
        term: Optional[str],
    ):
        stmt = select(Schedule)
        if year:
            stmt = stmt.filter_by(year=year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.order_by(Schedule.year.desc())
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_group_titles_depending_on_faculty(
        self,
        group_substring,
        faculty_substring,
    ):
        stmt = (
            select(
                Group.title,
            )
            .join(Faculty)
            .order_by(Group.title)
            .filter(Group.title.ilike(f"%{group_substring}%"))
            .filter(Faculty.title.ilike(f"%{faculty_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.fetchall()

    async def get_unique_mentors_fios(
        self,
        fio_substring: str,
    ):
        stmt = (
            select(Mentor.fio)
            .distinct()
            .order_by(Mentor.fio)
            .filter(Mentor.fio.ilike(f"%{fio_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_groups_titles(
        self,
        title_substring: str,
    ):
        stmt = (
            select(Group.title)
            .distinct()
            .order_by(Group.title)
            .filter(Group.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_subjects_titles(
        self,
        title_substring: str,
    ):
        stmt = (
            select(Subject.title)
            .distinct()
            .order_by(Subject.title)
            .filter(Subject.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_subject_types_titles(
        self,
        title_substring: str,
    ):
        stmt = (
            select(SubjectType.title)
            .distinct()
            .order_by(SubjectType.title)
            .filter(SubjectType.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_extended_local_schedule_records(
        self,
        schedule_id: int,
    ):
        stmt = (
            select(
                LocalScheduleRecord.day_of_week,
                LocalScheduleRecord.pair_number,
                LocalScheduleRecord.week_type,
                LocalScheduleRecord.subgroup,
                Audience.id.label("audience_id"),
                Audience.number.label("audience_number"),
                Audience.number_of_seats,
                Group.id.label("group_id"),
                Group.title.label("group_title"),
                Group.number_of_students,
                Mentor.id.label("mentor_id"),
                Mentor.fio.label("mentor_fio"),
                Mentor.scientific_degree,
                Subject.id.label("subject_id"),
                SubjectType.id.label("subject_type_id"),
                Subject.title.label("subject_title"),
                SubjectType.title.label("subject_type_title"),
                LocalScheduleRecord.mentor_free,
                LocalScheduleRecord.id.label("schedule_record_id"),
            )
            .join(Mentor)
            .join(Group)
            .join(Subject)
            .join(Audience)
            .join(SubjectType)
            .where(LocalScheduleRecord.schedule_id == schedule_id)
        )
        async with self.async_session() as session:
            query = await session.execute(stmt)
        return query.fetchall()

    async def get_global_schedule_records(
        self,
        schedule_id: int,
    ):
        stmt = select(ScheduleRecord).where(ScheduleRecord.schedule_id == schedule_id)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_local_schedule_records(
        self,
        schedule_id: int,
    ):
        stmt = select(LocalScheduleRecord).where(
            LocalScheduleRecord.schedule_id == schedule_id
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def clear_local_schedule_record(
        self,
        id_=None,
    ):
        if id_ is None:
            stmt = delete(LocalScheduleRecord)
        else:
            stmt = delete(LocalScheduleRecord).where(LocalScheduleRecord.id == id_)
        async with self.async_session() as session, session.begin():
            await session.execute(stmt)

    async def clear_global_schedule_record(
        self,
        schedule_id: int,
        id_=None,
    ):
        if id_ is None:
            stmt = delete(ScheduleRecord).where(
                ScheduleRecord.schedule_id == schedule_id
            )
        else:
            stmt = delete(ScheduleRecord).where(ScheduleRecord.id == id_)
        async with self.async_session() as session, session.begin():
            await session.execute(stmt)

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
        async with self.async_session() as session, session.begin():
            new_elem = LocalScheduleRecord(
                schedule_id=schedule_id,
                day_of_week=day_of_week,
                pair_number=pair_number,
                subject_id=subject_id,
                subject_type_id=subject_type_id,
                mentor_id=mentor_id,
                audience_id=audience_id,
                group_id=group_id,
                week_type=week_type,
                subgroup=subgroup,
                mentor_free=mentor_free,
            )
            session.add(new_elem)
            await session.flush()
        return new_elem

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
        async with self.async_session() as session, session.begin():
            new_elem = ScheduleRecord(
                schedule_id=schedule_id,
                day_of_week=day_of_week,
                pair_number=pair_number,
                subject_id=subject_id,
                subject_type_id=subject_type_id,
                mentor_id=mentor_id,
                audience_id=audience_id,
                group_id=group_id,
                week_type=week_type,
                subgroup=subgroup,
                mentor_free=mentor_free,
            )
            session.add(new_elem)
            await session.flush()
        return new_elem

    async def make_global_schedule_records_like_local(
        self,
        schedule_id: int,
    ):
        global_records = await self.get_global_schedule_records(schedule_id)
        await self.clear_local_schedule_record()
        for record in global_records:
            await self.create_local_schedule_record(
                record.schedule_id,
                record.day_of_week,
                record.pair_number,
                record.subject_id,
                record.subject_type_id,
                record.mentor_id,
                record.audience_id,
                record.group_id,
                record.week_type,
                record.subgroup,
                record.mentor_free,
            )

    async def make_local_schedule_records_like_global(
        self,
        schedule_id: int,
    ):
        local_records = await self.get_local_schedule_records(schedule_id)
        await self.clear_global_schedule_record(schedule_id)
        for record in local_records:
            await self.create_global_schedule_record(
                record.schedule_id,
                record.day_of_week,
                record.pair_number,
                record.subject_id,
                record.subject_type_id,
                record.mentor_id,
                record.audience_id,
                record.group_id,
                record.week_type,
                record.subgroup,
                record.mentor_free,
            )

    async def get_workloads(
        self,
        year: int,
        term: str,
    ):
        stmt = select(Workload).where(Workload.term == term and Workload.year == year)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.fetchall()

    async def get_row_workloads(
        self,
        group_substring,
        subject_substring,
        subject_type_substring,
        mentor_substring,
        year,
        term,
    ):
        stmt = (
            select(
                Mentor.fio,
                Group.title,
                Subject.title,
                SubjectType.title,
                Workload.hours,
            )
            .join(Mentor)
            .join(Group)
            .join(Subject)
            .join(SubjectType)
            .where(Workload.year == year and Workload.term == term)
            .filter(Group.title.ilike(f"%{group_substring}%"))
            .filter(Subject.title.ilike(f"%{subject_substring}%"))
            .filter(SubjectType.title.ilike(f"%{subject_type_substring}%"))
            .filter(Mentor.fio.ilike(f"%{mentor_substring}%"))
            .order_by(Mentor.fio)
        )
        async with self.async_session() as session:
            items = await session.execute(stmt)
        return items.fetchall()

    async def get_unique_groups_titles_depending_on_faculty(
        self,
        title_substring: str,
        faculty_title: str,
    ):
        stmt = (
            select(Group.title)
            .join(Faculty)
            .distinct()
            .filter(Group.title.ilike(f"%{title_substring}%"))
            .filter(Faculty.title.ilike(f"%{faculty_title}%"))
            .order_by(Group.title)
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_faculties_titles(
        self,
        title_substring: str,
    ):
        stmt = (
            select(Faculty.title)
            .order_by(Faculty.title)
            .filter(Faculty.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_departments_titles(
        self,
        title_substring: str,
    ):
        stmt = (
            select(Department.title)
            .order_by(Department.title)
            .filter(Department.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_years_depending_on_workload(
        self,
        term: str,
    ):
        stmt = (
            select(Workload.year)
            .filter(Workload.term.ilike(f"%{term}%"))
            .distinct()
            .order_by(Workload.year)
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_years_depending_on_schedule(
        self,
        term: Optional[str],
    ):
        stmt = select(Schedule.year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.distinct().order_by(Schedule.year)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_terms_depending_on_workload(
        self,
        year: Optional[str],
    ):
        stmt = select(Workload.term)
        if year:
            stmt = stmt.filter_by(year=year)
        stmt = stmt.distinct().order_by(Workload.term)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_terms_depending_on_schedule(
        self,
        year: Optional[str],
    ):
        stmt = select(Schedule.term)
        if year:
            stmt = stmt.filter_by(year=year)
        stmt = stmt.distinct().order_by(Schedule.term)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_10_schedules(
        self,
    ):
        stmt = select(Schedule).order_by(Schedule.year.desc()).limit(10)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_schedule_by_year_and_term(
        self,
        year,
        term,
    ):
        stmt = select(Schedule).filter_by(year=year).filter_by(term=term)
        async with self.async_session() as session:
            result = await session.scalar(stmt)
        return result

    async def create_schedule(
        self,
        year,
        term,
    ):
        async with self.async_session() as session, session.begin():
            new_elem = Schedule(year=year, term=term)
            session.add(new_elem)
            await session.flush()
        return new_elem

    async def delete_schedule(
        self,
        id_,
    ):
        stmt = delete(Schedule).where(Schedule.id == id_)
        async with self.async_session() as session, session.begin():
            await session.execute(stmt)

    async def get_unique_mentors_fios_depending_on_department(
        self,
        fio_substring: str,
        department_title: str,
    ):
        stmt = (
            select(Mentor.fio)
            .join(Department)
            .distinct()
            .filter(Mentor.fio.ilike(f"%{fio_substring}%"))
            .filter(Department.title.ilike(f"%{department_title}%"))
            .order_by(Mentor.fio)
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_audiences_numbers_depending_on_department(
        self,
        number_substring: str,
        department_title: str,
    ):
        stmt = (
            select(Audience.number)
            .join(Department)
            .distinct()
            .filter(Audience.number.ilike(f"%{number_substring}%"))
            .filter(Department.title.ilike(f"%{department_title}%"))
            .order_by(Audience.number)
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_mentors_for_schedule_item(
        self,
        info_record: ScheduleItemInfo,
    ):
        stmt = select(
            Mentor.id,
            Mentor.fio,
            Mentor.scientific_degree,
        ).order_by(Mentor.fio)
        async with self.async_session() as session:
            query = await session.execute(stmt)
        return query.fetchall()

    async def get_free_mentors_at_the_moment(
        self,
        mentor_id: int,
        day_of_week: str,
        pair_number: int,
        week_type: str,
        subgroup: str,
        subject_id: int,
        subject_type_id: int,
    ):
        not_allowed_week_types = [
            week_type,
            WeekType.BOTH.value,
        ]
        not_allowed_subgroups = [
            subgroup,
            Subgroup.BOTH.value,
        ]
        stmt = (
            select(LocalScheduleRecord)
            .filter(LocalScheduleRecord.mentor_id == mentor_id)
            .filter(LocalScheduleRecord.day_of_week == day_of_week)
            .filter(LocalScheduleRecord.pair_number == pair_number)
            .filter(LocalScheduleRecord.week_type.in_(not_allowed_week_types))
            .filter(LocalScheduleRecord.subgroup.in_(not_allowed_subgroups))
        )
        if subject_id != -1 and subject_type_id != -1:
            stmt = stmt.filter(
                (
                    (LocalScheduleRecord.subject_id == subject_id)
                    & (LocalScheduleRecord.subject_type_id != subject_type_id)
                )
                | (LocalScheduleRecord.subject_id != subject_id)
            )
        async with self.async_session() as session:
            query = await session.scalars(stmt)
        ans = query.fetchall()
        if mentor_id == 37:
            print(f"{subject_id = }")
            print(f"{subject_type_id = }")
            print(ans)
        return len(ans) == 0
