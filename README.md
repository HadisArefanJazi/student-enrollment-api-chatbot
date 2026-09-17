# Student Enrollment AI Assistant

A Python project demonstrating how a Large Language Model can interact with an existing REST API using LangChain tool calling.

The application stores university enrollment data by year and academic department. A FastAPI service exposes that data through an HTTP endpoint, while a LangChain agent allows users to query the same information using natural language.

For example, instead of manually calling:

```text
GET /enrollments/2025?department=Computer Science
```

a user can ask:

```text
How many Computer Science students were enrolled in 2025?
```

The language model understands the requested year and department, selects the appropriate Python tool, and uses the API result to produce the final response.

## Architecture

```text
User question
      ↓
LangChain Agent
      │
      ├── uses OpenAI LLM to understand the question and decide what to do
      │
      └── uses get_enrollment(year, department) to take action
                    ↓
                 FastAPI
                    ↓
            JSON Enrollment Data
                    ↓
        Tool result returns to the agent
                    ↓
        OpenAI LLM produces the answer
```

For example, the agent calls `get_enrollment(year=2025, department="Computer Science")`
and uses the API result to answer: "885 Computer Science students were enrolled in 2025."

## What LangChain Does

LangChain does not replace the language model, FastAPI, or the data source.

Each component has a separate responsibility:

```text
OpenAI LLM
    Understands the user's natural-language question.

LangChain
    Connects the LLM to Python tools and manages tool calling.

Python tool
    Gives the LLM a controlled way to access the application.

FastAPI
    Provides the enrollment data through a REST API.

JSON
    Stores the example enrollment records.
```

Without LangChain, the program would need custom code such as manually extracting a year or department from the user's question.

With LangChain, the LLM can determine the required tool arguments from natural language.

## Project Structure

```text
app/
├── __init__.py
├── main.py
├── chatbot.py
└── data/
    └── enrollment_data.json

tests/
├── test_api.py
└── test_chatbot.py
```

`main.py` contains the FastAPI application.

`chatbot.py` contains the LangChain agent and its enrollment tool.

`enrollment_data.json` contains the enrollment dataset.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
pip install -e ".[dev]"
```

Set an OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Never commit a real API key to GitHub.

## Run the API

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Example API request:

```text
GET /enrollments/2025?department=Computer Science
```

Example response:

```json
{
  "year": 2025,
  "department": "Computer Science",
  "students": 885
}
```

## Run the AI Assistant

Keep the API running.

Open another terminal, activate the virtual environment, and run:

```bash
python -m app.chatbot
```

Example:

```text
You: How many Computer Science students were enrolled in 2025?

AI: 885 Computer Science students were enrolled in 2025.
```

Other examples:

```text
How many Data Science students were enrolled in 2024?

What was Electrical Engineering enrollment in 2026?

How many Mathematics students were there in 2022?
```

Type:

```text
exit
```

to stop the chatbot.

## Tests

Run:

```bash
pytest
```

The tests check the API and LangChain tool without making real OpenAI API calls.

## Technology

* Python
* FastAPI
* LangChain
* OpenAI
* Requests
* Pytest
* JSON

## Main Learning Objective

The main concept demonstrated by this project is **LLM tool calling**.

The language model does not directly access the JSON file.

Instead:

```text
User question
 ↓
LangChain Agent
 ↓
OpenAI LLM decides what to do
 ↓
get_enrollment(year, department)
 ↓
FastAPI
 ↓
JSON
 ↓
Tool result returns to the agent
 ↓
OpenAI LLM produces the answer
```

This separation allows an AI model to interact with normal application code and APIs in a controlled way.
