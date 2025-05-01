import openai
import json
from typing import Dict

def evaluate_text(
    text: str, 
    model: str = "gpt-4o-mini",
    temperature: float = 0.0
) -> Dict[str, object]:
    """
    Ask the LLM to rate clarity and actionability.
    Returns e.g.:
      {
        "clarity_score": 4,
        "clarity_explanation": "...",
        "actionable": True,
        "actionability_comment": "..."
      }
    """
    prompt = f"""
You are an expert UX writer. Evaluate the following error message:

\"\"\"{text}\"\"\"

1) Rate its clarity on a scale of 1 (confusing) to 5 (crystal-clear).  
2) Is it immediately actionable? (Yes/No).  
3) For each, provide a brief explanation.

Respond in JSON, for example:
{{
  "clarity_score": 4,
  "clarity_explanation": "...",
  "actionable": true,
  "actionability_comment": "..."
}}
"""
    client = openai.OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        temperature=temperature,
    )
    raw = resp.choices[0].message.content.strip()
    return json.loads(raw)
