from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import registry

from src import config

mapper_registry = registry()
engine = create_async_engine(config.get_postgres_uri())
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables(connection_string=config.get_postgres_uri()):
    engine_ = create_async_engine(connection_string)

    async with engine_.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine_.dispose()


# class EquipmentKindForSubjectsType(Base):
#     __tablename__ = 'equipment_for_subjects_types'
#
#     id = Column(Integer, primary_key=True)
#     subject_title = Column(ForeignKey('subjects.title'))
#     subject_type_title = Column(ForeignKey('subject_types.title'))
#     equipment_kind = Column(ForeignKey('equipment_kinds.title'))
