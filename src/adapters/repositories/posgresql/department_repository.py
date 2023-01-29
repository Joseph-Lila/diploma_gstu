from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from src.domain.entities.department import Department
from src.adapters.repositories.abstract_repository import AbstractRepository


class DepartmentRepository(AbstractRepository):
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session: async_sessionmaker[AsyncSession] = async_session

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Department)
            result = await session.scalars(stmt)
        return result

    async def get_by_primary_key(self, key):
        async with self.async_session() as session:
            stmt = select(Department).filter_by(title=key)
            result = await session.scalar(stmt)
        return result

    async def create(self, item):
        async with self.async_session() as session:
            async with session.begin():
                session.add(item)

    async def delete(self, item_id: int):
        pass

    async def update(self, item):
        pass
