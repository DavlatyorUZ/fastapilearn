def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "xabar" in response.json()
    assert response.json()["xabar"] == "Blog API"
    assert response.json()["version"] == "5.0.0"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_headers(client):
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert "access-control-allow-origin" in response.headers