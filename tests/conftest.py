import pytest
from sqlalchemy.orm import sessionmaker
from src import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def postgres_db(postgres_uri):
    engine = create_async_engine(postgres_uri)
    return engine


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(
        bind=postgres_db,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
def postgres_uri():
    return config.get_test_postgres_uri()


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()
