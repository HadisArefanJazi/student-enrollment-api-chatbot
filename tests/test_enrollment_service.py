from pathlib import Path

import pytest

from app.services.enrollment_service import EnrollmentDataError, EnrollmentService
from app.services.query_parser import find_year


def test_service_loads_sorted_enrollment_records() -> None:
    service = EnrollmentService()

    assert service.list_records() == [
        {"year": 2024, "students": 1700},
        {"year": 2025, "students": 1650},
        {"year": 2026, "students": 1800},
    ]


def test_service_get_enrollment_for_valid_year() -> None:
    service = EnrollmentService()

    assert service.get_enrollment(2025) == {"year": 2025, "students": 1650}


def test_service_raises_for_unavailable_year() -> None:
    service = EnrollmentService()

    with pytest.raises(KeyError):
        service.get_enrollment(2030)


def test_service_raises_for_missing_data_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        EnrollmentService(tmp_path / "missing.json")


def test_service_rejects_invalid_records(tmp_path: Path) -> None:
    data_file = tmp_path / "bad.json"
    data_file.write_text('{"2025": -1}', encoding="utf-8")

    with pytest.raises(EnrollmentDataError):
        EnrollmentService(data_file)


def test_service_rejects_malformed_json(tmp_path: Path) -> None:
    data_file = tmp_path / "bad.json"
    data_file.write_text("{bad json", encoding="utf-8")

    with pytest.raises(EnrollmentDataError, match="malformed JSON"):
        EnrollmentService(data_file)


def test_service_rejects_non_object_data(tmp_path: Path) -> None:
    data_file = tmp_path / "bad.json"
    data_file.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(EnrollmentDataError, match="non-empty object"):
        EnrollmentService(data_file)


def test_find_year_returns_last_four_digit_year() -> None:
    assert find_year("compare 2024 and 2026 enrollment") == 2026


def test_find_year_returns_none_for_malformed_question() -> None:
    assert find_year("how many students enrolled?") is None


def test_find_year_rejects_non_string_question() -> None:
    with pytest.raises(TypeError, match="question must be a string"):
        find_year(2025)  # type: ignore[arg-type]
