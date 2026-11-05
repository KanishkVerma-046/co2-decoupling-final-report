"""Word counts for the report: body prose (excludes the executive summary, tables, code, figure lines, captions,
headings, references and appendices) and all-in."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9\u00C0-\u024F][A-Za-z0-9\u00C0-\u024F'\u2019\-./%$]*", text))


def split_sections(md: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^(## .+)$", md)
    out = [("front", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def prose_lines(block: str) -> list[str]:
    keep, in_code = [], False
    for line in block.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip():
            continue
        if line.startswith(("|", "#", "![", "**Table")):
            continue
        keep.append(line)
    return keep


def counts(md: str) -> dict[str, int]:
    body = 0
    exec_words = 0
    for head, block in split_sections(md):
        if head.startswith("## 1."):
            exec_words = sum(words(l) for l in prose_lines(block))
        elif re.match(r"## (?:[2-9]|1[01])\.", head):
            body += sum(words(l) for l in prose_lines(block))
    return {"body_prose": body, "executive_summary": exec_words, "all_in": words(md)}


if __name__ == "__main__":
    print(counts((ROOT / "report" / "report_content.md").read_text(encoding="utf-8")))
