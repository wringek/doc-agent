from doc_agent.linters.short_description import lint

def test_happy_path():
    txt = "Returns an OAuth token for the current user."
    assert lint(txt)["status"] == "PASS"

def test_multi_line_fails():
    txt = "Returns a token.\nIt is used for X."
    rep = lint(txt)
    assert rep["status"] == "FAIL"
    assert "one physical line" in rep["errors"]
