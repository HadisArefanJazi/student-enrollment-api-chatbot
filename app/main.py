"""FastAPI application factory and app instance."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router
from app.services.enrollment_service import EnrollmentService


def create_app() -> FastAPI:
    """Create and configure the Student Enrollment Data API."""

    app = FastAPI(title="Student Enrollment Data API")
    app.state.enrollment_service = EnrollmentService()
    app.include_router(router)
    return app


app = create_app()
