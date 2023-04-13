from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class ScheduleRecord:
    __tablename__ = "schedule_records"

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey(
            "schedules.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    day_of_week: Mapped[str]
    pair_number: Mapped[int]
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
            ondelete="CASCADE",
        ),
    )
    audience_id: Mapped[int] = mapped_column(
        ForeignKey(
            "audiences.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(
            "groups.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    week_type: Mapped[str]
    subgroup: Mapped[str]
