from sqlalchemy import Column, Integer, String, ForeignKey, Index, func, CheckConstraint
from sqlalchemy.orm import relationship, validates

from .base import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    connections_from = relationship(
        'Connection',
        foreign_keys='Connection.from_city_id',
        cascade="all, delete-orphan",
        viewonly=True
    )
    connections_to = relationship(
        'Connection',
        foreign_keys='Connection.to_city_id',
        cascade="all, delete-orphan",
        viewonly=True
    )


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, index=True)
    from_city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'))
    to_city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'))
    distance = Column(Integer)

    from_city = relationship("City", foreign_keys=[from_city_id])
    to_city = relationship("City", foreign_keys=[to_city_id])

    __table_args__ = (
        Index(
            'uq_connection',
            func.least(from_city_id, to_city_id),
            func.greatest(from_city_id, to_city_id),
            unique=True
        ),
        CheckConstraint('from_city_id <> to_city_id', name='check_from_to_city_diff'),
    )

    @validates('distance')
    def validate_distance(self, key, value):
        if value <= 0:
            raise ValueError('Distance must be greater than 0')
        return value
