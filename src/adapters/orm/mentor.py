from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Mentor:
    __tablename__ = 'mentors'

    fio: Mapped[str] = mapped_column(primary_key=True)
    scientific_degree: Mapped[str]
    salary: Mapped[float]
    experience: Mapped[int]
    department_title: Mapped[str] = mapped_column(ForeignKey("departments.title"))
    requirements: Mapped[str]
    duties: Mapped[str]
    department: Mapped["Department"] = relationship(default=None)
