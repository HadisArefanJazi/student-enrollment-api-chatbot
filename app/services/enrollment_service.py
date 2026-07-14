"""Enrollment data loading, validation, and lookup service."""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "enrollment_data.json"


class EnrollmentDataError(ValueError):
    """Raised when enrollment data cannot be loaded or validated."""


class EnrollmentService:
    """Service for retrieving and mutating enrollment records."""

    def __init__(self, data_path: str | Path = DEFAULT_DATA_PATH) -> None:
        self.data_path = Path(data_path)
        self._data = self._load_data(self.data_path)

    @staticmethod
    def _load_data(path: Path) -> dict[int, int]:
        if not path.exists():
            raise FileNotFoundError(f"Enrollment data file not found: {path}")

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise EnrollmentDataError(f"Enrollment data file is malformed JSON: {path}") from exc

        if not isinstance(raw, dict) or not raw:
            raise EnrollmentDataError("Enrollment data must be a non-empty object.")

        data: dict[int, int] = {}
        for year_text, students in raw.items():
            try:
                year = int(year_text)
                count = int(students)
            except (TypeError, ValueError) as exc:
                raise EnrollmentDataError("Enrollment records must map integer years to integer counts.") from exc

            if year < 1900 or year > 3000:
                raise EnrollmentDataError(f"Invalid enrollment year: {year}")
            if count < 0:
                raise EnrollmentDataError(f"Invalid student count for {year}: {count}")

            data[year] = count

        return data

    def list_records(self) -> list[dict[str, int]]:
        """Return all enrollment records sorted by year."""

        return [
            {"year": year, "students": students}
            for year, students in sorted(self._data.items())
        ]

    def get_enrollment(self, year: int) -> dict[str, int]:
        """Return enrollment for a year or raise KeyError when unavailable."""

        if year not in self._data:
            raise KeyError(year)
        return {"year": year, "students": self._data[year]}

    def add_enrollment(self, year: int, students: int) -> dict[str, int | str]:
        """Add a new enrollment record."""

        if year in self._data:
            raise KeyError(year)
        self._data[year] = students
        return {"message": "Enrollment record added", "year": year, "students": students}

    def update_enrollment(self, year: int, students: int) -> dict[str, int | str]:
        """Update an existing enrollment record."""

        if year not in self._data:
            raise KeyError(year)
        self._data[year] = students
        return {"message": "Enrollment record updated", "year": year, "students": students}

    def delete_enrollment(self, year: int) -> dict[str, int | str]:
        """Delete an existing enrollment record."""

        if year not in self._data:
            raise KeyError(year)
        students = self._data.pop(year)
        return {"message": "Enrollment record deleted", "year": year, "students": students}
