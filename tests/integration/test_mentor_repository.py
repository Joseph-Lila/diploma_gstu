import pytest

from src.adapters.orm import create_tables
from src.adapters.repositories.posgresql.department_repository import \
    DepartmentRepository
from src.adapters.repositories.posgresql.mentor_repository import \
    MentorRepository


@pytest.mark.asyncio
async def test_mentor_repository_create(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        get_fake_mentor_factory,
):
    await create_tables(postgres_uri)
    departments_repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    mentors_repo = MentorRepository(async_session_factory_=postgres_session_factory)
    new_department = get_fake_department_factory(None)
    await departments_repo.create(new_department)
    new_mentor = get_fake_mentor_factory(new_department.title)
    await mentors_repo.create(new_mentor)


@pytest.mark.asyncio
async def test_mentor_repository_get_by_primary_key(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        get_fake_mentor_factory,
):
    await create_tables(postgres_uri)
    departments_repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    mentors_repo = MentorRepository(async_session_factory_=postgres_session_factory)
    new_department = get_fake_department_factory(None)
    await departments_repo.create(new_department)
    new_mentor = get_fake_mentor_factory(new_department.title)
    await mentors_repo.create(new_mentor)
    got_item = await mentors_repo.get_by_primary_key(new_mentor.fio)
    assert got_item == new_mentor


@pytest.mark.asyncio
async def test_mentor_repository_get_all(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        get_fake_mentor_factory,
):
    await create_tables(postgres_uri)
    departments_repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    mentors_repo = MentorRepository(async_session_factory_=postgres_session_factory)
    new_department = get_fake_department_factory(None)
    await departments_repo.create(new_department)
    new_mentors = [
        get_fake_mentor_factory(new_department.title)
        for _ in range(3)
    ]
    for new_mentor in new_mentors:
        await mentors_repo.create(new_mentor)
    got_mentors = await mentors_repo.get_all()
    assert len(got_mentors) == len(new_mentors)


async def test_mentor_repository_update(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        get_fake_mentor_factory,
):
    await create_tables(postgres_uri)
    departments_repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    mentors_repo = MentorRepository(async_session_factory_=postgres_session_factory)

    # add two departments
    first_department = get_fake_department_factory(None)
    second_department = get_fake_department_factory(None)
    await departments_repo.create(first_department)
    await departments_repo.create(second_department)

    mentor = get_fake_mentor_factory(first_department.title)

    await mentors_repo.create(mentor)
    assert mentor.department_title == first_department.title
    mentor.department_title = second_department.title
    await mentors_repo.update(mentor)
    got_mentor = await mentors_repo.get_by_primary_key(mentor.fio)
    assert got_mentor.department_title == second_department.title
