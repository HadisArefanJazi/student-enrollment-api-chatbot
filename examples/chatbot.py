"""Terminal chatbot that requests one annual count from the running API."""

import argparse

import requests

from app.chatbot.parser import find_year
from app.schemas.enrollment import EnrollmentRecord

DEFAULT_API_URL = "http://127.0.0.1:8000"


def ask_api(year: int, api_url: str = DEFAULT_API_URL) -> dict[str, int] | dict[str, str]:
    """Query an API base URL and turn HTTP or response errors into terminal messages."""
    try:
        response = requests.get(f"{api_url.rstrip('/')}/enrollments/{year}", timeout=10)
        if response.status_code == 404:
            return {"error": "No data for this year"}
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {"error": "The API request timed out"}
    except requests.exceptions.HTTPError:
        return {"error": "The API returned an HTTP error"}
    except requests.exceptions.RequestException:
        return {"error": "Could not connect to the API"}

    try:
        record = EnrollmentRecord.model_validate(response.json())
        if record.year != year:
            return {"error": "The API returned a different year"}
        return record.model_dump()
    except ValueError:
        return {"error": "The API returned invalid enrollment data"}


def run_chatbot(api_url: str = DEFAULT_API_URL) -> None:
    """Read one question and print either an enrollment count or a useful error."""
    try:
        question = input("Ask me: ")
    except (EOFError, KeyboardInterrupt):
        print("Goodbye.")
        return
    try:
        year = find_year(question)
    except ValueError as exc:
        print(str(exc))
        return

    result = ask_api(year, api_url=api_url)
    if "error" in result:
        print(result["error"])
    else:
        print(f"{result['students']} students enrolled in {result['year']}.")


def main() -> None:
    """Run a single interaction using the optional API base URL."""
    parser = argparse.ArgumentParser(description="Terminal chatbot for enrollment API")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="API base URL")
    args = parser.parse_args()
    run_chatbot(args.api_url)


if __name__ == "__main__":
    main()
