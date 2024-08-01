from sqlalchemy.orm import Session
from app.db.models import Connection
from app.schemas.connection import ConnectionCreate


def get_all_connections(db: Session):
    return db.query(Connection).all()


def get_connections_for_city(db: Session, city_id: int):
    return db.query(Connection).filter(
        Connection.from_city_id == city_id | 
        Connection.to_city == city_id
    ).first()


def create_connection(db: Session, connection: ConnectionCreate):
    db_connections = [
        Connection(
            from_city_id=connection.from_city_id, 
            to_city_id=connection.to_city_id, 
            distance=connection.distance
        ),
        Connection(
            from_city_id=connection.to_city_id, 
            to_city_id=connection.from_city_id, 
            distance=connection.distance
        ),
    ]
    
    db.add_all(db_connections)
    db.commit()
    return db_connections
