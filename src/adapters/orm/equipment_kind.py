from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class EquipmentKind:
    __tablename__ = 'equipment_kinds'

    title: Mapped[str] = mapped_column(primary_key=True)
    cost: Mapped[float]
    description: Mapped[str]
