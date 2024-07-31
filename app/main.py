from fastapi import FastAPI
from app.db.session import engine
from app.db.models import Base
from app.routers import city

app = FastAPI()

print(engine, 'LOLOLOLOLOLOLOLOLOLO')

Base.metadata.create_all(bind=engine)

app.include_router(city.router, prefix="/cities", tags=["cities"])
