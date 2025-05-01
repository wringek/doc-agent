# tests/test_lint.py
import pytest
from doc_agent.tools import lint_copy

def test_lint_copy_passes_by_default():
    result = lint_copy("Any text")
    assert result["status"] == "PASS"
    assert isinstance(result.get("errors"), list)
