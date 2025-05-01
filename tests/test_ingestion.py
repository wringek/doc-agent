# tests/test_ingestion.py

import pytest

from doc_agent.ingestion import ingest

def test_ingest_strips_comments_and_parses_metadata(tmp_path):
    sample = """
    /**
     * Adds two numbers.
     *
     * @param {number} a – The first addend.
     * @param {number} b – The second addend.
     * @returns {number} The sum of a and b.
     */
    function add(a, b) {
        return a + b; // sum
    }
    """
    file = tmp_path / "sample.js"
    file.write_text(sample)

    result = ingest(str(file))

    # Comments should be stripped from the 'source'
    assert "Adds two numbers" not in result["source"]
    assert "function add(a, b)" in result["source"]

    # Metadata fields
    assert result["name"] == "add"
    assert isinstance(result["params"], list) and len(result["params"]) == 2

    # First param
    p0 = result["params"][0]
    assert p0["name"] == "a"
    assert p0["type"] == "number"
    assert "first addend" in p0["description"]

    # Second param
    p1 = result["params"][1]
    assert p1["name"] == "b"
    assert p1["type"] == "number"
    assert "second addend" in p1["description"]

    # Returns
    ret = result["returns"]
    assert ret["type"] == "number"
    assert "sum" in ret["description"]
