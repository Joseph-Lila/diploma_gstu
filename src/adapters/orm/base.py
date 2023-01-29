from sqlalchemy.orm import DeclarativeBase, as_declarative
from sqlalchemy.orm import registry


mapper_registry = registry()


@as_declarative(metadata=mapper_registry.metadata)
class Base:
    pass


# class Mentor(Base):
#     __tablename__ = 'mentors'
#
#     fio = Column(String, primary_key=True)
#     scientific_degree = Column(String)
#     salary = Column(Float)
#     experience = Column(Integer)
#     department = Column(ForeignKey('departments.title'))
#     requirements = Column(String)
#     duties = Column(String)
#
#
# class Subject(Base):
#     __tablename__ = 'subjects'
#
#     title = Column(String, primary_key=True)
#     description = Column(String)
#
#
# class Group(Base):
#     __tablename__ = 'groups'
#
#     title = Column(String, primary_key=True)
#     number_of_students = Column(Integer)
#
#
# class SubjectType(Base):
#     __tablename__ = 'subject_types'
#
#     title = Column(String, primary_key=True)
#     description = Column(String)
#
#
# class EquipmentKind(Base):
#     __tablename__ = 'equipment_kinds'
#
#     title = Column(String, primary_key=True, autoincrement=True)
#     cost = Column(String)
#     description = Column(String)
#     equipment = relationship('Equipment')
#     subjects_types = relationship('EquipmentKindForSubjectsType')
#
#     __mapper_args__ = {'eager_defaults': True}
#
#
# class Equipment(Base):
#     __tablename__ = 'equipment'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     equipment_kind = Column(ForeignKey('equipment_kinds.title'))
#     responsible_person = Column(String)
#     audience = relationship('AudienceEquipment')
#
#     __mapper_args__ = {'eager_defaults': True}
#
#
# class Audience(Base):
#     __tablename__ = 'audiences'
#
#     number = Column(Integer, primary_key=True)
#     number_of_seats = Column(Integer)
#     equipment = relationship('AudienceEquipment')
#
#     __mapper_args__ = {'eager_defaults': True}
#
#
# class AudienceEquipment(Base):
#     __tablename__ = 'audience_equipnemt'
#
#     id = Column(Integer, primary_key=True)
#     audience_number = Column(ForeignKey('audiences.number'))
#     equipment_id = Column(ForeignKey('equipment.id'))
#
#
# class EquipmentKindForSubjectsType(Base):
#     __tablename__ = 'equipment_for_subjects_types'
#
#     id = Column(Integer, primary_key=True)
#     subject_title = Column(ForeignKey('subjects.title'))
#     subject_type_title = Column(ForeignKey('subject_types.title'))
#     equipment_kind = Column(ForeignKey('equipment_kinds.title'))
