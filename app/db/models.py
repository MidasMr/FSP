from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates

from .base import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Добавить индексы


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, index=True)
    from_city_id = Column(Integer, ForeignKey('cities.id'))
    to_city_id = Column(Integer, ForeignKey('cities.id'))
    distance = Column(Integer)

    from_city = relationship("City", foreign_keys=[from_city_id])
    to_city = relationship("City", foreign_keys=[to_city_id])
    __table_args__ = (
        UniqueConstraint('from_city_id', 'to_city_id', name='_from_city_to_city_unique'),
    )

    @validates('distance')
    def validate_distance(self, key, value):
        if value <= 0:
            raise ValueError('Distance must be greater than 0')
        return value
