"""Load and validate a read-only snapshot of the bundled enrollment data."""

import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.enrollment import EnrollmentRecord

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "enrollment_data.json"


class EnrollmentDataError(ValueError):
    """The enrollment file does not contain valid annual counts."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    data: dict[str, object] = {}
    for key, value in pairs:
        if key in data:
            raise EnrollmentDataError(f"Duplicate enrollment year: {key}")
        data[key] = value
    return data


class EnrollmentRepository:
    """Read JSON once; return immutable records in ascending year order."""

    def __init__(self, data_path: str | Path = DEFAULT_DATA_PATH) -> None:
        path = Path(data_path)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise EnrollmentDataError(f"Enrollment data file is malformed JSON: {path}") from exc

        if not isinstance(raw, dict) or not raw:
            raise EnrollmentDataError("Enrollment data must be a non-empty object.")

        self._records: dict[int, EnrollmentRecord] = {}
        for year_text, students in raw.items():
            if not (year_text.isascii() and year_text.isdigit() and len(year_text) == 4):
                raise EnrollmentDataError(f"Invalid enrollment year: {year_text}")
            try:
                record = EnrollmentRecord(year=int(year_text), students=students)
            except ValidationError as exc:
                raise EnrollmentDataError(f"Invalid enrollment record for {year_text}") from exc
            self._records[record.year] = record

    def list_records(self) -> list[EnrollmentRecord]:
        """Return a new list so callers cannot alter the repository's collection."""
        return [self._records[year] for year in sorted(self._records)]

    def get_enrollment(self, year: int) -> EnrollmentRecord:
        """Return a record or raise KeyError when the year is unavailable."""
        return self._records[year]
