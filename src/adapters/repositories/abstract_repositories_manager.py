import abc
from .abstract_repository import AbstractRepository


class AbstractRepositoriesManager(abc.ABC):
    departments: AbstractRepository
    mentors: AbstractRepository
    subjects: AbstractRepository
