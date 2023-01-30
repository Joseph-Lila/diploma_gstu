from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.adapters.orm.base import async_session_factory, Mentor
from src.adapters.repositories.abstract_repository import AbstractRepository


class MentorRepository(AbstractRepository):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Mentor)
            items = await session.scalars(stmt)
        return [item for item in items]