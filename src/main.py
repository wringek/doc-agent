# src/main.py

import sys
from pathlib import Path

from doc_agent.ingestion import ingest
from doc_agent.outline import make_outline
from doc_agent.draft    import fill_sections
from doc_agent.lint     import self_lint
from doc_agent.publish  import write_doc

def main(path: str):
    """
    End-to-end pipeline: ingest source, outline, draft, lint, and publish.
    """
    # 1. Ingest & parse metadata
    data = ingest(path)

    # 2. Create outline skeleton
    outline = make_outline(data)

    # 3. Draft + lint, with fallback on errors
    try:
        drafted   = fill_sections(outline, data.get("source", ""))
        finalized = self_lint(drafted)
    except Exception as err:
        print(f"⚠️  Warning: drafting/linting failed: {err}")
        # fallback to publishing the raw outline
        finalized = outline

    # 4. Publish the document
    name = data.get("name") or Path(path).stem
    write_doc(finalized, name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <path_to_source>")
        sys.exit(1)

    source_path = sys.argv[1]
    if not Path(source_path).exists():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    main(source_path)
