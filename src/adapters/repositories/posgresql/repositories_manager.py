from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ...orm import async_session_factory
from ..abstract_repositories_manager import AbstractRepositoriesManager
from . import DepartmentRepository, MentorRepository, SubjectRepository


class RepositoriesManager(AbstractRepositoriesManager):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.mentors = MentorRepository(async_session_factory_)
        self.departments = DepartmentRepository(async_session_factory_)
        self.subjects = SubjectRepository(async_session_factory_)
