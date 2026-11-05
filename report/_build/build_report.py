"""Build report/report_content.md from the section templates in report/_build/sections/.

Rules
  * Every number comes from results/claims_ledger.csv through {claim_id} placeholders (src/placeholders.py). An unknown id
    stops the build with an error.
  * [[table:NAME]]   inserts a pipe table rendered from a results/*.csv file (see TABLES below).
  * [@Key; @Key2]   inserts an in-text citation, [[references]] the reference list; only Crossref-VERIFIED keys are allowed.
  * Output uses LF line endings only.
Run:  python report/_build/build_report.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from placeholders import load_ledger, placeholder_ids, render  # noqa: E402

RESULTS = ROOT / "results"
SECTIONS = ROOT / "report" / "_build" / "sections"
OUT = ROOT / "report" / "report_content.md"
INC_NAME = {"Low income": "Low", "Lower middle income": "Lower-middle", "Upper middle income": "Upper-middle", "High income": "High"}


def clean(x) -> str:
    return str(x).replace("|", "/").replace("\n", " ").strip()


def fmt_p(p: float) -> str:
    if pd.isna(p):
        return "not adjusted"
    return "below 0.001" if p < 0.001 else f"{p:.4f}"


# ----------------------------------------------------------------------------------------------------------------
def t_triangulation():
    d = pd.read_csv(RESULTS / "triangulation.csv")
    rows = [[f"**{r.id}.** {r.question}", r.week1, r.week2, r.week3, r.agreement, f"**{r.confidence}**"] for r in d.itertuples()]
    return ["Question", "Week 1 (exploration)", "Week 2 (tests)", "Week 3 (model)", "Do they agree?", "Confidence"], rows


def t_recommendations():
    d = pd.read_csv(RESULTS / "recommendations.csv")
    rows = [[r.id, f"**{r.short_title}.** {r.recommendation}", r.evidence, f"**{r.confidence}**", r.audience, r.next_step, r.success_measure, r.caveat]
            for r in d.itertuples()]
    return ["ID", "Recommendation", "Evidence", "Confidence", "Audience", "Concrete next step", "Success measure", "Caveat"], rows


def t_reconciliation():
    d = pd.read_csv(RESULTS / "reconciliation.csv")
    rows = [[f"**{r.topic}**", r.week1, r.week2, r.week3, r.why_it_differs, r.how_this_report_handles_it] for r in d.itertuples()]
    return ["Topic", "Week 1", "Week 2", "Week 3", "Why it differs", "How this report handles it"], rows


HYP_Q = {"H1": "Do richer countries emit more CO2 per person?", "H2": "Does CO2 per person differ across the four income groups?",
         "H3": "Do high-income countries emit more than lower-middle plus low income combined?",
         "H4": "Is the income-emissions slope different by income group?", "H5": "Did CO2 per person fall in high-income countries, 1990 to 2022?",
         "H6": "Is decoupling linked to income group?", "H7": "Do industry share and urbanisation add to income? (exploratory)"}


def t_hypothesis_summary():
    h = pd.read_csv(ROOT / "data/inputs/week2/results/hypothesis_results.csv")
    cr = pd.read_csv(RESULTS / "confidence_ratings.csv").set_index("finding_id")
    rows = []
    for k in ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]:
        p = h[(h.hypothesis == k) & h.variant.str.startswith("primary")].iloc[0]
        res = f"{p.effect_size_name} {p.effect_size:.3f} [{p.ci_low:.3f}, {p.ci_high:.3f}]"
        c = cr.loc[k]
        rob = "not applicable" if k == "H7" else f"{int(c.robustness_passed)} of {int(c.robustness_variants)}"
        rows.append([k, HYP_Q[k], f"{int(p.n)}", res, fmt_p(p.p_holm), rob, f"**{c.rating}**"])
    return ["ID", "Question", "Countries", "Effect size [95% interval]", "Holm-adjusted p", "Robustness checks passed", "Confidence"], rows


def t_lineage():
    d = pd.read_csv(RESULTS / "lineage.csv")
    pt = pd.read_csv(RESULTS / "reference_pytest.csv").set_index("week")
    rows = []
    for r in d[d.row_type == "repo"].itertuples():
        t = pt.loc[r.week]
        checks = "none" if r.week == "week1" else f"{int(t.reported_by_repo)} reported; {int(t.passed)} pass and {int(t.failed)} fail on a fresh clone here"
        rows.append([r.week.replace("week", "Week "), f"[{r.repo_url.split('/')[-1]}]({r.repo_url})", f"`{r.commit[:10]}`", r.contribution, checks])
    return ["Week", "Repository", "Commit used", "What it contributed", "Pytest checks"], rows


def t_vintage():
    d = pd.read_csv(RESULTS / "data_vintage_check.csv")
    rows = []
    for r in d.itertuples():
        same = r.hash_identical
        same = "yes" if str(same) == "True" else ("no" if str(same) == "False" else ("not checkable" if str(same) == "not checkable" else "n/a"))
        rows.append([f"`{r.file}`", same, r.verdict])
    return ["File", "Same hash in Weeks 2 and 3?", "What the comparison shows"], rows


def t_test_metrics():
    m = pd.read_csv(ROOT / "data/inputs/week3/results/test_metrics.csv").set_index("model")
    names = {"lr": "Logistic regression (chosen in advance)", "rf": "Random forest (post hoc comparison)", "hgb": "Gradient boosting (post hoc comparison)",
             "persistence": "Persistence rule", "prior": "Base rate only (prior)"}
    rows = []
    for k, n in names.items():
        r = m.loc[k]
        rows.append([n, f"{r.pr_auc:.3f} [{r.pr_auc_lo:.2f}, {r.pr_auc_hi:.2f}]", f"{r.roc_auc:.3f}", f"{r.precision:.3f}", f"{r.recall:.3f}", f"{r.f1:.3f}", f"{r.mcc:.3f}"])
    return ["Model", "PR-AUC [95% interval]", "ROC-AUC", "Precision", "Recall", "F1", "MCC"], rows


def t_top20():
    d = pd.read_csv(RESULTS / "model_skill_top20.csv")
    rows = [[r.label, f"{100 * r.precision_top:.0f}% [{100 * r.precision_lo:.0f}%, {100 * r.precision_hi:.0f}%]", f"{r.lift_over_base_rate:.1f}",
             f"{100 * r.gain_over_base_rate:.0f} points [{100 * r.gain_lo:.0f}, {100 * r.gain_hi:.0f}]"] for r in d.itertuples()]
    return ["Model", "Top-scored windows that really decoupled [95% interval]", "Times the base rate", "Gain over the base rate [95% interval]"], rows


def t_group_decoupling():
    d = pd.read_csv(RESULTS / "decoupling_by_income_1990_2022.csv")
    rows = [[INC_NAME.get(r.income_group, r.income_group), f"{int(r.n_countries)}", f"{int(r.n_decoupled)}", f"{100 * r.share_decoupled:.0f}%",
             f"{100 * r.wilson_lo:.0f}% to {100 * r.wilson_hi:.0f}%"] for r in d.itertuples()]
    return ["Income group", "Countries compared", "Decoupled", "Share", "95% interval"], rows


def t_confidence():
    d = pd.read_csv(RESULTS / "confidence_ratings.csv")
    rows = []
    for r in d.itertuples():
        rob = "none run" if r.robustness_variants == 0 else f"{int(r.robustness_passed)} of {int(r.robustness_variants)}"
        rows.append([r.finding_id, r.finding, r.kind, rob, f"**{r.rating}**", r.why])
    return ["ID", "Finding", "Kind of evidence", "Robustness checks passed", "Rating", "Why"], rows


VER_IDS = ["W2-H1-n", "W2-H1-rho", "W2-H1-ci-lo", "W2-H1-ci-hi", "W2-H3-ratio", "W2-H6-share-high", "W2-H6-share-low", "W2-H5-median", "W2-H4-slope-high",
           "W3-label-rate-pool", "W3-label-rate-test", "W3-label-test-mismatches", "W3-lr-prauc", "W3-lr-rocauc", "W3-lr-mcc", "W3-lr-fp", "W3-persistence-prauc"]


def t_verification():
    d = pd.read_csv(RESULTS / "verification.csv").set_index("id")
    rows = []
    for i in VER_IDS:
        r = d.loc[i]
        f = (lambda v: f"{v:.0f}") if float(r.original).is_integer() and abs(r.original) > 5 else (lambda v: f"{v:.4g}")
        rows.append([r.quantity, f(r.original), f(r.recomputed), f"{r.abs_diff:.1g}", f"{r.tolerance:g}", "pass" if r.result == "pass" else "FAIL"])
    return ["Quantity", "Original", "Recomputed here", "Difference", "Tolerance", "Result"], rows


LEDGER_EXCERPT = ["h1_rho", "h1_ci_lo", "h1_n", "h3_ratio", "med_high", "med_low", "dec_pct_high", "dec_pct_low", "dec_pct_um", "dec_notdec_pct_high", "h6_v",
                  "h5_median", "h5_ci_lo", "h5_ci_hi", "h5_fell", "h5_mde", "h4_p_holm", "h4_p_small", "h4_dr2", "slope_high", "h7_dr2", "h7_industry_pct",
                  "w3_test_rate", "w3_pool_rate", "cv_prauc_rf", "cv_prauc_lr", "test_prauc_lr", "test_prauc_persistence", "test_diff_persist", "test_mcc_lr",
                  "test_prec_lr", "ph_lr_minus_group", "test_prauc_rf", "top_prec_lr", "dec_all_share", "w1_smoke_rho3", "vint_overlap_diff", "ver_pass"]


def t_ledger_excerpt():
    d = pd.read_csv(RESULTS / "claims_ledger.csv").set_index("claim_id")
    rows = []
    for k in LEDGER_EXCERPT:
        r = d.loc[k]
        repo = "Week 4 (this repository)" if str(r.source_repo).startswith("this") else r.source_repo.split("/")[-1]
        rows.append([f"`{k}`", r.text, f"{r.display} {r.unit}".strip(), f"{repo}: `{r.source_file}`", r.originally_reported])
    return ["Claim id", "What it says", "Value", "Source file", "First reported"], rows


def t_sample_flow():
    f2 = pd.read_csv(ROOT / "data/inputs/week2/results/sample_flow.csv")
    f2 = f2[f2.hypothesis == "H1"]
    f3 = pd.read_csv(ROOT / "data/inputs/week3/results/sample_flow.csv")
    rows = [["Week 2 (income and emissions, 2022)", r.stage, f"{int(r.n_remaining)}", f"{int(r.n_excluded)}"] for r in f2.itertuples()]
    rows += [["Week 3 (decoupling windows)", r.stage, f"{int(r.n_remaining):,}", f"{int(r.n_dropped)}"] for r in f3.itertuples()]
    return ["Analysis", "Step", "Remaining", "Dropped at this step"], rows


TABLES = {"triangulation": t_triangulation, "recommendations": t_recommendations, "reconciliation": t_reconciliation,
          "hypothesis_summary": t_hypothesis_summary, "lineage": t_lineage, "vintage": t_vintage, "test_metrics": t_test_metrics,
          "top20": t_top20, "group_decoupling": t_group_decoupling, "confidence": t_confidence, "verification": t_verification,
          "ledger_excerpt": t_ledger_excerpt, "sample_flow": t_sample_flow}


def md_table(headers, rows) -> str:
    lines = ["| " + " | ".join(clean(h) for h in headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        assert len(r) == len(headers), (headers, r)
        lines.append("| " + " | ".join(clean(c) for c in r) + " |")
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------------------------------
def references() -> dict[str, dict]:
    d = pd.read_csv(RESULTS / "reference_check.csv")
    d = d[d.status == "VERIFIED"]
    return {r.key: r._asdict() for r in d.itertuples(index=False)}


def surname_list(authors: str) -> list[str]:
    return [a.split(",")[0].strip() for a in str(authors).split(";") if a.strip()]


def cite_text(k: str, refs) -> str:
    r = refs[k]
    s = surname_list(r["authors"])
    who = s[0] if len(s) == 1 else (f"{s[0]} and {s[1]}" if len(s) == 2 else f"{s[0]} et al.")
    return f"{who}, {int(r['year'])}"


def cite_sub(text: str, refs, used: set) -> str:
    def sub(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        for k in keys:
            if k not in refs:
                raise KeyError(f"citation [@{k}] is not a Crossref-verified reference")
            used.add(k)
        return "(" + "; ".join(cite_text(k, refs) for k in keys) + ")"
    return re.sub(r"\[(@[A-Za-z0-9]+(?:;\s*@[A-Za-z0-9]+)*)\]", sub, text)


def initials(given: str) -> str:
    return " ".join(p[0] + "." for p in re.split(r"[\s\-]+", given.strip()) if p)


def ref_line(r) -> str:
    auth = []
    for a in str(r["authors"]).split(";"):
        a = a.strip()
        if not a:
            continue
        fam, _, giv = a.partition(",")
        auth.append(f"{fam.strip()}, {initials(giv)}" if giv.strip() else fam.strip())
    names = auth[0] if len(auth) == 1 else (", ".join(auth[:-1]) + ", & " + auth[-1] if len(auth) <= 6 else ", ".join(auth[:6]) + ", et al.")
    vol = f", *{int(float(r['volume']))}*" if pd.notna(r["volume"]) and str(r["volume"]) != "" else ""
    iss = f"({int(float(r['issue']))})" if pd.notna(r["issue"]) and str(r["issue"]) != "" else ""
    pg = f", {r['pages']}" if pd.notna(r["pages"]) and str(r["pages"]) != "" else ""
    return f"{names} ({int(r['year'])}). {r['title']}. *{r['container']}*{vol}{iss}{pg}. https://doi.org/{r['crossref_doi']}"


def reference_list(refs, used: set) -> str:
    items = sorted((refs[k] for k in used), key=lambda r: (surname_list(r["authors"])[0].lower(), int(r["year"])))
    return "\n\n".join(ref_line(r) for r in items)


def build() -> str:
    led = load_ledger()
    refs = references()
    used: set[str] = set()
    parts = []
    for f in sorted(SECTIONS.glob("*.md")):
        parts.append(f.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\n"))
    text = "\n\n".join(parts) + "\n"

    def tbl(m):
        name = m.group(1)
        if name not in TABLES:
            raise KeyError(f"unknown table '{name}'")
        return md_table(*TABLES[name]())

    text = re.sub(r"\[\[table:([a-z0-9_]+)\]\]", tbl, text)
    text = cite_sub(text, refs, used)
    missing = sorted(placeholder_ids(text) - set(led))
    if missing:
        raise KeyError(f"{len(missing)} claim id(s) used in the template are missing from the ledger: {', '.join(missing)}")
    text = render(text, led, where="report template")
    text = text.replace("[[references]]", reference_list(refs, used))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def build_notes(report_text: str) -> str:
    from wordcount import counts
    led = load_ledger()
    refs = pd.read_csv(RESULTS / "reference_check.csv")
    cited = len(re.findall(r"https://doi\.org/", report_text.split("## 12. References")[1].split("*Data sources")[0]))
    src = (ROOT / "report" / "_build" / "notes_template.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    c = counts(report_text)
    for k, v in c.items():
        src = src.replace(f"[[wc:{k}]]", f"{v:,}")
    src = src.replace("[[ref:n_candidates]]", str(len(refs))).replace("[[ref:n_verified]]", str(int((refs.status == "VERIFIED").sum())))
    src = src.replace("[[ref:n_cited]]", str(cited))
    return render(src, led, where="report notes")


def main() -> int:
    text = build()
    OUT.write_bytes(text.encode("utf-8"))  # LF endings
    (ROOT / "report" / "report_notes.md").write_bytes(build_notes(text).encode("utf-8"))
    words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-.,%]*", text))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text.splitlines())} lines, about {words} tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
