from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import city as city_crud, connection as connection_crud
from app.schemas.city import City as CitySchema, CityCreate as CityCreateSchema, CityUpdate as CityUpdateSchema
from app.schemas.connection import Connection as ConnectionSchema, ConnectionNestedCreate, ConnectionCreate
from app.algorithms.dijkstra import dijkstra
from app.db.models import Connection

router = APIRouter()


@router.post("/", response_model=CitySchema, status_code=201)
def create_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    return city_crud.create_city(db=db, city=city)


@router.get("/", response_model=list[CitySchema])
def all_cities(db: Session = Depends(get_db)):
    return city_crud.get_all_cities(db)


@router.get("/{city_id}/findShortestPath")
def find_shortest_path(city_id: int, target_city: int, db: Session = Depends(get_db)):
    from_city = city_crud.get_city_by_id(id=city_id, db=db)
    to_city = city_crud.get_city_by_id(id=target_city, db=db)

    if not from_city:
        raise HTTPException(status_code=404, detail="City not found")
    elif not to_city:
        raise HTTPException(status_code=404, detail="Target city not found")

    graph = defaultdict(dict)
    connections = db.query(Connection).all()
    for connection in connections:
        graph[connection.from_city.id][connection.to_city.id] = connection.distance
        graph[connection.to_city.id][connection.from_city.id] = connection.distance

    distances = dijkstra(graph, from_city.id)
    distance = distances.get(to_city.id, float('infinity'))

    if distance == float('infinity'):
        raise HTTPException(status_code=404, detail="Path not found")

    return {
        "city": from_city.name,
        "result": {
            "distance": distance,
            "targetCity": to_city.name
        }
    }


@router.get("/{city_id}/connections", response_model=list[ConnectionSchema])
def connections_for_city(city_id: int, db: Session = Depends(get_db)):
    return connection_crud.get_connections_for_city(db=db, city_id=city_id)


@router.post("/{city_id}/connections", response_model=ConnectionSchema, status_code=201)
def create_connection_for_city(city_id: int, connection: ConnectionNestedCreate, db: Session = Depends(get_db)):
    return connection_crud.create_connection(db=db, connection=ConnectionCreate(**connection.model_dump(), from_city_id=city_id))


@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not city_crud.get_city_by_id(id=city_id, db=db):
        raise HTTPException(status_code=404, detail="City not found")
    city_crud.delete_city(db=db, id=city_id)


@router.get("/{city_id}", response_model=CitySchema)
def get_city(city_id: int, db: Session = Depends(get_db)):
    if not (city := city_crud.get_city_by_id(id=city_id, db=db)):
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.patch("/{city_id}", response_model=CitySchema)
def update_city(city_id: int, city: CityUpdateSchema, db: Session = Depends(get_db)):
    if not (db_city := city_crud.get_city_by_id(id=city_id, db=db)):
        raise HTTPException(status_code=404, detail="City not found")
    if db_city.name == city.name:
        raise HTTPException(status_code=400, detail="Prodvided city name matches current name")
    return city_crud.update_city(db=db, id=city_id, city=city)
