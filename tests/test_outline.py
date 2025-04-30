# tests/test_outline.py

import pytest
from agent.outline import make_outline

def test_make_outline_keys():
    data = {"name": "add"}
    outline = make_outline(data)
    expected_keys = {
        "title",
        "summary",    # ← newly added
        "purpose",
        "usage",
        "arguments",
        "returns",
        "examples"
    }
    assert set(outline.keys()) == expected_keys
    assert outline["title"] == "add"
    assert outline["summary"] == ""   # default blank summary
