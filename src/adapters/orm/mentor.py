from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Mentor:
    __tablename__ = 'mentors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fio: Mapped[str]
    scientific_degree: Mapped[str]
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
