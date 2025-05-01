import pytest
from doc_agent.evaluators import all_evaluators, run_heuristics, run_rubric

def test_all_evaluators_list():
    """Test that all_evaluators contains the expected functions."""
    # Default evaluators include heuristics, rubric, and clarity
    assert len(all_evaluators) == 3
    
    # Check that we have evaluators for each type
    evaluator_names = {evaluator("test").name for evaluator in all_evaluators}
    assert "heuristics" in evaluator_names
    assert "rubric" in evaluator_names
    assert "clarity" in evaluator_names

def test_heuristics_evaluator():
    """Test the heuristics evaluator with a known-good string."""
    text = "Enter your email address to continue."
    result = run_heuristics(text, forbidden_file="src/doc_agent/evaluators/forbidden_words.txt")
    assert isinstance(result, dict)
    assert "readability" in result
    assert "forbidden" in result
    assert "errors" in result
    assert isinstance(result["readability"], float)
    assert isinstance(result["forbidden"], list)
    assert isinstance(result["errors"], list)

def test_rubric_evaluator():
    """Test the rubric evaluator with a known-good string."""
    text = "Enter your email address to continue."
    result = run_rubric(text)
    assert result["status"] == "PASS" 