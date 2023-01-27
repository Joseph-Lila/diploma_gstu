import sqlalchemy.orm

from src.adapters.repositories.abstract_repository import AbstractRepository


class DepartmentRepository(AbstractRepository):
    def __init__(self, session):
        self.session: sqlalchemy.orm.Session = session

    def get_all(self):
        return self.session.query()

    def get_by_id(self, item_id: int):
        pass

    def create(self, item):
        pass

    def delete(self, item_id: int):
        pass

    def update(self, item):
        pass