# class AudienceEquipment(Base):
#     __tablename__ = 'audience_equipnemt'
#
#     id = Column(Integer, primary_key=True)
#     audience_number = Column(ForeignKey('audiences.number'))
#     equipment_id = Column(ForeignKey('equipment.id'))
#

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class AudienceEquipment:
    __tablename__ = 'audience_equipment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    audience_number: Mapped[str] = mapped_column(ForeignKey("audiences.number"))
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
