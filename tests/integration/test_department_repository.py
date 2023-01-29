import pytest
from src.adapters.orm.create_tables import create_tables
from src.adapters.repositories.posgresql.department_repository import DepartmentRepository
from src.domain.entities import Department


pytestmark = pytest.mark.usefixtures("mappers")


@pytest.mark.asyncio
async def test_department_repository_create(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
    await repo.create(new_item)


@pytest.mark.asyncio
async def test_department_repository_get_by_primary_key(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
    await repo.create(new_item)
    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item


@pytest.mark.asyncio
async def test_department_repository_get_all(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)

    # add data
    items = [
        Department(title='Наименование кафедры1', head='ФИО зав. кафедры1'),
        Department(title='Наименование кафедры2', head='ФИО зав. кафедры2'),
        Department(title='Наименование кафедры3', head='ФИО зав. кафедры3'),
    ]
    for item in items:
        await repo.create(item)

    # get data
    data = await repo.get_all()
    assert data == items


@pytest.mark.asyncio
async def test_department_repository_update(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
    changed_new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры2')

    await repo.create(new_item)

    got_item = await repo.get_by_primary_key(new_item.title)
    assert got_item == new_item

    await repo.update(changed_new_item)

    got_changed_item = await repo.get_by_primary_key(changed_new_item.title)
    assert got_changed_item == changed_new_item


@pytest.mark.asyncio
async def test_department_repository_delete(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session_factory_=postgres_session_factory)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')

    await repo.create(new_item)

    items = await repo.get_all()
    assert len(items) == 1

    await repo.delete(new_item.title)

    items = await repo.get_all()
    assert len(items) == 0
