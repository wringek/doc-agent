from dataclasses import dataclass
from typing import Literal, Optional

EvalStatus = Literal["PASS", "FAIL"]

@dataclass
class EvalResult:
    """Result from running an evaluator.
    
    Attributes:
        name: Name of the evaluator that produced this result
        status: Whether the evaluation passed or failed
        error: Optional error message explaining why the evaluation failed
    """
    name: str
    status: EvalStatus
    error: str = ""
    
    def __bool__(self) -> bool:
        """Allow using EvalResult in boolean context to check if it passed."""
        return self.status == "PASS" 