import pytest
from sqlalchemy.orm import sessionmaker, clear_mappers
from tenacity import retry, stop_after_delay
from src import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm.start_mappers import start_mappers


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@pytest.fixture
def postgres_db():
    engine = create_async_engine(config.get_test_postgres_uri())
    return engine


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(
        bind=postgres_db,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()
