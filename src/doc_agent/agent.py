from typing import List, Callable, Dict, Any, Union, Set
import logging
from collections import Counter

from doc_agent.draft import draft_copy_tool
from doc_agent.evaluators import all_evaluators, get_evaluators
from doc_agent.evaluators.types import EvalResult

# Maximum times to retry the same error message before giving up
MAX_SAME_ERROR_ATTEMPTS = 3

def run_agent(
    scenario: str,
    style: str,
    evaluators: List[Callable[[str], Union[Dict[str, Any], EvalResult]]],
    llm: Callable,
    max_iters: int = 5
) -> Dict[str, Any]:
    """Internal implementation of the agent loop with dependency injection.
    
    Args:
        scenario: The scenario to generate text for
        style: The style to use for generation
        evaluators: List of evaluator functions that return either Dict or EvalResult
        llm: The language model to use for generation and fixes
        max_iters: Maximum number of iterations to try
        
    Returns:
        Dict containing:
            - text: The final generated text
            - reports: List of evaluation reports or "ALL_PASS"
            - iterations: Number of iterations taken
            - final_status: "success" or "failure"
            - final_reports: List of evaluation results
    """
    logging.info(f"Starting agent with scenario: {scenario}")
    logging.info(f"Style: {style}")
    logging.debug(f"Using {len(evaluators)} evaluators")
    
    try:
        text = llm(scenario=scenario, style=style)
        logging.debug("Generated initial text")
        iterations = 0
        
        # Track which evaluators have passed
        passing = set()  # type: Set[str]
        
        # Track error message frequency to detect loops
        error_counts = Counter()  # type: Counter[str]
        
        for i in range(max_iters):
            iterations = i + 1
            logging.info(f"\nIteration {iterations}/{max_iters}")
            
            # Run evaluators and collect results
            failures = []
            all_reports = []
            found_failure = False  # Track if we found any failures this iteration
            
            logging.debug(f"\nIteration {iterations}: Starting evaluator loop")
            logging.debug(f"Current passing evaluators: {passing}")
            
            # Reset passing set at the start of each iteration after the first failure
            if failures_from_last_iter := (i > 0):
                logging.debug("Resetting passing set for new iteration")
                passing.clear()
            
            for evaluator in evaluators:
                # Get evaluator name before running
                eval_name = (evaluator.__name__ if hasattr(evaluator, '__name__') 
                           else 'evaluator')
                
                # Skip if already passing and not first iteration and no failures found yet
                if i > 0 and eval_name in passing and not found_failure:
                    logging.debug(f"Skipping {eval_name} (already passing)")
                    continue
                
                logging.debug(f"Running {eval_name} (found_failure={found_failure})")
                
                # Run evaluator and handle both dict and EvalResult formats
                result = evaluator(text)
                
                # Convert dict result to standard format
                if isinstance(result, dict):
                    report = {
                        "evaluator": eval_name,
                        "status": result["status"],
                        "details": result.get("error", "Pass")
                    }
                else:
                    report = {
                        "evaluator": result.name,
                        "status": result.status,
                        "details": result.error if result.status == "FAIL" else "Pass"
                    }
                
                all_reports.append(report)
                
                if isinstance(result, dict):
                    if result["status"] == "PASS":
                        passing.add(eval_name)
                        logging.debug(f"{eval_name} passed, added to passing set")
                    else:
                        failures.append({"name": eval_name, "error": result.get("error", "Unknown error")})
                        found_failure = True
                        logging.debug(f"{eval_name} failed")
                else:
                    if result:  # Uses __bool__ to check if PASS
                        passing.add(result.name)
                        logging.debug(f"{eval_name} passed, added to passing set")
                    else:
                        failures.append(result)
                        found_failure = True
                        logging.debug(f"{eval_name} failed")
                
                # Track error message if failure
                if isinstance(result, dict) and result["status"] == "FAIL":
                    error_msg = result.get("error", "Unknown error")
                    error_counts[error_msg] += 1
                    if error_counts[error_msg] >= MAX_SAME_ERROR_ATTEMPTS:
                        logging.warning(f"Error message repeated {MAX_SAME_ERROR_ATTEMPTS} times, giving up: {error_msg}")
                        return {
                            "text": text,
                            "reports": [(f["name"], f["error"]) for f in failures],
                            "iterations": iterations,
                            "final_status": "failure",
                            "final_reports": all_reports,
                            "reason": f"Max retries ({MAX_SAME_ERROR_ATTEMPTS}) exceeded for error: {error_msg}"
                        }
                elif not isinstance(result, dict):
                    error_counts[result.error] += 1
                    if error_counts[result.error] >= MAX_SAME_ERROR_ATTEMPTS:
                        logging.warning(f"Error message repeated {MAX_SAME_ERROR_ATTEMPTS} times, giving up: {result.error}")
                        return {
                            "text": text,
                            "reports": [(f.name, f.error) for f in failures],
                            "iterations": iterations,
                            "final_status": "failure",
                            "final_reports": all_reports,
                            "reason": f"Max retries ({MAX_SAME_ERROR_ATTEMPTS}) exceeded for error: {result.error}"
                        }
            
            logging.debug(f"End of iteration {iterations}")
            logging.debug(f"Failures: {failures}")
            logging.debug(f"Passing set: {passing}")
            
            # If no failures, we're done
            if not failures:
                logging.info("All evaluators passed!")
                return {
                    "text": text,
                    "reports": "ALL_PASS",
                    "iterations": iterations,
                    "final_status": "success",
                    "final_reports": all_reports
                }
                
            # Combine all failure messages for a comprehensive fix
            all_errors = "\n".join(
                f"{f['name']}: {f['error']}" if isinstance(f, dict) else f"{f.name}: {f.error}"
                for f in failures
            )
            logging.info(f"🔧 Found {len(failures)} issues to fix")
            for f in failures:
                if isinstance(f, dict):
                    logging.debug(f"  - {f['name']}: {f['error']}")
                else:
                    logging.debug(f"  - {f.name}: {f.error}")
            
            # Use previous and combined fixes for the LLM
            text = llm(
                scenario=scenario,
                style=style,
                previous=text,
                fix=all_errors
            )
            logging.debug("Generated improved text")
        
        # If we get here, we've hit max iterations
        logging.warning(f"Hit maximum iterations ({max_iters})")
        return {
            "text": text,
            "reports": [(f["name"], f["error"]) if isinstance(f, dict) else (f.name, f.error) for f in failures],
            "iterations": iterations,
            "final_status": "failure",
            "final_reports": all_reports
        }

    except KeyboardInterrupt:
        logging.warning("\nOperation interrupted by user")
        return {
            "text": text if 'text' in locals() else "",
            "reports": [(f["name"], f["error"]) if isinstance(f, dict) else (f.name, f.error) for f in failures] if 'failures' in locals() else [],
            "iterations": iterations if 'iterations' in locals() else 0,
            "final_status": "interrupted",
            "final_reports": all_reports if 'all_reports' in locals() else []
        }

def run_doc_agent(
    scenario: str,
    style: str = "Clear and professional",
    max_iters: int = 5,
    evaluator_names: List[str] = None,
    forbidden_file: str = None,
    no_eval: bool = False,
    fast: bool = False
) -> Dict[str, Any]:
    """Generate and evaluate text using the doc agent.
    
    This is the main public interface for the doc agent. It uses the specified evaluators
    (or all available evaluators by default) and the default language model to generate
    and improve text based on the given scenario.
    
    Args:
        scenario: The scenario to generate text for
        style: The style to use for generation (default: "Clear and professional")
        max_iters: Maximum number of iterations to try (default: 5)
        evaluator_names: List of evaluator names to use (default: all evaluators)
        forbidden_file: Path to forbidden words file (default: built-in file)
        no_eval: If True, skips all evaluation (fastest, for development)
        fast: If True, uses only fast evaluators (no AI calls)
        
    Returns:
        Dict containing:
            - text: The final generated text
            - reports: List of evaluation reports or "ALL_PASS"
            - iterations: Number of iterations taken
            - final_status: "success" or "failure"
            - final_reports: List of evaluation results
    """
    evaluators = get_evaluators(
        evaluator_names,
        forbidden_file=forbidden_file,
        no_eval=no_eval,
        fast=fast
    )
    return run_agent(
        scenario=scenario,
        style=style,
        evaluators=evaluators,
        llm=draft_copy_tool,
        max_iters=max_iters
    ) 