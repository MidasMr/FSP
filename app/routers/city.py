from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import city as city_crud
from app.schemas.city import City as CitySchema, CityCreate as CityCreateSchema
from app.algorithms.dijkstra import dijkstra
from app.db.models import Connection

router = APIRouter()


@router.post("/", response_model=CitySchema)
def create_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    if city_crud.get_city_by_name(db, name=city.name):
        raise HTTPException(status_code=400, detail="City already registered")
    return city_crud.create_city(db=db, city=city)


@router.get("/", response_model=list[CitySchema])
def all_cities(db: Session = Depends(get_db)):
    return city_crud.get_all_cities(db)


@router.get("/{city}/findShortestPath")
def find_shortest_path(city: str, target_city: str, db: Session = Depends(get_db)):
    from_city = city_crud.get_city_by_name(name=city, db=db)
    to_city = city_crud.get_city_by_name(name=target_city, db=db)

    if not from_city or not to_city:
        raise HTTPException(status_code=404, detail="City not found")

    graph = defaultdict(dict)
    connections = db.query(Connection).all()
    for connection in connections:
        graph[connection.from_city.name][connection.to_city.name] = connection.distance

    distances = dijkstra(graph, from_city.name)
    distance = distances.get(to_city.name, float('infinity'))

    if distance == float('infinity'):
        raise HTTPException(status_code=404, detail="Path not found")

    return {
        "city": from_city.name,
        "result": {
            "distance": distance,
            "targetCity": to_city.name
        }
    }
