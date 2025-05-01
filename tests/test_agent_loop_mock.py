import pytest

# Import the loop function
from doc_agent.agent_loop import run_agent_loop

@pytest.fixture
def fake_forbidden_file(tmp_path):
    # We won't actually read this file in our fake heuristics
    p = tmp_path / "forbidden.txt"
    p.write_text("please\n")
    return str(p)

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    """
    Replace draft_copy_tool, run_heuristics, and lint_copy with fakes
    so we can simulate:
      1. A heuristic failure on the first draft
      2. A lint failure on the second draft
      3. Success on the third draft
    """
    # 1) Fake drafts sequence
    drafts = ["first", "second", "final"]
    counter = {"n": 0}

    def fake_draft(scenario, style, previous=None, fix=None):
        idx = min(counter["n"], len(drafts) - 1)
        text = drafts[idx]
        counter["n"] += 1
        return text

    monkeypatch.setattr(
        "doc_agent.agent_loop.draft_copy_tool", fake_draft
    )

    # 2) Fake heuristics: fail only on "first"
    def fake_heur(text, forbidden_file):
        if text == "first":
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

    monkeypatch.setattr(
        "doc_agent.agent_loop.run_heuristics", fake_heur
    )

    # 3) Fake lint: fail on "second", pass otherwise
    def fake_lint(text):
        if text == "second":
            return {"status": "FAIL", "errors": [{"msg": "dummy"}]}
        return {"status": "PASS", "errors": []}

    monkeypatch.setattr(
        "doc_agent.agent_loop.lint_copy", fake_lint
    )

    # 4) Fake build_fix to a no-op (not under test here)
    monkeypatch.setattr(
        "doc_agent.agent_loop.build_fix", lambda errors: "FIX"
    )

def test_loop_converges_in_three_steps(fake_forbidden_file):
    final = run_agent_loop(
        scenario="irrelevant",
        style="irrelevant",
        forbidden_file=fake_forbidden_file,
        max_iters=5,
    )
    assert final == "final"

def test_loop_raises_on_max_iters(fake_forbidden_file):
    # Reset counter by calling run_agent_loop with max_iters=1
    with pytest.raises(RuntimeError, match="No PASS after 1 iterations"):
        run_agent_loop(
            scenario="irrelevant",
            style="irrelevant",
            forbidden_file=fake_forbidden_file,
            max_iters=1,
        )
