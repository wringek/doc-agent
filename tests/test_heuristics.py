#heuristics.py

import pytest

from doc_agent.evaluators.heuristics import (
    load_forbidden_words,
    forbidden_word_checks,
    readability_grade,
    sentence_length_issues,
    passive_voice_issues,
    weasel_word_issues,
    acronym_issues,
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
    found = forbidden_word_checks(text, words)
    assert len(found) == 3  # All three words are found
    assert any(f["word"] == "please" for f in found)
    assert any(f["word"] == "streamline" for f in found)
    assert any(f["word"] == "seamless" for f in found)

def test_forbidden_word_checks_path(fw_file):
    text = "Please streamline this seamlessly."
    found = forbidden_word_checks(text, ["please", "streamline"])
    assert len(found) == 2
    assert any(f["word"] == "please" for f in found)
    assert any(f["word"] == "streamline" for f in found)

def test_readability_grade_range():
    # Simple sentence should score higher (easier) than a complex one
    simple = "The cat sat on the mat."
    complex = "The feline positioned itself upon the horizontal surface designed for floor covering."
    assert readability_grade(simple) > readability_grade(complex)

def test_sentence_length_issues():
    text = "This is a short sentence. This is a very long sentence that should be flagged because it exceeds the maximum word count limit."
    issues = sentence_length_issues(text, max_words=10)
    assert len(issues) == 1
    assert "exceeds 10 words" in issues[0]["msg"]

def test_passive_voice_issues():
    text = "The ball was thrown. The game was played. The score was kept."
    issues = passive_voice_issues(text, threshold=0.5)
    assert len(issues) == 1
    assert "passive voice" in issues[0]["msg"]

def test_weasel_word_issues():
    text = "This is very good, just perfect, basically amazing."
    issues = weasel_word_issues(text)
    assert len(issues) == 3
    assert any(f["word"] == "very" for f in issues)
    assert any(f["word"] == "just" for f in issues)
    assert any(f["word"] == "basically" for f in issues)

def test_acronym_issues():
    text = "The API was used to fetch JSON data from the DB."
    issues = acronym_issues(text)
    assert len(issues) == 3
    assert any(f["acronym"] == "API" for f in issues)
    assert any(f["acronym"] == "JSON" for f in issues)
    assert any(f["acronym"] == "DB" for f in issues)
