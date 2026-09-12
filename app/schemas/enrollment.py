"""Validated enrollment and health responses."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Year = Annotated[int, Field(ge=1900, le=3000)]


class EnrollmentRecord(BaseModel):
    """An annual enrollment count, not an individual student."""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    year: Year
    students: int = Field(ge=0)


class HealthResponse(BaseModel):
    """Health endpoint response."""

    message: str
