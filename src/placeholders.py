"""Resolve {claim_id} placeholders against results/claims_ledger.csv. Fails loudly on an unknown id.

Syntax
  {claim_id}        the ledger's display string (already formatted, e.g. 0.855 or 14.1)
  {claim_id:.2f}    the numeric value formatted with a Python format spec (only for numeric claims)
  {{ and }}         literal braces
"""
from __future__ import annotations

import csv
import re

from common import RESULTS

PATTERN = re.compile(r"\{([A-Za-z][A-Za-z0-9_]*)(?::([^{}]+))?\}")


class MissingClaim(KeyError):
    pass


def load_ledger() -> dict[str, dict]:
    with open(RESULTS / "claims_ledger.csv", newline="", encoding="utf-8") as fh:
        return {r["claim_id"]: r for r in csv.DictReader(fh)}


def render(text: str, ledger: dict[str, dict], where: str = "") -> str:
    text = text.replace("{{", "\x00").replace("}}", "\x01")

    def sub(m: re.Match) -> str:
        cid, spec = m.group(1), m.group(2)
        if cid not in ledger:
            raise MissingClaim(f"{where}: claim id '{cid}' is not in results/claims_ledger.csv")
        row = ledger[cid]
        if spec:
            return format(float(row["value"]), spec)
        return row["display"]

    out = PATTERN.sub(sub, text)
    if re.search(r"[{}]", out):
        bad = re.search(r".{0,30}[{}].{0,30}", out).group(0)
        raise MissingClaim(f"{where}: stray brace left after rendering: ...{bad}...")
    return out.replace("\x00", "{").replace("\x01", "}")


def placeholder_ids(text: str) -> set[str]:
    text = text.replace("{{", "").replace("}}", "")
    return {m.group(1) for m in PATTERN.finditer(text)}
