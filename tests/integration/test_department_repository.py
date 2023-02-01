import pytest

from src.adapters.orm import Department, create_tables
from src.adapters.repositories.posgresql.department_repository import \
    DepartmentRepository
from src.adapters.repositories.posgresql.mentor_repository import MentorRepository


@pytest.mark.asyncio
async def test_department_repository_create(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_department_factory(None)
    await repo.create(new_item)


@pytest.mark.asyncio
async def test_department_repository_get_by_primary_key(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        get_fake_mentor_factory,
):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_department_factory(None)
    await repo.create(new_item)

    mentors_quantity = 3
    mentors = [get_fake_mentor_factory(new_item.title) for _ in range(mentors_quantity)]
    mentors_repo = MentorRepository(async_session_factory_=postgres_session_factory)
    for mentor in mentors:
        await mentors_repo.create(mentor)
    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item

    got_mentors = await mentors_repo.get_all()
    got_mentors = [mentor for mentor in mentors if mentor.department_title == got_item.title]

    assert len(got_mentors) == mentors_quantity


@pytest.mark.asyncio
async def test_department_repository_get_all(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)

    # add data
    items = [get_fake_department_factory(None) for _ in range(3)]
    for item in items:
        await repo.create(item)

    # get data
    data = await repo.get_all()
    assert data == items


@pytest.mark.asyncio
async def test_department_repository_update(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
        random_fio_factory,
):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_department_factory(None)
    changed_new_item = Department(title=new_item.title, head=random_fio_factory())

    await repo.create(new_item)

    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item

    await repo.update(changed_new_item)

    got_changed_item = await repo.get_by_primary_key(changed_new_item.title)
    assert got_changed_item == changed_new_item


@pytest.mark.asyncio
async def test_department_repository_delete(
        postgres_uri,
        postgres_session_factory,
        get_fake_department_factory,
):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_department_factory(None)

    await repo.create(new_item)

    items = await repo.get_all()
    assert len(items) == 1

    await repo.delete(new_item.title)

    items = await repo.get_all()
    assert len(items) == 0
