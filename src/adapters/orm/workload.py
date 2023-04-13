from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Workload:
    __tablename__ = "workloads"

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(
            "groups.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subjects.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    subject_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subject_types.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    mentor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mentors.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
    )
    hours: Mapped[int]
    year: Mapped[int]
    term: Mapped[str]
