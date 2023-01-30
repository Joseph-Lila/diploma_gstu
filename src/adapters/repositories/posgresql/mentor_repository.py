from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.orm.base import Mentor, async_session_factory
from src.adapters.repositories.abstract_repository import AbstractRepository


class MentorRepository(AbstractRepository):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Mentor)
            items = await session.scalars(stmt)
        return [item for item in items]