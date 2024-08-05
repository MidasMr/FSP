from sqlalchemy.orm import Session
from app.db.models import Connection
from app.schemas.connection import ConnectionCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def get_all_connections(db: Session):
    return db.query(Connection).all()


def get_connections_for_city(db: Session, city_id: int):
    return db.query(Connection).filter(
        (Connection.from_city_id == city_id) |
        (Connection.to_city_id == city_id)
    ).all()


def create_connection(db: Session, connection: ConnectionCreate):
    if connection.from_city_id == connection.to_city_id:
        raise HTTPException(status_code=400, detail='Connection cannot be created between one city')

    try:
        connection = Connection(
            from_city_id=connection.from_city_id,
            to_city_id=connection.to_city_id,
            distance=connection.distance
        )
        db.add(connection)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Connection already exists or incorrect data provided')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return connection


def delete_connection(db: Session, connection_id: int):
    db.query(Connection).filter(Connection.id == connection_id).delete()
    db.commit()
