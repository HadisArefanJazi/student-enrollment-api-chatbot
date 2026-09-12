import pytest
from pydantic import ValidationError

from app.repositories.enrollment import EnrollmentDataError, EnrollmentRepository


def test_records_are_sorted(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"3000": 3, "1900": 0, "2025": 5}')
    records = EnrollmentRepository(path).list_records()
    assert [record.year for record in records] == [1900, 2025, 3000]
    assert records[0].students == 0


def test_lookup():
    assert EnrollmentRepository().get_enrollment(2025).students == 1650


def test_missing_year():
    with pytest.raises(KeyError):
        EnrollmentRepository().get_enrollment(2030)


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        EnrollmentRepository(tmp_path / "missing.json")


@pytest.mark.parametrize(
    "content",
    [
        "{bad json",
        "[]",
        "{}",
        "null",
        '{"2025": -1}',
        '{"2025": true}',
        '{"2025": 1.5}',
        '{"2025": "100"}',
        '{"2025": null}',
        '{"2025": {}}',
        '{"1899": 1}',
        '{"3001": 1}',
        '{"year": 1}',
        '{"02025": 1}',
        '{" 2025": 1}',
        '{"２０２５": 1}',
        '{"2025": 1, "2025": 2}',
    ],
)
def test_rejects_invalid_data(tmp_path, content):
    path = tmp_path / "data.json"
    path.write_text(content)
    with pytest.raises(EnrollmentDataError):
        EnrollmentRepository(path)


def test_rejects_invalid_encoding(tmp_path):
    path = tmp_path / "data.json"
    path.write_bytes(b"\xff")
    with pytest.raises(EnrollmentDataError):
        EnrollmentRepository(path)


def test_returned_records_cannot_mutate_repository():
    repository = EnrollmentRepository()
    records = repository.list_records()
    records.clear()
    with pytest.raises(ValidationError):
        repository.get_enrollment(2025).students = 1
    assert len(repository.list_records()) == 3
    assert repository.get_enrollment(2025).students == 1650


def test_snapshot_changes_only_after_reload(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"2025": 1}')
    repository = EnrollmentRepository(path)
    path.write_text('{"2025": 2}')
    assert repository.get_enrollment(2025).students == 1
    assert EnrollmentRepository(path).get_enrollment(2025).students == 2
