import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from src import config
from src.adapters.orm import Base


async def create_tables(connection_string=config.get_postgres_uri()):
    engine = create_async_engine(connection_string)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_tables())
