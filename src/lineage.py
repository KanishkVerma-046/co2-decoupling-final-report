"""Lineage and data-vintage consistency across Weeks 1-3.

Writes
  results/lineage.csv             one row per earlier repo plus one row per raw data file (sha256 from that repo's manifest)
  results/data_vintage_check.csv  file-by-file comparison of Week 2 and Week 3 (hash, then overlapping values), and the
                                  Week 1 facts that can be checked without a manifest
  results/reference_pytest.csv    pytest counts of the earlier repos (counted from the test files; executed results are
                                  read from results/reference_pytest_runs.json when that file exists)

Raw files are read from the committed blobs (`git show`), not from the working tree.
Run:  python src/lineage.py
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys

import pandas as pd

from common import INPUTS, REF, REPOS, RESULTS, git_date, git_head

LF = bytes([10])
CRLF = bytes([13, 10])

CONTRIBUTION = {
    "week1": "Question, two data sources, cleaning rules, exploratory plan, chart choices, preliminary profiling "
             "(a plan with real profiling; the full exploratory analysis was not run).",
    "week2": "Analysis plan committed before the tests; hypotheses H1-H7 (H1-H6 confirmatory, Holm correction); "
             "cleaned 2022 cross-section and 1990-2022 paired tables; effect sizes, robustness, power.",
    "week3": "ML plan committed before any model; leakage-safe 3-year-ahead decoupling label and splits; "
             "model comparison; one locked test run; post hoc comparison of saved predictions.",
}


def blob(repo: str, rel: str) -> bytes:
    commit = git_head(REF / repo)
    return subprocess.run(["git", "-C", str(REF / repo), "show", f"{commit}:{rel}"], capture_output=True,
                          check=True).stdout


def count_tests(repo: str, rel: str) -> int:
    """Number of test functions (each `def test_` once; parametrised cases are counted separately below)."""
    text = blob(repo, rel).decode("utf-8")
    return len(re.findall(r"^def test_", text, flags=re.M))


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    manifests = {
        "week2": json.loads(blob("week2", "data/raw/manifest.json")),
        "week3": json.loads(blob("week3", "data/raw/manifest.json")),
    }
    runs_path = RESULTS / "reference_pytest_runs.json"
    runs = json.loads(runs_path.read_text(encoding="utf-8")) if runs_path.exists() else {}

    test_files = {"week1": None, "week2": "tests/test_data_integrity.py", "week3": "tests/test_pipeline_integrity.py"}
    rows = []
    pytest_rows = []
    for wk, info in REPOS.items():
        n_def = count_tests(wk, test_files[wk]) if test_files[wk] else 0
        run = runs.get(wk, {})
        pytest_rows.append({"week": wk, "test_file": test_files[wk] or "(none: Week 1 has no test suite)",
                            "test_functions_counted": n_def, "reported_by_repo": {"week1": 0, "week2": 25, "week3": 31}[wk],
                            "executed_here": run.get("summary", "not executed"), "passed": run.get("passed"),
                            "failed": run.get("failed")})
        rows.append({"row_type": "repo", "week": wk, "repo_url": info["url"], "commit": git_head(REF / wk),
                     "commit_date": git_date(REF / wk), "contribution": CONTRIBUTION[wk],
                     "pytest_checks_reported": {"week1": 0, "week2": 25, "week3": 31}[wk],
                     "pytest_executed_here": run.get("summary", "not executed"),
                     "raw_file": "", "source_url": "", "downloaded_utc": "", "bytes": "", "sha256": ""})
        if wk in manifests:
            for fname, m in manifests[wk].items():
                rows.append({"row_type": "raw_file", "week": wk, "repo_url": info["url"],
                             "commit": git_head(REF / wk), "commit_date": "", "contribution": "",
                             "pytest_checks_reported": "", "pytest_executed_here": "", "raw_file": fname,
                             "source_url": m["url"], "downloaded_utc": m["downloaded_utc"], "bytes": m["bytes"],
                             "sha256": m["sha256"]})
        else:
            rows.append({"row_type": "raw_file", "week": wk, "repo_url": info["url"], "commit": git_head(REF / wk),
                         "commit_date": "", "contribution": "", "pytest_checks_reported": "",
                         "pytest_executed_here": "", "raw_file": "(no manifest and no raw files committed)",
                         "source_url": "", "downloaded_utc": "", "bytes": "", "sha256": ""})
    pd.DataFrame(rows).to_csv(RESULTS / "lineage.csv", index=False, lineterminator="\n")
    pd.DataFrame(pytest_rows).to_csv(RESULTS / "reference_pytest.csv", index=False, lineterminator="\n")

    # ---- vintage check ------------------------------------------------------------------------------
    chk = []
    files = sorted(set(manifests["week2"]) | set(manifests["week3"]))
    for f in files:
        m2, m3 = manifests["week2"].get(f), manifests["week3"].get(f)
        def blob_ok(wk, m):
            """Does the committed blob hash to the manifest value? If not, does it after LF -> CRLF?"""
            if not m:
                return ""
            try:
                b = blob(wk, f"data/raw/{f}")
            except subprocess.CalledProcessError:
                return "file not committed"
            if hashlib.sha256(b).hexdigest() == m["sha256"]:
                return "yes"
            lf = b.replace(CRLF, LF)
            crlf = lf.replace(LF, CRLF)
            return "only after LF->CRLF" if hashlib.sha256(crlf).hexdigest() == m["sha256"] else "no"

        row = {"file": f, "in_week1": "no manifest", "in_week2": m2 is not None, "in_week3": m3 is not None,
               "sha256_week2": m2["sha256"] if m2 else "", "sha256_week3": m3["sha256"] if m3 else "",
               "bytes_week2": m2["bytes"] if m2 else "", "bytes_week3": m3["bytes"] if m3 else "",
               "request_week2": m2["url"] if m2 else "", "request_week3": m3["url"] if m3 else "",
               "week2_committed_file_matches_manifest": blob_ok("week2", m2),
               "week3_committed_file_matches_manifest": blob_ok("week3", m3)}
        if m2 and m3:
            row["hash_identical"] = m2["sha256"] == m3["sha256"]
            if row["hash_identical"]:
                row["overlap_rows_compared"] = ""
                row["overlap_values_different"] = ""
                row["verdict"] = "identical file (same sha256)"
            elif f.startswith("wb_") and f.endswith(".csv") and f != "wb_country_metadata.csv":
                a = pd.read_csv(io.BytesIO(blob("week2", f"data/raw/{f}")))
                b = pd.read_csv(io.BytesIO(blob("week3", f"data/raw/{f}")))
                a = a[a["year"].between(1990, 2022)]
                b = b[b["year"].between(1990, 2022)]
                mm = a.merge(b, on=["iso3", "wb_id", "year"], how="outer", suffixes=("_w2", "_w3"), indicator=True)
                both = mm[mm["_merge"] == "both"]
                same = (both["value_w2"] == both["value_w3"]) | (both["value_w2"].isna() & both["value_w3"].isna())
                n_diff = int((~same).sum())
                n_only = int((mm["_merge"] != "both").sum())
                row["overlap_rows_compared"] = len(both)
                row["overlap_values_different"] = n_diff + n_only
                row["verdict"] = ("hash differs only because the requested year range differs (1990-2022 vs 1988-2022); "
                                  f"all {len(both)} overlapping 1990-2022 rows have identical values"
                                  if n_diff + n_only == 0 else
                                  f"hash differs and {n_diff + n_only} overlapping values differ")
            else:
                row["overlap_rows_compared"] = ""
                row["overlap_values_different"] = ""
                row["verdict"] = "hash differs; not compared further"
        else:
            row["hash_identical"] = ""
            row["overlap_rows_compared"] = ""
            row["overlap_values_different"] = ""
            row["verdict"] = "used in only one of Weeks 2 and 3"
        chk.append(row)

    # Week 1 (no manifest): compare what it reported with what Weeks 2 and 3 recorded
    w1 = json.loads((INPUTS / "week1" / "data/processed/profiling/profiling_summary.json").read_text(encoding="utf-8"))
    owid_bytes = manifests["week2"]["owid-co2-data.csv"]["bytes"]
    mb = round(owid_bytes / 1e6, 2)
    chk.append({"file": "owid-co2-data.csv (Week 1, by reported facts only)", "in_week1": "reported facts",
                "in_week2": True, "in_week3": True,
                "sha256_week2": "", "sha256_week3": "", "bytes_week2": owid_bytes, "bytes_week3": owid_bytes,
                "request_week2": "", "request_week3": "", "hash_identical": "not checkable",
                "overlap_rows_compared": "", "overlap_values_different": "",
                "verdict": (f"Week 1 reported {w1['owid']['file_size_mb']} MB, {w1['owid']['shape'][0]:,} rows x "
                            f"{w1['owid']['shape'][1]} columns, years {w1['owid']['year_min']}-{w1['owid']['year_max']}; "
                            f"Weeks 2 and 3 recorded {owid_bytes:,} bytes (= {mb} MB). Consistent with the same file, "
                            "but a hash was not stored in Week 1, so identity cannot be proven.")})
    # Week 1 World Bank facts versus Week 2's cleaning log (same indicators, country rows, 1990-2022)
    cl = pd.read_csv(INPUTS / "week2" / "results/cleaning_log.csv")
    wbw = w1["worldbank"]["window_pct_missing_by_indicator"]
    for code, w1key in [("NY.GDP.PCAP.KD", "gdp_per_capita_const2015usd"),
                        ("NY.GDP.PCAP.PP.KD", "gdp_per_capita_ppp_const2021intl"),
                        ("NV.IND.TOTL.ZS", "industry_value_added_pct_gdp")]:
        r = cl[cl["step"] == f"wb_ind:{code}"].iloc[0]
        n_null = int(str(r["note"]).split(" null")[0].replace(",", ""))
        pct2 = round(100 * n_null / r["rows_after"], 2)
        chk.append({"file": f"{code} (Week 1, by reported facts only)", "in_week1": "reported facts", "in_week2": True,
                    "in_week3": code != "NY.GDP.PCAP.PP.KD", "sha256_week2": "", "sha256_week3": "", "bytes_week2": "",
                    "bytes_week3": "", "request_week2": "", "request_week3": "", "hash_identical": "not checkable",
                    "overlap_rows_compared": "", "overlap_values_different": "",
                    "verdict": (f"Share of country rows missing in 1990-2022: Week 1 profiling {wbw[w1key]}%, "
                                f"Week 2 cleaning log {n_null:,} of {int(r['rows_after']):,} = {pct2}%. "
                                + ("Agree." if abs(pct2 - wbw[w1key]) < 0.01 else "DISAGREE."))})
    pd.DataFrame(chk).to_csv(RESULTS / "data_vintage_check.csv", index=False, lineterminator="\n")
    print(pd.DataFrame(chk)[["file", "hash_identical", "overlap_rows_compared", "overlap_values_different"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
