import os
import random
import tempfile
import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src import config
from src.adapters.orm import Department, Mentor, Subject


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


@pytest.fixture
def fake():
    fake = Faker(locale="ru_RU")
    return fake


@pytest.fixture
def random_fio_factory(fake):
    return lambda: fake.unique.name()


@pytest.fixture
def get_fake_department_factory(
        fake,
        random_fio_factory,
):
    return lambda x: Department(
        title=fake.unique.text() if x is None else x,
        head=random_fio_factory(),
    )


@pytest.fixture
def get_fake_subject_factory(
        get_fake_text_factory,
):
    return lambda: Subject(
        title=get_fake_text_factory(),
        description=get_fake_text_factory(),
    )


@pytest.fixture
def get_fake_salary_factory():
    return lambda: random.uniform(1000, 5000)


@pytest.fixture
def get_fake_scientific_degree_factory():
    return lambda: random.choice(
        [
            'Старший преподаватель',
            'Преподаватель',
            'Доцент',
            'Ассистент',
            'Профессор',
        ]
    )


@pytest.fixture
def get_fake_experience_factory():
    return lambda: random.randint(0, 35)


@pytest.fixture
def get_fake_text_factory(fake):
    return lambda: fake.unique.text()


@pytest.fixture
def get_fake_mentor_factory(
        random_fio_factory,
        get_fake_scientific_degree_factory,
        get_fake_salary_factory,
        get_fake_experience_factory,
        get_fake_text_factory,
        fake,
):
    return lambda x: Mentor(
        fio=random_fio_factory(),
        scientific_degree=get_fake_scientific_degree_factory(),
        salary=get_fake_salary_factory(),
        experience=get_fake_experience_factory(),
        department_title=fake.unique.text() if x is None else x,
        requirements=get_fake_text_factory(),
        duties=get_fake_text_factory(),
    )


@pytest.fixture
def csv_file_path():
    temp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
    yield temp.name
    temp.close()
    os.unlink(temp.name)
