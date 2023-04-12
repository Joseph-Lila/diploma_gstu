from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.orm import Schedule, Workload, async_session_factory
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
