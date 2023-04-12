from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class SubjectAudience:
    __tablename__ = 'subject_audiences'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    audience_id: Mapped[int] = mapped_column(ForeignKey('audiences.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    subject_type_id: Mapped[int] = mapped_column(ForeignKey('subject_types.id'))
