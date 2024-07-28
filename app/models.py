from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, index=True)
    from_city_id = Column(Integer, ForeignKey('cities.id'))
    to_city_id = Column(Integer, ForeignKey('cities.id'))
    distance = Column(Integer) # Сделать только положитьельным

    from_city = relationship("City", foreign_keys=[from_city_id])
    to_city = relationship("City", foreign_keys=[to_city_id])
