from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, delete
from src.adapters.orm import async_session_factory
from src.domain.entities.department import Department
from src.adapters.repositories.abstract_repository import AbstractRepository


class DepartmentRepository(AbstractRepository):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Department)
            items = await session.scalars(stmt)
        return [item for item in items]

    async def get_by_primary_key(self, key: str):
        async with self.async_session() as session:
            stmt = select(Department).filter_by(title=key)
            result = await session.scalar(stmt)
        return result

    async def create(self, item: Department):
        async with self.async_session() as session:
            async with session.begin():
                session.add(item)

    async def delete(self, key: str):
        async with self.async_session() as session:
            async with session.begin():
                stmt = delete(Department).filter_by(title=key)
                await session.execute(stmt)

    async def update(self, item: Department):
        async with self.async_session() as session:
            async with session.begin():
                stmt = select(Department).filter_by(title=item.title)
                result = await session.scalar(stmt)
                result.head = item.head
