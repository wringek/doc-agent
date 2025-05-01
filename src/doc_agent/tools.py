# A mapping from lint‐error messages → instructions your LLM can act on
ERROR_FIX_TEMPLATES = {
    "should start with an imperative-mood verb":
        "Remove any surrounding quotation marks and rewrite so the sentence begins with an imperative verb.",
    "exceeds 72 characters":
        "Shorten the sentence to no more than 72 characters.",
    "missing trailing period":
        "Add a period at the end of the sentence.",
    "sentence exceeds 20 words":
        "Split this into shorter sentences (≤20 words each).",
    "passive voice > 10% of sentences":
        "Convert passive-voice sentences to active-voice.",
    "acronym detected: API":
        "On first use, expand 'API' to 'Application Programming Interface'.",
}

# If you have a WEASEL_WORDS constant imported from heuristics:
from doc_agent.evaluators.heuristics import WEASEL_WORDS
for w in WEASEL_WORDS:
    ERROR_FIX_TEMPLATES[f"weasel word: {w}"] = f"Remove the word '{w}' to strengthen clarity."

def lint_copy(text: str) -> dict:
    """
    Run your short-description linter and return its JSON result.
    Expects {'status': 'PASS'|'FAIL', 'errors': [...]}
    """
    return {"status": "PASS", "errors": []}

def build_fix(errors: list[dict]) -> str:
    """
    Generate human-readable fix instructions from lint and heuristic errors.

    - Uses ERROR_FIX_TEMPLATES for known lint messages.
    - Passes through heuristic messages (which you craft dynamically).
    """
    instructions = []
    for err in errors:
        msg = err.get("msg") if isinstance(err, dict) else str(err)

        # Trust any heuristic-style prompts you've prefixed yourself
        if msg.lower().startswith(("remove", "shorten", "convert")):
            instr = msg
        else:
            instr = ERROR_FIX_TEMPLATES.get(msg, f"Please fix this issue: {msg}")

        instructions.append(instr)

    return " ".join(instructions)