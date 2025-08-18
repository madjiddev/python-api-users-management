"""
tests/test_auth_users.py — Tests d'intégration rapides
- health
- register / login
- me (protégé)
- list users (protégé)
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db

# DB de test (fichier local dédié)
TEST_DB_URL = "sqlite:///./test.db"
engine_test = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Override de la dépendance get_db pour utiliser la DB de test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Réinitialiser les tables de test
Base.metadata.drop_all(bind=engine_test)
Base.metadata.create_all(bind=engine_test)

client = TestClient(app)

def register(email: str, password: str):
    return client.post("/auth/register", json={"email": email, "password": password})

def login(email: str, password: str):
    return client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

def auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_register_login_me_and_list():
    # Register
    r = register("t1@example.com", "password1234")
    assert r.status_code == 201
    uid = r.json()["id"]

    # Login → token
    r = login("t1@example.com", "password1234")
    assert r.status_code == 200
    token = r.json()["access_token"]

    # /auth/me sans token
    r = client.get("/auth/me")
    assert r.status_code == 401

    # /auth/me avec token
    r = client.get("/auth/me", headers=auth_header(token))
    assert r.status_code == 200
    assert r.json()["id"] == uid

    # /users/ list
    r = client.get("/users/", headers=auth_header(token))
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert any(u["id"] == uid for u in r.json())
