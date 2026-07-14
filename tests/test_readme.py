from pathlib import Path


def test_readme_contains_mermaid_architecture_diagram() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "```mermaid\nflowchart TD" in readme
    assert 'A["Terminal chatbot example"] --> B["query_parser.py"]' in readme
    assert 'F --> G["app/data/enrollment_data.json"]' in readme
    assert "```" in readme.split("```mermaid", 1)[1]


def test_readme_does_not_reference_old_branch_name() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "refactor/professional-project-structure" not in readme
