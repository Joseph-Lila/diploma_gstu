import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_primary_key(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, item):
        raise NotImplementedError
