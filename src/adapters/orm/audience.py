from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Audience:
    __tablename__ = 'audiences'

    number: Mapped[str] = mapped_column(primary_key=True)
    number_of_seats: Mapped[int]
