import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base


class Department(Base):
    __tablename__ = 'departments'

    title = sa.Column(sa.String, primary_key=True)
    head = sa.Column(sa.String)
    mentors = relationship('Mentor')

    __mapper_args__ = {'eager_defaults': True}