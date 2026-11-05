"""Independent recomputation of the headline numbers of Weeks 2 and 3 from saved processed data / saved predictions.

Deliberately different code from the original repositories:
  * Spearman rho = Pearson correlation of average ranks (scipy.stats.rankdata), not scipy.stats.spearmanr
  * percentile bootstrap written here with its own seed
  * decoupling flags rebuilt from the 1990 and 2022 values, not read from the saved flag
  * PR-AUC (step-wise average precision), ROC-AUC (rank statistic), F1, MCC and the confusion matrix are written with
    numpy; scikit-learn is not used
  * the Week 3 label is rebuilt from the panel (src/labels.py)

Writes results/verification.csv with columns
  id, week, quantity, original, recomputed, abs_diff, tolerance, result, original_source, method
Run:  python src/verify_headlines.py          (exit code 1 if any check fails)
"""
from __future__ import annotations

import json
import re
import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import INPUTS, INCOME_ORDER, RESULTS
from labels import build_labels

W2 = INPUTS / "week2"
W3 = INPUTS / "week3"
SEED = 20261105  # not the seed used by the earlier repositories (42)
B = 10_000

rows: list[dict] = []


def add(id_, week, quantity, original, recomputed, tol, source, method):
    diff = abs(float(original) - float(recomputed))
    rows.append({"id": id_, "week": week, "quantity": quantity, "original": float(original),
                 "recomputed": float(recomputed), "abs_diff": diff, "tolerance": tol,
                 "result": "pass" if diff <= tol else "FAIL", "original_source": source, "method": method})


# ----------------------------------------------------------------------------------------------------
# numpy-only metric implementations
# ----------------------------------------------------------------------------------------------------
def average_precision(y: np.ndarray, p: np.ndarray) -> float:
    """Step-wise average precision: sum over distinct score thresholds of (recall gain) x (precision there)."""
    y = np.asarray(y, int)
    order = np.argsort(-p, kind="mergesort")
    ys, ps = y[order], p[order]
    last_in_group = np.r_[np.diff(ps) != 0, True]  # last row of each run of tied scores
    tp = np.cumsum(ys)[last_in_group]
    n_pred = (np.arange(len(ys)) + 1)[last_in_group]
    precision = tp / n_pred
    recall = tp / ys.sum()
    recall_prev = np.r_[0.0, recall[:-1]]
    return float(np.sum((recall - recall_prev) * precision))


def roc_auc(y: np.ndarray, p: np.ndarray) -> float:
    y = np.asarray(y, int)
    r = rankdata(p)  # average ranks for ties
    n1 = y.sum()
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def confusion(y: np.ndarray, yhat: np.ndarray) -> dict:
    tp = int(((y == 1) & (yhat == 1)).sum())
    fp = int(((y == 0) & (yhat == 1)).sum())
    tn = int(((y == 0) & (yhat == 0)).sum())
    fn = int(((y == 1) & (yhat == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    denom = np.sqrt(float(tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = (tp * tn - fp * fn) / denom if denom > 0 else 0.0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": prec, "recall": rec, "f1": f1, "mcc": mcc}


def spearman_via_ranks(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(rankdata(x), rankdata(y))[0, 1])


# ----------------------------------------------------------------------------------------------------
def verify_week2() -> None:
    hyp = pd.read_csv(W2 / "results/hypothesis_results.csv")
    cs = pd.read_csv(W2 / "data/processed/cross_section_2022.csv")
    src = "week2 results/hypothesis_results.csv"

    # H1: rank correlation, 2022 cross-section
    d = cs[(cs["gdp_pc"] > 0) & (cs["co2_pc"] > 0)].dropna(subset=["gdp_pc", "co2_pc"])
    h1 = hyp[(hyp.hypothesis == "H1") & (hyp.variant == "primary")].iloc[0]
    add("W2-H1-n", "week2", "Countries in the income-emissions correlation (n)", h1["n"], len(d), 0, src + " H1 primary n", "count of rows with GDP and CO2 per person > 0")
    rho = spearman_via_ranks(d["gdp_pc"].to_numpy(), d["co2_pc"].to_numpy())
    add("W2-H1-rho", "week2", "Spearman rho, GDP per person vs CO2 per person (2022)", h1["effect_size"], rho, 1e-9,
        src + " H1 primary effect_size", "Pearson correlation of average ranks")
    rng = np.random.default_rng(SEED)
    x, y = d["gdp_pc"].to_numpy(), d["co2_pc"].to_numpy()
    n = len(d)
    idx = rng.integers(0, n, size=(B, n))
    boots = np.empty(B)
    for b in range(B):
        i = idx[b]
        boots[b] = np.corrcoef(rankdata(x[i]), rankdata(y[i]))[0, 1]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    add("W2-H1-ci-lo", "week2", "Lower end of the 95% interval for rho", h1["ci_low"], lo, 0.02, src + " H1 primary ci_low",
        f"percentile bootstrap, {B:,} resamples, own seed (interval ends differ by resampling noise)")
    add("W2-H1-ci-hi", "week2", "Upper end of the 95% interval for rho", h1["ci_high"], hi, 0.02, src + " H1 primary ci_high",
        f"percentile bootstrap, {B:,} resamples, own seed")
    pear = float(np.corrcoef(np.log10(x), np.log10(y))[0, 1])
    comp = hyp[(hyp.hypothesis == "H1") & (hyp.variant.str.startswith("companion"))].iloc[0]
    add("W2-H1-pearson", "week2", "Pearson r on log10 values", comp["effect_size"], pear, 1e-9, src + " H1 companion", "np.corrcoef on log10")

    # H2/H3: group medians and the 14x ratio
    g = pd.read_csv(W2 / "results/h2_group_descriptives.csv").set_index("income_group")
    d2 = cs.dropna(subset=["co2_pc", "income_group"])
    d2 = d2[d2["co2_pc"] > 0]
    for grp in INCOME_ORDER:
        sub = d2[d2.income_group == grp]["co2_pc"]
        add(f"W2-H2-median-{grp.split()[0].lower()}", "week2", f"Median CO2 per person, {grp} (tonnes)", g.loc[grp, "median_co2_pc"],
            sub.median(), 1e-9, "week2 results/h2_group_descriptives.csv median_co2_pc", "groupby median")
        add(f"W2-H2-n-{grp.split()[0].lower()}", "week2", f"Countries in {grp} (H2 sample)", g.loc[grp, "n"], len(sub), 0,
            "week2 results/h2_group_descriptives.csv n", "count")
    hi = np.log10(d2[d2.income_group == "High income"]["co2_pc"])
    low = np.log10(d2[d2.income_group.isin(["Lower middle income", "Low income"])]["co2_pc"])
    diff = hi.mean() - low.mean()
    perm = hyp[(hyp.hypothesis == "H3") & (hyp.variant == "robustness: permutation of mean difference")].iloc[0]
    add("W2-H3-diff", "week2", "Mean difference in log10 CO2 per person, high vs lower-middle plus low", perm["effect_size"], diff, 1e-9,
        src + " H3 permutation row (statistic)", "difference of group means of log10")
    ratio_orig = float(re.search(r"geometric-mean ratio=([0-9.]+)x", hyp[(hyp.hypothesis == "H3") & (hyp.variant == "primary")].iloc[0]["comment"]).group(1))
    add("W2-H3-ratio", "week2", "High-income to lower-income ratio of geometric-mean CO2 per person", ratio_orig, 10 ** diff, 0.005,
        src + " H3 primary comment (printed to 2 decimals)", "10 ** (difference of group means of log10)")
    add("W2-H3-n", "week2", "Countries in the high vs lower-income comparison", hyp[(hyp.hypothesis == "H3") & (hyp.variant == "primary")].iloc[0]["n"],
        len(hi) + len(low), 0, src + " H3 primary n", "count")

    # H6: decoupling shares from the 1990 and 2022 values themselves
    pr = pd.read_csv(W2 / "data/processed/paired_1990_2022.csv")
    ok = (pr[["co2_pc_1990", "co2_pc_2022", "gdp_pc_1990", "gdp_pc_2022"]].notna().all(axis=1)
          & (pr["co2_pc_1990"] > 0) & (pr["co2_pc_2022"] > 0) & (pr["gdp_pc_1990"] > 0) & (pr["gdp_pc_2022"] > 0)
          & pr["income_group"].notna())
    q = pr[ok].copy()
    q["dec"] = ((q["co2_pc_2022"] < q["co2_pc_1990"]) & (q["gdp_pc_2022"] > q["gdp_pc_1990"])).astype(int)
    h6 = pd.read_csv(W2 / "results/h6_contingency_and_residuals.csv")
    add("W2-H6-n", "week2", "Countries in the decoupling comparison (n)", hyp[(hyp.hypothesis == "H6") & (hyp.variant == "primary")].iloc[0]["n"], len(q), 0,
        src + " H6 primary n", "count of countries with CO2 and GDP in both years")
    for grp in INCOME_ORDER:
        sub = q[q.income_group == grp]
        o = h6[(h6.income_group == grp)]
        n_dec_orig = int(o[o.outcome == "Decoupled"]["observed"].iloc[0])
        n_tot_orig = int(o["observed"].sum())
        key = grp.split()[0].lower()
        add(f"W2-H6-count-{key}", "week2", f"Decoupled countries, {grp}", n_dec_orig, sub["dec"].sum(), 0, "week2 results/h6_contingency_and_residuals.csv observed", "rebuilt flag, count")
        add(f"W2-H6-total-{key}", "week2", f"Countries compared, {grp}", n_tot_orig, len(sub), 0, "week2 results/h6_contingency_and_residuals.csv observed", "count")
        add(f"W2-H6-share-{key}", "week2", f"Share decoupled 1990-2022, {grp} (%)", o[o.outcome == "Decoupled"]["row_pct_decoupled"].iloc[0],
            100 * sub["dec"].mean(), 1e-9, "week2 results/h6_contingency_and_residuals.csv row_pct_decoupled", "mean of rebuilt flag x 100")

    # H5: high-income change
    h5 = hyp[(hyp.hypothesis == "H5") & (hyp.variant == "primary")].iloc[0]
    m = re.search(r"median change=(-?[0-9.]+)% \[(-?[0-9.]+), (-?[0-9.]+)\]; (\d+) of (\d+)", h5["comment"])
    hi_c = pr[(pr.income_group == "High income") & (pr.co2_pc_1990 > 0) & (pr.co2_pc_2022 > 0)]
    chg = 100 * (hi_c["co2_pc_2022"] / hi_c["co2_pc_1990"] - 1)
    add("W2-H5-n", "week2", "High-income countries with CO2 in both years (n)", h5["n"], len(hi_c), 0, src + " H5 primary n", "count")
    add("W2-H5-median", "week2", "Median change in CO2 per person, high-income countries (%)", float(m.group(1)), chg.median(), 0.05,
        src + " H5 primary comment (printed to 1 decimal)", "median of 100 x (CO2_2022 / CO2_1990 - 1)")
    add("W2-H5-fell", "week2", "High-income countries whose CO2 per person fell", int(m.group(4)), int((chg < 0).sum()), 0, src + " H5 primary comment", "count of negative changes")

    # H4: log-log slope in high-income countries (point estimate)
    s = pd.read_csv(W2 / "results/h4_slopes_by_group.csv").set_index("income_group")
    d4 = cs[(cs.gdp_pc > 0) & (cs.co2_pc > 0)].dropna(subset=["income_group"])
    for grp in INCOME_ORDER:
        sub = d4[d4.income_group == grp]
        slope = np.polyfit(np.log10(sub["gdp_pc"]), np.log10(sub["co2_pc"]), 1)[0]
        add(f"W2-H4-slope-{grp.split()[0].lower()}", "week2", f"Log-log slope of CO2 on income, {grp}", s.loc[grp, "slope"], slope, 1e-9,
            "week2 results/h4_slopes_by_group.csv slope", "np.polyfit degree 1 on log10 values")


# ----------------------------------------------------------------------------------------------------
def verify_week3() -> None:
    panel = pd.read_csv(W3 / "data/processed/panel.csv")
    L = build_labels(panel)
    base = pd.read_csv(W3 / "results/label_base_rate_overall.csv").set_index("scope")
    src = "week3 results/label_base_rate_overall.csv"
    for scope, split in [("pool", "pool"), ("test", "test")]:
        sub = L[L.split == split]
        add(f"W3-label-n-{scope}", "week3", f"Eligible decoupling windows, {scope}", base.loc[scope, "n_rows"], len(sub), 0, src + " n_rows", "label rebuilt from panel")
        add(f"W3-label-pos-{scope}", "week3", f"Decoupling windows, {scope}", base.loc[scope, "n_positive"], sub["y"].sum(), 0, src + " n_positive", "label rebuilt from panel")
        add(f"W3-label-rate-{scope}", "week3", f"Base rate of decoupling windows, {scope}", base.loc[scope, "base_rate"], sub["y"].mean(), 1e-12, src + " base_rate", "label rebuilt from panel")
    allrows = L[L.split.isin(["pool", "test"])]
    add("W3-label-rate-all", "week3", "Base rate, pool plus test", base.loc["all eligible pool + test rows", "base_rate"], allrows["y"].mean(), 1e-12, src, "label rebuilt from panel")
    flow = pd.read_csv(W3 / "results/sample_flow.csv")
    add("W3-flow-final", "week3", "Eligible windows after all drops (t = 1993-2019)", flow["n_remaining"].iloc[-1], len(L), 0, "week3 results/sample_flow.csv last row", "label rebuilt from panel")
    by = pd.read_csv(W3 / "results/label_base_rate_by_year.csv")
    mine = L.groupby("t")["y"].agg(["size", "sum"])
    n_bad = 0
    for _, r in by.iterrows():
        if mine.loc[int(r["year"]), "size"] != r["n_rows"] or mine.loc[int(r["year"]), "sum"] != r["n_positive"]:
            n_bad += 1
    add("W3-label-by-year-mismatches", "week3", "Window start years (of 24) whose row count or positive count differs", 0, n_bad, 0, "week3 results/label_base_rate_by_year.csv", "per-year comparison")

    tp = pd.read_csv(W3 / "data/processed/test_predictions.csv")
    mm = tp.merge(L[["iso3", "t", "y"]], left_on=["iso3", "year"], right_on=["iso3", "t"], how="left", suffixes=("", "_rebuilt"))
    add("W3-label-test-mismatches", "week3", "Test windows whose saved label differs from the rebuilt label", 0, int((mm["y"] != mm["y_rebuilt"]).sum()), 0,
        "week3 data/processed/test_predictions.csv y", "row-by-row comparison with the rebuilt label")

    met = pd.read_csv(W3 / "results/test_metrics.csv").set_index("model")
    cfg = json.loads((W3 / "results/frozen_config.json").read_text(encoding="utf-8"))
    thr = {m: cfg["models"][m]["threshold"] for m in ["lr", "rf", "hgb"]}
    thr["persistence"] = float(met.loc["persistence", "threshold"])
    thr["prior"] = float(met.loc["prior", "threshold"])
    for m in ["lr", "rf", "hgb"]:
        add(f"W3-thr-{m}", "week3", f"Threshold used for {m} in the test table equals the frozen threshold", cfg["models"][m]["threshold"], met.loc[m, "threshold"], 0,
            "week3 results/frozen_config.json vs results/test_metrics.csv", "comparison")
    y = tp["y"].to_numpy()
    names = {"lr": "Logistic regression", "rf": "Random forest", "hgb": "Gradient boosting", "persistence": "Persistence rule", "prior": "Prior (base rate)"}
    srcm = "week3 results/test_metrics.csv"
    for m, label in names.items():
        p = tp[f"p_{m}"].to_numpy(float)
        yhat = (p >= thr[m]).astype(int)
        c = confusion(y, yhat)
        add(f"W3-{m}-prauc", "week3", f"Test PR-AUC, {label}", met.loc[m, "pr_auc"], average_precision(y, p), 1e-9, srcm + " pr_auc", "numpy step-wise average precision")
        add(f"W3-{m}-rocauc", "week3", f"Test ROC-AUC, {label}", met.loc[m, "roc_auc"], roc_auc(y, p), 1e-9, srcm + " roc_auc", "rank statistic with average ranks")
        for k in ["f1", "mcc", "precision", "recall"]:
            add(f"W3-{m}-{k}", "week3", f"Test {k.upper() if k in ('f1', 'mcc') else k}, {label}", met.loc[m, k], c[k], 1e-9, srcm + f" {k}", "numpy from the confusion counts at the frozen threshold")
        for k in ["tp", "fp", "tn", "fn"]:
            add(f"W3-{m}-{k}", "week3", f"Test confusion count {k.upper()}, {label}", met.loc[m, k], c[k], 0, srcm + f" {k}", "counts at the frozen threshold")


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    verify_week2()
    verify_week3()
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "verification.csv", index=False, lineterminator="\n")
    n_fail = int((df["result"] != "pass").sum())
    print(f"{len(df)} checks, {len(df) - n_fail} pass, {n_fail} fail; max abs diff among passes = {df['abs_diff'].max():.3e}")
    if n_fail:
        print(df[df["result"] != "pass"].to_string())
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
