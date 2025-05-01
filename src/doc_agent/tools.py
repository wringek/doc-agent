# src/doc_agent/tools.py

from doc_agent.linters.short_description import lint

# A mapping from lint‐error messages → instructions your LLM can act on
ERROR_FIX_TEMPLATES = {
    "should start with an imperative-mood verb":
        "Remove any surrounding quotation marks and rewrite so the sentence begins with an imperative verb.",
    "exceeds 72 characters":
        "Shorten the sentence to no more than 72 characters.",
    "missing trailing period":
        "Add a period at the end of the sentence.",
    # You can add more mappings here as you introduce new lint rules...
}

def lint_copy(text: str) -> dict:
    """
    Run your short-description linter and return its JSON result.
    Expects {'status': 'PASS'|'FAIL', 'errors': [...]}
    """
    return lint(text)


def build_fix(errors: list[dict]) -> str:
    """
    Generate human-readable fix instructions from lint and heuristic errors.
    
    - Uses ERROR_FIX_TEMPLATES for known lint messages.
    - Passes through heuristic messages (which you craft dynamically).
    """
    instructions = []
    for err in errors:
        # err may be a dict with 'msg', or a plain string
        msg = err.get("msg") if isinstance(err, dict) else str(err)

        # If it’s already an instruction (heuristic), trust it
        if msg.lower().startswith("remove") or msg.lower().startswith("shorten"):
            instr = msg

        # Otherwise, look up a template for known lint errors
        else:
            instr = ERROR_FIX_TEMPLATES.get(
                msg,
                f"Please fix this issue: {msg}"  # fallback
            )

        instructions.append(instr)

    # Join them into one clear prompt
    return " ".join(instructions)