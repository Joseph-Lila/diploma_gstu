from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncResult,
)
from sqlalchemy.orm import registry

from src import config

mapper_registry = registry()
engine = create_async_engine(config.get_postgres_uri())
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables(connection_string=config.get_postgres_uri()):
    engine_ = create_async_engine(connection_string)

    async with engine_.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine_.dispose()


async def init_database_with_data(
    initial_data_file_path=config.get_initial_data_file_path(),
    connection_string=config.get_postgres_uri(),
):
    with open(initial_data_file_path, "r", encoding="utf-8") as file:
        sql_string = file.read()

    sql_statements = sql_string.split("\n")
    sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]

    engine_ = create_async_engine(connection_string)

    async with engine_.begin() as conn:
        for stmt in sql_statements:
            await conn.execute(text(stmt))

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine_.dispose()
