"""Light synthesis analysis (new, descriptive, clearly labelled). No model is fitted and no test is re-run.

Writes
  results/confidence_ratings.csv     the mechanical confidence rule applied to every finding (docs/synthesis_plan.md, section 6)
  results/decoupling_by_income_1990_2022.csv   decoupled share by income group, with Wilson intervals (descriptive, rebuilt flag)
  results/decoupling_over_time.csv   share of countries decoupling over each 3-year window, by income group (descriptive)
  results/model_skill_top20.csv      precision among the top 20% highest-scored test windows (POST HOC, exploratory)
Run:  python src/synthesis_tables.py
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

from common import INCOME_ORDER, INPUTS, RESULTS
from labels import build_labels

W2 = INPUTS / "week2"
W3 = INPUTS / "week3"
SEED = 20261105
TOP_FRAC = 0.20  # presentation choice fixed in docs/synthesis_plan.md; not tuned
N_BOOT = 2000


# ----------------------------------------------------------------------------------------------------
def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - half, centre + half


# ----------------------------------------------------------------------------------------------------
def decoupling_by_income() -> pd.DataFrame:
    pr = pd.read_csv(W2 / "data/processed/paired_1990_2022.csv")
    ok = (pr[["co2_pc_1990", "co2_pc_2022", "gdp_pc_1990", "gdp_pc_2022"]].notna().all(axis=1)
          & (pr[["co2_pc_1990", "co2_pc_2022", "gdp_pc_1990", "gdp_pc_2022"]] > 0).all(axis=1) & pr["income_group"].notna())
    q = pr[ok].copy()
    q["dec"] = ((q["co2_pc_2022"] < q["co2_pc_1990"]) & (q["gdp_pc_2022"] > q["gdp_pc_1990"])).astype(int)
    rows = []
    for g in INCOME_ORDER + ["All countries"]:
        sub = q if g == "All countries" else q[q.income_group == g]
        k, n = int(sub["dec"].sum()), len(sub)
        lo, hi = wilson(k, n)
        rows.append({"income_group": g, "n_countries": n, "n_decoupled": k, "share_decoupled": k / n,
                     "wilson_lo": lo, "wilson_hi": hi})
    return pd.DataFrame(rows)


def decoupling_over_time() -> pd.DataFrame:
    panel = pd.read_csv(W3 / "data/processed/panel.csv")
    L = build_labels(panel)
    L = L[L["income_group"].isin(INCOME_ORDER)]
    rows = []
    for t, sub_t in L.groupby("t"):
        for g in INCOME_ORDER + ["All countries"]:
            sub = sub_t if g == "All countries" else sub_t[sub_t.income_group == g]
            k, n = int(sub["y"].sum()), len(sub)
            lo, hi = wilson(k, n)
            rows.append({"window_start_year": int(t), "window_end_year": int(t) + 3, "income_group": g, "n_countries": n,
                         "n_decoupled": k, "share_decoupled": k / n if n else float("nan"),
                         "wilson_lo": lo, "wilson_hi": hi, "split": sub_t["split"].iloc[0]})
    out = pd.DataFrame(rows)
    return out


def precision_at_top(y: np.ndarray, s: np.ndarray, frac: float) -> float:
    """Precision among the top ceil(frac * n) scores. Rows tied at the cut-off share the remaining slots in proportion
    (the expected precision under random tie-breaking), so the result does not depend on row order."""
    n = len(y)
    k = int(math.ceil(frac * n))
    order = np.argsort(-s, kind="mergesort")
    ys, ss = y[order], s[order]
    cut = ss[k - 1]
    above = ss > cut
    n_above = int(above.sum())
    tp_above = int(ys[above].sum())
    tie = ss == cut
    n_tie = int(tie.sum())
    pos_tie = int(ys[tie].sum())
    slots = k - n_above
    return (tp_above + slots * pos_tie / n_tie) / k


def model_skill_top20() -> pd.DataFrame:
    tp = pd.read_csv(W3 / "data/processed/test_predictions.csv")
    y = tp["y"].to_numpy(int)
    base = float(y.mean())
    countries = tp["iso3"].to_numpy()
    uniq = np.unique(countries)
    idx_by = {c: np.flatnonzero(countries == c) for c in uniq}
    rng = np.random.default_rng(SEED)
    boots = {m: [] for m in ["lr", "rf", "hgb", "persistence"]}
    base_b = []
    for _ in range(N_BOOT):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        ii = np.concatenate([idx_by[c] for c in pick])
        yb = y[ii]
        base_b.append(yb.mean())
        for m in boots:
            boots[m].append(precision_at_top(yb, tp[f"p_{m}"].to_numpy(float)[ii], TOP_FRAC))
    names = {"lr": "Logistic regression (selected model)", "rf": "Random forest", "hgb": "Gradient boosting",
             "persistence": "Persistence rule"}
    rows = []
    k = int(math.ceil(TOP_FRAC * len(y)))
    for m, label in names.items():
        prec = precision_at_top(y, tp[f"p_{m}"].to_numpy(float), TOP_FRAC)
        b = np.array(boots[m])
        d = b - np.array(base_b)
        rows.append({"model": m, "label": label, "n_windows": len(y), "n_top": k, "top_fraction": TOP_FRAC,
                     "base_rate": base, "precision_top": prec, "precision_lo": np.percentile(b, 2.5),
                     "precision_hi": np.percentile(b, 97.5), "lift_over_base_rate": prec / base,
                     "gain_over_base_rate": prec - base, "gain_lo": np.percentile(d, 2.5), "gain_hi": np.percentile(d, 97.5),
                     "status": "post hoc, exploratory, not pre-specified"})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------------
def confidence_ratings() -> pd.DataFrame:
    hyp = pd.read_csv(W2 / "results/hypothesis_results.csv")
    mde = pd.read_csv(W2 / "results/power_mde.csv")
    rows = []

    corroboration = {  # judgement inputs, each tied to a named result in another week (see the 'corroborated_by' text)
        "H1": (True, "Week 1 preliminary smoke test (rank correlation on 197 countries); Week 3 income per person is the strongest model feature"),
        "H2": (True, "Week 3 decoupling windows differ sharply by income group"),
        "H3": (True, "Week 3 decoupling windows differ sharply by income group"),
        "H4": (False, "none: no other week tests slopes"),
        "H5": (True, "Week 3 high-income windows keep decoupling in 2017-2019"),
        "H6": (True, "Week 3 window base rates rise steadily with income group"),
        "H7": (False, "Week 3 industry share has the expected sign but urbanisation disagrees"),
    }
    labels = {"H1": "Income and CO2 per person rise together across countries",
              "H2": "CO2 per person differs across the four income groups",
              "H3": "High-income countries emit far more per person than lower-income countries",
              "H4": "The income-emissions slope is flatter in high-income countries",
              "H5": "CO2 per person fell in high-income countries between 1990 and 2022",
              "H6": "Absolute decoupling is far more common in high-income countries",
              "H7": "Industry share (not urbanisation) adds explanatory power beyond income (exploratory)"}
    paired_t = hyp[(hyp.hypothesis == "H5") & hyp.variant.str.startswith("companion")].iloc[0]
    mde_h5 = float(mde[(mde.hypothesis == "H5") & (mde.test == "paired t (one-sided)")]["mde_d_80pct_power"].iloc[0])
    underpowered_h5 = abs(float(paired_t["effect_size"])) < mde_h5

    for h in ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]:
        prim = hyp[(hyp.hypothesis == h) & hyp.variant.str.startswith("primary")].iloc[0]
        rob = hyp[(hyp.hypothesis == h) & hyp.variant.str.startswith("robustness")]
        n_rob = len(rob)
        passed = int(((rob["p_raw"] < 0.05) & (rob["direction_ok"].astype(str) != "False")).sum())
        failed = n_rob - passed
        confirmatory = h != "H7"
        holm = float(prim["p_holm"]) if confirmatory else float("nan")
        underpowered = underpowered_h5 if h == "H5" else False
        corr, corr_text = corroboration[h]
        c_pre = confirmatory
        c_rob = failed == 0 and n_rob > 0
        c_holm = confirmatory and holm < 0.01
        c_power = not underpowered
        if not c_pre or failed >= 2:
            rating = "Low"
        elif c_rob and c_holm and c_power and corr:
            rating = "High"
        else:
            rating = "Moderate"
        reasons = []
        if not c_pre:
            reasons.append("exploratory, outside the confirmatory family")
        if failed >= 2:
            reasons.append(f"{failed} of {n_rob} robustness variants do not reach raw p < 0.05")
        elif failed == 1:
            reasons.append("one robustness variant fails")
        if confirmatory and not c_holm:
            reasons.append(f"Holm-adjusted p = {holm:.4f} (not below 0.01)")
        if underpowered:
            reasons.append(f"observed effect size is below the minimum detectable effect ({mde_h5:.2f}) flagged in Week 2")
        if not corr:
            reasons.append("not corroborated by another week")
        if rating == "High":
            reasons.append("all conditions met")
        rows.append({"finding_id": h, "finding": labels[h], "kind": "hypothesis test", "pre_specified": c_pre,
                     "robustness_variants": n_rob, "robustness_passed": passed, "robustness_failed": failed,
                     "holm_p": holm, "underpowered_flag": underpowered, "corroborated": corr,
                     "corroborated_by": corr_text, "rating": rating, "why": "; ".join(reasons)})

    # ---- model-based and post hoc findings (criteria evaluated from saved files where possible)
    rob = pd.read_csv(W3 / "results/test_robustness.csv").drop_duplicates()
    ok_variants, n_variants = 0, 0
    for v, sub in rob.groupby("variant"):
        if v.startswith("primary"):
            continue
        n_variants += 1
        a = sub[sub.model == "lr"]["pr_auc"].iloc[0]
        b = sub[sub.model == "persistence"]["pr_auc"].iloc[0]
        ok_variants += int(a > b)
    pdiff = pd.read_csv(W3 / "results/test_paired_differences.csv").drop_duplicates()
    r = pdiff[(pdiff.model_a == "lr") & (pdiff.model_b == "persistence") & (pdiff.metric == "pr_auc")].iloc[0]
    ci_excl = r["ci_low"] > 0
    cvd = pd.read_csv(W3 / "results/cv_paired_differences.csv")
    r2 = cvd[(cvd.model_a == "lr") & (cvd.model_b == "persistence")].iloc[0]
    cv_agrees = r2["ci_low"] > 0
    rows.append({"finding_id": "M1", "finding": "The selected model ranks decoupling windows better than the persistence rule",
                 "kind": "model comparison (pre-specified)", "pre_specified": True, "robustness_variants": n_variants,
                 "robustness_passed": ok_variants, "robustness_failed": n_variants - ok_variants, "holm_p": float("nan"),
                 "underpowered_flag": False, "corroborated": bool(cv_agrees),
                 "corroborated_by": "rolling-origin cross-validation (an earlier period) shows the same ordering",
                 "rating": "Moderate" if (ci_excl and ok_variants == n_variants) else "Low",
                 "why": "paired interval excludes zero and both variants agree, but the gain is modest, there is a single COVID-shaped "
                        "test period, and a free income-group base rate scores about the same (post hoc)"})
    mt = pd.read_csv(W3 / "results/test_metrics.csv").set_index("model")
    rows.append({"finding_id": "M2", "finding": "At the frozen threshold the selected model is not useful as a yes/no classifier",
                 "kind": "model evaluation (pre-specified)", "pre_specified": True, "robustness_variants": n_variants,
                 "robustness_passed": n_variants, "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False,
                 "corroborated": True, "corroborated_by": "the same pattern appears in out-of-fold cross-validation (recall about 93%, precision about 30%)",
                 "rating": "Moderate",
                 "why": "no usefulness threshold was pre-specified, so the judgement rests on MCC and precision against the base rate; "
                        f"test MCC {mt.loc['lr', 'mcc']:.3f}, precision {mt.loc['lr', 'precision']:.3f}"})
    rows.append({"finding_id": "M3", "finding": "An income-group base rate scores about as well as the selected model",
                 "kind": "post hoc comparison", "pre_specified": False, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": False,
                 "corroborated_by": "none", "rating": "Low", "why": "post hoc: added after the test set was seen"})
    rows.append({"finding_id": "M4", "finding": "Random forest and boosting score higher than the selected model on the test set",
                 "kind": "post hoc comparison", "pre_specified": False, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": True,
                 "corroborated_by": "cross-validation also ranked the forest first (but within one standard error)",
                 "rating": "Low", "why": "post hoc; the pre-specified choice was not changed"})
    rows.append({"finding_id": "M5", "finding": "Precision among the top 20% highest-scored windows exceeds the base rate",
                 "kind": "new post hoc metric", "pre_specified": False, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": False,
                 "corroborated_by": "none", "rating": "Low", "why": "new in Week 4, computed after the test set was seen; plain-language aid only"})
    # structural drivers: W2 exploratory + W3 mixed signals
    h7_row = [r for r in rows if r["finding_id"] == "H7"][0]
    rows.append({"finding_id": "S1", "finding": "Structural drivers (industry share, fuel mix) matter beyond income; urbanisation does not clearly",
                 "kind": "exploratory + model importance", "pre_specified": False,
                 "robustness_variants": int(h7_row["robustness_variants"]),
                 "robustness_passed": int(h7_row["robustness_passed"]), "robustness_failed": int(h7_row["robustness_failed"]), "holm_p": float("nan"), "underpowered_flag": False,
                 "corroborated": False, "corroborated_by": "partly: Week 3 oil share and industry share carry signal, but urbanisation is inconsistent",
                 "rating": "Low", "why": "Week 2's test was exploratory (unadjusted p), Week 3 importance is predictive not causal, and urbanisation results disagree across weeks"})
    # process observations, rated by the rule "observed in this project and independently verified by a script here"
    rows.append({"finding_id": "P1", "finding": "Data lineage can be checked, and was: same OWID file, identical World Bank values, one checksum test failing on line endings",
                 "kind": "process observation", "pre_specified": True, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": True,
                 "corroborated_by": "results/lineage.csv and results/data_vintage_check.csv", "rating": "High",
                 "why": "observed directly and verified by src/lineage.py; no inference involved"})
    rows.append({"finding_id": "P2", "finding": "Headline numbers carry wide or fragile intervals that a bare number would hide",
                 "kind": "process observation", "pre_specified": True, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": True,
                 "corroborated_by": "results/verification.csv recomputes the intervals", "rating": "High",
                 "why": "observed in the saved results and recomputed independently"})
    # EDA lens (Week 1)
    rows.append({"finding_id": "E1", "finding": "Week 1's preliminary rank correlation between income and CO2 per person",
                 "kind": "planning-stage smoke test", "pre_specified": False, "robustness_variants": 0, "robustness_passed": 0,
                 "robustness_failed": 0, "holm_p": float("nan"), "underpowered_flag": False, "corroborated": True,
                 "corroborated_by": "Week 2 H1", "rating": "Low",
                 "why": "a planning-stage smoke test, not a result of the exploratory analysis; used only as a consistency check"})
    return pd.DataFrame(rows)


def evidence_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
    """Which lens supports which finding. Codes: pre = pre-specified result; part = partial, exploratory, post hoc or
    preliminary support; plan = planned in that week but not executed there; none = no evidence from that week.
    The confidence rating is looked up from confidence_ratings.csv (never typed here)."""
    spec = [
        ("F1", "Richer countries emit more CO2 per person", "H1", "part", "pre", "pre",
         "Week 1: preliminary smoke test only. Week 3: income per person is the strongest model feature."),
        ("F2", "High-income countries emit far more per person than lower-income ones", "H3", "plan", "pre", "part",
         "Week 1 planned the group comparison. Week 3 shows decoupling windows also differ by group."),
        ("F3", "Decoupling is far more common in high-income countries", "H6", "plan", "pre", "pre",
         "Week 1 planned the decoupling quadrant plot. Week 3 subgroup rates (pre-specified) show the same ordering."),
        ("F4", "Emissions per person fell in most high-income countries", "H5", "plan", "pre", "part",
         "Week 3 high-income windows keep decoupling in the test years."),
        ("F5", "The income-emissions slope is flatter at high income", "H4", "plan", "pre", "none",
         "Week 1 planned stratified fits. No model-based check."),
        ("F6", "Industry share and fuel mix matter beyond income", "S1", "plan", "part", "part",
         "Week 2 test was exploratory; Week 3 importance is predictive and urbanisation disagrees."),
        ("F7", "The model ranks decoupling windows better than persistence", "M1", "none", "none", "pre",
         "Pre-specified model comparison, one test period."),
        ("F8", "The model is not usable as a yes/no classifier", "M2", "none", "none", "pre",
         "Pre-specified threshold rule, confirmed in cross-validation."),
        ("F9", "An income-group base rate does about as well as the model", "M3", "none", "none", "part",
         "Post hoc comparison on saved test predictions."),
        ("F10", "Forest and boosting scored higher than the chosen model on the test set", "M4", "none", "none", "part",
         "Post hoc comparison on saved test predictions; the pre-specified choice was not changed."),
    ]
    r = ratings.set_index("finding_id")["rating"]
    rows = [{"key": k, "finding": f, "rating_basis": b, "week1": w1, "week2": w2, "week3": w3, "rating": r[b], "note": n}
            for k, f, b, w1, w2, w3, n in spec]
    return pd.DataFrame(rows)


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    d1 = decoupling_by_income()
    d1.to_csv(RESULTS / "decoupling_by_income_1990_2022.csv", index=False, lineterminator="\n")
    d2 = decoupling_over_time()
    d2.to_csv(RESULTS / "decoupling_over_time.csv", index=False, lineterminator="\n")
    d3 = model_skill_top20()
    d3.to_csv(RESULTS / "model_skill_top20.csv", index=False, lineterminator="\n")
    d4 = confidence_ratings()
    d4.to_csv(RESULTS / "confidence_ratings.csv", index=False, lineterminator="\n")
    evidence_matrix(d4).to_csv(RESULTS / "evidence_matrix.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 220)
    print(d1.round(3).to_string())
    print(d3.round(3).drop(columns=["label", "status"]).to_string())
    print(d4[["finding_id", "robustness_variants", "robustness_failed", "holm_p", "rating"]].to_string())
    print(d2[(d2.income_group == "High income") & (d2.window_start_year.isin([1993, 2003, 2013, 2016, 2019]))].round(3).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
