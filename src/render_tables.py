"""Render the text-heavy tables (triangulation, reconciliation, recommendations) from their templates in
report/_build/tables/ into results/*.csv. Placeholders are resolved from the claims ledger; confidence is computed
from the evidence ratings (never typed).

  confidence of a row = the weakest rating among its 'basis' findings
  (F keys come from results/evidence_matrix.csv, P/H/M keys from results/confidence_ratings.csv).
Run:  python src/render_tables.py   (after synthesis_tables.py and build_ledger.py)
"""
from __future__ import annotations

import csv
import sys

import pandas as pd

from common import REPORT, RESULTS
from placeholders import load_ledger, render

ORDER = {"Low": 0, "Moderate": 1, "High": 2}
NAME = {v: k for k, v in ORDER.items()}


def ratings() -> dict[str, str]:
    em = pd.read_csv(RESULTS / "evidence_matrix.csv")
    cr = pd.read_csv(RESULTS / "confidence_ratings.csv")
    out = dict(zip(cr["finding_id"], cr["rating"]))
    out.update(dict(zip(em["key"], em["rating"])))
    return out


def weakest(keys: str, r: dict[str, str]) -> str:
    ks = [k.strip() for k in keys.split(";") if k.strip()]
    return NAME[min(ORDER[r[k]] for k in ks)]


def read_template(name: str) -> list[dict]:
    with open(REPORT / "_build" / "tables" / f"{name}.csv", newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write(rows: list[dict], name: str) -> None:
    with open(RESULTS / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    led = load_ledger()
    r = ratings()
    # ---- recommendations
    out = []
    for row in read_template("recommendations"):
        new = {k: render(v, led, where=f"recommendations {row['id']} {k}") for k, v in row.items()}
        claims = [c.strip() for c in row["evidence_claims"].split(";") if c.strip()]
        for c in claims:
            if c not in led:
                raise SystemExit(f"{row['id']}: unknown evidence claim {c}")
        findings = [k for k in (row["basis"].split(";") + row["context"].split(";")) if k.strip()]
        new["confidence"] = weakest(row["basis"], r)
        new["evidence"] = "Findings " + ", ".join(findings) + "; claims " + ", ".join(claims)
        out.append(new)
    write(out, "recommendations")
    # ---- triangulation
    out = []
    for row in read_template("triangulation"):
        new = {k: render(v, led, where=f"triangulation {row['id']} {k}") for k, v in row.items()}
        new["confidence"] = weakest(row["basis"], r)
        out.append(new)
    write(out, "triangulation")
    # ---- reconciliation
    out = []
    for i, row in enumerate(read_template("reconciliation")):
        out.append({k: render(v, led, where=f"reconciliation {row['topic']} {k}") for k, v in row.items()})
    write(out, "reconciliation")
    print("rendered recommendations, triangulation, reconciliation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
