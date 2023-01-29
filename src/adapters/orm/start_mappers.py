from src.adapters.orm import DepartmentTable
from src.adapters.orm.base import mapper_registry
from src.domain.entities import Department


def start_mappers():
    department_mapper = mapper_registry.map_imperatively(Department, DepartmentTable)
