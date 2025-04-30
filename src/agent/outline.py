# src/agent/outline.py

from typing import Dict, List

def make_outline(data: Dict) -> Dict[str, str]:
    """
    Build the Markdown skeleton for documentation.
    """
    title = data.get("name", "")
    summary_md = data.get("summary", "").strip()

    # 1) Arguments table
    params: List[Dict[str, str]] = data.get("params", [])
    if params:
        table_lines = [
            "| Name | Type | Description |",
            "| ---- | ---- | ----------- |"
        ]
        for p in params:
            table_lines.append(
                f"| `{p['name']}` | {p['type']} | {p['description']} |"
            )
        arguments_md = "\n".join(table_lines)
    else:
        arguments_md = ""

    # 2) Returns description
    ret = data.get("returns", {})
    if ret:
        returns_md = f"{ret.get('type','')} – {ret.get('description','')}"
    else:
        returns_md = ""

    # 3) Usage snippet
    example_params = ", ".join(p["name"] for p in params)
    usage_md = f"```js\n{title}({example_params});\n```" if title else ""

    return {
        "title":     title,
        "summary":   summary_md,
        "purpose":   "",           # to be filled by draft
        "usage":     usage_md,
        "arguments": arguments_md,
        "returns":   returns_md,
        "examples":  ""            # to be filled by draft
    }
