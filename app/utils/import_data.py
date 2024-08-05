import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, get_db
from app.db.models import City, Connection
from fastapi import Depends


def load_data(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    cities_by_name = {}
    connections = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            city1_name, city2_name, distance = parts

            city1 = cities_by_name.get(city1_name) or City(name=city1_name)
            city2 = cities_by_name.get(city2_name) or City(name=city2_name)

            connections.append(Connection(from_city=city1, to_city=city2, distance=int(distance)))

            cities_by_name[city1_name] = city1
            cities_by_name[city2_name] = city2

    return cities_by_name, connections


def save_data_to_db(cities: dict[str, City], connections: list[Connection], db: Session):
    db.add_all(cities.values())
    db.add_all(connections)
    db.commit()


def main(db: Session = Depends(get_db)):
    db = SessionLocal()
    cities, connections = load_data('sample.txt')
    save_data_to_db(cities, connections, db)


if __name__ == '__main__':
    main()
