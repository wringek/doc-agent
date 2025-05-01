#!/usr/bin/env python
"""
Agent loop that combines LLM drafting, static heuristics, AI‐lint fixes,
and a suite of AI‐driven evaluations (clarity, tone, empathy).
"""

import os
from typing import Dict
from doc_agent.evaluators.heuristics import run_heuristics
from doc_agent.draft import draft_copy_tool
from doc_agent.tools import lint_copy, build_fix

# Import your new evaluators individually
from doc_agent.evaluators.ai_eval import (
    evaluate_clarity_and_actionability,
    evaluate_tone,
    evaluate_empathy,
    # ...you can import more here as you add them
)


def run_agent_loop(
    scenario: str,
    style: str,
    forbidden_file: str,
    max_iters: int = 10,
) -> str:
    text = draft_copy_tool(scenario=scenario, style=style)

    for i in range(1, max_iters + 1):
        heur = run_heuristics(text, forbidden_file=forbidden_file)
        if heur["errors"]:
            fix_prompt = build_fix(heur["errors"])
            print(f"🔧 Iter {i}: heuristic fixes → {fix_prompt}")
            text = draft_copy_tool(
                scenario=scenario,
                style=style,
                previous=text,
                fix=fix_prompt,
            )
            continue

        lint_result = lint_copy(text)
        if lint_result["status"] == "PASS":
            print(f"✅ Iter {i}: lint passed")
            break

        fix_prompt = build_fix(lint_result["errors"])
        print(f"🔧 Iter {i}: lint fixes → {fix_prompt}")
        text = draft_copy_tool(
            scenario=scenario,
            style=style,
            previous=text,
            fix=fix_prompt,
        )
    else:
        raise RuntimeError(f"No PASS after {max_iters} iterations")

    return text


def main():
    here = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "evaluators", "forbidden_words.txt")

    # 1️⃣ Run your drafting/heuristics/lint loop
    final = run_agent_loop(
        scenario="User submits a form without filling the 'Email' field which is required",
        style="Shopify inline error - be direct, avoid 'please', use active voice",
        forbidden_file=forbidden_file,
        max_iters=5,
    )

    # 2️⃣ Now run your AI‐driven evaluations
    clarity = evaluate_clarity_and_actionability(final)
    tone    = evaluate_tone(final, brand_voice="friendly and empathetic")
    empathy = evaluate_empathy(final)

    # 3️⃣ Print out each report
    print("\n--- AI Evaluations ---")
    print(f"Clarity ({clarity['clarity_score']}/5): {clarity['clarity_explanation']}")
    print(f"Actionable? {clarity['actionable']}. {clarity['actionability_comment']}\n")

    print(f"Tone ({tone['tone_score']}/5, aligned={tone['tone_alignment']}):")
    print(f"  {tone['tone_explanation']}\n")

    print(f"Empathy ({4 if empathy['empathetic'] else 2}/5):")
    print(f"  {empathy['suggestion']}\n")

    print("--- Final Text ---")
    print(final)


if __name__ == "__main__":
    main()
