import os
import pytest

# Import the function we just refactored
from doc_agent.agent_loop import run_agent_loop

class DummyError(Exception):
    pass

@pytest.fixture(autouse=True)
def patch_tools(monkeypatch, tmp_path):
    # 1️⃣ Fake forbidden_file path (not actually read in our fake run_heuristics)
    ff = tmp_path / "forbidden.txt"
    ff.write_text("please\n")
    forbidden_file = str(ff)

    # 2️⃣ Mock draft_copy_tool
    #   - first call returns "draft1"
    #   - second call (heuristic fix) returns "draft2"
    #   - third call (AI lint fix) returns "final_text."
    drafts = ["draft1", "draft2", "final_text."]
    call = {"n": 0}
    def fake_draft(scenario, style, previous=None, fix=None):
        idx = min(call["n"], len(drafts)-1)
        text = drafts[idx]
        call["n"] += 1
        return text
    monkeypatch.setattr("doc_agent.agent_loop.draft_copy_tool", fake_draft)

    # 3️⃣ Mock run_heuristics
    #   - On "draft1", return a forbidden‐word error
    #   - On "draft2" or later, return clean
    def fake_heur(text, forbidden_file):
        if text == "draft1":
            return {
                "readability": 0,
                "forbidden": ["please"],
                "errors": [{"msg": "forbidden word: please", "word": "please"}]
            }
        return {
            "readability": 0,
            "forbidden": [],
            "errors": []
        }
    monkeypatch.setattr("doc_agent.agent_loop.run_heuristics", fake_heur)

    # 4️⃣ Mock lint_copy
    #   - On "draft2", return FAIL with one error
    #   - On "final_text.", return PASS
    def fake_lint(text):
        if text == "draft2":
            return {"status": "FAIL", "errors": [{"msg": "some-lint-error"}]}
        return {"status": "PASS", "errors": []}
    monkeypatch.setattr("doc_agent.agent_loop.lint_copy", fake_lint)

    # 5️⃣ Monkeypatch build_fix to be a no-op (we just care draft sequence)
    monkeypatch.setattr("doc_agent.agent_loop.build_fix", lambda errors: "FIX")

    return {"forbidden_file": forbidden_file}

def test_run_agent_loop_converges(patch_tools):
    final = run_agent_loop(
        scenario="irrelevant",
        style="irrelevant",
        forbidden_file=patch_tools["forbidden_file"],
        max_iters=5,
    )
    # Our fake_draft sequence yields "final_text." on 3rd invocation
    assert final == "final_text."

def test_run_agent_loop_success():
    """Test that the agent loop can successfully generate valid text."""
    here = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "..", "src", "doc_agent", "evaluators", "forbidden_words.txt")
    
    result = run_agent_loop(
        scenario="User submits a form without filling a required field",
        style="Shopify inline error",
        forbidden_file=forbidden_file,
        max_iters=5,
    )
    
    # Check that the result is a string
    assert isinstance(result, str)
    # Check that it's not empty
    assert len(result.strip()) > 0
    # Check that it ends with a period
    assert result.strip().endswith(".")
    # Check that it doesn't start with a quote
    assert not result.strip().startswith('"')
    # Check that it's under 72 characters
    assert len(result.strip()) <= 72

def test_run_agent_loop_max_iterations():
    """Test that the agent loop raises an exception when max iterations is reached."""
    here = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "..", "src", "doc_agent", "evaluators", "forbidden_words.txt")
    
    with pytest.raises(RuntimeError, match="No PASS after 1 iterations"):
        run_agent_loop(
            scenario="User submits a form without filling a required field",
            style="Shopify inline error",
            forbidden_file=forbidden_file,
            max_iters=1,  # Set to 1 to force failure
        )
