from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import City, Connection, Base
from .algorithms import dijkstra


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cities/{city}/findShortestPath")
def find_shortest_path(city: str, target_city: str, db: Session = Depends(get_db)):
    from_city = db.query(City).filter(City.name == city).first()
    to_city = db.query(City).filter(City.name == target_city).first()
    
    if not from_city or not to_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    graph = {}
    connections = db.query(Connection).all()
    for connection in connections:
        if connection.from_city.name not in graph:
            graph[connection.from_city.name] = {}
        graph[connection.from_city.name][connection.to_city.name] = connection.distance

    distances = dijkstra(graph, city)
    distance = distances.get(target_city, float('infinity'))
    
    if distance == float('infinity'):
        raise HTTPException(status_code=404, detail="Path not found")
    
    return {
        "city": city,
        "result": {
            "distance": distance,
            "targetCity": target_city
        }
    }
