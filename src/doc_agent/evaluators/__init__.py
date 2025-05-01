import os
import logging
from functools import partial
from typing import Dict, Any, List, Callable, Optional

from .heuristics import run_heuristics
from .rubric import run_rubric
from .types import EvalResult
from .ai_eval import (
    evaluate_clarity_and_actionability,
    evaluate_empathy,
    evaluate_tone
)

# Get the default path to the forbidden words file
FORBIDDEN_FILE = os.path.join(os.path.dirname(__file__), "forbidden_words.txt")

def make_heuristics_evaluator(forbidden_file: str = FORBIDDEN_FILE) -> Callable[[str], EvalResult]:
    """Create a heuristics evaluator with the given forbidden words file."""
    def _run(text: str) -> EvalResult:
        result = run_heuristics(text, forbidden_file=forbidden_file)
        
        if result["errors"]:
            logging.debug(f"Heuristics found {len(result['errors'])} issues")
            for error in result["errors"]:
                logging.debug(f"  - {error['msg']}")
            return EvalResult(
                name="heuristics",
                status="FAIL",
                error="\n".join(error["msg"] for error in result["errors"])
            )
        logging.debug("Heuristics passed")
        return EvalResult(name="heuristics", status="PASS")
    
    return _run

def make_rubric_evaluator() -> Callable[[str], EvalResult]:
    """Create a rubric evaluator."""
    def _run(text: str) -> EvalResult:
        result = run_rubric(text)
        logging.debug(f"Rubric evaluation: {result['status']}")
        return EvalResult(
            name="rubric",
            status=result["status"],
            error=result.get("error", "")
        )
    
    return _run

def make_ai_clarity_evaluator() -> Callable[[str], EvalResult]:
    """Create an AI clarity evaluator."""
    def _run(text: str) -> EvalResult:
        result = evaluate_clarity_and_actionability(text)
        if result["clarity_score"] < 3 or not result["actionable"]:
            return EvalResult(
                name="clarity",
                status="FAIL",
                error=f"Clarity: {result['clarity_explanation']}\nActionability: {result['actionability_comment']}"
            )
        return EvalResult(name="clarity", status="PASS")
    
    return _run

def make_ai_empathy_evaluator() -> Callable[[str], EvalResult]:
    """Create an AI empathy evaluator."""
    def _run(text: str) -> EvalResult:
        result = evaluate_empathy(text)
        if not result["empathetic"]:
            return EvalResult(
                name="empathy",
                status="FAIL",
                error=result["suggestion"]
            )
        return EvalResult(name="empathy", status="PASS")
    
    return _run

def make_ai_tone_evaluator() -> Callable[[str], EvalResult]:
    """Create an AI tone evaluator."""
    def _run(text: str) -> EvalResult:
        result = evaluate_tone(text, brand_voice="clear and professional")
        if result["tone_score"] < 3 or not result["tone_alignment"]:
            return EvalResult(
                name="tone",
                status="FAIL",
                error=result["tone_explanation"]
            )
        return EvalResult(name="tone", status="PASS")
    
    return _run

# Registry of available evaluator factories
FAST_EVALUATORS = {
    "heuristics": make_heuristics_evaluator,
    "rubric": make_rubric_evaluator
}

AI_EVALUATORS = {
    "clarity": make_ai_clarity_evaluator,
    "empathy": make_ai_empathy_evaluator,
    "tone": make_ai_tone_evaluator
}

# Combined registry
EVALUATOR_REGISTRY = {**FAST_EVALUATORS, **AI_EVALUATORS}

def get_evaluators(
    names: Optional[List[str]] = None,
    forbidden_file: str = FORBIDDEN_FILE,
    no_eval: bool = False,
    fast: bool = False
) -> List[Callable[[str], EvalResult]]:
    """Get a list of evaluator functions by name.
    
    Args:
        names: List of evaluator names to include. If None, includes default evaluators.
        forbidden_file: Path to the forbidden words file for heuristics evaluator.
        no_eval: If True, returns an empty list (skips all evaluation)
        fast: If True, only includes non-AI evaluators
        
    Returns:
        List of evaluator functions ready to use.
        
    Raises:
        ValueError: If an invalid evaluator name is provided.
    """
    if no_eval:
        return []
        
    if names is None:
        # Default evaluators based on mode
        if fast:
            names = list(FAST_EVALUATORS.keys())
        else:
            # Use fast evaluators plus minimal AI set
            names = list(FAST_EVALUATORS.keys()) + ["clarity"]
    
    evaluators = []
    for name in names:
        if name not in EVALUATOR_REGISTRY:
            raise ValueError(f"Unknown evaluator: {name}. Available: {', '.join(EVALUATOR_REGISTRY.keys())}")
        
        factory = EVALUATOR_REGISTRY[name]
        if name == "heuristics":
            evaluator = factory(forbidden_file=forbidden_file)
        else:
            evaluator = factory()
        evaluators.append(evaluator)
    
    return evaluators

# Default list of all evaluators with default settings
all_evaluators = get_evaluators()
