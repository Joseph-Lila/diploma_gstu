from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Equipment:
    __tablename__ = 'equipment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    equipment_kind: Mapped[str] = mapped_column(ForeignKey("equipment_kinds.title"))
    responsible_person: Mapped[str]
