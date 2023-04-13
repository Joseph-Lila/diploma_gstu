from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Group:
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str]
    number_of_students: Mapped[int]
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey(
            "faculties.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
