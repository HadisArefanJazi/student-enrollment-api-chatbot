import pytest

from app.chatbot.parser import find_year


@pytest.mark.parametrize(
    "question,year",
    [
        ("How many students enrolled in 2025?", 2025),
        ("2024", 2024),
        ("In 2025, yes 2025", 2025),
        ("enrollment (1900)", 1900),
        ("enrollment 3000?", 3000),
    ],
)
def test_extracts_one_distinct_year(question, year):
    assert find_year(question) == year


@pytest.mark.parametrize(
    "question",
    [
        "",
        "next year",
        "enrollment 25",
        "20255",
        "abc2025",
        "2025abc",
        "１８９９",
        "1899",
        "3001",
        "0000",
        "Compare 2024 and 2026",
        "2024–2026",
    ],
)
def test_rejects_missing_invalid_or_ambiguous_year(question):
    with pytest.raises(ValueError):
        find_year(question)


def test_rejects_non_string():
    with pytest.raises(TypeError, match="question must be a string"):
        find_year(2025)
