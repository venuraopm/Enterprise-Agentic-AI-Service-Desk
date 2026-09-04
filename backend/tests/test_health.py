from fastapi.testclient import TestClient

from app.core.config import settings


def test_health_check(client: TestClient) -> None:
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }


def test_home(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_cors_preflight_from_vite(client: TestClient) -> None:
    response = client.options(
        "/health/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
