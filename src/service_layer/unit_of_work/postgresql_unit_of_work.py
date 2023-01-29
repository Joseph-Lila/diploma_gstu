import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src import config
from src.adapters.repositories.posgresql.department_repository import DepartmentRepository
from src.service_layer.unit_of_work.abstract_unit_of_work import AbstractRepositoryManager


class PostgresRepositoryManager(AbstractRepositoryManager):
    def __init__(
            self,
            connection_string=config.get_postgres_uri(),
    ):
        engine = create_async_engine(connection_string)

        async_session = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

        self.departments = DepartmentRepository(async_session)
