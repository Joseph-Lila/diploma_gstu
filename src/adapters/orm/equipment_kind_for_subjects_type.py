from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class EquipmentKindForSubjectsType:
    __tablename__ = 'equipment_for_subjects_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_title: Mapped[str] = mapped_column(ForeignKey("subjects.title"))
    subject_type_title: Mapped[str] = mapped_column(ForeignKey("subject_types.title"))
    equipment_kind: Mapped[str] = mapped_column(ForeignKey("equipment_kinds.title"))
