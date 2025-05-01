# src/doc_agent/linters/short_description.py
import re
from textwrap import shorten

MAX_CHARS = 72
PATTERN_VERB_FIRST = re.compile(r"^[A-Z][a-z]+\s")        # crude but cheap

def check(line: str) -> list[str]:
    """Return a list of rule-violations for *line* (empty → PASS)."""
    errs = []
    if "\n" in line:
        errs.append("one physical line")
    if len(line) > MAX_CHARS:
        errs.append(f"exceeds {MAX_CHARS} characters")
    if not line.endswith("."):
        errs.append("missing trailing period")
    if not PATTERN_VERB_FIRST.match(line):
        errs.append("should start with an imperative-mood verb")
    if line.split()[0].lower() in {"this", "a", "an"}:
        errs.append("don't start with fillers like 'This ...'")
    return errs

def lint(docstring: str) -> dict:
    """Lint a docstring for short description rules."""
    # Check for newlines in the entire input first
    if "\n" in docstring:
        return {"status": "FAIL", "errors": ["one physical line"]}
    
    # Then process the first sentence
    first_sentence = shorten(docstring.split(".", 1)[0] + ".", MAX_CHARS + 5)
    errors = check(first_sentence.strip())
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}
