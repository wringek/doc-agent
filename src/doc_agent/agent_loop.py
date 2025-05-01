#!/usr/bin/env python
"""
Agent loop that combines heuristics and AI-based linting to improve text.
"""

import os
from typing import Dict, Any

from doc_agent.evaluators.heuristics import run_heuristics
from doc_agent.draft import draft_copy_tool
from doc_agent.tools import lint_copy
from doc_agent.tools import build_fix  # or wherever you keep it

def main(max_iters: int = 10):
    scenario = "User submits a form without filling a required field"
    style    = "Shopify inline error"

    here           = os.path.dirname(__file__)
    forbidden_file = os.path.join(here, "evaluators", "forbidden_words.txt")

    # 0️⃣ Seed initial draft
    text = draft_copy_tool(scenario=scenario, style=style)


    for i in range(1, 11):
        print(f"\n— Iteration {i} —")

        # 1️⃣ Run static heuristics first
        metrics = run_heuristics(text, forbidden_file=forbidden_file)
        print("Heuristic metrics:", metrics)
        if metrics.get("forbidden"):
            # Build and apply a heuristic fix
            fix_prompt = build_fix([{"msg": f"Remove forbidden words: {', '.join(metrics['forbidden'])}"}])
            print("🔧 Applying heuristic fix:", fix_prompt)
            text = draft_copy_tool(scenario=scenario, style=style, previous=text, fix=fix_prompt)
            continue
        else:
            print("✅ Heuristics clean")

        # 2️⃣ Now run the AI linter
        lint_result = lint_copy(text)
        if lint_result.get("status") == "PASS":
            print("🚀 Lint passed — done!")
            break

        # 3️⃣ Build and apply an AI‐driven fix
        print("⚠️ Lint errors:", lint_result["errors"])
        fix_prompt = build_fix(lint_result["errors"])
        print("🔧 Applying AI fix:", fix_prompt)
        text = draft_copy_tool(scenario=scenario, style=style, previous=text, fix=fix_prompt)
    else:
        print("❌ Exceeded max iterations without passing lint.")

    print("\n--- Final Text ---\n")
    print(text)


if __name__ == "__main__":
    main()
