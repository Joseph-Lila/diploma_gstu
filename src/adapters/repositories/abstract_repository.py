import abc
from typing import Optional


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_schedules(self, year: Optional[int], term: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_years_depending_on_workload(self, term: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_years_depending_on_schedule(self, term: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_terms_depending_on_workload(self, year: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_terms_depending_on_schedule(self, year: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_mentors_fios(self, fio_substring: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_groups_titles(self, title_substring: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_10_schedules(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_schedule_by_year_and_term(self, year, term):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_schedule(self, year, term):
        raise NotImplementedError
