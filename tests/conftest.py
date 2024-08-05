import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from testcontainers.postgres import PostgresContainer


from app.db.base import Base
from app.db.session import get_db
from app.utils import import_data
from app.main import app


@pytest.fixture(scope="session")
def db_container():
    with PostgresContainer("postgres:15.2") as postgres:
        engine = create_engine(postgres.get_connection_url())
        SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        yield SessionTesting, engine

        engine.dispose()


@pytest.fixture(scope="function")
def clean_container(db_container):
    SessionTesting, engine = db_container
    Base.metadata.create_all(bind=engine)

    yield SessionTesting, engine

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def db_session(clean_container) -> Session:
    """Create a new database session with a rollback at the end of the test."""
    session_testing, engine = clean_container

    connection = engine.connect()
    connection.begin()
    session = session_testing(bind=connection)
    yield session
    session.close()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def setup_database(db_session):
    db = db_session
    try:
        cities, connections = import_data.load_data('sample.txt')
        import_data.save_data_to_db(cities, connections, db)
    finally:
        db.close()
