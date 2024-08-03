from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import connection as connection_crud
from app.schemas.connection import Connection as ConnectionSchema, ConnectionCreate
from app.db.models import City, Connection

router = APIRouter()


@router.post('/', response_model=list[ConnectionSchema], status_code=201)
def create_connection(connection: ConnectionCreate, db: Session = Depends(get_db)):
    return connection_crud.create_connection(connection=connection, db=db)


@router.get('/', response_model=list[ConnectionSchema])
def all_connections(db: Session = Depends(get_db)):
    return connection_crud.get_all_connections(db)


@router.delete("/{connection_id}", status_code=204)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    connection_crud.delete_connection(db=db, connection_id=connection_id)
