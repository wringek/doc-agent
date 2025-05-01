# src/agent/publish.py
# src/agent/publish.py

from pathlib import Path

def write_doc(sections: dict, name: str):
    """
    Merge section outputs into a Markdown file and save under output/.
    Includes the 'summary' field under the title, then only non-empty
    sections in a fixed order.
    """
    # 1) Title
    lines = [f"# {name}", ""]

    # 2) Short summary under the title
    summary = sections.get("summary", "").strip()
    if summary:
        lines.append(summary)
        lines.append("")  # blank line after summary

    # 3) Render the rest of the sections in order
    for section in ["purpose", "usage", "arguments", "returns", "examples"]:
        content = sections.get(section, "").strip()
        if not content:
            continue

        lines.append(f"## {section.capitalize()}")
        lines.append(content)
        lines.append("")  # blank line

    # 4) Join and write out
    md = "\n".join(lines)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    out = output_dir / f"{name}.md"
    out.write_text(md)

    print(f"Document written to {out}")
