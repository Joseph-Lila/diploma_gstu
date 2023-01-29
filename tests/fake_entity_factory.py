from faker import Faker

from src.domain.entities.department import Department


def get_department():
    fake = Faker()
    return Department(fake.name(), fake.name())
