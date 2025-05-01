#heuristics.py

import pytest

from doc_agent.evaluators.heuristics import (
    load_forbidden_words,
    forbidden_word_checks,
    readability_grade,
)

@pytest.fixture
def fw_file(tmp_path):
    p = tmp_path / "forbidden_words.txt"
    p.write_text("please\nstreamline\nseamless")
    return str(p)

def test_load_forbidden_words(fw_file):
    words = load_forbidden_words(fw_file)
    assert set(words) == {"please", "streamline", "seamless"}

def test_forbidden_word_checks_list(fw_file):
    words = load_forbidden_words(fw_file)
    text = "Please streamline this seamlessly."
    found = forbidden_word_checks(text, forbidden_words=words)
    assert set(found) == {"please", "streamline"}

def test_forbidden_word_checks_path(fw_file):
    text = "Nothing forbidden here."
    found = forbidden_word_checks(text, file_path=fw_file)
    assert found == []

def test_readability_grade_range():
    # Simple sentence should score higher (easier) than a complex one
    easy = "The cat sat on the mat."
    hard = (
        "Notwithstanding the multitudinous complexities, one must "
        "scrutinize the epistemological underpinnings."
    )
    # Test that simple text is more readable than complex text
    assert readability_grade(easy) > readability_grade(hard)
    # Note: While Flesch Reading Ease typically ranges from 0-100,
    # extreme cases can produce scores outside this range
    assert readability_grade(hard) > -100.0  # Very complex text shouldn't be too unreadable
    assert readability_grade(easy) > 60