from sqlalchemy.orm import Session
from app.db.models import City
from app.schemas.city import CityCreate


def get_all_cities(db: Session):
    return db.query(City).all()


def get_city_by_name(db: Session, name: str):
    return db.query(City).filter(City.name == name).first()


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city
