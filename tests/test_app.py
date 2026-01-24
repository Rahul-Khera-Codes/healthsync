import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import DATABASE_URL

# Set up the test database
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as client:
        yield client

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_create_item(client):
    response = client.post("/items/", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

def test_read_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_update_item(client):
    response = client.put("/items/1", json={"name": "Updated Item", "description": "This is an updated test item."})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_delete_item(client):
    response = client.delete("/items/1")
    assert response.status_code == 204
    response = client.get("/items/1")
    assert response.status_code == 404

def test_invalid_item_creation(client):
    response = client.post("/items/", json={"name": "", "description": "This should fail."})
    assert response.status_code == 422

def test_user_acceptance(client):
    response = client.get("/user/")
    assert response.status_code == 200
    assert "user" in response.json()