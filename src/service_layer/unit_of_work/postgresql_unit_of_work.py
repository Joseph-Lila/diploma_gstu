from src.adapters.orm import async_session_factory
from src.adapters.repositories.posgresql.department_repository import \
    DepartmentRepository
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractRepositoryManager


class PostgresRepositoryManager(AbstractRepositoryManager):
    def __init__(self, async_session_factory_=async_session_factory):
        self.departments = DepartmentRepository(async_session_factory_)
