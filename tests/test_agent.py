import pytest
from doc_agent.agent import run_agent

def test_agent_pass_path():
    """Test the agent loop with all evaluators passing."""
    # Stub evaluators that always pass
    def stub_evaluator1(text: str) -> dict:
        return {"status": "PASS"}
    
    def stub_evaluator2(text: str) -> dict:
        return {"status": "PASS"}
    
    # Stub LLM that just returns the scenario
    def stub_llm(scenario: str, **kwargs) -> str:
        return scenario
    
    # Run the agent
    result = run_agent(
        scenario="Test scenario",
        style="Test style",
        evaluators=[stub_evaluator1, stub_evaluator2],
        llm=stub_llm,
        max_iters=5
    )
    
    # Verify the result structure
    assert isinstance(result, dict)
    assert result["text"] == "Test scenario"
    assert result["reports"] == "ALL_PASS"
    assert result["iterations"] == 1
    assert result["final_status"] == "success"
    assert len(result["final_reports"]) == 2
    for report in result["final_reports"]:
        assert report["status"] == "PASS"

def test_agent_fail_path():
    """Test the agent loop with one evaluator failing once."""
    # Track how many times each evaluator was called
    calls = {"evaluator1": 0, "evaluator2": 0}
    
    def stub_evaluator1(text: str) -> dict:
        calls["evaluator1"] += 1
        print(f"\nstub_evaluator1 called (call #{calls['evaluator1']})")
        # Fail on first call, pass on subsequent calls
        result = {"status": "FAIL", "error": "Test error"} if calls["evaluator1"] == 1 else {"status": "PASS"}
        print(f"stub_evaluator1 returning: {result}")
        return result
    
    def stub_evaluator2(text: str) -> dict:
        calls["evaluator2"] += 1
        print(f"\nstub_evaluator2 called (call #{calls['evaluator2']})")
        result = {"status": "PASS"}
        print(f"stub_evaluator2 returning: {result}")
        return result
    
    # Stub LLM that just returns the scenario with a suffix
    def stub_llm(scenario: str, **kwargs) -> str:
        print("\nstub_llm called")
        result = f"{scenario} (fixed)"
        print(f"stub_llm returning: {result}")
        return result
    
    print("\nStarting test_agent_fail_path")
    # Run the agent
    result = run_agent(
        scenario="Test scenario",
        style="Test style",
        evaluators=[stub_evaluator1, stub_evaluator2],
        llm=stub_llm,
        max_iters=5
    )
    
    print(f"\nFinal result: {result}")
    print(f"Final calls: {calls}")
    
    # Verify the result structure
    assert isinstance(result, dict)
    assert result["text"] == "Test scenario (fixed)"
    assert result["final_status"] == "success"
    assert result["iterations"] == 2
    
    # Verify evaluator1 was called twice (once failed, once passed)
    assert calls["evaluator1"] == 2
    # Verify evaluator2 was called twice (once before fix, once after)
    assert calls["evaluator2"] == 2

def test_agent_max_iterations():
    """Test the agent loop when max iterations is reached."""
    # Stub evaluator that always fails
    def stub_evaluator(text: str) -> dict:
        return {"status": "FAIL", "error": "Always fails"}
    
    # Stub LLM that just returns the scenario
    def stub_llm(scenario: str, **kwargs) -> str:
        return scenario
    
    # Run the agent with max_iters=2
    result = run_agent(
        scenario="Test scenario",
        style="Test style",
        evaluators=[stub_evaluator],
        llm=stub_llm,
        max_iters=2
    )
    
    # Verify the result structure
    assert isinstance(result, dict)
    assert result["text"] == "Test scenario"
    assert result["final_status"] == "failure"
    assert result["iterations"] == 2
    assert len(result["reports"]) == 1
    assert result["reports"][0][1] == "Always fails"  # Check error message 