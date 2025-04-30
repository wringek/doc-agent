#tools.py
from doc_agent.linters.short_description import lint as short_lint

def draft_copy(text: str, fix: str) -> str:
    """
    Generate an improved version of the text based on fix instructions.
    This should call the OpenAI Edits or Chat API in practice.
    """
    # TODO: Integrate with OpenAI API
    return text

def lint_copy(text: str, section: str = "") -> dict:
    """
    Lint function output. If section == 'summary', use static short_description.lint;
    otherwise, apply general Polaris-style rules (stubbed here).

    Returns:
        dict: { status: 'PASS'|'FAIL', errors: [...] }
    """
    if section == "summary":
        return short_lint(text)
    # General lint stub: always pass
    return {"status": "PASS", "errors": []}