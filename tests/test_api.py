def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_register_and_login(client):
    registered = client.post("/api/auth/register", json={
        "username": "alice", "email": "alice@example.com", "password": "password123"
    })
    assert registered.status_code == 201
    logged_in = client.post("/api/auth/login", json={
        "identity": "alice@example.com", "password": "password123"
    })
    assert logged_in.status_code == 200
    assert "access_token" in logged_in.get_json()

def test_create_and_list_task(client, auth_headers):
    created = client.post("/api/tasks", headers=auth_headers, json={
        "title": "Build portfolio API", "priority": "high"
    })
    assert created.status_code == 201
    listed = client.get("/api/tasks", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.get_json()["pagination"]["total_items"] == 1

def test_task_requires_authentication(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401
