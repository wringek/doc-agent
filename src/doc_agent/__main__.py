import argparse
import logging
from pathlib import Path
from typing import List

from doc_agent.agent import run_doc_agent
from doc_agent.draft import draft_copy_tool
from doc_agent.evaluators import all_evaluators, EVALUATOR_REGISTRY, FORBIDDEN_FILE
from doc_agent.pipeline import process_document
from doc_agent.release_notes import generate_release_notes

def setup_logging(verbosity: int) -> None:
    """Configure logging based on verbosity level."""
    if verbosity == 0:  # -q/--quiet
        level = logging.WARNING
    elif verbosity == 1:  # default
        level = logging.INFO
    else:  # -v/--verbose
        level = logging.DEBUG
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format='%(message)s',  # Keep it clean for user output
        handlers=[logging.StreamHandler()]
    )
    
    # Set higher level for http client libraries to avoid connection lifecycle spam
    logging.getLogger("httpx").setLevel(logging.INFO)
    logging.getLogger("httpcore").setLevel(logging.INFO)
    
    # Ensure our app's logger still respects the verbosity
    logging.getLogger("doc_agent").setLevel(level)

def print_report(result: dict, show_details: bool = False) -> None:
    """Print the agent result in a structured format."""
    # Print iteration summary
    print(f"\n📊 Completed in {result['iterations']} iteration(s)")
    print(f"Status: {'✅ Success' if result['final_status'] == 'success' else '❌ Failed'}")
    
    # Print evaluation reports if requested
    if show_details:
        print("\n🔍 Evaluation Reports:")
        for report in result["final_reports"]:
            status_icon = "✅" if report["status"] == "PASS" else "❌"
            print(f"{status_icon} {report['evaluator']}: {report['details']}")
    
    # Print the final text
    print("\n✨ Final Text ✨")
    print(result["text"])

def main(args: List[str] = None) -> None:
    """CLI wrapper for running the doc agent."""
    parser = argparse.ArgumentParser(
        prog="doc-agent",  # Set the program name explicitly
        description="Run the doc agent to generate and evaluate text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and evaluate text:
  python -m doc_agent generate --scenario "Write a function that sorts a list" --style "Clear and concise"
  python -m doc_agent generate --scenario "Explain how to use argparse" --eval heuristics,rubric -v
  
  # Process a document:
  python -m doc_agent process path/to/source.py
  
  # Generate release notes:
  python -m doc_agent release-notes --from v1.0.0 --to HEAD --output RELEASE_NOTES.md
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate and evaluate text")
    gen_parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=1,
        help="Increase output verbosity (-v for debug)"
    )
    gen_parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors and final result"
    )
    gen_parser.add_argument(
        "--scenario",
        required=True,
        help="The scenario to generate text for"
    )
    gen_parser.add_argument(
        "--style",
        default="Clear and professional",
        help="The style to use for generation (default: Clear and professional)"
    )
    gen_parser.add_argument(
        "--max-iters",
        type=int,
        default=5,
        help="Maximum number of iterations to try (default: 5)"
    )
    gen_parser.add_argument(
        "--show-details",
        action="store_true",
        help="Show detailed evaluation reports"
    )
    gen_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    gen_parser.add_argument(
        "--eval",
        help=f"Comma-separated list of evaluators to run (available: {','.join(EVALUATOR_REGISTRY.keys())})"
    )
    gen_parser.add_argument(
        "--forbidden-file",
        default=FORBIDDEN_FILE,
        help="Path to custom forbidden words file"
    )
    
    # Add development optimization flags
    gen_parser.add_argument(
        "--no-eval",
        action="store_true",
        help="Skip all evaluations (fastest, for development)"
    )
    gen_parser.add_argument(
        "--fast",
        action="store_true",
        help="Use only fast evaluators (no AI calls)"
    )
    
    # Process command
    proc_parser = subparsers.add_parser("process", help="Process a document through the pipeline")
    proc_parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=1,
        help="Increase output verbosity (-v for debug)"
    )
    proc_parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors and final result"
    )
    proc_parser.add_argument(
        "source_path",
        help="Path to the source file to process"
    )
    proc_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    proc_parser.add_argument(
        "--forbidden-file",
        default=FORBIDDEN_FILE,
        help="Path to custom forbidden words file"
    )
    
    # Release notes command
    notes_parser = subparsers.add_parser("release-notes", help="Generate release notes from git commits")
    notes_parser.add_argument("--repo", default=".", help="Path to git repository")
    notes_parser.add_argument("--from", dest="rev_from", required=True, help="Starting revision (e.g. v1.0.0)")
    notes_parser.add_argument("--to", dest="rev_to", default="HEAD", help="Ending revision")
    notes_parser.add_argument("--output", help="Output file path")
    notes_parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    
    args = parser.parse_args(args)
    
    if not args.command:
        parser.print_help()
        exit(1)
    
    # Set up logging (quiet overrides verbose)
    verbosity = 0 if args.quiet else args.verbose
    setup_logging(verbosity)
    
    try:
        if args.command == "generate":
            # Parse evaluator list if provided
            evaluator_names = None
            if args.eval:
                evaluator_names = [name.strip() for name in args.eval.split(",")]
            
            result = run_doc_agent(
                scenario=args.scenario,
                style=args.style,
                max_iters=args.max_iters,
                evaluator_names=evaluator_names,
                forbidden_file=args.forbidden_file,
                no_eval=args.no_eval,
                fast=args.fast
            )
            
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            else:
                print_report(result, show_details=args.show_details)
                
        elif args.command == "process":
            if not Path(args.source_path).exists():
                print(f"Error: file not found: {args.source_path}")
                exit(1)
                
            result = process_document(
                args.source_path,
                forbidden_file=args.forbidden_file
            )
            
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            else:
                status_icon = "✅" if result["status"] == "success" else "❌"
                print(f"\n{status_icon} Status: {result['status']}")
                
                if result["status"] == "success":
                    print("\n✨ Processed Document ✨")
                    print(result["text"])
                else:
                    print(f"\n❌ Error: {result['error']}")
                    
        elif args.command == "release-notes":
            try:
                notes = generate_release_notes(
                    repo_path=args.repo,
                    rev_from=args.rev_from,
                    rev_to=args.rev_to,
                    output_file=args.output,
                    model=args.model
                )
                if not args.output:
                    print(notes)
            except Exception as e:
                print(f"Error generating release notes: {e}", file=sys.stderr)
                sys.exit(1)
                
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        if verbosity > 1:  # Show traceback in debug mode
            import traceback
            traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main() 