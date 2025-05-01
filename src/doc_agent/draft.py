# src/agent/draft.py

import os
import time
import openai
import json
from typing import Dict
from httpx import HTTPError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fallback if openai.error.Timeout isn't available
try:
    from openai.error import Timeout as OpenAITimeout
except ImportError:
    OpenAITimeout = Exception

# Configure OpenAI API key and default timeout
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.request_timeout = 15

def fill_sections(sections: Dict[str, str], source: str) -> Dict[str, str]:
    """
    Generate content for each documentation section.

    - Pass through 'title', 'usage', and 'arguments' unchanged.
    - Draft 'summary', 'purpose', 'returns', and 'examples' with section-specific prompts.
    """
    filled: Dict[str, str] = {}

    # 1) Pass-through static sections
    for key in ("title", "usage", "arguments"):
        if key in sections:
            filled[key] = sections[key]

    # 2) Draftable sections
    for name in ("summary", "purpose", "returns", "examples"):
        if name not in sections:
            continue

        if name == "summary":
            prompt = (
                "You are a concise technical writer using Shopify Polaris style.\n"
                "Write exactly one sentence (≤72 characters), in imperative mood,\n"
                "summarizing what this function does. No markdown headings.\n\n"
                f"{source}\n\n"
                "Summary:"
            )

        elif name == "returns":
            prompt = (
                "You are a technical writer using Shopify Polaris style.\n"
                "Generate *only* the return value type and what it represents,\n"
                "in the exact format `<type> – <description>`.\n"
                "Do NOT start with the word 'Returns' or form a full sentence.\n\n"
                "(type and meaning). **Do not** write any retail return policies or shipping/returns instructions—just the function's return value."
                f"{source}\n\n"
                "Return value (type and description):"
            )

        elif name == "purpose":
            prompt = (
                "You are a technical writer using Shopify Polaris style.\n"
                "Write a short paragraph explaining why a developer would use this function.\n\n"
                f"{source}\n\n"
                "Purpose:"
            )
        else:  # examples
            prompt = (
                "You are a technical writer using Shopify Polaris style.\n"
                "Provide up to two JavaScript code examples demonstrating how to use this function.\n"
                "For each example, first write a very brief sentence (1–2 lines) explaining what it shows,\n"
                "then include the code block itself.\n\n"
                f"{source}\n\n"
                "Examples:"
            )

        # 3) Retry logic for API calls
        attempts = 0
        while True:
            try:
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": prompt}],
                    temperature=0,
                    timeout=15
                )
                raw = resp.choices[0].message.content.strip()
                # Strip any accidental markdown headings
                lines = [line for line in raw.splitlines() if not line.lstrip().startswith("#")]
                filled[name] = "\n".join(lines).strip()
                break

            except (HTTPError, OpenAITimeout) as e:
                attempts += 1
                if attempts >= 3:
                    raise RuntimeError(f"Failed to draft '{name}' after {attempts} attempts: {e}")
                time.sleep(2 ** attempts)

    return filled

def draft_copy_tool(scenario: str, style: str, previous: str = None, fix: str = None) -> str:
    """
    Generate or improve text based on a scenario and style.
    
    Args:
        scenario: Description of the situation to write about
        style: Writing style to use (e.g., "Shopify inline error")
        previous: Optional previous version of the text to improve
        fix: Optional fix instructions to apply
        
    Returns:
        Generated or improved text
    """
    if previous and fix:
        prompt = (
            f"You are a technical writer using {style} style.\n"
            f"Improve the following text by applying these fixes: {fix}\n\n"
            f"Previous text:\n{previous}\n\n"
            "Improved text:"
        )
    else:
        prompt = (
            f"You are a technical writer using {style} style.\n"
            f"Write text for this scenario: {scenario}\n\n"
            "Text:"
        )
    
    # Retry logic for API calls
    attempts = 0
    while True:
        try:
            resp = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                timeout=15
            )
            return resp.choices[0].message.content.strip()
            
        except (HTTPError, OpenAITimeout) as e:
            attempts += 1
            if attempts >= 3:
                raise RuntimeError(f"Failed to generate text after {attempts} attempts: {e}")
            time.sleep(2 ** attempts)
