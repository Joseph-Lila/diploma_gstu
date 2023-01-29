import pytest
from src import config
from src.adapters.orm.create_tables import create_tables
from src.service_layer.unit_of_work.postgresql_unit_of_work import PostgresRepositoryManager
from tests.fake_entity_factory import get_department


pytestmark = pytest.mark.usefixtures("mappers")


@pytest.mark.asyncio
async def test_department_repository_get_by_primary_key():
    await create_tables(config.get_test_postgres_uri())
    repos_manager = PostgresRepositoryManager(connection_string=config.get_test_postgres_uri())
    new_item = get_department()
    await repos_manager.departments.create(new_item)
    item = await repos_manager.departments.get_by_primary_key(new_item.title)
    assert item == new_item
