"""Shared paths and small helpers for the Week 4 synthesis repository."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference"
INPUTS = ROOT / "data" / "inputs"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
REUSED = FIGURES / "reused"
REPORT = ROOT / "report"

REPOS = {
    "week1": {"name": "co2-economy-eda-proposal",
              "url": "https://github.com/KanishkVerma-046/co2-economy-eda-proposal",
              "title": "Week 1, Data Exploration and Visualization Strategy"},
    "week2": {"name": "co2-gdp-hypothesis-testing",
              "url": "https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing",
              "title": "Week 2, Statistical Analysis and Hypothesis Testing Framework"},
    "week3": {"name": "co2-decoupling-ml-pipeline",
              "url": "https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline",
              "title": "Week 3, Machine Learning Model Development and Evaluation Plan"},
}

INCOME_ORDER = ["Low income", "Lower middle income", "Upper middle income", "High income"]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head(repo_dir: Path) -> str:
    return subprocess.run(["git", "-C", str(repo_dir), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()


def git_date(repo_dir: Path) -> str:
    return subprocess.run(["git", "-C", str(repo_dir), "log", "-1", "--format=%cI"], capture_output=True, text=True,
                          check=True).stdout.strip()


def commits() -> dict[str, str]:
    """Commit hash of each reference clone (read from the clones; also recorded in data/inputs/manifest.csv)."""
    return {k: git_head(REF / k) for k in REPOS}


# ----------------------------------------------------------------------------------------------------
# Claim resolver: turns (file, locator, derivation) into a value, using only csv / json / re (no pandas), so tests can
# re-resolve every ledger row independently of the code that built it.
#
# locator grammar
#   CSV  : "<column> | <col>=<value> & <col>=<value>"   exactly one distinct matching row (exact duplicate rows allowed)
#          "#rows | <filters>"                          number of matching rows
#   JSON : "json: a.b.0.c"                              key path (list indexes are integers)
#   text : "regex: <pattern>"                           group 1 of the first match in the file text
# derivation (applied to the located value)
#   ""            none (number if numeric, else string)
#   "x100"        value * 100
#   "100-x"       100 - value
#   "abs"         absolute value
#   "pow10"       10 ** value
#   "pct_pow10"   (10 ** value - 1) * 100
#   "first10"     first 10 characters
#   "regex:<pat>" group 1 of the pattern applied to the located cell text, as a number
#   steps can be chained with " >> ", e.g. "regex:(-?[0-9.]+)% >> abs"
# ----------------------------------------------------------------------------------------------------
import csv as _csv
import json as _json
import re as _re


def _num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return x


def _rows(path: Path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(_csv.DictReader(fh))


def resolve(file: str, locator: str, derivation: str = ""):
    path = ROOT / file
    loc = locator.strip()
    if loc.startswith("json:"):
        obj = _json.loads(path.read_text(encoding="utf-8"))
        for part in loc[5:].strip().split("."):
            obj = obj[int(part)] if isinstance(obj, list) else obj[part]
        val = obj
    elif loc.startswith("regex:"):
        m = _re.search(loc[6:].strip(), path.read_text(encoding="utf-8"), flags=_re.S)
        if not m:
            raise KeyError(f"pattern not found in {file}: {loc}")
        val = _num(m.group(1))
    else:
        col, _, filt = [s.strip() for s in loc.partition("|")]
        rows = _rows(path)
        for cond in [c for c in filt.split(" & ") if c.strip()]:
            k, _, v = cond.partition("=")
            rows = [r for r in rows if r[k.strip()].strip() == v.strip()]
        if col == "#rows":
            val = float(len(rows))
        else:
            distinct = {tuple(sorted(r.items())) for r in rows}
            if len(distinct) != 1:
                raise KeyError(f"{file}: locator '{locator}' matched {len(distinct)} distinct rows")
            val = _num(rows[0][col])
    out = val
    for d in [x.strip() for x in derivation.split(" >> ")] if derivation.strip() else []:
        out = _apply(out, d)
    return out


def _apply(val, d):
    if d == "x100":
        return float(val) * 100
    if d == "100-x":
        return 100 - float(val)
    if d == "abs":
        return abs(float(val))
    if d == "pow10":
        return 10 ** float(val)
    if d == "pct_pow10":
        return (10 ** float(val) - 1) * 100
    if d == "first10":
        return str(val)[:10]
    if d.startswith("regex:"):
        m = _re.search(d[6:], str(val))
        if not m:
            raise KeyError(f"derivation pattern not found in '{val}'")
        return _num(m.group(1))
    raise ValueError(f"unknown derivation {d}")
