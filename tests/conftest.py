import pytest
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET_KEY": "test-secret"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_headers(client):
    client.post("/api/auth/register", json={
        "username": "tester", "email": "tester@example.com", "password": "password123"
    })
    response = client.post("/api/auth/login", json={
        "identity": "tester", "password": "password123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
