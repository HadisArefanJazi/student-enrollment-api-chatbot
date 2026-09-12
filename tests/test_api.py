import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.enrollment import EnrollmentDataError


@pytest.fixture
def client():
    with TestClient(create_app()) as api:
        yield api


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_list_enrollments(client):
    response = client.get("/enrollments")
    assert response.status_code == 200
    assert response.json() == [
        {"year": 2024, "students": 1700},
        {"year": 2025, "students": 1650},
        {"year": 2026, "students": 1800},
    ]


def test_get_enrollment(client):
    response = client.get("/enrollments/2025")
    assert response.status_code == 200
    assert response.json() == {"year": 2025, "students": 1650}


def test_unavailable_year(client):
    response = client.get("/enrollments/2030")
    assert response.status_code == 404
    assert response.json() == {"detail": "No data for this year"}


@pytest.mark.parametrize("year", ["abc", "2025.5", "1899", "3001"])
def test_invalid_year(client, year):
    assert client.get(f"/enrollments/{year}").status_code == 422


@pytest.mark.parametrize(
    "method,path",
    [
        ("post", "/enrollments"),
        ("post", "/enrollments/2025"),
        ("put", "/enrollments/2025"),
        ("patch", "/enrollments/2025"),
        ("delete", "/enrollments/2025"),
    ],
)
def test_api_is_read_only(client, method, path):
    before = client.get("/enrollments").json()
    assert client.request(method, path, json={"students": 1}).status_code == 405
    assert client.get("/enrollments").json() == before


@pytest.mark.parametrize("path", ["/", "/students", "/students/enrollment"])
def test_old_routes_removed(client, path):
    assert client.get(path).status_code == 404


def test_openapi_only_exposes_read_endpoints(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert set(paths) == {"/health", "/enrollments", "/enrollments/{year}"}
    assert all(set(operations) == {"get"} for operations in paths.values())


def test_app_uses_custom_data(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"2000": 0}')
    with TestClient(create_app(path)) as client:
        assert client.get("/enrollments/2000").json() == {"year": 2000, "students": 0}


def test_invalid_data_prevents_app_creation(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"2025": true}')
    with pytest.raises(EnrollmentDataError):
        create_app(path)
