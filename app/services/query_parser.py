"""Natural-language query parsing helpers for the terminal chatbot."""

from __future__ import annotations

import re


def find_year(question: str) -> int | None:
    """Return the last four-digit year in a question."""

    if not isinstance(question, str):
        raise TypeError("question must be a string.")

    matches = re.findall(r"\b\d{4}\b", question)
    if not matches:
        return None
    return int(matches[-1])
