from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Subject:
    __tablename__ = 'subjects'

    title: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
