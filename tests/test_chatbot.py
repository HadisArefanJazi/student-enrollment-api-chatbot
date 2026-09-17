from unittest.mock import Mock

from app import chatbot


def test_enrollment_tool(monkeypatch):

    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "year": 2025,
        "department": "Computer Science",
        "students": 885,
    }

    monkeypatch.setattr(
        chatbot.requests,
        "get",
        Mock(return_value=response),
    )

    result = chatbot.get_enrollment.invoke({
        "year": 2025,
        "department": "Computer Science",
    })

    assert result["students"] == 885
