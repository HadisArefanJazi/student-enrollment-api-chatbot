"""FastAPI application factory and ASGI entry point."""

from pathlib import Path

from fastapi import FastAPI

from app.api.routes import router
from app.repositories.enrollment import DEFAULT_DATA_PATH, EnrollmentRepository


def create_app(data_path: str | Path = DEFAULT_DATA_PATH) -> FastAPI:
    """Validate the data before serving requests; fail early on invalid files."""
    app = FastAPI(title="Student Enrollment Data API")
    app.state.enrollment_repository = EnrollmentRepository(data_path)
    app.include_router(router)
    return app


app = create_app()
