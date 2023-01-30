from typing import List
from src.adapters.orm import mapper_registry
from sqlalchemy.orm import Mapped, mapped_column, relationship


@mapper_registry.mapped_as_dataclass
class Department:
    __tablename__ = 'departments'

    title: Mapped[str] = mapped_column(primary_key=True)
    head: Mapped[str]
    mentors: Mapped[List["Mentor"]] = relationship(
        default_factory=list, back_populates="department"
    )