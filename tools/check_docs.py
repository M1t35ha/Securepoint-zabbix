#!/usr/bin/env python3
"""Check relative Markdown links against tracked working-tree files.

Run from any directory; URLs and fragment-only anchors are intentionally skipped.
"""
from pathlib import Path
from urllib.parse import unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)")

def main() -> int:
    errors = []
    md_files = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))
    if not md_files:
        print("No markdown files", file=sys.stderr)
        return 1
    for source in md_files:
        content = source.read_text(encoding="utf-8")
        for match in LINK.finditer(content):
            uri = match.group(1).split()[0].strip("<>")
            if uri.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = unquote(uri.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing relative link {uri}")
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: {len(md_files)} Markdown files, no broken relative links")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
