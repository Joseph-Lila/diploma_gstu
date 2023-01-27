from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
)
from sqlalchemy.orm import mapper
from loguru import logger
from src.domain.entities.department import Department


metadata = MetaData()


departments = Table(
    'departments',
    metadata,
    Column('title', String, primary_key=True),
    Column('head', String, nullable=False),
)


def start_mappers():
    logger.info('Starting mappers')
    departments_mapper = mapper(Department, departments)
