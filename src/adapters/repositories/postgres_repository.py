from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.orm import (
    Schedule,
    Workload,
    async_session_factory,
    Mentor,
    Group, Faculty,
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

    async def get_schedules(self, year: Optional[int], term: Optional[str]):
        stmt = select(Schedule)
        if year:
            stmt = stmt.filter_by(year=year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.order_by(Schedule.year.desc())
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_mentors_fios(self, fio_substring: str):
        stmt = (
            select(Mentor.fio)
            .distinct()
            .order_by(Mentor.fio)
            .filter(Mentor.fio.ilike(f"%{fio_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_groups_titles(self, title_substring: str):
        stmt = (
            select(Group.title)
            .distinct()
            .order_by(Group.title)
            .filter(Group.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_groups_titles_depending_on_faculty(self, title_substring: str, faculty_title: Optional[str]):
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

    async def get_unique_faculties_titles(self, title_substring: str):
        stmt = (
            select(Faculty.title)
            .order_by(Faculty.title)
            .filter(Faculty.title.ilike(f"%{title_substring}%"))
        )
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_years_depending_on_workload(self, term: Optional[str]):
        stmt = select(Workload.year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.distinct().order_by(Workload.year)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_years_depending_on_schedule(self, term: Optional[str]):
        stmt = select(Schedule.year)
        if term:
            stmt = stmt.filter_by(term=term)
        stmt = stmt.distinct().order_by(Schedule.year)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_terms_depending_on_workload(self, year: Optional[str]):
        stmt = select(Workload.term)
        if year:
            stmt = stmt.filter_by(year=year)
        stmt = stmt.distinct().order_by(Workload.term)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_unique_terms_depending_on_schedule(self, year: Optional[str]):
        stmt = select(Schedule.term)
        if year:
            stmt = stmt.filter_by(year=year)
        stmt = stmt.distinct().order_by(Schedule.term)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_10_schedules(self):
        stmt = select(Schedule).order_by(Schedule.year.desc()).limit(10)
        async with self.async_session() as session:
            items = await session.scalars(stmt)
        return items.all()

    async def get_schedule_by_year_and_term(self, year, term):
        stmt = select(Schedule).filter_by(year=year).filter_by(term=term)
        async with self.async_session() as session:
            result = await session.scalar(stmt)
        return result

    async def create_schedule(self, year, term):
        async with self.async_session() as session, session.begin():
            new_elem = Schedule(year=year, term=term)
            session.add(new_elem)
            await session.flush()
        return new_elem

    async def delete_schedule(self, id_):
        print('delete')
        stmt = (
            delete(Schedule)
            .where(Schedule.id == id_)
        )
        async with self.async_session() as session, session.begin():
            await session.execute(stmt)
