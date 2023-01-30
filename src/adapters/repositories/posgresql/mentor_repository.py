from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from src.adapters.orm import Mentor, async_session_factory
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.adapters.repositories.posgresql.department_repository import \
    DepartmentRepository


class MentorRepository(AbstractRepository):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Mentor).options(selectinload(Mentor.department))
            items = await session.scalars(stmt)
        return [item for item in items]

    async def get_by_primary_key(self, key: str):
        async with self.async_session() as session:
            stmt = select(Mentor).filter_by(fio=key).options(selectinload(Mentor.department))
            result = await session.scalar(stmt)
        return result

    async def create(self, item: Mentor):
        if item.department is None and item.department_title:
            item.department = await DepartmentRepository(self.async_session).get_by_primary_key(item.department_title)
        async with self.async_session() as session:
            async with session.begin():
                session.add(item)

    async def delete(self, key: str):
        async with self.async_session() as session:
            async with session.begin():
                stmt = delete(Mentor).filter_by(fio=key)
                await session.execute(stmt)

    async def update(self, item: Mentor):
        async with self.async_session() as session:
            async with session.begin():
                stmt = select(Mentor).filter_by(fio=item.fio)
                result = await session.scalar(stmt)
                result.scientific_degree = item.scientific_degree
                result.salary = item.salary
                result.experience = item.experience
                result.department_title = item.department_title
                result.requirements = item.requirements
                result.duties = item.duties
