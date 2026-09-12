"""Read-only HTTP endpoints for annual enrollment counts."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request

from app.repositories.enrollment import EnrollmentRepository
from app.schemas.enrollment import EnrollmentRecord, HealthResponse, Year

router = APIRouter()


def get_repository(request: Request) -> EnrollmentRepository:
    """Use the validated snapshot owned by this application instance."""
    return request.app.state.enrollment_repository


Repository = Annotated[EnrollmentRepository, Depends(get_repository)]


@router.get("/health", response_model=HealthResponse)
def health() -> dict[str, str]:
    return {"message": "API is running"}


@router.get("/enrollments", response_model=list[EnrollmentRecord])
def list_enrollments(repository: Repository) -> list[EnrollmentRecord]:
    """Return annual records in ascending year order."""
    return repository.list_records()


@router.get("/enrollments/{year}", response_model=EnrollmentRecord)
def get_enrollment(year: Year, repository: Repository) -> EnrollmentRecord:
    """Return one annual record; a valid but unavailable year returns 404."""
    try:
        return repository.get_enrollment(year)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="No data for this year") from exc
