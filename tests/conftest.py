import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tenacity import retry, stop_after_delay
from src import config
from sqlalchemy.orm import clear_mappers

from src.adapters.orm import metadata, start_mappers


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(
        config.get_test_postgres_uri(),
        isolation_level="SERIALIZABLE",
    )
    wait_for_postgres_to_come_up(engine)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(bind=postgres_db)


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()
