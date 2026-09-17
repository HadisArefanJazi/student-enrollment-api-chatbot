import requests
from langchain.agents import create_agent
from langchain.tools import tool

API_URL = "http://127.0.0.1:8000"


@tool
def get_enrollment(year: int, department: str) -> dict:
    """Get student enrollment for a department in a specific year."""

    response = requests.get(
        f"{API_URL}/enrollments/{year}",
        params={"department": department},
        timeout=10,
    )

    if response.status_code == 404:
        return {"error": "No enrollment data found"}

    response.raise_for_status()

    return response.json()


def main():
    agent = create_agent(
        model="openai:gpt-4.1-mini",
        tools=[get_enrollment],
        system_prompt=(
            "You are a university enrollment assistant. "
            "For enrollment questions, use the get_enrollment tool. "
            "Never invent enrollment numbers."
        ),
    )

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        })

        print(
            "AI:",
            result["messages"][-1].content,
        )


if __name__ == "__main__":
    main()
