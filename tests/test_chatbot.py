from unittest.mock import Mock

import pytest
import requests

from examples import chatbot


@pytest.fixture
def get(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(chatbot.requests, "get", mock)
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {"year": 2025, "students": 1650}
    return mock


def test_success_and_request_url(get):
    assert chatbot.ask_api(2025, "http://example.test/") == {"year": 2025, "students": 1650}
    get.assert_called_once_with("http://example.test/enrollments/2025", timeout=10)


def test_not_found_with_non_json_body(get):
    get.return_value.status_code = 404
    get.return_value.json.side_effect = ValueError("HTML body")
    assert chatbot.ask_api(2025) == {"error": "No data for this year"}


@pytest.mark.parametrize(
    "error,message",
    [
        (requests.exceptions.Timeout(), "The API request timed out"),
        (requests.exceptions.ConnectionError(), "Could not connect to the API"),
    ],
)
def test_network_failures(get, error, message):
    get.side_effect = error
    assert chatbot.ask_api(2025) == {"error": message}


def test_http_failure(get):
    get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
    assert chatbot.ask_api(2025) == {"error": "The API returned an HTTP error"}


@pytest.mark.parametrize(
    "body",
    [
        None,
        [],
        {},
        {"year": 2025},
        {"year": 2025, "students": -1},
        {"year": "2025", "students": 1},
        {"year": 2025, "students": True},
    ],
)
def test_invalid_response(get, body):
    get.return_value.json.return_value = body
    assert chatbot.ask_api(2025) == {"error": "The API returned invalid enrollment data"}


def test_invalid_json(get):
    get.return_value.json.side_effect = ValueError("not JSON")
    assert chatbot.ask_api(2025) == {"error": "The API returned invalid enrollment data"}


def test_wrong_year(get):
    get.return_value.json.return_value = {"year": 2024, "students": 1}
    assert chatbot.ask_api(2025) == {"error": "The API returned a different year"}


def test_terminal_success(monkeypatch, capsys, get):
    monkeypatch.setattr("builtins.input", lambda _: "Enrollment in 2025?")
    chatbot.run_chatbot()
    assert capsys.readouterr().out == "1650 students enrolled in 2025.\n"


def test_terminal_api_error(monkeypatch, capsys, get):
    monkeypatch.setattr("builtins.input", lambda _: "2025")
    get.return_value.status_code = 404
    chatbot.run_chatbot()
    assert capsys.readouterr().out == "No data for this year\n"


@pytest.mark.parametrize("question", ["hello", "2024 and 2025", "1899"])
def test_terminal_invalid_question_never_calls_http(monkeypatch, capsys, get, question):
    monkeypatch.setattr("builtins.input", lambda _: question)
    chatbot.run_chatbot()
    assert "Please" in capsys.readouterr().out
    get.assert_not_called()


@pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
def test_terminal_interruption(monkeypatch, capsys, get, error):
    monkeypatch.setattr("builtins.input", Mock(side_effect=error))
    chatbot.run_chatbot()
    assert capsys.readouterr().out == "Goodbye.\n"
    get.assert_not_called()


def test_cli_custom_url(monkeypatch, get):
    monkeypatch.setattr("sys.argv", ["chatbot", "--api-url", "http://example.test:9000"])
    monkeypatch.setattr("builtins.input", lambda _: "2025")
    chatbot.main()
    get.assert_called_once_with("http://example.test:9000/enrollments/2025", timeout=10)
