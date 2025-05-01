import pytest
from unittest.mock import Mock, MagicMock, patch
from doc_agent.agent_loop import main
from doc_agent.evaluators.ai_eval import get_openai_client

@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client with predefined responses."""
    client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = '''{
        "clarity_score": 4,
        "clarity_explanation": "The message is clear and concise.",
        "actionable": true,
        "actionability_comment": "User knows what to do next.",
        "tone_score": 4,
        "tone_alignment": true,
        "tone_explanation": "The tone is friendly and empathetic.",
        "empathy_score": 4,
        "empathy_explanation": "The message shows understanding.",
        "empathy_suggestions": "Add more personal touch."
    }'''
    client.chat.completions.create.return_value = mock_completion
    return client

@pytest.fixture
def mock_dependencies(mock_openai_client):
    """Mock all dependencies for the main function."""
    with patch("doc_agent.agent_loop.run_agent_loop") as mock_run_agent_loop, \
         patch("doc_agent.evaluators.ai_eval.get_openai_client", return_value=mock_openai_client):
        mock_run_agent_loop.return_value = "This is a test error message."
        yield {
            "openai_client": mock_openai_client,
            "run_agent_loop": mock_run_agent_loop
        }

def test_main_success(mock_dependencies, capsys):
    """Test that main() runs successfully and prints the expected output."""
    main()
    captured = capsys.readouterr()
    assert "--- AI Evaluations ---" in captured.out
    assert "Clarity (4/5)" in captured.out
    assert "Tone (4/5, aligned=True)" in captured.out
    assert "Empathy (4/5)" in captured.out

def test_main_with_low_clarity(mock_dependencies, capsys):
    """Test main() with a low clarity score from AI evaluation."""
    # Override the mock completion response for clarity evaluation
    mock_client = mock_dependencies["openai_client"]
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = '''{
        "clarity_score": 2,
        "clarity_explanation": "The message is confusing.",
        "actionable": false,
        "actionability_comment": "No clear next steps provided.",
        "tone_score": 3,
        "tone_alignment": false,
        "tone_explanation": "The tone could be more friendly.",
        "empathy_score": 2,
        "empathy_explanation": "The message lacks empathy.",
        "empathy_suggestions": "Show more understanding."
    }'''
    mock_client.chat.completions.create.return_value = mock_completion

    main()
    captured = capsys.readouterr()
    assert "Clarity (2/5)" in captured.out
    assert "Actionable? False" in captured.out

def test_main_with_api_error(mock_dependencies, capsys):
    """Test main() handles OpenAI API errors gracefully."""
    # Make the OpenAI client raise an error
    mock_client = mock_dependencies["openai_client"]
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    main()
    captured = capsys.readouterr()
    assert "Error evaluating text" in captured.out
    assert "API Error" in captured.out

def test_main_with_json_error(mock_dependencies, capsys):
    """Test main() handles JSON parsing errors gracefully."""
    # Make the OpenAI client return invalid JSON
    mock_client = mock_dependencies["openai_client"]
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = "Invalid JSON"
    mock_client.chat.completions.create.return_value = mock_completion

    main()
    captured = capsys.readouterr()
    assert "Error evaluating text" in captured.out
    assert "Expecting value" in captured.out  # This is the actual error message from json.loads
