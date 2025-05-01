"""
Simple static heuristics for doc-agent:
- readability_grade: returns Flesch Reading Ease score
- forbidden_word_checks: finds forbidden words in text, loading from file if needed
- run_heuristics: aggregates checks
- load_forbidden_words: helper to read forbidden words from a file
"""
from typing import List, Dict
import os

# If you don't yet have textstat installed, add it to your dependencies:
# pip install textstat
try:
    import textstat
except ImportError:
    textstat = None


def readability_grade(text: str) -> float:
    """
    Return the Flesch Reading Ease score for the given text.
    Higher scores are easier to read.
    """
    if textstat:
        return textstat.flesch_reading_ease(text)
    raise RuntimeError("textstat not installed. Please install textstat to use readability metrics.")


def load_forbidden_words(file_path: str) -> List[str]:
    """
    Load forbidden words from a file, one per line.
    Ignores empty lines and lines starting with '#'.
    """
    words: List[str] = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            words.append(line)
    return words


def forbidden_word_checks(
    text: str,
    forbidden_words: List[str] = None,
    file_path: str = None
) -> List[str]:
    """
    Return a list of forbidden words found in the text (case-insensitive).
    Provide either a list of words or a file_path to load them.
    Only matches whole words, not substrings.
    """
    if forbidden_words is None:
        if file_path:
            forbidden_words = load_forbidden_words(file_path)
        else:
            raise ValueError(
                "Must provide either 'forbidden_words' list or 'file_path' to load them."
            )
    
    # Split text into words and convert to lowercase
    words = text.lower().split()
    # Only match whole words
    return [w for w in forbidden_words if w.lower() in words]


def run_heuristics(
    text: str,
    forbidden_words: List[str] = None,
    forbidden_file: str = None
) -> Dict[str, object]:
    """
    Run all heuristics and return a summary dict.
    If forbidden_words is None, will load from forbidden_file.
    """
    if forbidden_words is None and forbidden_file:
        forbidden_words = load_forbidden_words(forbidden_file)

    return {
        "readability": readability_grade(text),
        "forbidden": forbidden_word_checks(
            text, forbidden_words=forbidden_words, file_path=None
        ),
    }


if __name__ == "__main__":
    # Demo loop showing how to use these heuristics in your agent
    from src.tools.draft_copy_tool import draft_copy_tool
    from src.tools.lint_copy_tool import lint_copy_tool
    from src.tools.agent import build_fix

    scenario = "User submits a form without filling a required field"
    style = "Shopify inline error"

    # locate forbidden words file in same directory as heuristics.py
    here = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "forbidden_words.txt")

    # ensure you have a 'forbidden_words.txt' file alongside this script
    text = draft_copy_tool(scenario=scenario, style=style)

    # Loop until lint passes
    for i in range(10):
        print(f"Iteration {i+1}")
        # Static heuristics
        metrics = run_heuristics(text, forbidden_file=forbidden_file)
        print("Heuristic metrics:", metrics)

        # Lint via AI rules
        lint = lint_copy_tool(text)
        if lint.get("status") == "PASS":
            print("PASS ✅")
            break

        # Build a fix prompt based on lint errors
        fix_instructions = build_fix(lint.get("errors", []))
        print("Applying fix prompt:", fix_instructions)
        text = draft_copy_tool(
            scenario=scenario,
            style=style,
            fix=fix_instructions,
        )
    else:
        print("❌ Failed to meet lint rules after 10 iterations")

    print("Final text:\n", text)
