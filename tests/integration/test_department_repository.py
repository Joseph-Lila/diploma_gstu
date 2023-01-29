import pytest
from src.adapters.orm.create_tables import create_tables
from src.adapters.repositories.posgresql.department_repository import DepartmentRepository
from src.domain.entities import Department
from src.service_layer.unit_of_work.postgresql_unit_of_work import PostgresRepositoryManager

pytestmark = pytest.mark.usefixtures("mappers")


@pytest.mark.asyncio
async def test_department_repository_create(postgres_uri, postgres_session_factory):
    await create_tables(postgres_uri)
    repo = DepartmentRepository(async_session=postgres_session_factory)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
    await repo.create(new_item)


@pytest.mark.asyncio
async def test_department_repository_get_by_primary_key(postgres_uri):
    await create_tables(postgres_uri)
    repos_manager = PostgresRepositoryManager(connection_string=postgres_uri)
    new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
    await repos_manager.departments.create(new_item)
    item = await repos_manager.departments.get_by_primary_key(new_item.title)
    assert item == new_item


# @pytest.mark.asyncio
# async def test_department_repository_get_by_primary_key(postgres_uri, postgres_session_factory):
#     await create_tables(postgres_uri)
#     repo = DepartmentRepository(async_session=postgres_session_factory)
#     new_item = Department(title='Наименование кафедры', head='ФИО зав. кафедры')
#     await repo.create(new_item)
#     got_item = await repo.get_by_primary_key(new_item.title)
#     assert got_item == new_item


# @pytest.mark.asyncio
# @drop_and_create_tables
# async def test_department_repository_get_all(postgres_uri, postgres_session_factory):
#     repo = DepartmentRepository(async_session=postgres_session_factory)
#
#     # add data
#     items = [
#         Department(title='Наименование кафедры1', head='ФИО зав. кафедры1'),
#         Department(title='Наименование кафедры2', head='ФИО зав. кафедры2'),
#         Department(title='Наименование кафедры3', head='ФИО зав. кафедры3'),
#     ]
#     for item in items:
#         await repo.create(item)
#
#     # get data
#     data = await repo.get_all()
#     assert data == items
