from typing import Optional
import pandas as pd
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
)
from src.adapters.repositories.abstract_repository import AbstractRepository


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

    async def get_extended_schedule_records(
        self,
        schedule_id: int,
    ):
        stmt = (
            select(
                ScheduleRecord.day_of_week,
                ScheduleRecord.pair_number,
                ScheduleRecord.week_type,
                ScheduleRecord.subgroup,
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
                ScheduleRecord.mentor_free,
                ScheduleRecord.id.label("schedule_record_id"),
            )
            .join(Mentor)
            .join(Group)
            .join(Subject)
            .join(Audience)
            .join(SubjectType)
            .where(ScheduleRecord.schedule_id == schedule_id)
        )
        async with self.async_session() as session:
            query = await session.execute(stmt)
        return pd.DataFrame(query.fetchall())

    async def get_workloads(
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
        faculty_title: Optional[str],
    ):
        if faculty_title is not None:
            stmt = (
                select(Group.title)
                .join(Faculty)
                .where(Faculty.title == faculty_title)
                .distinct()
                .filter(Group.title.ilike(f"%{title_substring}%"))
                .order_by(Group.title)
            )
        else:
            stmt = (
                select(Group.title)
                .distinct()
                .order_by(Group.title)
                .filter(Group.title.ilike(f"%{title_substring}%"))
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
        term: Optional[str],
    ):
        stmt = select(Workload.year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.distinct().order_by(Workload.year)
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
        department_title: Optional[str],
    ):
        if department_title is not None:
            stmt = (
                select(Mentor.fio)
                .join(Department)
                .where(Department.title == department_title)
                .distinct()
                .filter(Mentor.fio.ilike(f"%{fio_substring}%"))
                .order_by(Mentor.fio)
            )
        else:
            stmt = (
                select(Mentor.fio)
                .distinct()
                .order_by(Mentor.fio)
                .filter(Mentor.fio.ilike(f"%{fio_substring}%"))
            )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_audiences_numbers_depending_on_department(
        self,
        number_substring: str,
        department_title: Optional[str],
    ):
        if department_title is not None:
            stmt = (
                select(Audience.number)
                .join(Department)
                .where(Department.title == department_title)
                .distinct()
                .filter(Audience.number.ilike(f"%{number_substring}%"))
                .order_by(Audience.number)
            )
        else:
            stmt = (
                select(Audience.number)
                .distinct()
                .order_by(Audience.number)
                .filter(Audience.number.ilike(f"%{number_substring}%"))
            )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()
