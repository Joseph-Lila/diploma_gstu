import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, item_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, item_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, item):
        raise NotImplementedError
