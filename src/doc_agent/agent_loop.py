#agent_loop.py

#!/usr/bin/env python
"""
Agent loop that combines LLM drafting, static heuristics, AI‐lint fixes, 
and a final AI‐driven evaluation.
"""

import os
from typing import Dict
from doc_agent.evaluators.heuristics import run_heuristics
from doc_agent.draft import draft_copy_tool
from doc_agent.tools import lint_copy, build_fix

# Import the new evaluator
from doc_agent.evaluators.ai_eval import evaluate_text


def run_agent_loop(
    scenario: str,
    style: str,
    forbidden_file: str,
    max_iters: int = 10,
) -> str:
    """
    Returns the final, lint‐approved text after at most max_iters.
    """
    text = draft_copy_tool(scenario=scenario, style=style)

    for i in range(1, max_iters + 1):
        # 1️⃣ Static heuristics
        heur = run_heuristics(text, forbidden_file=forbidden_file)
        if heur["errors"]:
            fix_prompt = build_fix(heur["errors"])
            print(f"🔧 Iter {i}: applying heuristic fixes → {fix_prompt}")
            text = draft_copy_tool(
                scenario=scenario,
                style=style,
                previous=text,
                fix=fix_prompt
            )
            continue

        # 2️⃣ AI‐based lint
        lint_result = lint_copy(text)
        if lint_result["status"] == "PASS":
            print(f"✅ Iter {i}: lint passed")
            break

        # 3️⃣ AI‐driven fix
        fix_prompt = build_fix(lint_result["errors"])
        print(f"🔧 Iter {i}: applying AI‐lint fixes → {fix_prompt}")
        text = draft_copy_tool(
            scenario=scenario,
            style=style,
            previous=text,
            fix=fix_prompt
        )
    else:
        raise RuntimeError(f"No PASS after {max_iters} iterations")

    return text


def main():
    here = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "evaluators", "forbidden_words.txt")

    # 0️⃣ Run the loop
    final = run_agent_loop(
        scenario="User submits a form without filling a required field",
        style="Shopify inline error",
        forbidden_file=forbidden_file,
        max_iters=5,
    )

    # 4️⃣ AI‐evaluation on the final draft
    eval_report = evaluate_text(final)
    print("\n--- AI Evaluation ---")
    print(f"Clarity ({eval_report['clarity_score']}/5): {eval_report['clarity_explanation']}")
    print(f"Actionable: {eval_report['actionable']}. {eval_report['actionability_comment']}")

    # 5️⃣ Print the final copy
    print("\n--- Final Text ---\n", final)


if __name__ == "__main__":
    main()
