from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.orm import Subject, async_session_factory
from src.adapters.repositories.abstract_repository import AbstractRepository


class SubjectRepository(AbstractRepository):

    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Subject)
            items = await session.scalars(stmt)
        return [item for item in items]

    async def get_by_primary_key(self, key):
        async with self.async_session() as session:
            stmt = select(Subject).filter_by(title=key)
            result = await session.scalar(stmt)
        return result

    async def create(self, item):
        async with self.async_session() as session:
            async with session.begin():
                session.add(item)

    async def delete(self, key):
        async with self.async_session() as session:
            async with session.begin():
                stmt = delete(Subject).filter_by(title=key)
                await session.execute(stmt)

    async def update(self, item: Subject):
        async with self.async_session() as session:
            async with session.begin():
                stmt = select(Subject).filter_by(title=item.title)
                result = await session.scalar(stmt)
                result.description = item.description
