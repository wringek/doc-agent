"""
End-to-end document processing pipeline that:
1. Ingests source files
2. Creates document outlines
3. Drafts and lints content
4. Publishes final documents
"""

from pathlib import Path
from typing import Dict, Any, Optional

from doc_agent.ingestion import ingest
from doc_agent.outline import make_outline
from doc_agent.draft import fill_sections
from doc_agent.lint import self_lint
from doc_agent.publish import write_doc
from doc_agent.evaluators import FORBIDDEN_FILE

def process_document(path: str, forbidden_file: Optional[str] = FORBIDDEN_FILE) -> Dict[str, Any]:
    """
    End-to-end pipeline: ingest source, outline, draft, lint, and publish.
    
    Args:
        path: Path to the source file to process
        forbidden_file: Path to custom forbidden words file (optional)
        
    Returns:
        Dict containing:
            - status: "success" or "error"
            - text: The processed document text
            - error: Error message if status is "error"
    """
    try:
        # 1. Ingest & parse metadata
        data = ingest(path)

        # 2. Create outline skeleton
        outline = make_outline(data)

        # 3. Draft + lint, with fallback on errors
        try:
            drafted = fill_sections(outline, data.get("source", ""))
            finalized = self_lint(drafted, forbidden_file=forbidden_file)
        except Exception as err:
            print(f"⚠️  Warning: drafting/linting failed: {err}")
            # fallback to publishing the raw outline
            finalized = outline

        # 4. Publish the document
        name = data.get("name") or Path(path).stem
        doc_path = write_doc(finalized, name)
        
        return {
            "status": "success",
            "text": finalized
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        } 