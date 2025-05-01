# tests/test_lint.py
import pytest
from doc_agent.tools import lint_copy
from unittest.mock import Mock, call
from doc_agent.lint import self_lint

def test_lint_copy_passes_by_default():
    result = lint_copy("Any text")
    assert result["status"] == "PASS"
    assert isinstance(result.get("errors"), list)

@pytest.fixture
def mock_tools(monkeypatch):
    # Mock draft_copy
    draft_mock = Mock()
    draft_mock.side_effect = ["improved_text1", "improved_text2", "improved_text3"]
    monkeypatch.setattr("doc_agent.lint.draft_copy", draft_mock)
    
    # Mock lint_copy
    lint_mock = Mock()
    lint_mock.side_effect = [
        {"status": "FAIL", "errors": [{"msg": "error1"}]},
        {"status": "PASS", "errors": []},
        {"status": "PASS", "errors": []}
    ]
    monkeypatch.setattr("doc_agent.lint.lint_copy", lint_mock)
    
    return {"draft": draft_mock, "lint": lint_mock}

def test_self_lint_passes_after_one_fix(mock_tools):
    """Test that self_lint can fix a section after one iteration."""
    sections = {"test_section": "initial_text"}
    result = self_lint(sections)
    
    # Check the result
    assert result == {"test_section": "improved_text1"}
    
    # Check that lint_copy was called with the correct sequence
    expected_calls = [
        call("initial_text", section="test_section"),
        call("improved_text1", section="test_section")
    ]
    assert mock_tools["lint"].call_args_list == expected_calls
    
    # Check that draft_copy was called correctly
    mock_tools["draft"].assert_called_with(text="initial_text", fix="error1")

def test_self_lint_handles_string_errors(monkeypatch):
    """Test that self_lint can handle string errors from linters."""
    # Mock tools with string errors
    draft_mock = Mock(return_value="improved_text")
    lint_mock = Mock(side_effect=[
        {"status": "FAIL", "errors": ["string_error"]},
        {"status": "PASS", "errors": []}
    ])
    monkeypatch.setattr("doc_agent.lint.draft_copy", draft_mock)
    monkeypatch.setattr("doc_agent.lint.lint_copy", lint_mock)
    
    sections = {"test_section": "initial_text"}
    result = self_lint(sections)
    
    assert result == {"test_section": "improved_text"}
    draft_mock.assert_called_with(text="initial_text", fix="string_error")

def test_self_lint_max_iterations(monkeypatch):
    """Test that self_lint stops after MAX_LINT_ITERATIONS."""
    # Mock tools to always fail
    draft_mock = Mock(return_value="improved_text")
    lint_mock = Mock(return_value={"status": "FAIL", "errors": ["error"]})
    monkeypatch.setattr("doc_agent.lint.draft_copy", draft_mock)
    monkeypatch.setattr("doc_agent.lint.lint_copy", lint_mock)
    
    sections = {"test_section": "initial_text"}
    result = self_lint(sections)
    
    # Should still return the last attempted text
    assert result == {"test_section": "improved_text"}
    # Should have been called MAX_LINT_ITERATIONS times
    assert lint_mock.call_count == 5  # MAX_LINT_ITERATIONS

def test_self_lint_multiple_sections(monkeypatch):
    """Test that self_lint processes multiple sections correctly."""
    # Mock tools with different responses for each section
    draft_mock = Mock(side_effect=["improved_text1", "improved_text2"])
    lint_mock = Mock(side_effect=[
        {"status": "FAIL", "errors": ["error1"]},
        {"status": "PASS", "errors": []},
        {"status": "PASS", "errors": []}
    ])
    monkeypatch.setattr("doc_agent.lint.draft_copy", draft_mock)
    monkeypatch.setattr("doc_agent.lint.lint_copy", lint_mock)
    
    sections = {
        "section1": "text1",
        "section2": "text2"
    }
    result = self_lint(sections)
    
    assert "section1" in result
    assert "section2" in result
    assert result["section1"] == "improved_text1"
    assert result["section2"] == "text2"  # Second section passes first try
    assert lint_mock.call_count == 3  # 2 for first section (fail then pass), 1 for second (pass)
