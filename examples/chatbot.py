"""Terminal chatbot example that queries the running enrollment API."""

from __future__ import annotations

import argparse
import logging

import requests

from app.services.query_parser import find_year

LOGGER = logging.getLogger(__name__)


def ask_api(year: int, api_url: str = "http://127.0.0.1:8000/students/enrollment") -> dict[str, object]:
    """Request enrollment data from the API."""

    try:
        response = requests.get(api_url, params={"year": year}, timeout=10)
        if response.status_code == 404:
            return {"error": response.json().get("detail", "No data found")}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Could not connect to the API"}


def run_chatbot(api_url: str) -> None:
    """Run one terminal chatbot interaction."""

    question = input("Ask me: ")
    year = find_year(question)

    if year is None:
        LOGGER.info("Please include a year.")
        return

    result = ask_api(year, api_url=api_url)

    if "error" in result:
        LOGGER.info("%s", result["error"])
        return

    LOGGER.info("%s students enrolled in %s.", result["students"], result["year"])


def main() -> None:
    """CLI entry point for the chatbot example."""

    parser = argparse.ArgumentParser(description="Terminal chatbot for enrollment API")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000/students/enrollment")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run_chatbot(args.api_url)


if __name__ == "__main__":
    main()
