import pytest
from unittest.mock import Mock, patch
from doc_agent.agent_loop import main

@pytest.fixture
def mock_dependencies(monkeypatch):
    """Mock all external dependencies for testing main()"""
    # Mock run_agent_loop
    run_mock = Mock(return_value="This is a test error message.")
    monkeypatch.setattr("doc_agent.agent_loop.run_agent_loop", run_mock)
    
    # Mock evaluate_text
    eval_mock = Mock(return_value={
        "clarity_score": 4,
        "clarity_explanation": "The message is clear and concise.",
        "actionable": True,
        "actionability_comment": "User knows what to do next."
    })
    monkeypatch.setattr("doc_agent.agent_loop.evaluate_text", eval_mock)
    
    return {
        "run_agent_loop": run_mock,
        "evaluate_text": eval_mock
    }

def test_main_success(mock_dependencies, capsys):
    """Test that main() runs successfully and prints the expected output."""
    main()
    
    # Check that run_agent_loop was called with correct arguments
    mock_dependencies["run_agent_loop"].assert_called_once()
    args = mock_dependencies["run_agent_loop"].call_args[1]
    assert args["scenario"] == "User submits a form without filling a required field"
    assert args["style"] == "Shopify inline error"
    assert args["max_iters"] == 5
    assert "forbidden_file" in args
    
    # Check that evaluate_text was called with the result from run_agent_loop
    mock_dependencies["evaluate_text"].assert_called_once_with("This is a test error message.")
    
    # Check the printed output
    captured = capsys.readouterr()
    assert "--- AI Evaluation ---" in captured.out
    assert "Clarity (4/5)" in captured.out
    assert "The message is clear and concise" in captured.out
    assert "--- Final Text ---" in captured.out
    assert "This is a test error message" in captured.out

def test_main_with_low_clarity(mock_dependencies, capsys):
    """Test main() with a low clarity score from AI evaluation."""
    # Override evaluate_text mock for this test
    mock_dependencies["evaluate_text"].return_value = {
        "clarity_score": 2,
        "clarity_explanation": "The message is confusing.",
        "actionable": False,
        "actionability_comment": "No clear next steps provided."
    }
    
    main()
    
    captured = capsys.readouterr()
    assert "Clarity (2/5)" in captured.out
    assert "The message is confusing" in captured.out
    assert "No clear next steps provided" in captured.out
