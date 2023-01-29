from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class DepartmentTable(Base):
    __tablename__ = 'departments'

    title: Mapped[str] = mapped_column(primary_key=True)
    head: Mapped[str]
    # mentors = relationship('Mentor')

    # __mapper_args__ = {'eager_defaults': True}
