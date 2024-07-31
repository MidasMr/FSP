from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import connection as connection_crud
from app.schemas.connection import Connection as ConnectionSchema, ConnectionCreate
from app.db.models import City, Connection

router = APIRouter()


@router.post('/create_connection/', response_model=list[ConnectionSchema])
def create_connection(connection: ConnectionCreate, db: Session = Depends(get_db)):
    return connection_crud.create_connection(connection=connection, db=db)
