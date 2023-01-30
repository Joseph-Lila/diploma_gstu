import random

from faker import Faker

from src.adapters.orm import Department

fake = Faker(locale="ru_RU")
department_titles = [
    'Физического воспитания и спорта',
    'Педагогики и проблем развития образования',
    'Информатики',
    'Информационных технологий',
    'Искусствоведения',
    'Искуственного интеллекта',
    'Иностранных языков',
    'Экономики и управления',
    'Истории',
    'Промышленной экологии',
    'Электроники',
]


def get_random_fio():
    return fake.name()


def get_department():
    global department_titles
    index = random.randint(0, len(department_titles) - 1)
    title = department_titles.pop(index)
    department = Department(
        title=title,
        head=get_random_fio(),
    )
    return department
