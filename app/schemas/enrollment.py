"""Enrollment API request and response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EnrollmentRecord(BaseModel):
    """Request body for creating an enrollment record."""

    year: int = Field(..., ge=1900, le=3000)
    students: int = Field(..., ge=0)


class EnrollmentUpdate(BaseModel):
    """Request body for updating an enrollment record."""

    students: int = Field(..., ge=0)


class EnrollmentResponse(BaseModel):
    """Enrollment data returned by read endpoints."""

    year: int
    students: int


class EnrollmentMutationResponse(BaseModel):
    """Response returned after create, update, and delete operations."""

    message: str
    year: int
    students: int


class HealthResponse(BaseModel):
    """Root endpoint response."""

    message: str
