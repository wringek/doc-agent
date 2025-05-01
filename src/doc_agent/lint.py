# src/agent/lint.py

from doc_agent.tools import draft_copy, lint_copy

MAX_LINT_ITERATIONS = 5  # prevent infinite loops

def self_lint(filled_sections: dict) -> dict:
    """
    Run draft_copy -> lint_copy loop until PASS for each section.
    Handles both dict- and string-based errors from linters.
    Outputs debug messages to trace progress and stops after a max number of retries.
    """
    final = {}
    for name, text in filled_sections.items():
        print(f"[self_lint] Starting lint for section: {name}")
        doc = text
        iteration = 0
        while True:
            iteration += 1
            print(f"[self_lint] Section '{name}', iteration {iteration}")
            if iteration > MAX_LINT_ITERATIONS:
                print(f"[self_lint] Warning: Section '{name}' still failing after {iteration-1} attempts, skipping further fixes.")
                break

            result = lint_copy(doc, section=name)
            if result.get("status") == "PASS":
                print(f"[self_lint] Section '{name}' passed lint.")
                break

            errors = result.get("errors") or []
            fixes = [e["msg"] if isinstance(e, dict) and "msg" in e else str(e) for e in errors]
            print(f"[self_lint] Section '{name}' failed lint. Errors: {fixes}")
            print(f"[self_lint] Applying fixes and requesting new draft...")
            doc = draft_copy(text=doc, fix="\n".join(fixes))

        final[name] = doc
    return final
