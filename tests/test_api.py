from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200


def test_enrollment():
    response = client.get(
        "/enrollments/2025",
        params={"department": "Computer Science"},
    )

    assert response.status_code == 200

    assert response.json() == {
        "year": 2025,
        "department": "Computer Science",
        "students": 885,
    }


def test_missing_data():
    response = client.get(
        "/enrollments/2030",
        params={"department": "Computer Science"},
    )

    assert response.status_code == 404
