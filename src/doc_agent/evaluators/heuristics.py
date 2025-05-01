"""
Simple static heuristics for doc-agent:

- load_forbidden_words: helper to read forbidden words from a file
- forbidden_word_checks: finds forbidden words in text
- readability_grade: returns Flesch Reading Ease score
- sentence_length_issues: flags sentences over N words
- passive_voice_issues: flags high passive-voice %
- weasel_word_issues: catches words like "very", "just"
- acronym_issues: detects all-caps tokens (ACRONYMS)
- run_heuristics: aggregates all of the above into a single report
"""

import os
import re
from typing import List, Dict
from textstat import flesch_reading_ease

# --- CONFIGURATION ---
MAX_WORDS_PER_SENTENCE = 20
PASSIVE_REGEX = re.compile(r'\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en|t)\b', re.IGNORECASE)
WEASEL_WORDS = {
    "very", "just", "basically", "in order to", "actually", "really", "fairly", "quite"
}
ACRONYM_PATTERN = re.compile(r'\b([A-Z]{2,})s?\b')


# --- HELPERS ---
def load_forbidden_words(file_path: str) -> List[str]:
    words: List[str] = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            words.append(line)
    return words


def forbidden_word_checks(text: str, forbidden_list: List[str]) -> List[Dict]:
    found = []
    lowered_text = text.lower()
    for w in forbidden_list:
        # Use regex to find word boundaries and handle variations
        pattern = rf'\b{re.escape(w)}(?:ly|ing|ed|s|es)?\b'
        if re.search(pattern, lowered_text, re.IGNORECASE):
            found.append({"msg": f"forbidden word: {w}", "word": w})
    return found


def readability_grade(text: str) -> float:
    return flesch_reading_ease(text)


def sentence_length_issues(text: str, max_words: int = MAX_WORDS_PER_SENTENCE) -> List[Dict]:
    issues = []
    for sent in re.split(r'(?<=[.!?])\s+', text.strip()):
        if len(sent.split()) > max_words:
            issues.append({
                "msg": f"sentence exceeds {max_words} words",
                "sentence": sent
            })
    return issues


def passive_voice_issues(text: str, threshold: float = 0.1) -> List[Dict]:
    sentences = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s]  # Filter out empty strings
    if not sentences:
        return []
    passive_count = sum(1 for s in sentences if PASSIVE_REGEX.search(s))
    ratio = passive_count / len(sentences)
    if ratio >= threshold:  # Changed from > to >= to match test case
        return [{"msg": f"passive voice > {int(threshold * 100)}% of sentences", "ratio": ratio}]
    return []


def weasel_word_issues(text: str) -> List[Dict]:
    found = [w for w in WEASEL_WORDS if re.search(rf'\b{re.escape(w)}\b', text, re.IGNORECASE)]
    return [{"msg": f"weasel word: {w}", "word": w} for w in found]


def acronym_issues(text: str) -> List[Dict]:
    found = set(ACRONYM_PATTERN.findall(text))
    return [{"msg": f"acronym detected: {a}", "acronym": a} for a in found]


# --- AGGREGATOR ---
def run_heuristics(text: str, forbidden_file: str) -> Dict[str, object]:
    """
    Runs every static check and returns:
      {
        "readability": <float>,
        "forbidden": [<words>],
        "errors": [ {msg:…, …}, … ]
      }
    """
    forbidden_list = load_forbidden_words(forbidden_file)
    errors: List[Dict] = []

    # 1. Forbidden words
    errors.extend(forbidden_word_checks(text, forbidden_list))

    # 2. Sentence length
    errors.extend(sentence_length_issues(text))

    # 3. Passive voice
    errors.extend(passive_voice_issues(text))

    # 4. Weasel words
    errors.extend(weasel_word_issues(text))

    # 5. Acronyms
    errors.extend(acronym_issues(text))

    return {
        "readability": readability_grade(text),
        "forbidden": [e["word"] for e in errors if e["msg"].startswith("forbidden word")],
        "errors": errors
    }


# --- DEMO BLOCK ---
if __name__ == "__main__":
    from doc_agent.agent.draft import draft_copy_tool
    from doc_agent.tools import lint_copy, build_fix

    scenario = "User submits a form without filling a required field"
    style    = "Shopify inline error"
    here     = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "forbidden_words.txt")

    text = draft_copy_tool(scenario=scenario, style=style)

    for i in range(1, 6):
        print(f"\nIteration {i}")
        heur = run_heuristics(text, forbidden_file)
        print("Heuristic report:", heur)

        lint = lint_copy(text)
        if lint["status"] == "PASS":
            print("PASS ✅")
            break

        fix = build_fix(lint["errors"])
        print("Applying fix:", fix)
        text = draft_copy_tool(scenario=scenario, style=style, previous=text, fix=fix)

    print("\nFinal text:\n", text)
