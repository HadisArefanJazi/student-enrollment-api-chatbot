import json
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Student Enrollment API",
    version="1.0.0",
)

DATA_FILE = Path(__file__).parent / "data" / "enrollment_data.json"
DATA = json.loads(DATA_FILE.read_text())


@app.get("/health")
def health():
    return {"message": "API is running"}


@app.get("/enrollments/{year}")
def get_enrollment(year: int, department: str):

    for item in DATA:
        if (
            item["year"] == year
            and item["department"].lower() == department.lower()
        ):
            return item

    raise HTTPException(
        status_code=404,
        detail="Enrollment data not found",
    )
