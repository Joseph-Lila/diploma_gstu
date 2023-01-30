import abc
from typing import Optional

from src.adapters.repositories.abstract_repository import AbstractRepository


class AbstractRepositoryManager(abc.ABC):
    departments: Optional[AbstractRepository]
