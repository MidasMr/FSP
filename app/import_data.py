import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, City, Connection

Base.metadata.create_all(bind=engine)

def load_data(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    cities_set = set()
    connections = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            city1, city2, distance = parts
            distance = int(distance)
            cities_set.update([city1, city2])
            connections.append((city1, city2, distance))

    return cities_set, connections

def save_data_to_db(cities, connections, db: Session):
    city_map = {}
    for city in cities:
        db_city = City(name=city)
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        city_map[city] = db_city.id

    for city1, city2, distance in connections:
        from_city_id = city_map[city1]
        to_city_id = city_map[city2]
        db_connection = Connection(from_city_id=from_city_id, to_city_id=to_city_id, distance=distance)
        db.add(db_connection)

    db.commit()

def main():
    db = SessionLocal()
    try:
        file_path = 'sample.txt'
        cities, connections = load_data(file_path)
        save_data_to_db(cities, connections, db)
    finally:
        db.close()

if __name__ == '__main__':
    main()
