import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.adapters.orm import Base
from src.config import get_test_postgres_uri


async def async_main():
    print("start")
    engine = create_async_engine(
        get_test_postgres_uri(),
    )
    print(f"{engine = }")

    async with engine.begin() as conn:
        print(f"{conn = }")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(async_main())
