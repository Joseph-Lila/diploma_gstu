from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Group:
    __tablename__ = 'groups'

    title: Mapped[str] = mapped_column(primary_key=True)
    number_of_students: Mapped[int]
