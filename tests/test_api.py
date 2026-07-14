from fastapi.testclient import TestClient

from app.main import create_app


def client() -> TestClient:
    return TestClient(create_app())


def test_root_endpoint() -> None:
    response = client().get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_get_all_students_schema() -> None:
    response = client().get("/students")

    assert response.status_code == 200
    assert response.json() == [
        {"year": 2024, "students": 1700},
        {"year": 2025, "students": 1650},
        {"year": 2026, "students": 1800},
    ]


def test_get_enrollment_valid_year() -> None:
    response = client().get("/students/enrollment", params={"year": 2026})

    assert response.status_code == 200
    assert response.json() == {"year": 2026, "students": 1800}


def test_get_enrollment_missing_year_parameter() -> None:
    response = client().get("/students/enrollment")

    assert response.status_code == 422


def test_get_enrollment_unavailable_year() -> None:
    response = client().get("/students/enrollment", params={"year": 2030})

    assert response.status_code == 404
    assert response.json() == {"detail": "No data for this year"}


def test_create_update_and_delete_enrollment() -> None:
    api = client()

    create_response = api.post("/students/enrollment", json={"year": 2027, "students": 1900})
    assert create_response.status_code == 201
    assert create_response.json() == {
        "message": "Enrollment record added",
        "year": 2027,
        "students": 1900,
    }

    duplicate_response = api.post("/students/enrollment", json={"year": 2027, "students": 1901})
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {"detail": "Year already exists"}

    update_response = api.put("/students/enrollment/2027", json={"students": 1950})
    assert update_response.status_code == 200
    assert update_response.json() == {
        "message": "Enrollment record updated",
        "year": 2027,
        "students": 1950,
    }

    delete_response = api.delete("/students/enrollment/2027")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Enrollment record deleted",
        "year": 2027,
        "students": 1950,
    }


def test_malformed_post_body_returns_422() -> None:
    response = client().post("/students/enrollment", json={"year": 2028})

    assert response.status_code == 422
