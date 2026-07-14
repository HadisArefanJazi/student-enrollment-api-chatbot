"""FastAPI route definitions for student enrollment records."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.enrollment import (
    EnrollmentMutationResponse,
    EnrollmentRecord,
    EnrollmentResponse,
    EnrollmentUpdate,
    HealthResponse,
)
from app.services.enrollment_service import EnrollmentService

router = APIRouter()


def get_service(request: Request) -> EnrollmentService:
    """Retrieve the application enrollment service."""

    return request.app.state.enrollment_service


@router.get("/", response_model=HealthResponse)
def home() -> dict[str, str]:
    """Health check endpoint."""

    return {"message": "API is running"}


@router.get("/students", response_model=list[EnrollmentResponse])
def get_all_students(request: Request) -> list[dict[str, int]]:
    """Return all enrollment records."""

    return get_service(request).list_records()


@router.get("/students/enrollment", response_model=EnrollmentResponse)
def get_enrollment(year: int, request: Request) -> dict[str, int]:
    """Return enrollment for a requested year."""

    try:
        return get_service(request).get_enrollment(year)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data for this year") from exc


@router.post(
    "/students/enrollment",
    response_model=EnrollmentMutationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_enrollment(record: EnrollmentRecord, request: Request) -> dict[str, int | str]:
    """Add a new enrollment record."""

    try:
        return get_service(request).add_enrollment(record.year, record.students)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Year already exists") from exc


@router.put("/students/enrollment/{year}", response_model=EnrollmentMutationResponse)
def update_enrollment(year: int, record: EnrollmentUpdate, request: Request) -> dict[str, int | str]:
    """Update an existing enrollment record."""

    try:
        return get_service(request).update_enrollment(year, record.students)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Year not found") from exc


@router.delete("/students/enrollment/{year}", response_model=EnrollmentMutationResponse)
def delete_enrollment(year: int, request: Request) -> dict[str, int | str]:
    """Delete an existing enrollment record."""

    try:
        return get_service(request).delete_enrollment(year)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Year not found") from exc
