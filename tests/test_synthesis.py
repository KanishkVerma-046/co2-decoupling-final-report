"""Integrity checks for the Week 4 synthesis repository (run with:  pytest)."""
from __future__ import annotations

import csv
import hashlib
import math
import re
import subprocess

import pandas as pd
from PIL import Image

from common import ROOT, resolve
from placeholders import placeholder_ids
from wordcount import counts

REPORT = ROOT / "report" / "report_content.md"
SECTIONS = sorted((ROOT / "report" / "_build" / "sections").glob("*.md"))
LEDGER = list(csv.DictReader(open(ROOT / "results" / "claims_ledger.csv", newline="", encoding="utf-8")))
LED = {r["claim_id"]: r for r in LEDGER}
TEXT = REPORT.read_text(encoding="utf-8")


def test_01_ledger_ids_unique_and_complete():
    ids = [r["claim_id"] for r in LEDGER]
    assert len(ids) == len(set(ids))
    cols = ["claim_id", "text", "value", "display", "unit", "source_repo", "source_commit", "source_file", "locator",
            "originally_reported", "evidence_status"]
    for r in LEDGER:
        for col in cols:
            assert str(r[col]).strip() != "", (r["claim_id"], col)
        if r["source_repo"].startswith("https://github.com/"):
            assert re.fullmatch(r"[0-9a-f]{40}", r["source_commit"]), r["claim_id"]


def test_02_all_template_placeholders_resolve():
    used = set()
    for f in SECTIONS:
        used |= placeholder_ids(f.read_text(encoding="utf-8"))
    for name in ["recommendations", "triangulation", "reconciliation"]:
        path = ROOT / "report" / "_build" / "tables" / f"{name}.csv"
        for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
            for v in r.values():
                used |= placeholder_ids(v)
    assert used, "no placeholders found"
    assert not (used - set(LED)), sorted(used - set(LED))


def test_03_every_ledger_value_matches_its_source_file():
    for r in LEDGER:
        v = resolve(r["input_copy"], r["locator"], r["derivation"])
        if isinstance(v, str):
            assert v == r["value"], r["claim_id"]
        else:
            assert math.isclose(float(v), float(r["value"]), rel_tol=1e-12, abs_tol=1e-12), (r["claim_id"], v, r["value"])
        assert r["fmt"].format(v) == r["display"], r["claim_id"]


def test_04_independent_recomputation_within_tolerance():
    v = pd.read_csv(ROOT / "results" / "verification.csv")
    assert len(v) >= 60
    assert (v["abs_diff"] <= v["tolerance"] + 1e-15).all(), v[v["abs_diff"] > v["tolerance"]]
    assert set(v["result"]) == {"pass"}


def test_05_input_copies_match_manifest_hashes():
    man = pd.read_csv(ROOT / "data" / "inputs" / "manifest.csv")
    for r in man.itertuples():
        assert hashlib.sha256((ROOT / r.copy_path).read_bytes()).hexdigest() == r.sha256, r.copy_path


def test_06_no_placeholder_text_anywhere():
    bad = re.compile(r"\bTODO\b|\bTBD\b|author to enter|lorem ipsum|\bFIXME\b|\bXXX\b|\[\[|\]\]|\{[A-Za-z_][A-Za-z0-9_]*\}", re.I)
    for f in [REPORT, ROOT / "README.md", ROOT / "report" / "report_notes.md"]:
        assert f.exists(), f
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            assert not bad.search(line), f"{f.name}:{i}: {line[:120]}"
    for p in (ROOT / "figures").rglob("*.png"):
        assert "placeholder" not in p.name.lower()


def _tables(md: str):
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            yield i, lines[i:j]
            i = j
        else:
            i += 1


def test_07_table_rows_have_consistent_cell_counts():
    n_tables = 0
    for start, block in _tables(TEXT):
        n_tables += 1
        pipes = {len(re.findall(r"\|", row)) for row in block}
        assert len(pipes) == 1, f"table at line {start + 1}: {pipes}"
        assert re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", block[1]), f"table at line {start + 1} lacks a separator row"
    assert n_tables >= 20


def test_08_line_endings_are_lf():
    for p in [REPORT, ROOT / "report" / "report_notes.md", ROOT / "README.md", *SECTIONS]:
        assert b"\r" not in p.read_bytes(), p.name


def test_09_figures_exist_are_wide_and_200dpi():
    refs = re.findall(r"!\[Figure (\d+\.\d+): [^\]]+\]\(\.\./(figures/[^)]+\.png)\)", TEXT)
    assert len(refs) == 16
    nums = [n for n, _ in refs]
    assert len(nums) == len(set(nums))
    for _, rel in refs:
        p = ROOT / rel
        assert p.exists(), rel
        w, h = Image.open(p).size
        assert h <= 0.8 * w + 1, (rel, w, h)
    for p in (ROOT / "figures").glob("fig_*.png"):
        dpi = Image.open(p).info.get("dpi", (0, 0))
        assert round(dpi[0]) == 200, p.name
    assert len(list((ROOT / "figures").glob("fig_*.png"))) == 8
    assert 6 <= len(list((ROOT / "figures" / "reused").glob("*.png"))) <= 8


def test_10_every_recommendation_has_evidence_and_confidence():
    rec = pd.read_csv(ROOT / "results" / "recommendations.csv")
    assert len(rec) >= 6
    for r in rec.itertuples():
        assert str(r.evidence).strip() and r.confidence in {"High", "Moderate", "Low"}, r.id
        for cid in str(r.evidence_claims).split(";"):
            assert cid.strip() in LED, (r.id, cid)
        for col in ["recommendation", "audience", "next_step", "success_measure", "caveat"]:
            assert str(getattr(r, col)).strip() and str(getattr(r, col)) != "nan", (r.id, col)


def test_11_no_high_confidence_claim_rests_only_on_post_hoc_or_exploratory_evidence():
    bad = {"post hoc", "exploratory", "planning-stage"}
    rec = pd.read_csv(ROOT / "results" / "recommendations.csv")
    for r in rec[rec.confidence == "High"].itertuples():
        statuses = {LED[c.strip()]["evidence_status"] for c in str(r.evidence_claims).split(";")}
        assert statuses - bad, (r.id, statuses)
    cr = pd.read_csv(ROOT / "results" / "confidence_ratings.csv")
    for r in cr[cr.rating == "High"].itertuples():
        assert bool(r.pre_specified), r.finding_id
    em = pd.read_csv(ROOT / "results" / "evidence_matrix.csv")
    for r in em[em.rating == "High"].itertuples():
        assert "pre" in {r.week1, r.week2, r.week3}, r.key
    tri = pd.read_csv(ROOT / "results" / "triangulation.csv")
    assert set(tri.confidence) <= {"High", "Moderate", "Low"}


ALLOWED = [
    r"\b(?:Sections?|Appendices|Appendix|Figures?|Tables?) [A-E0-9]+(?:\.\d+)?(?:(?:,| and| to) [A-E0-9]+(?:\.\d+)?)*",
    r"\bWeeks? \d\b(?: (?:to|and) \d\b)?",
    r"\b(?:19[0-9]{2}|20[0-3][0-9]|1[7-8][0-9]{2})\b", r"\b[A-Za-z_][A-Za-z0-9_]*[0-9][A-Za-z0-9_]*\b", r"\b[0-9]+[A-Za-z]+[A-Za-z0-9]*\b",
    r"(?m)^\s*\d+\. ", r"(?m)^#+ [0-9.]+ ?", r"\*\*\d+\. ", r"\b95%", r"\b80%", r"\b5%", r"\b0\.01\b", r"\b0\.02\b", r"Python 3\.13",
    r"(?m)\| [0-9]+\.[0-9]+ ",
]


def test_12_template_has_no_bare_numbers():
    """Numbers must come from the ledger. Allowed: week/section/figure/table references, years, identifiers such as H1 or
    CO2, list numbering, and the conventional 95% / 80% / 5% levels."""
    problems = []
    for f in SECTIONS:
        txt = f.read_text(encoding="utf-8")
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)
        txt = re.sub(r"`[^`]*`", "", txt)
        txt = re.sub(r"\{[A-Za-z_][A-Za-z0-9_]*(?::[^{}]+)?\}", "", txt)
        txt = re.sub(r"\]\([^)]*\)", "]", txt)
        txt = re.sub(r"https?://\S+", "", txt)
        txt = re.sub(r"\[@[A-Za-z0-9; @]+\]", "", txt)
        for pat in ALLOWED:
            txt = re.sub(pat, " ", txt)
        for m in re.finditer(r"(?<![A-Za-z])-?\d[\d,.]*", txt):
            line = txt[max(0, m.start() - 40): m.end() + 20].replace("\n", " ")
            problems.append(f"{f.name}: ...{line}...")
    assert not problems, "\n".join(problems[:40])


def test_13_markdown_stays_inside_the_converter_limits():
    in_code = False
    for i, line in enumerate(TEXT.splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        assert not line.startswith(">"), f"blockquote at {i}"
        assert not re.match(r"#{4,} ", line), f"heading level at {i}"
        assert not re.search(r"</?[A-Za-z][^>]*>", re.sub(r"`[^`]*`", "", line)), f"html at {i}: {line[:80]}"
        assert "[^" not in line, f"footnote at {i}"
        assert not re.match(r"\s+[-*] ", line), f"nested list at {i}"
    lines = TEXT.splitlines()
    assert lines[0] == "# Does Wealth Burn Carbon? Comprehensive Data Science Project Report and Recommendations"
    assert lines[2].startswith("*Week 4 Task - Comprehensive Data Science Project Report and Recommendations")
    assert lines[4] == "---"
    assert [l for l in lines if l.startswith("# ")] == [lines[0]]


def test_14_callouts_and_captions_follow_the_pattern():
    n_callouts = 0
    for start, block in _tables(TEXT):
        if block[0].strip() == "| In short |":
            n_callouts += 1
            assert len(block) == 3, f"callout at line {start + 1} must have header, separator and one body row"
            assert block[1].count("|") == 2
    assert n_callouts >= 10
    lines = TEXT.split("\n")
    caps = [l for l in lines if re.match(r"\*\*Table [A-E0-9]+\.[0-9]+:", l)]
    assert len(caps) == len(set(caps)) and len(caps) >= 15
    for i, l in enumerate(lines):
        if re.match(r"\*\*Table [A-E0-9]+\.[0-9]+:", l):
            assert l.endswith(".**"), f"caption at line {i + 1}"
            assert lines[i + 1] == "" and lines[i + 2].startswith("|"), f"caption at line {i + 1} must sit directly above its table"
        if l.startswith("![Figure"):
            ok = re.fullmatch(r"!\[Figure [0-9]+\.[0-9]+: [^\]]+\]\(\.\./figures/(?:reused/)?[A-Za-z0-9_]+\.png\)", l)
            assert ok, f"figure syntax at line {i + 1}"


def test_15_word_counts_within_the_brief():
    c = counts(TEXT)
    assert 6000 <= c["body_prose"] <= 7500, c
    assert 450 <= c["executive_summary"] <= 600, c


def test_16_references_are_crossref_verified_and_cited():
    chk = pd.read_csv(ROOT / "results" / "reference_check.csv")
    ok = chk[chk.status == "VERIFIED"]
    assert len(ok) >= 20 and ok["title_match"].all() and ok["year_match"].all()
    tail = TEXT.split("## 12. References")[1].split("*Data sources")[0]
    dois = re.findall(r"https://doi\.org/(\S+)", tail)
    assert dois and all(d.lower() in set(ok["crossref_doi"].str.lower()) for d in dois)
    assert "†" not in TEXT and "verify later" not in TEXT.lower()
    cited = set(re.findall(r"@([A-Za-z0-9]+)", "".join(f.read_text(encoding="utf-8") for f in SECTIONS)))
    assert cited <= set(ok["key"])
    assert len(dois) == len(cited)


def test_17_no_effort_or_hours_tables():
    assert not re.search(r"\bhours?\b", TEXT, re.I)


def test_18_figure_captions_say_what_to_look_at_and_credit_a_source():
    caps = re.findall(r"!\[(Figure [0-9.]+: [^\]]+)\]", TEXT)
    assert len(caps) == 16
    for c in caps:
        assert "Source:" in c, c
        assert re.search(r"\b(look|read|left|right)\b", c, re.I), c


def test_19_synthesis_plan_was_committed_before_analysis_code():
    plan = subprocess.run(["git", "-C", str(ROOT), "log", "--reverse", "--format=%H", "--", "docs/synthesis_plan.md"], capture_output=True, text=True).stdout.split()
    code = subprocess.run(["git", "-C", str(ROOT), "log", "--reverse", "--format=%H", "--", "src"], capture_output=True, text=True).stdout.split()
    order = subprocess.run(["git", "-C", str(ROOT), "rev-list", "--reverse", "HEAD"], capture_output=True, text=True).stdout.split()
    assert plan and code
    assert order.index(plan[0]) < order.index(code[0])


def test_20_vintage_and_lineage_outputs_are_complete():
    lin = pd.read_csv(ROOT / "results" / "lineage.csv")
    repos = lin[lin.row_type == "repo"]
    assert set(repos.week) == {"week1", "week2", "week3"}
    assert repos.commit.str.fullmatch(r"[0-9a-f]{40}").all()
    vint = pd.read_csv(ROOT / "results" / "data_vintage_check.csv")
    owid = vint[vint.file == "owid-co2-data.csv"].iloc[0]
    assert str(owid.hash_identical) == "True"
    wb = vint[vint.file.str.startswith("wb_") & vint.overlap_rows_compared.notna()]
    assert len(wb) >= 4 and (wb.overlap_values_different == 0).all()
