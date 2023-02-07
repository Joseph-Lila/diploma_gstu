import pytest

from src.adapters.orm import Subject, create_tables
from src.adapters.repositories.posgresql.subject_repository import \
    SubjectRepository


@pytest.mark.asyncio
async def test_subject_repository_create(
        postgres_uri,
        postgres_session_factory,
        get_fake_subject_factory,
):
    await create_tables(postgres_uri)
    repo = SubjectRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_subject_factory()
    await repo.create(new_item)


@pytest.mark.asyncio
async def test_subject_repository_get_by_primary_key(
        postgres_uri,
        postgres_session_factory,
        get_fake_subject_factory,
):
    await create_tables(postgres_uri)
    repo = SubjectRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_subject_factory()
    await repo.create(new_item)

    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item


@pytest.mark.asyncio
async def test_subject_repository_get_all(
        postgres_uri,
        postgres_session_factory,
        get_fake_subject_factory,
):
    await create_tables(postgres_uri)
    repo = SubjectRepository(async_session_factory_=postgres_session_factory)

    # add data
    items = [get_fake_subject_factory() for _ in range(3)]
    for item in items:
        await repo.create(item)

    # get data
    data = await repo.get_all()
    assert data == items


@pytest.mark.asyncio
async def test_subject_repository_update(
        postgres_uri,
        postgres_session_factory,
        get_fake_subject_factory,
        get_fake_text_factory,
):
    await create_tables(postgres_uri)
    repo = SubjectRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_subject_factory()
    changed_new_item = Subject(title=new_item.title, description=get_fake_text_factory())

    await repo.create(new_item)

    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item

    await repo.update(changed_new_item)

    got_changed_item = await repo.get_by_primary_key(changed_new_item.title)
    assert got_changed_item == changed_new_item


@pytest.mark.asyncio
async def test_subject_repository_delete(
        postgres_uri,
        postgres_session_factory,
        get_fake_subject_factory,
):
    await create_tables(postgres_uri)
    repo = SubjectRepository(async_session_factory_=postgres_session_factory)
    new_item = get_fake_subject_factory()

    await repo.create(new_item)

    items = await repo.get_all()
    assert len(items) == 1

    await repo.delete(new_item.title)

    items = await repo.get_all()
    assert len(items) == 0
