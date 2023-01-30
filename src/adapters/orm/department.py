from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Department:
    __tablename__ = 'departments'

    title: Mapped[str] = mapped_column(primary_key=True)
    head: Mapped[str]
    mentors: Mapped[List["Mentor"]] = relationship(
        default_factory=list,
        back_populates="department",
        lazy='joined',
    )
