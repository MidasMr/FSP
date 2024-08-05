from fastapi import FastAPI
from app.db.session import engine
from app.db.models import Base
from app.routers import city, connection
from app.core.config import settings

app = FastAPI()

if not settings.TESTS_RUN:
    Base.metadata.create_all(bind=engine)

app.include_router(city.router, prefix="/cities", tags=["cities"])
app.include_router(connection.router, prefix="/connections", tags=["connections"])
