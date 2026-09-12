"""Extract one explicit year; comparisons and relative dates are unsupported."""

import re

from pydantic import TypeAdapter, ValidationError

from app.schemas.enrollment import Year

_YEAR = TypeAdapter(Year)


def find_year(question: str) -> int:
    """Accept one distinct standalone four-digit year in the range 1900–3000."""
    if not isinstance(question, str):
        raise TypeError("question must be a string.")

    matches = set(re.findall(r"\b[0-9]{4}\b", question))
    if not matches:
        raise ValueError("Please include a four-digit year between 1900 and 3000.")
    if len(matches) > 1:
        raise ValueError("Please ask about one year at a time.")
    try:
        return _YEAR.validate_python(int(matches.pop()))
    except ValidationError as exc:
        raise ValueError("Please use a year between 1900 and 3000.") from exc
