from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class SubjectType:
    __tablename__ = 'subject_types'

    title: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
