"""Draw the new figures and copy the reused ones.

New figures (figures/*.png, 200 dpi, height <= 0.8 x width, colour-blind-safe, one style):
  fig_journey, fig_findings_glance, fig_income_vs_co2, fig_decoupling_by_group, fig_decoupling_over_time,
  fig_model_skill, fig_evidence_matrix, fig_roadmap
Reused figures are copied byte-for-byte from the committed blobs of the earlier repositories to figures/reused/.
Every number drawn on a figure is read from the claims ledger or from a results/ file, never typed here.
Run:  python src/make_figures.py   (after build_ledger.py and render_tables.py)
"""
from __future__ import annotations

import csv
import subprocess
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Wedge, Circle

from common import FIGURES, INCOME_ORDER, INPUTS, REF, REUSED, RESULTS, ROOT

DPI = 200
W = 6.8  # inches (about 17 cm); reads at 16 cm wide
INK, INK2, MUTED, GRID = "#1F2933", "#52606D", "#7B8794", "#E4E7EB"
BLUE, VERM, GREEN, ORANGE, GREY = "#0072B2", "#D55E00", "#009E73", "#E69F00", "#9AA5B1"
# ordered income groups: one hue, light -> dark (lightness stays inside the validated band)
INC_COL = {"Low income": "#8DB8E0", "Lower middle income": "#5E9BD1", "Upper middle income": "#2F78B7", "High income": "#0B4F8A"}
INC_SHORT = {"Low income": "Low", "Lower middle income": "Lower-middle", "Upper middle income": "Upper-middle", "High income": "High"}
INC_MARK = {"Low income": "o", "Lower middle income": "s", "Upper middle income": "^", "High income": "D"}
CONF_COL = {"High": (BLUE, "white"), "Moderate": (ORANGE, INK), "Low": ("#CBD2D9", INK)}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "axes.titlesize": 10.5,
    "axes.titleweight": "bold", "axes.titlecolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False, "figure.dpi": 100, "savefig.dpi": DPI,
    "axes.titlelocation": "left", "legend.frameon": False,
})

LEDGER = {r["claim_id"]: r for r in csv.DictReader(open(RESULTS / "claims_ledger.csv", encoding="utf-8"))}


def L(cid: str) -> str:
    return LEDGER[cid]["display"]


def save(fig, name: str, max_ratio: float = 0.8) -> None:
    FIGURES.mkdir(exist_ok=True)
    path = FIGURES / name
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(path).size
    assert h <= max_ratio * w + 1, f"{name} is too tall: {h}x{w}"
    print(f"{name}: {w}x{h} (ratio {h / w:.2f})")


def badge(ax, x, y, level, w=0.2, h=0.06, size=8.5, transform=None):
    bg, fg = CONF_COL[level]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.015", fc=bg, ec="none",
                                transform=transform or ax.transAxes, zorder=3))
    ax.text(x + w / 2, y + h / 2, f"{level} confidence", ha="center", va="center", color=fg, fontsize=size, fontweight="bold",
            transform=transform or ax.transAxes, zorder=4)


NL = chr(10)
BULLET = chr(0x2022) + " "
MINUS = chr(0x2212)
TIMES = chr(0xD7)


def wrap(t: str, n: int) -> str:
    return NL.join(textwrap.wrap(t, n))


# =========================================================================================== reused figures
def copy_reused() -> None:
    REUSED.mkdir(parents=True, exist_ok=True)
    man = pd.read_csv(INPUTS / "manifest.csv")
    for _, r in man[man["kind"] == "reused figure"].iterrows():
        data = subprocess.run(["git", "-C", str(REF / r["week"]), "show", f"{r['commit']}:{r['source_path']}"],
                              capture_output=True, check=True).stdout
        (ROOT / r["copy_path"]).write_bytes(data)
    print(f"copied {int((man['kind'] == 'reused figure').sum())} reused figures")


# =========================================================================================== 1 journey
def fig_journey() -> None:
    fig, ax = plt.subplots(figsize=(W, 4.1))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis("off")
    cols = [
        ("Week 1", "Plan the exploration", "Which questions can two open datasets answer?",
         [f"{L('w1_n_questions')} questions, two data sources", f"{L('w1_iso_matched')} countries matched on ISO3 code", "Cleaning rules and chart plan"], "A plan, with real data profiling"),
        ("Week 2", "Test the claims", "Is the pattern real, or chance?",
         [f"{L('n_hypotheses')} hypotheses, plan written first", f"Rank correlation {L('h1_rho')} across {L('h1_n')} countries", "Holm correction, effect sizes, robustness"], "Strong for income; fragile for slopes"),
        ("Week 3", "Try to predict it", "Can we tell which countries will decouple next?",
         [f"{L('w3_all_rows')} country windows, 3 years ahead", "Time-aware splits, one locked test run", f"Test PR-AUC {L('test_prauc2_lr')} vs {L('test_prauc2_persistence')} for a simple rule"], "A modest ranking aid, not a classifier"),
        ("Week 4", "Check, combine, advise", "What do the three lenses say together?",
         [f"{L('ver_n')} numbers recomputed independently", "Every number traced to its source file", "Evidence ratings and recommendations"], "This report"),
    ]
    for i, (wk, title, q, bullets, out) in enumerate(cols):
        x0 = i + 0.03
        ax.add_patch(FancyBboxPatch((x0, 0.03), 0.94, 0.94, boxstyle="round,pad=0,rounding_size=0.03", fc="#F5F7FA", ec=GRID, lw=1))
        ax.add_patch(FancyBboxPatch((x0, 0.84), 0.94, 0.13, boxstyle="round,pad=0,rounding_size=0.03", fc=[BLUE, BLUE, BLUE, "#0B4F8A"][i], ec="none"))
        ax.text(x0 + 0.47, 0.905, wk, ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
        ax.text(x0 + 0.47, 0.79, wrap(title, 17), ha="center", va="center", fontsize=9.3, fontweight="bold", color=INK, linespacing=1.15)
        ax.text(x0 + 0.47, 0.655, wrap(q, 23), ha="center", va="center", fontsize=7.9, style="italic", color=INK2, linespacing=1.15)
        yb = 0.55
        for b_ in bullets:
            t = wrap(b_, 23)
            ax.text(x0 + 0.05, yb, BULLET + t.replace(NL, NL + "   "), ha="left", va="top", fontsize=7.9, color=INK, linespacing=1.15)
            yb -= 0.052 * (t.count(NL) + 1) + 0.035
        ax.add_patch(FancyBboxPatch((x0 + 0.04, 0.06), 0.86, 0.1, boxstyle="round,pad=0,rounding_size=0.02", fc="white", ec=GRID, lw=1))
        ax.text(x0 + 0.47, 0.11, wrap(out, 22), ha="center", va="center", fontsize=7.9, fontweight="bold", color=BLUE, linespacing=1.1)
        if i < 3:
            ax.annotate("", xy=(i + 1.03, 0.5), xytext=(i + 0.97, 0.5), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))
    ax.set_title("The project at a glance: from a question to evidence-based advice", loc="left", pad=8)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.02)
    save(fig, "fig_journey.png")


# =========================================================================================== 2 findings at a glance
def fig_findings() -> None:
    fig, axes = plt.subplots(2, 3, figsize=(W, 4.9))
    panels = [
        (L("h1_rho"), "Rank correlation between income and CO2 per person",
         f"Richer countries emit more per person ({L('h1_n')} countries, 2022).", "High"),
        (f"{L('h3_ratio')}×", "High-income vs lower-middle plus low income",
         "Typical CO2 per person is about fourteen times higher.", "High"),
        (f"{L('dec_pct_high')}%", f"of high-income countries cut CO2 per person while growing",
         f"Against {L('dec_pct_low')}% to {L('dec_pct_um')}% in the other groups (1990-2022).", "High"),
        (f"−{L('h5_median_abs')}%", "Median change in CO2 per person, high-income countries",
         f"It fell in {L('h5_fell')} of {L('h5_n')} countries; the interval is wide.", "Moderate"),
        (f"{L('test_prauc2_lr')} vs {L('test_prauc2_persistence')}", "Model vs simple rule at ranking decoupling windows",
         f"Better than the rule, but not a usable yes/no classifier.", "Moderate"),
    ]
    for ax, (num, label, meaning, conf) in zip(axes.flat, panels):
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.add_patch(FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0,rounding_size=0.04", fc="#F5F7FA", ec=GRID, lw=1))
        ax.text(0.07, 0.86, num, fontsize=22 if len(num) < 8 else 17, fontweight="bold", color=BLUE, va="center", ha="left")
        ax.text(0.07, 0.68, wrap(label, 27), fontsize=8.3, fontweight="bold", va="top", color=INK)
        ax.text(0.07, 0.40, wrap(meaning, 34), fontsize=8, va="top", color=INK2)
        badge(ax, 0.07, 0.07, conf, w=0.7, h=0.1, size=7.8)
    ax = axes.flat[5]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.04, 0.93, "How to read the badges", fontsize=9.5, fontweight="bold", va="top")
    y = 0.80
    for lvl, txt in [("High", "tested in advance, survives every check, backed by another week"),
                     ("Moderate", "supported, but modest, under-powered or tied to one choice"),
                     ("Low", "exploratory, after the fact, or fragile")]:
        badge(ax, 0.04, y - 0.02, lvl, w=0.62, h=0.085, size=7.8)
        ax.text(0.04, y - 0.045, wrap(txt, 38), fontsize=7.6, va="top", color=INK2)
        y -= 0.29
    fig.suptitle("Key findings at a glance", x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=0.985)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.01, wspace=0.05, hspace=0.06)
    save(fig, "fig_findings_glance.png")


# =========================================================================================== 3 income vs CO2
def fig_income_scatter() -> None:
    cs = pd.read_csv(INPUTS / "week2/data/processed/cross_section_2022.csv")
    d = cs[(cs.gdp_pc > 0) & (cs.co2_pc > 0)].dropna(subset=["income_group"]).copy()
    x, y = np.log10(d.gdp_pc), np.log10(d.co2_pc)
    slope, icpt = np.polyfit(x, y, 1)
    fig, ax = plt.subplots(figsize=(W, 4.7))
    for g in INCOME_ORDER:
        s = d[d.income_group == g]
        ax.scatter(s.gdp_pc, s.co2_pc, s=30, marker=INC_MARK[g], color=INC_COL[g], edgecolor="white", linewidth=0.5, alpha=0.95, label=f"{INC_SHORT[g]} income", zorder=3)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(10 ** xs, 10 ** (icpt + slope * xs), color=VERM, lw=2, zorder=2, label="Trend line (fitted to the logged values)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([500, 1000, 10000, 100000])
    ax.set_xticklabels(["$500", "$1,000", "$10,000", "$100,000"])
    ax.set_yticks([0.1, 1, 10])
    ax.set_yticklabels(["0.1", "1", "10"])
    ax.minorticks_off()
    ax.set_xlabel("Income per person in 2022 (US$, log scale: each step is ten times more)")
    ax.set_ylabel("CO2 per person in 2022\n(tonnes, log scale)")
    ax.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    pick = {"QAT": (-8, 4), "LUX": (-6, 16), "USA": (-8, -16), "CHN": (6, 6), "IND": (8, -8), "CHE": (-6, -14), "NGA": (7, -8),
            "COD": (6, -6), "BRB": (5, 3), "DEU": (-4, 7)}
    names = {"QAT": "Qatar", "LUX": "Luxembourg", "USA": "United States", "CHN": "China", "IND": "India", "CHE": "Switzerland",
             "NGA": "Nigeria", "COD": "DR Congo", "BRB": "", "DEU": ""}
    for iso, (dx, dy) in pick.items():
        r = d[d.iso3 == iso]
        if len(r) and names[iso]:
            ha = "right" if dx < 0 else "left"
            ax.annotate(names[iso], (r.gdp_pc.iloc[0], r.co2_pc.iloc[0]), xytext=(dx, dy), textcoords="offset points", fontsize=8.3,
                        color=INK, ha=ha, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, shrinkA=0, shrinkB=2))
    ax.legend(loc="upper left", fontsize=8.5, title="Income group (World Bank, current)", title_fontsize=8.3, ncol=1, handletextpad=0.3, borderaxespad=0.3)
    ax.set_xlim(280, 190000)
    ax.set_title(f"Richer countries emit more per person (rank correlation {L('h1_rho')})")
    fig.text(0.01, 0.01, "Sources: Our World in Data (CO2, production-based), World Bank (GDP per person, constant 2015 US$). Each dot is a country.", fontsize=7.5, color=MUTED)
    fig.subplots_adjust(left=0.12, right=0.98, top=0.92, bottom=0.14)
    save(fig, "fig_income_vs_co2.png")


# =========================================================================================== 4 decoupling by group
def fig_decoupling_by_group() -> None:
    d = pd.read_csv(RESULTS / "decoupling_by_income_1990_2022.csv").set_index("income_group")
    fig, ax = plt.subplots(figsize=(W, 4.0))
    xs = np.arange(4)
    for i, g in enumerate(INCOME_ORDER):
        r = d.loc[g]
        ax.bar(i, 100 * r.share_decoupled, width=0.62, color=INC_COL[g], zorder=3)
        ax.plot([i, i], [100 * r.wilson_lo, 100 * r.wilson_hi], color=INK, lw=1.4, zorder=4)
        for yy in (r.wilson_lo, r.wilson_hi):
            ax.plot([i - 0.07, i + 0.07], [100 * yy] * 2, color=INK, lw=1.4, zorder=4)
        ax.text(i, 100 * r.wilson_hi + 3, f"{100 * r.share_decoupled:.0f}%", ha="center", fontsize=12, fontweight="bold", color=INK)
        ax.text(i, 100 * r.wilson_hi + 11, f"{int(r.n_decoupled)} of {int(r.n_countries)}", ha="center", fontsize=8.8, color=INK2)
        ax.text(i, -9, INC_SHORT[g] + NL + "income", ha="center", va="top", fontsize=9, color=INK)
    allr = d.loc["All countries"]
    ax.axhline(100 * allr.share_decoupled, color=VERM, lw=1.6, ls=(0, (5, 3)), zorder=2)
    ax.text(-0.5, 95, f"Dashed line: all countries together ({100 * allr.share_decoupled:.0f}%)", color=VERM, fontsize=8.8, fontweight="bold", ha="left", va="center")
    ax.set_xticks([])
    ax.set_xlim(-0.55, 3.55)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_ylabel("Countries whose CO2 per person fell\nwhile income per person rose")
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_title("Decoupling between 1990 and 2022 is mostly a high-income story")
    fig.text(0.01, 0.01, "Whiskers: 95% intervals (Wilson). Counts are countries with data in both years." + NL + "Groups use the current World Bank classification.", fontsize=7.5, color=MUTED)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.92, bottom=0.2)
    save(fig, "fig_decoupling_by_group.png")


# =========================================================================================== 5 decoupling over time
def fig_decoupling_over_time() -> None:
    d = pd.read_csv(RESULTS / "decoupling_over_time.csv")
    fig, ax = plt.subplots(figsize=(W, 4.4))
    ax.axvspan(2013.5, 2016.5, color="#EDEFF2", zorder=0)
    ax.axvspan(2016.5, 2019.5, color="#DCE9F5", zorder=0)
    ax.text(2015, 66, "Gap", ha="center", va="top", fontsize=8, color=INK2)
    ax.text(2018, 66, "Test", ha="center", va="top", fontsize=8, color=INK2)
    ends = {}
    for g in INCOME_ORDER:
        s = d[d.income_group == g].sort_values("window_start_year")
        ax.plot(s.window_start_year, 100 * s.share_decoupled, color=INC_COL[g], lw=2.2, marker=INC_MARK[g], ms=4.6, zorder=3)
        ends[g] = 100 * s.share_decoupled.iloc[-1]
    s = d[d.income_group == "All countries"].sort_values("window_start_year")
    ax.plot(s.window_start_year, 100 * s.share_decoupled, color=VERM, lw=1.8, ls=(0, (4, 2)), zorder=3)
    ends["All countries"] = 100 * s.share_decoupled.iloc[-1]
    # direct labels with simple de-overlap
    order = sorted(ends.items(), key=lambda kv: kv[1])
    ypos, last = {}, -99
    for g, v in order:
        yv = max(v, last + 5.2)
        ypos[g] = yv
        last = yv
    for g, v in ends.items():
        lab = "All countries" if g == "All countries" else INC_SHORT[g]
        col = VERM if g == "All countries" else INC_COL[g]
        ax.text(2019.9, ypos[g], lab, color=INK, fontsize=8.6, va="center", fontweight="bold")
        ax.plot([2019.2, 2019.8], [v, ypos[g]], color=col, lw=1.0)
    ax.set_xlim(1993, 2027.5)
    ax.set_ylim(0, 68)
    ax.set_xticks([1993, 1998, 2003, 2008, 2013, 2019])
    ax.set_xlabel("First year of the three-year window (a window starting in 2019 ends in 2022)")
    ax.set_ylabel("Countries decoupling in the window\n(% of countries with data)")
    ax.set_yticks([0, 20, 40, 60])
    ax.set_yticklabels(["0%", "20%", "40%", "60%"])
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_title("High-income countries decouple most often, in most windows")
    fig.text(0.01, 0.01, "Each point: share of countries whose CO2 per person fell and income per person rose over the next three years." + NL + "Grey band (gap): start years 2014-2016, not used by the model. Blue band: test years 2017-2019." + NL + "Income groups: current World Bank classification.", fontsize=7.3, color=MUTED)
    fig.subplots_adjust(left=0.12, right=0.985, top=0.92, bottom=0.25)
    save(fig, "fig_decoupling_over_time.png")


# =========================================================================================== 6 model skill
def fig_model_skill() -> None:
    tm = pd.read_csv(INPUTS / "week3/results/test_metrics.csv").set_index("model")
    tk = pd.read_csv(RESULTS / "model_skill_top20.csv").set_index("model")
    base = float(tm.loc["prior", "pr_auc"])
    fig = plt.figure(figsize=(W, 3.9))
    a1 = fig.add_axes([0.255, 0.2, 0.30, 0.58])
    a2 = fig.add_axes([0.66, 0.2, 0.33, 0.58])
    models = [("lr", "Logistic regression" + NL + "(chosen in advance)", BLUE), ("rf", "Random forest" + NL + "(post hoc)", GREY),
              ("hgb", "Gradient boosting" + NL + "(post hoc)", GREY), ("persistence", "Simple rule:" + NL + "copy the recent past", VERM)]
    ys = []
    for i, (m, lab, col) in enumerate(models):
        y = len(models) - 1 - i
        ys.append(y)
        a1.plot([tm.loc[m, "pr_auc_lo"], tm.loc[m, "pr_auc_hi"]], [y, y], color=col, lw=2.4, zorder=3, solid_capstyle="round")
        a1.scatter(tm.loc[m, "pr_auc"], y, s=60, color=col, edgecolor="white", zorder=4)
        a1.text(tm.loc[m, "pr_auc_hi"] + 0.015, y, f"{tm.loc[m, 'pr_auc']:.2f}", va="center", fontsize=8.8, fontweight="bold")
    a1.axvline(base, color=INK2, lw=1.4, ls=(0, (3, 2)), zorder=1)
    a1.text(base - 0.005, -0.62, f"No skill{NL}= {base:.2f}", fontsize=7.8, color=INK2, va="bottom", ha="right")
    a1.set_xlim(0.15, 0.66)
    a1.set_ylim(-0.7, 3.5)
    a1.set_yticks(ys)
    a1.set_yticklabels([m[1] for m in models], fontsize=8.2)
    a1.tick_params(axis="y", length=0)
    a1.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6])
    a1.set_xlabel("PR-AUC on test years" + NL + "(higher is better)")
    a1.set_title("Ranking skill (95% interval)")
    a1.spines["left"].set_visible(False)
    a1.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    order = ["lr", "rf", "hgb", "persistence"]
    cols = [BLUE, GREY, GREY, VERM]
    for i, m in enumerate(order):
        r = tk.loc[m]
        a2.bar(i, 100 * r.precision_top, color=cols[i], width=0.62, zorder=3)
        a2.plot([i, i], [100 * r.precision_lo, 100 * r.precision_hi], color=INK, lw=1.3, zorder=4)
        a2.text(i + 0.07, 100 * r.precision_hi + 1.4, f"{100 * r.precision_top:.0f}%", ha="center", fontsize=9.2, fontweight="bold")
    a2.axhline(100 * tk.loc["lr", "base_rate"], color=INK2, lw=1.4, ls=(0, (3, 2)), zorder=5)
    a2.text(-0.45, 100 * tk.loc["lr", "base_rate"] - 1.5, f"Base rate {100 * tk.loc['lr', 'base_rate']:.0f}%", ha="left", va="top", fontsize=7.8, color=INK2, zorder=6,
            bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.85))
    a2.set_xticks(range(4))
    a2.set_xticklabels(["Logistic", "Forest", "Boosting", "Simple" + NL + "rule"], fontsize=8.2)
    a2.set_ylim(0, 78)
    a2.set_yticks([0, 25, 50, 75])
    a2.set_yticklabels(["0%", "25%", "50%", "75%"])
    a2.set_ylabel("Share that really decoupled")
    a2.set_title(f"Top {int(round(100 * tk.loc['lr', 'top_fraction']))}% of scores: hit rate", fontsize=9.6)
    a2.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    fig.text(0.66, 0.855, "Post hoc, not pre-specified", fontsize=7.8, color=VERM, fontweight="bold", va="bottom")
    fig.suptitle("Better than chance and than a simple rule, but only modestly", x=0.01, ha="left", fontsize=10.5, fontweight="bold", y=0.985)
    fig.text(0.01, 0.015, "Test windows 2017-2019 (country windows; intervals resample whole countries). Forest and boosting were not the pre-specified choice.", fontsize=7.0, color=MUTED)
    save(fig, "fig_model_skill.png")


def _marker(ax, x, y, code, ms=13):
    if code == "pre":
        ax.plot(x, y, "o", ms=ms, mfc=BLUE, mec=BLUE, zorder=3)
    elif code == "part":
        ax.plot(x, y, "o", ms=ms, mfc=BLUE, mfcalt="white", mec=BLUE, mew=1.5, fillstyle="left", zorder=3)
    elif code == "plan":
        ax.plot(x, y, "o", ms=ms, mfc="white", mec=BLUE, mew=1.5, zorder=3)
    else:
        ax.plot([x - 0.18, x + 0.18], [y, y], color=MUTED, lw=1.6, zorder=3)


def fig_evidence_matrix() -> None:
    em = pd.read_csv(RESULTS / "evidence_matrix.csv")
    fig, ax = plt.subplots(figsize=(W, 5.15))
    ax.set_xlim(0, 10)
    n = len(em)
    ax.set_ylim(-1.7, n + 0.9)
    ax.invert_yaxis()
    ax.axis("off")
    xcols = {"week1": 5.0, "week2": 6.3, "week3": 7.6}
    heads = {"week1": "Week 1" + NL + "exploration", "week2": "Week 2" + NL + "tests", "week3": "Week 3" + NL + "model"}
    for k, x in xcols.items():
        ax.text(x, -0.25, heads[k], ha="center", va="bottom", fontsize=8.6, fontweight="bold")
    ax.text(0.0, -0.25, "Finding", ha="left", va="bottom", fontsize=8.6, fontweight="bold")
    ax.text(9.0, -0.25, "Confidence", ha="center", va="bottom", fontsize=8.6, fontweight="bold")
    for i, r in em.iterrows():
        y = i + 0.5
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((-0.1, i), 10.2, 1, fc="#F5F7FA", ec="none", zorder=0))
        ax.text(0.0, y, wrap(r["finding"], 44), ha="left", va="center", fontsize=8.6)
        for k, x in xcols.items():
            _marker(ax, x, y, r[k])
        bg, fg = CONF_COL[r["rating"]]
        ax.add_patch(FancyBboxPatch((8.2, y - 0.3), 1.6, 0.6, boxstyle="round,pad=0,rounding_size=0.2", fc=bg, ec="none", zorder=3))
        ax.text(9.0, y, r["rating"], ha="center", va="center", color=fg, fontsize=8.6, fontweight="bold", zorder=4)
    yk = n + 0.55
    xk = 0.0
    for code, lab, adv in [("pre", "Pre-specified result", 2.3), ("part", "Partial, exploratory or post hoc", 3.9), ("plan", "Planned only", 2.3), ("none", "No evidence", 2)]:
        _marker(ax, xk + 0.2, yk, code, ms=10)
        ax.text(xk + 0.5, yk, lab, va="center", fontsize=7.8, color=INK2)
        xk += adv
    ax.set_title("How strong is the evidence for each finding?", loc="left", pad=6)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02)
    save(fig, "fig_evidence_matrix.png")


# =========================================================================================== 8 roadmap
def fig_roadmap() -> None:
    rec = pd.read_csv(RESULTS / "recommendations.csv")
    phases = [("Do now", "Ready to start"), ("Do next", "Needs a small piece of new work"), ("Explore later", "Needs new data or a new test")]
    fig, ax = plt.subplots(figsize=(W, 4.6))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for j, (ph, sub) in enumerate(phases):
        ax.add_patch(FancyBboxPatch((j + 0.03, 0.9), 0.94, 0.09, boxstyle="round,pad=0,rounding_size=0.02", fc=BLUE if j == 0 else ("#2F78B7" if j == 1 else "#5E9BD1"), ec="none"))
        ax.text(j + 0.5, 0.945, ph, ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
        ax.text(j + 0.5, 0.87, sub, ha="center", va="top", fontsize=8, color=INK2, style="italic")
        items = rec[rec["phase"] == ph]
        ycur = 0.8
        for _, r in items.iterrows():
            h = 0.255
            ax.add_patch(FancyBboxPatch((j + 0.05, ycur - h), 0.9, h - 0.02, boxstyle="round,pad=0,rounding_size=0.02", fc="#F5F7FA", ec=GRID, lw=1))
            ax.text(j + 0.09, ycur - 0.035, r["id"], fontsize=9.5, fontweight="bold", color=BLUE, va="top")
            ax.text(j + 0.25, ycur - 0.035, wrap(r["short_title"], 25), fontsize=8.1, va="top", color=INK)
            bg, fg = CONF_COL[r["confidence"]]
            ax.add_patch(FancyBboxPatch((j + 0.09, ycur - h + 0.02), 0.34, 0.045, boxstyle="round,pad=0,rounding_size=0.015", fc=bg, ec="none"))
            ax.text(j + 0.26, ycur - h + 0.0425, f"{r['confidence']}", fontsize=7.6, ha="center", va="center", color=fg, fontweight="bold")
            ycur -= h + 0.005
    ax.set_title("Recommendations roadmap (badge: confidence in the evidence behind each)", loc="left", pad=6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.01)
    save(fig, "fig_roadmap.png")


def main() -> int:
    which = sys.argv[1:] or ["reused", "journey", "findings", "scatter", "bygroup", "overtime", "skill", "matrix", "roadmap"]
    fn = {"reused": copy_reused, "journey": fig_journey, "findings": fig_findings, "scatter": fig_income_scatter,
          "bygroup": fig_decoupling_by_group, "overtime": fig_decoupling_over_time, "skill": fig_model_skill,
          "matrix": fig_evidence_matrix, "roadmap": fig_roadmap}
    for k in which:
        fn[k]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
