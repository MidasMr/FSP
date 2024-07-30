# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.crud.city import create_city
from app.schemas.city import CityCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Создаем тестовые данные в базе
    db = TestingSessionLocal()
    renton = create_city(db, CityCreate(name="Renton"))
    sodo = create_city(db, CityCreate(name="SoDo"))
    factoria = create_city(db, CityCreate(name="Factoria"))
    
    # crud.create_route(db, schemas.RouteCreate(from_city_id=renton.id, to_city_id=sodo.id, distance=12))
    # crud.create_route(db, schemas.RouteCreate(from_city_id=renton.id, to_city_id=factoria.id, distance=8))
    # crud.create_route(db, schemas.RouteCreate(from_city_id=sodo.id, to_city_id=factoria.id, distance=8))
    db.commit()
    db.close()

def test_find_shortest_path():
    response = client.get("/cities/Renton/findShortestPath?to=Factoria")
    assert response.status_code == 200
    assert response.json() == {
        "city": "Renton",
        "result": {
            "distance": 8,
            "targetCity": "Factoria"
        }
    }

def test_find_shortest_path_non_existent_city():
    response = client.get("/cities/NonExistentCity/findShortestPath?to=Factoria")
    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}

def test_find_shortest_path_no_route():
    response = client.get("/cities/SoDo/findShortestPath?to=Renton")
    assert response.status_code == 404
    assert response.json() == {"detail": "Route not found"}
