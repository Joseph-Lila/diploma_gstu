import abc
from typing import Optional


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_schedules(self, year: Optional[int], term: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unique_years(self, term: Optional[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_10_schedules(self):
        raise NotImplementedError
