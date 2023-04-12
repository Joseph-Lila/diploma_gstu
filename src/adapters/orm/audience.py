from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Audience:
    __tablename__ = 'audiences'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str]
    number_of_seats: Mapped[int]
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
