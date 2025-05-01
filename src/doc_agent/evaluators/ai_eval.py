import openai
import json
from typing import Dict, List, Optional, Any
from functools import wraps

# ─── CLARITY & ACTIONABILITY ───────────────────────────────

def get_openai_client() -> openai.OpenAI:
    """Get or create an OpenAI client instance."""
    return openai.OpenAI()

def handle_openai_call(func):
    """Decorator to handle OpenAI API calls and error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            client = kwargs.pop('client', None) or get_openai_client()
            prompt = func(*args, **kwargs)
            resp = client.chat.completions.create(
                model=kwargs.get('model', "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.0),
            )
            raw = resp.choices[0].message.content.strip()
            return json.loads(raw)
        except Exception as e:
            print(f"Error evaluating text: {str(e)}")
            return {
                # Clarity fields
                "clarity_score": 0,
                "clarity_explanation": "Error during evaluation",
                "actionable": False,
                "actionability_comment": "Error during evaluation",
                # Tone fields
                "tone_score": 0,
                "tone_alignment": False,
                "tone_explanation": "Error during evaluation",
                # Empathy fields
                "empathy_score": 0,
                "empathy_explanation": "Error during evaluation",
                "empathy_suggestions": "Error during evaluation"
            }
    return wrapper

@handle_openai_call
def evaluate_clarity_and_actionability(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    1) Rates clarity on a scale 1–5
    2) Checks whether it's immediately actionable
    Returns JSON:
      {
        "clarity_score": 4,
        "clarity_explanation": "...",
        "actionable": true,
        "actionability_comment": "..."
      }
    """
    return f"""
You are an expert UX writer. Evaluate the following error message:

\"\"\"{text}\"\"\"

1) Rate its clarity on a scale of 1 (confusing) to 5 (crystal-clear).  
2) Is it immediately actionable? (Yes/No).  
3) For each, provide a brief explanation.

Respond ONLY with a JSON object, for example:
{{
  "clarity_score": 4,
  "clarity_explanation": "It's straightforward and uses clear verbs.",
  "actionable": true,
  "actionability_comment": "It tells the user exactly which fields to fill."
}}
"""


# ─── TONE & BRAND VOICE ────────────────────────────────────

@handle_openai_call
def evaluate_tone(
    text: str,
    brand_voice: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Checks how well `text` matches the specified `brand_voice` (e.g. "friendly and empathetic").
    Returns:
      {
        "tone_score": 1–5 int,
        "tone_alignment": true|false,
        "explanation": "…"
      }
    """
    return f"""
You are a brand voice expert. The desired voice is: {brand_voice}

Evaluate this message:

\"\"\"{text}\"\"\"

1) On a scale of 1 (not at all) to 5 (perfectly), how well does this match?
2) Does it use appropriate formality and friendliness? (Yes/No)
3) Briefly explain any mismatches.

Respond ONLY with JSON, for example:
{{
  "tone_score": 4,
  "tone_alignment": true,
  "explanation": "Language is polite but could be more empathetic."
}}
"""


# ─── EMPATHY & USER COMFORT ───────────────────────────────

@handle_openai_call
def evaluate_empathy(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Checks whether the message expresses empathy and avoids blaming language.
    Returns:
      {
        "empathetic": true|false,
        "suggestion": "Add an empathetic opening sentence."
      }
    """
    return f"""
You are an expert UX writer focused on empathy in user messaging.

Evaluate this message:

\"\"\"{text}\"\"\"

- Does it acknowledge user frustration or confusion? (Yes/No)
- Does it avoid blaming language? (Yes/No)
- If empathy is missing, suggest one brief sentence to add.

Respond ONLY with JSON, for example:
{{
  "empathetic": false,
  "suggestion": "Add 'We're here to help–let's get this sorted out together.'"
}}
"""

# ─── INCLUSIVITY & BIAS SCREENING───────────────────────────────────────────
@handle_openai_call
def evaluate_inclusivity(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Flags any potentially biased or exclusionary language.
    Returns:
    {
      "inclusive": true|false,
      "issues": ["<flag1>", "<flag2>"],
      "suggestions": ["<alt1>", "<alt2>"]
    }
    """
    return f"""
You are an inclusivity reviewer. Identify any non-inclusive or biased phrasing in this message:

\"\"\"{text}\"\"\"

- List the exact words or phrases to change.
- Provide a neutral alternative for each.

Respond in JSON, for example:
{{
  "inclusive": false,
  "issues": ["master/slave terminology"],
  "suggestions": ["primary/replica"]
}}
"""


# ─── READABILITY FOR NON-NATIVE SPEAKERS ───────────────────────────────

@handle_openai_call
def evaluate_readability_for_non_native(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Rates how easy the text is for non-native English speakers.
    Returns:
    {
      "readability_non_native": <1–5 int>,
      "simplification_suggestions": ["<…>", …]
    }
    """
    return f"""
You are an expert in plain English for global audiences.

Rate this message's ease for non-native speakers on a 1–5 scale.
If below 3, suggest up to two simplifications.

Message:
\"\"\"{text}\"\"\"

Respond only with JSON:
{{
  "readability_non_native": 3,
  "simplification_suggestions": [
    "Replace 'resubmitting' with 'sending again'"
  ]
}}
"""

# ─── COGNITIVE LOAD & CONCISENESS ───────────────────────────────────────────────

@handle_openai_call
def evaluate_conciseness(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Identifies phrases that can be shortened without losing meaning.
    Returns:
    {
      "concise": true|false,
      "suggestions": ["<alt phrase1>", …]
    }
    """
    return f"""
You are a copy editor focused on brevity.

Identify any wordy or redundant phrases in this message and suggest more concise alternatives.

Message:
\"\"\"{text}\"\"\"

Respond only with JSON:
{{
  "concise": false,
  "suggestions": [
    "'before submitting' → 'prior to submit'",
    …
  ]
}}
"""

# ─── ACCESSIBILITY COMPLIANCE ───────────────────────────────────────────────

@handle_openai_call
def evaluate_accessibility(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Flags screen-reader pitfalls (ambiguous pronouns, all-caps acronyms, etc.).
    Returns:
    {
      "accessible": true|false,
      "issues": ["<issue1>", …],
      "recommendations": ["<rec1>", …]
    }
    """
    return f"""
You are an accessibility consultant for UI text.

Inspect this message for screen-reader issues (e.g., ambiguous pronouns, acronyms).

Message:
\"\"\"{text}\"\"\"

Respond only with JSON:
{{
  "accessible": false,
  "issues": ["Pronoun 'it' with no clear antecedent"],
  "recommendations": ["Use 'your form' instead of 'it'"]
}}
"""

# ─── CONSISTENCY ACROSS MESSAGES ─────────────────────────────────────────────── 

@handle_openai_call
def evaluate_consistency(
    text: str,
    others: List[str],
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Compares `text` against a list of other messages for style/term consistency.
    Returns:
    {
      "consistent": true|false,
      "inconsistencies": [{"term": "<t>", "suggestion": "<alt>"}, …]
    }
    """
    return f"""
You are a UX writing style enforcer. Compare this message to these examples:
{others}

Message:
\"\"\"{text}\"\"\"

List any inconsistent terminology or style choices and propose corrections.

Respond with JSON:
{{
  "consistent": false,
  "inconsistencies": [
    {{"term": "resubmit", "suggestion": "submit again"}}
  ]
}}
"""




# ─── USER TRUST & CONFIDENCE ───────────────────────────────────────────────

@handle_openai_call
def evaluate_trust(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Rates how likely this message is to maintain user trust (1–5)
    and explains why.
    Returns:
    {
      "trust_score": <1–5>,
      "explanation": "<…>"
    }
    """
    return f"""
You are a user-experience psychologist. On a scale of 1 (undermines trust) 
to 5 (builds strong trust), rate this message and briefly explain why.

Message:
\"\"\"{text}\"\"\"

Respond only with JSON:
{{
  "trust_score": 4,
  "explanation": "It is clear but could use a more reassuring tone."
}}
"""

# ─── INTERNATIONALIZATION & TRANSLATION READINESS  ───────────────────────────────────────────────


@handle_openai_call
def evaluate_i18n(
    text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    client: Optional[openai.OpenAI] = None
) -> Dict[str, Any]:
    """
    Flags locale-specific formatting or idioms that could break in translation.
    Returns:
    {
      "i18n_ready": true|false,
      "issues": ["<issue1>", …],
      "recommendations": ["<rec1>", …]
    }
    """
    return f"""
You are a localization engineer. Identify any locale-specific 
formats, idioms, or plurals in this message that may not translate well.

Message:
\"\"\"{text}\"\"\"

Respond only with JSON:
{{
  "i18n_ready": false,
  "issues": ["'resubmitting' might translate awkwardly"],
  "recommendations": ["Use 'send again' instead"]
}}
"""

