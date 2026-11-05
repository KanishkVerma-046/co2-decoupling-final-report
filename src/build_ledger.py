"""Build results/claims_ledger.csv: one row per number or factual claim used in the report.

Every value is read from a file by `common.resolve` (a located cell, optionally with a one-step derivation such as x100).
Nothing is typed in by hand. Run after: collect_inputs.py, lineage.py, verify_headlines.py, synthesis_tables.py.
Run:  python src/build_ledger.py
"""
from __future__ import annotations

import csv
import sys

from common import INPUTS, REPOS, RESULTS, ROOT, commits, resolve

CM = commits()
SRC = {
    "w1": ("week1", REPOS["week1"]["url"], CM["week1"]),
    "w2": ("week2", REPOS["week2"]["url"], CM["week2"]),
    "w3": ("week3", REPOS["week3"]["url"], CM["week3"]),
    "new": (None, "this repository (Week 4)", "n/a (computed here from the inputs; see git log)"),
}

CLAIMS: list[dict] = []


def c(id_, text, unit, fmt, src, file, locator, deriv="", orig="", status="pre-specified"):
    wk, repo, commit = SRC[src]
    path = f"data/inputs/{wk}/{file}" if wk else file
    CLAIMS.append({"claim_id": id_, "text": text, "unit": unit, "fmt": fmt, "source_repo": repo, "source_commit": commit,
                   "source_file": file if wk else file, "input_copy": path, "locator": locator, "derivation": deriv,
                   "originally_reported": orig, "evidence_status": status})


H = "results/hypothesis_results.csv"
H6 = "results/h6_contingency_and_residuals.csv"
TM = "results/test_metrics.csv"
PROF = "data/processed/profiling/profiling_summary.json"


def hyp(id_, text, unit, fmt, h, variant, col, orig, deriv="", status="pre-specified"):
    c(id_, text, unit, fmt, "w2", H, f"{col} | hypothesis={h} & variant={variant}", deriv, orig, status)


# =============================================================================================== Week 1 (planning + profiling)
w1 = "Week 1, Section "
c("w1_owid_rows", "Rows in the Our World in Data (OWID) CO2 file", "rows", "{:,.0f}", "w1", PROF, "json: owid.shape.0", "", w1 + "2.2", "descriptive")
c("w1_owid_cols", "Columns in the OWID CO2 file", "columns", "{:.0f}", "w1", PROF, "json: owid.shape.1", "", w1 + "2.2", "descriptive")
c("w1_owid_mb", "Size of the OWID CO2 file", "MB", "{:.1f}", "w1", PROF, "json: owid.file_size_mb", "", w1 + "2.2", "descriptive")
c("w1_owid_entities", "Entities in the OWID file (countries plus regions and groups)", "entities", "{:.0f}", "w1", PROF, "json: owid.n_entities", "", w1 + "2.2", "descriptive")
c("w1_owid_countries", "OWID entities that are countries with an ISO3 code", "countries", "{:.0f}", "w1", PROF, "json: owid.n_countries_proper", "", w1 + "2.2", "descriptive")
c("w1_owid_non_countries", "OWID entities that are regions, groups or special entities", "entities", "{:.0f}", "w1", PROF, "json: owid.n_non_country_entities", "", w1 + "2.2", "descriptive")
c("w1_owid_year_min", "First year in the OWID file", "year", "{:.0f}", "w1", PROF, "json: owid.year_min", "", w1 + "2.2", "descriptive")
c("w1_owid_year_max", "Last year in the OWID file", "year", "{:.0f}", "w1", PROF, "json: owid.year_max", "", w1 + "2.2", "descriptive")
c("w1_owid_cols_half_missing", "OWID columns that are more than half empty", "columns", "{:.0f}", "w1", PROF, "json: owid.n_cols_over_50pct_missing", "", w1 + "2.2", "descriptive")
c("w1_window_co2_missing", "Share of OWID country-years missing CO2 in 1990-2022", "%", "{:.1f}", "w1", PROF, "json: owid.window_co2_pct_missing", "", w1 + "2.2", "descriptive")
c("w1_window_owid_gdp_missing", "Share of OWID country-years missing OWID's own GDP column in 1990-2022", "%", "{:.1f}", "w1", PROF, "json: owid.window_gdp_pct_missing", "", w1 + "2.2", "descriptive")
c("w1_window_wb_gdp_missing", "Share of World Bank country-years missing GDP per person in 1990-2022", "%", "{:.1f}", "w1", PROF, "json: worldbank.window_pct_missing_by_indicator.gdp_per_capita_const2015usd", "", w1 + "2.3", "descriptive")
c("w1_wb_entities", "Entities in the World Bank download", "entities", "{:.0f}", "w1", PROF, "json: worldbank.n_entities", "", w1 + "2.3", "descriptive")
c("w1_wb_aggregates", "World Bank entities that are aggregates (regions, income groups)", "entities", "{:.0f}", "w1", PROF, "json: worldbank.n_aggregates", "", w1 + "2.3", "descriptive")
c("w1_wb_snapshot", "Date of the World Bank data snapshot reported in Week 1", "date", "{}", "w1", PROF, "json: worldbank.source_last_updated", "", w1 + "2.3", "descriptive")
c("w1_iso_matched", "Countries found in both sources when matched on ISO3 code", "countries", "{:.0f}", "w1", PROF, "json: join.iso3_matched", "", w1 + "2.5", "descriptive")
c("w1_name_matched", "Countries found in both sources when matched on exact country name", "countries", "{:.0f}", "w1", PROF, "json: join.name_matched", "", w1 + "2.5", "descriptive")
c("w1_name_lost", "Countries a name-based join would have lost", "countries", "{:.0f}", "w1", PROF, "json: join.iso_matched_but_name_differs", "", w1 + "2.5", "descriptive")
c("w1_joined_rows", "Joined country-year rows in the 1990-2022 preview", "rows", "{:,.0f}", "w1", PROF, "json: join.joined_rows_window", "", w1 + "2.5", "descriptive")
c("w1_complete_rows", "Preview rows with both CO2 per person and GDP per person", "rows", "{:,.0f}", "w1", PROF, "json: join.complete_pairs_co2pc_gdppc_window", "", w1 + "2.5", "descriptive")
c("w1_complete_pct", "Share of preview rows with both CO2 per person and GDP per person", "%", "{:.1f}", "w1", PROF, "json: join.pct_window_rows_complete_pairs", "", w1 + "2.5", "descriptive")
c("w1_smoke_rho", "Week 1 preliminary rank correlation, income vs CO2 per person, 2022", "correlation", "{:.2f}", "w1", PROF, "json: join.preview_spearman_2022", "", w1 + "6 (smoke test)", "planning-stage")
c("w1_smoke_rho3", "Week 1 preliminary rank correlation to three decimals", "correlation", "{:.3f}", "w1", PROF, "json: join.preview_spearman_2022", "", w1 + "6 (smoke test)", "planning-stage")
c("w1_smoke_n", "Countries in the Week 1 preliminary correlation", "countries", "{:.0f}", "w1", PROF, "json: join.countries_complete_pair_2022", "", w1 + "6 (smoke test)", "planning-stage")
c("w1_smoke_pearson_raw", "Week 1 preliminary Pearson correlation on raw (unlogged) values", "correlation", "{:.2f}", "w1", PROF, "json: join.preview_raw_pearson_2022", "", w1 + "6 (smoke test)", "planning-stage")
c("w1_smoke_pearson_log", "Week 1 preliminary Pearson correlation on log values", "correlation", "{:.2f}", "w1", PROF, "json: join.preview_log_pearson_2022", "", w1 + "6 (smoke test)", "planning-stage")
c("w1_n_questions", "Questions in the Week 1 exploratory plan", "questions", "{:.0f}", "w1", "report/report_content.md", r"regex: \| Q(10) \| How sensitive", "", w1 + "3", "planning-stage")
c("w1_top_emitter_value", "Highest CO2 per person in 2022 in the OWID file (Qatar)", "tonnes per person", "{:.1f}", "w1", "data/processed/profiling/owid_top10_co2_per_capita_2022.csv", "co2_per_capita | country=Qatar", "", w1 + "4 (profiling)", "descriptive")
c("w1_skew_raw", "Skewness of raw CO2 per person in 2022", "skewness", "{:.2f}", "w1", "report/report_content.md", r"regex: Raw 2022 CO2 per capita skew (\d\.\d\d)", "", w1 + "4", "descriptive")

# =============================================================================================== Week 2: data and cleaning
c("w2_entities", "Country entities considered before any exclusion", "entities", "{:.0f}", "w2", "results/sample_flow.csv", "n_remaining | hypothesis=H1 & stage=all country entities (WB country list U OWID countries)", "", "Week 2, Section 3.4", "descriptive")
c("w2_no_co2_2022", "Entities without CO2 per person in 2022", "entities", "{:.0f}", "w2", "results/sample_flow.csv", "n_excluded | hypothesis=H1 & stage=no CO2 pc in 2022 (or <= 0)", "", "Week 2, Section 3.4", "descriptive")
c("w2_no_gdp_2022", "Further entities without GDP per person in 2022", "entities", "{:.0f}", "w2", "results/sample_flow.csv", "n_excluded | hypothesis=H1 & stage=no GDP pc in 2022 (or <= 0)", "", "Week 2, Section 3.4", "descriptive")
c("w2_owid_aggregates", "OWID non-country entities removed (no ISO3 code)", "entities", "{:.0f}", "w2", "results/cleaning_log.csv", "note | step=owid_agg", "regex:(\\d+) non-country", "Week 2, Section 3.3", "descriptive")
c("w2_wb_aggregates", "World Bank aggregate entities removed", "entities", "{:.0f}", "w2", "results/cleaning_log.csv", "rows_dropped_or_changed | step=wb_meta", "", "Week 2, Section 3.3", "descriptive")
c("w2_join_both", "Country-years present in both sources after the join", "country-years", "{:,.0f}", "w2", "results/cleaning_log.csv", "note | step=join", r"regex:both=([\d,]+)", "Week 2, Section 3.3", "descriptive")
c("w2_join_owid_only", "Country-years only in OWID after the join", "country-years", "{:,.0f}", "w2", "results/cleaning_log.csv", "note | step=join", r"regex:owid_only=([\d,]+)", "Week 2, Section 3.3", "descriptive")
c("w2_join_wb_only", "Country-years only in the World Bank data after the join", "country-years", "{:,.0f}", "w2", "results/cleaning_log.csv", "note | step=join", r"regex:wb_only=([\d,]+)", "Week 2, Section 3.3", "descriptive")
c("w2_kosovo_rows", "Kosovo rows re-keyed by the one-line crosswalk", "rows", "{:.0f}", "w2", "results/cleaning_log.csv", "rows_before | step=owid_crosswalk", "", "Week 2, Section 3.3", "descriptive")
c("w2_log_guard_rows", "Country-years with CO2 per person of zero, kept but excluded from log transforms", "country-years", "{:.0f}", "w2", "results/cleaning_log.csv", "rows_dropped_or_changed | step=logguard:co2_pc", "", "Week 2, Section 3.3", "descriptive")

# =============================================================================================== Week 2: hypothesis tests
S = "Week 2, Section "
c("n_hypotheses", "Hypotheses in the Week 2 plan", "hypotheses", "{:.0f}", "w2", H, "hypothesis | hypothesis=H7 & variant=primary (exploratory)", "regex:H(\\d)", S + "2.2", "pre-specified")
c("n_confirmatory", "Confirmatory hypotheses corrected with Holm", "hypotheses", "{:.0f}", "w2", H, "hypothesis | hypothesis=H6 & variant=primary", "regex:H(\\d)", S + "2.4", "pre-specified")
hyp("h1_n", "Countries in the income-emissions rank correlation (2022)", "countries", "{:.0f}", "H1", "primary", "n", S + "6.2")
hyp("h1_rho", "Spearman rank correlation, GDP per person vs CO2 per person (2022)", "correlation", "{:.3f}", "H1", "primary", "effect_size", S + "6.1")
hyp("h1_rho2", "Same correlation to two decimals", "correlation", "{:.2f}", "H1", "primary", "effect_size", S + "6.1")
hyp("h1_ci_lo", "Lower end of the 95% interval for the rank correlation", "correlation", "{:.3f}", "H1", "primary", "ci_low", S + "6.1")
hyp("h1_ci_hi", "Upper end of the 95% interval for the rank correlation", "correlation", "{:.3f}", "H1", "primary", "ci_high", S + "6.1")
hyp("h1_pearson", "Pearson correlation of the log10 values (companion)", "correlation", "{:.3f}", "H1", "companion: Pearson on log10 values", "effect_size", S + "6.2")
hyp("h1_rho_ppp", "Rank correlation using the PPP income measure", "correlation", "{:.3f}", "H1", "robustness: PPP GDP", "effect_size", S + "6.2")
hyp("h1_rho_ppp_n", "Countries in the PPP robustness check", "countries", "{:.0f}", "H1", "robustness: PPP GDP", "n", S + "6.2")
hyp("h1_rho_small", "Rank correlation without countries under one million people", "correlation", "{:.3f}", "H1", "robustness: excluding population < 1 million", "effect_size", S + "6.2")
hyp("h1_rho_oil", "Rank correlation without oil and gas exporters", "correlation", "{:.3f}", "H1", "robustness: excluding oil/gas exporters", "effect_size", S + "6.2")
hyp("h1_p_holm", "Holm-adjusted p-value, H1", "p-value", "{:.0e}", "H1", "primary", "p_holm", S + "6.1")
c("h2_n", "Countries in the income-group comparison (H2)", "countries", "{:.0f}", "w2", H, "n | hypothesis=H2 & variant=primary", "", S + "6.3")
c("h2_eps2", "Effect size (epsilon-squared) for CO2 per person across income groups", "effect size", "{:.2f}", "w2", H, "effect_size | hypothesis=H2 & variant=primary", "", S + "6.3")
c("h2_eps2_lo", "Lower end of the 95% interval for epsilon-squared", "effect size", "{:.2f}", "w2", H, "ci_low | hypothesis=H2 & variant=primary", "", S + "6.3")
c("h2_eps2_hi", "Upper end of the 95% interval for epsilon-squared", "effect size", "{:.2f}", "w2", H, "ci_high | hypothesis=H2 & variant=primary", "", S + "6.3")
G = "results/h2_group_descriptives.csv"
for key, grp in [("low", "Low income"), ("lm", "Lower middle income"), ("um", "Upper middle income"), ("high", "High income")]:
    c(f"med_{key}", f"Median CO2 per person in 2022, {grp}", "tonnes per person", "{:.2f}", "w2", G, f"median_co2_pc | income_group={grp}", "", S + "6.3")
    c(f"n_{key}", f"Countries in {grp} (2022 emissions sample)", "countries", "{:.0f}", "w2", G, f"n | income_group={grp}", "", S + "6.3")
c("geo_high", "Geometric-mean CO2 per person in 2022, high-income countries", "tonnes per person", "{:.1f}", "w2", G, "geom_mean_co2_pc | income_group=High income", "", S + "6.3")
c("h3_n", "Countries in the high vs lower-income comparison", "countries", "{:.0f}", "w2", H, "n | hypothesis=H3 & variant=primary", "", S + "6.3")
c("h3_ratio", "High-income countries' CO2 per person relative to lower-middle plus low income combined (geometric means)", "times", "{:.1f}", "w2", H, "effect_size | hypothesis=H3 & variant=robustness: permutation of mean difference", "pow10", S + "6.3")
c("h3_ratio2", "Same ratio to two decimals", "times", "{:.2f}", "w2", H, "effect_size | hypothesis=H3 & variant=robustness: permutation of mean difference", "pow10", S + "6.3")
c("h3_d", "Cohen's d for the high vs lower-income difference", "effect size", "{:.2f}", "w2", H, "effect_size | hypothesis=H3 & variant=primary", "", S + "6.3")
c("h3_ratio_small", "Same ratio without countries under one million people", "times", "{:.1f}", "w2", H, "comment | hypothesis=H3 & variant=robustness: excluding population < 1 million", r"regex:ratio=([\d.]+)x", S + "6.3")
c("h3_ratio_oil", "Same ratio without oil and gas exporters", "times", "{:.1f}", "w2", H, "comment | hypothesis=H3 & variant=robustness: excluding oil/gas exporters", r"regex:ratio=([\d.]+)x", S + "6.3")
hyp("h4_p_raw", "Raw p-value of the slope-difference test (H4)", "p-value", "{:.3f}", "H4", "primary", "p_raw", S + "6.4")
hyp("h4_p_holm", "Holm-adjusted p-value of the slope-difference test (H4)", "p-value", "{:.4f}", "H4", "primary", "p_holm", S + "6.4")
hyp("h5_p_holm", "Holm-adjusted p-value of the high-income decline test (H5)", "p-value", "{:.4f}", "H5", "primary", "p_holm", S + "6.5")
hyp("h4_dr2", "Extra variance explained by letting the slope differ by income group", "share of variance", "{:.3f}", "H4", "primary", "effect_size", S + "6.4")
hyp("h4_p_small", "H4 p-value without countries under one million people", "p-value", "{:.3f}", "H4", "robustness: excluding population < 1 million", "p_raw", S + "6.4")
hyp("h4_p_labelperm", "H4 p-value from the planned label-permutation check", "p-value", "{:.3f}", "H4", "robustness: income-group label permutation (as planned)", "p_raw", S + "6.4")
hyp("h4_p_fl", "H4 p-value from the Freedman-Lane permutation (added after planning)", "p-value", "{:.3f}", "H4", "robustness: Freedman-Lane residual permutation (added)", "p_raw", S + "6.4")
hyp("h4_p_oil", "H4 p-value without oil and gas exporters", "p-value", "{:.3f}", "H4", "robustness: excluding oil/gas exporters", "p_raw", S + "6.4")
hyp("h4_p_ppp", "H4 p-value using the PPP income measure", "p-value", "{:.3f}", "H4", "robustness: PPP GDP", "p_raw", S + "6.4")
SL = "results/h4_slopes_by_group.csv"
for key, grp in [("low", "Low income"), ("lm", "Lower middle income"), ("um", "Upper middle income"), ("high", "High income")]:
    c(f"slope_{key}", f"Slope of log CO2 on log income, {grp}", "slope", "{:.2f}", "w2", SL, f"slope | income_group={grp}", "", S + "6.4")
c("slope_high_lo", "Lower end of the 95% interval, high-income slope", "slope", "{:.2f}", "w2", SL, "ci_low | income_group=High income", "", S + "6.4")
c("slope_high_hi", "Upper end of the 95% interval, high-income slope", "slope", "{:.2f}", "w2", SL, "ci_high | income_group=High income", "", S + "6.4")
c("h5_n", "High-income countries with CO2 in both 1990 and 2022", "countries", "{:.0f}", "w2", H, "n | hypothesis=H5 & variant=primary", "", S + "6.5")
c("h5_median", "Median change in CO2 per person, high-income countries, 1990-2022", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=primary", r"regex:median change=(-?[\d.]+)%", S + "6.5")
c("h5_median_abs", "Same median change as a positive number (size of the fall)", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=primary", r"regex:median change=(-?[\d.]+)% >> abs", S + "6.5")
c("h5_ci_lo", "Lower end of the 95% interval for the median change", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=primary", r"regex:\[(-?[\d.]+), -?[\d.]+\]", S + "6.5")
c("h5_ci_hi", "Upper end of the 95% interval for the median change", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=primary", r"regex:\[-?[\d.]+, (-?[\d.]+)\]", S + "6.5")
c("h5_fell", "High-income countries whose CO2 per person fell", "countries", "{:.0f}", "w2", H, "comment | hypothesis=H5 & variant=primary", r"regex:; (\d+) of", S + "6.5")
c("h5_fell_pct", "Share of high-income countries whose CO2 per person fell", "%", "{:.0f}", "w2", H, "effect_size | hypothesis=H5 & variant=robustness: sign test", "x100", S + "6.5")
hyp("h5_rbc", "Matched-pairs rank-biserial correlation, H5", "effect size", "{:.2f}", "H5", "primary", "effect_size", S + "6.5")
hyp("h5_rbc_hi", "Upper end of the 95% interval for the H5 effect size", "effect size", "{:.2f}", "H5", "primary", "ci_high", S + "6.5")
hyp("h5_dz", "Paired-t effect size (d_z) for H5, companion test", "effect size", "{:.2f}", "H5", "companion: paired t-test on log ratios (normality VIOLATED - shown for transparency only)", "effect_size", S + "6.5", deriv="abs")
c("h5_mde", "Smallest paired effect the H5 design could detect with 80% power", "effect size", "{:.2f}", "w2", "results/power_mde.csv", "mde_d_80pct_power | hypothesis=H5 & test=paired t (one-sided)", "", S + "4.6")
c("h5_median_small", "Median change without countries under one million people", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=robustness: excluding population < 1 million", r"regex:median change=(-?[\d.]+)%", S + "6.5")
c("h5_median_oil", "Median change without oil and gas exporters", "%", "{:.1f}", "w2", H, "comment | hypothesis=H5 & variant=robustness: excluding oil/gas exporters", r"regex:median change=(-?[\d.]+)%", S + "6.5")
c("h6_n", "Countries in the decoupling comparison", "countries", "{:.0f}", "w2", H, "n | hypothesis=H6 & variant=primary", "", S + "6.6")
for key, grp in [("low", "Low income"), ("lm", "Lower middle income"), ("um", "Upper middle income"), ("high", "High income")]:
    c(f"dec_pct_{key}", f"Share of {grp} countries that decoupled, 1990-2022", "%", "{:.0f}", "w2", H6, f"row_pct_decoupled | income_group={grp} & outcome=Decoupled", "", S + "6.6")
    c(f"dec_pct1_{key}", f"Same share to one decimal, {grp}", "%", "{:.1f}", "w2", H6, f"row_pct_decoupled | income_group={grp} & outcome=Decoupled", "", S + "6.6")
    c(f"dec_k_{key}", f"Decoupled countries, {grp}", "countries", "{:.0f}", "w2", H6, f"observed | income_group={grp} & outcome=Decoupled", "", S + "6.6")
c("dec_notdec_high", "High-income countries that did not decouple", "countries", "{:.0f}", "w2", H6, "observed | income_group=High income & outcome=Not decoupled", "", S + "6.6")
c("dec_notdec_pct_high", "Share of high-income countries that did not decouple", "%", "{:.0f}", "w2", H6, "row_pct_decoupled | income_group=High income & outcome=Decoupled", "100-x", S + "6.6")
hyp("h6_v", "Cramer's V for income group vs decoupling", "effect size", "{:.2f}", "H6", "primary", "effect_size", S + "6.6")
hyp("h6_v_lo", "Lower end of the 95% interval for Cramer's V", "effect size", "{:.2f}", "H6", "primary", "ci_low", S + "6.6")
hyp("h6_v_hi", "Upper end of the 95% interval for Cramer's V", "effect size", "{:.2f}", "H6", "primary", "ci_high", S + "6.6")
hyp("h6_or", "Odds ratio, high-income vs other countries, decoupling", "odds ratio", "{:.1f}", "H6", "check: 2x2 Fisher exact (High vs not High)", "effect_size", S + "6.6")
hyp("h6_or_lo", "Lower end of the 95% interval for the odds ratio", "odds ratio", "{:.1f}", "H6", "check: 2x2 Fisher exact (High vs not High)", "ci_low", S + "6.6")
hyp("h6_or_hi", "Upper end of the 95% interval for the odds ratio", "odds ratio", "{:.1f}", "H6", "check: 2x2 Fisher exact (High vs not High)", "ci_high", S + "6.6")
hyp("h6_p_holm", "Holm-adjusted p-value, H6", "p-value", "{:.0e}", "H6", "primary", "p_holm", S + "6.6")
c("h7_n", "Countries in the exploratory structural-drivers model", "countries", "{:.0f}", "w2", H, "n | hypothesis=H7 & variant=primary (exploratory)", "", S + "6.7", "exploratory")
c("h7_dr2", "Extra variance explained by industry share and urbanisation beyond income", "share of variance", "{:.2f}", "w2", H, "effect_size | hypothesis=H7 & variant=primary (exploratory)", "", S + "6.7", "exploratory")
c("h7_r2_full", "Variance explained by income, industry share and urbanisation together", "share of variance", "{:.2f}", "w2", H, "comment | hypothesis=H7 & variant=primary (exploratory)", r"regex:R2 full=([\d.]+)", S + "6.7", "exploratory")
c("h7_r2_gdp", "Variance explained by income alone in the same sample", "share of variance", "{:.2f}", "w2", H, "comment | hypothesis=H7 & variant=primary (exploratory)", r"regex:GDP only=([\d.]+)", S + "6.7", "exploratory")
c("h7_industry_pct", "CO2 per person higher by this share per extra percentage point of industry in GDP, at the same income", "%", "{:.1f}", "w2", "results/h7_coefficients.csv", "coef | variant=primary (exploratory) & term=industry_pct_latest", "pct_pow10", S + "6.7", "exploratory")
c("h7_industry_pr2", "Partial R-squared of industry share", "share of variance", "{:.2f}", "w2", "results/h7_coefficients.csv", "partial_r2 | variant=primary (exploratory) & term=industry_pct_latest", "", S + "6.7", "exploratory")
c("h7_urban_lo", "Urbanisation coefficient, lower end of 95% interval", "log10 units per point", "{:.4f}", "w2", "results/h7_coefficients.csv", "ci_low | variant=primary (exploratory) & term=urban_pct_latest", "", S + "6.7", "exploratory")
c("h7_urban_hi", "Urbanisation coefficient, upper end of 95% interval", "log10 units per point", "{:.4f}", "w2", "results/h7_coefficients.csv", "ci_high | variant=primary (exploratory) & term=urban_pct_latest", "", S + "6.7", "exploratory")
c("h7_income_coef", "Income elasticity in the exploratory model", "elasticity", "{:.2f}", "w2", "results/h7_coefficients.csv", "coef | variant=primary (exploratory) & term=lg_gdp", "", S + "6.7", "exploratory")
c("w2_pytest_reported", "Pytest checks reported by Week 2", "checks", "{:.0f}", "new", "results/reference_pytest.csv", "reported_by_repo | week=week2", "", "Week 2, Section 7", "process")
c("w2_pytest_passed", "Week 2 pytest checks passing on a fresh clone", "checks", "{:.0f}", "new", "results/reference_pytest.csv", "passed | week=week2", "", "Week 4 (executed here)", "process")
c("w2_pytest_failed", "Week 2 pytest checks failing on a fresh clone (line-ending effect on raw-file hashes)", "checks", "{:.0f}", "new", "results/reference_pytest.csv", "failed | week=week2", "", "Week 4 (executed here)", "process")

# =============================================================================================== Week 3
S3 = "Week 3, Section "
LB = "results/label_base_rate_overall.csv"
c("w3_pool_rows", "Decoupling windows in the training pool (1993-2013 start years)", "windows", "{:,.0f}", "w3", LB, "n_rows | scope=pool", "", S3 + "8.1")
c("w3_pool_pos", "Decoupling windows (label = 1) in the pool", "windows", "{:,.0f}", "w3", LB, "n_positive | scope=pool", "", S3 + "8.1")
c("w3_pool_rate", "Share of pool windows that are decoupling windows", "%", "{:.1f}", "w3", LB, "base_rate | scope=pool", "x100", S3 + "8.1")
c("w3_pool_countries", "Countries in the pool", "countries", "{:.0f}", "w3", LB, "n_countries | scope=pool", "", S3 + "8.1")
c("w3_test_rows", "Windows in the test set (start years 2017-2019)", "windows", "{:,.0f}", "w3", LB, "n_rows | scope=test", "", S3 + "8.1")
c("w3_test_pos", "Decoupling windows in the test set", "windows", "{:,.0f}", "w3", LB, "n_positive | scope=test", "", S3 + "8.1")
c("w3_test_rate", "Share of test windows that are decoupling windows (the no-skill PR-AUC line)", "%", "{:.1f}", "w3", LB, "base_rate | scope=test", "x100", S3 + "8.1")
c("w3_test_countries", "Countries in the test set", "countries", "{:.0f}", "w3", LB, "n_countries | scope=test", "", S3 + "8.1")
c("w3_all_rows", "Eligible decoupling windows in the pool plus test", "windows", "{:,.0f}", "w3", LB, "n_rows | scope=all eligible pool + test rows", "", S3 + "8.1")
for yr in (2017, 2018, 2019):
    c(f"w3_rate_{yr}", f"Share of windows starting in {yr} that are decoupling windows", "%", "{:.1f}", "w3", "results/label_base_rate_by_year.csv", f"base_rate | year={yr}", "x100", S3 + "8.1")
c("w3_flow_start", "Country-years before any eligibility rule (start years 1993-2019)", "country-years", "{:,.0f}", "w3", "results/sample_flow.csv", "n_remaining | stage=all entity-years, t = 1993-2019", "", S3 + "2.2", "descriptive")
c("w3_flow_end", "Eligible windows after all eligibility rules (pool + purge gap + test)", "windows", "{:,.0f}", "w3", "results/sample_flow.csv", "n_remaining | stage=no GDP per capita > 0 at t+3", "", S3 + "2.2", "descriptive")
CV = "results/cv_model_comparison.csv"
for m, nm in [("lr", "elastic-net logistic regression"), ("rf", "random forest"), ("hgb", "gradient boosting"), ("persistence", "persistence rule"), ("prior", "base-rate (prior) baseline")]:
    c(f"cv_prauc_{m}", f"Cross-validated PR-AUC, {nm}", "PR-AUC", "{:.3f}", "w3", CV, f"pr_auc_mean | model={m}", "", S3 + "8.3")
c("cv_se_rf", "Standard error of the random forest's cross-validated PR-AUC", "PR-AUC", "{:.3f}", "w3", CV, "pr_auc_se | model=rf", "", S3 + "8.3")
c("cv_cutoff", "Cross-validated PR-AUC a simpler model needed to be within one standard error of the best", "PR-AUC", "{:.3f}", "w3", "results/model_selection.csv", "threshold_for_simpler", "", S3 + "8.3")
c("cv_lr_minus_persist", "Cross-validated PR-AUC advantage of the logistic regression over persistence", "PR-AUC", "{:.3f}", "w3", "results/cv_paired_differences.csv", "diff | model_a=lr & model_b=persistence", "", S3 + "8.3")
c("cv_lr_minus_persist_lo", "Lower end of the 95% interval", "PR-AUC", "{:.3f}", "w3", "results/cv_paired_differences.csv", "ci_low | model_a=lr & model_b=persistence", "", S3 + "8.3")
c("cv_lr_minus_persist_hi", "Upper end of the 95% interval", "PR-AUC", "{:.3f}", "w3", "results/cv_paired_differences.csv", "ci_high | model_a=lr & model_b=persistence", "", S3 + "8.3")
c("thr_lr", "Frozen decision threshold of the logistic regression", "probability", "{:.3f}", "w3", "results/frozen_config.json", "json: models.lr.threshold", "", S3 + "8.3")
c("frozen_utc", "Time the Week 3 configuration was frozen", "UTC", "{}", "w3", "results/frozen_config.json", "json: frozen_utc", "", S3 + "8.4")
c("test_run_utc", "Time of the single Week 3 test run", "UTC", "{}", "w3", "results/test_run_lock.json", "json: run_utc", "", S3 + "8.4")
for m, nm in [("lr", "logistic regression"), ("rf", "random forest"), ("hgb", "gradient boosting"), ("persistence", "persistence rule"), ("prior", "base-rate (prior) baseline")]:
    st = "post hoc" if m in ("rf", "hgb") else "pre-specified"
    c(f"test_prauc_{m}", f"Test PR-AUC, {nm}", "PR-AUC", "{:.3f}", "w3", TM, f"pr_auc | model={m}", "", S3 + "8.4", st)
    c(f"test_prauc2_{m}", f"Test PR-AUC, {nm} (two decimals)", "PR-AUC", "{:.2f}", "w3", TM, f"pr_auc | model={m}", "", S3 + "8.4", st)
    c(f"test_prauc_lo_{m}", f"Lower end of the 95% interval, test PR-AUC, {nm}", "PR-AUC", "{:.2f}", "w3", TM, f"pr_auc_lo | model={m}", "", S3 + "8.4", st)
    c(f"test_prauc_hi_{m}", f"Upper end of the 95% interval, test PR-AUC, {nm}", "PR-AUC", "{:.2f}", "w3", TM, f"pr_auc_hi | model={m}", "", S3 + "8.4", st)
    c(f"test_roc_{m}", f"Test ROC-AUC, {nm}", "ROC-AUC", "{:.3f}", "w3", TM, f"roc_auc | model={m}", "", S3 + "8.4", st)
    c(f"test_f1_{m}", f"Test F1 at the frozen threshold, {nm}", "F1", "{:.3f}", "w3", TM, f"f1 | model={m}", "", S3 + "8.4", st)
    c(f"test_mcc_{m}", f"Test MCC at the frozen threshold, {nm}", "MCC", "{:.3f}", "w3", TM, f"mcc | model={m}", "", S3 + "8.4", st)
    c(f"test_prec_{m}", f"Test precision at the frozen threshold, {nm}", "share", "{:.3f}", "w3", TM, f"precision | model={m}", "", S3 + "8.4", st)
    c(f"test_rec_{m}", f"Test recall at the frozen threshold, {nm}", "share", "{:.3f}", "w3", TM, f"recall | model={m}", "", S3 + "8.4", st)
    c(f"test_acc_{m}", f"Test accuracy at the frozen threshold, {nm}", "share", "{:.3f}", "w3", TM, f"accuracy | model={m}", "", S3 + "8.4", st)
for k in ("tp", "fp", "tn", "fn"):
    c(f"test_{k}_lr", f"Logistic regression test confusion count {k.upper()}", "windows", "{:.0f}", "w3", "results/test_confusion.csv", f"{k} | model=lr", "", S3 + "8.4")
c("test_mcc_lo_lr", "Lower end of the 95% interval, logistic regression test MCC", "MCC", "{:.3f}", "w3", TM, "mcc_lo | model=lr", "", S3 + "8.4")
c("test_mcc_hi_lr", "Upper end of the 95% interval, logistic regression test MCC", "MCC", "{:.3f}", "w3", TM, "mcc_hi | model=lr", "", S3 + "8.4")
TP = "results/test_paired_differences.csv"
c("test_diff_persist", "Test PR-AUC advantage of the logistic regression over persistence", "PR-AUC", "{:.3f}", "w3", TP, "diff | model_a=lr & model_b=persistence & metric=pr_auc", "", S3 + "8.4")
c("test_diff_persist_lo", "Lower end of the 95% interval", "PR-AUC", "{:.3f}", "w3", TP, "ci_low | model_a=lr & model_b=persistence & metric=pr_auc", "", S3 + "8.4")
c("test_diff_persist_hi", "Upper end of the 95% interval", "PR-AUC", "{:.3f}", "w3", TP, "ci_high | model_a=lr & model_b=persistence & metric=pr_auc", "", S3 + "8.4")
PH = "results/test_posthoc.csv"
c("ph_group_prior", "Test PR-AUC of a rule that scores each window by its income group's base rate (post hoc reference)", "PR-AUC", "{:.3f}", "w3", PH, "value_b | model_a=lr & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_group", "Logistic regression minus income-group base rate, test PR-AUC (post hoc)", "PR-AUC", "{:.3f}", "w3", PH, "diff | model_a=lr & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_group_lo", "Lower end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_low | model_a=lr & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_group_hi", "Upper end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_high | model_a=lr & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_rf", "Logistic regression minus random forest, test PR-AUC (post hoc)", "PR-AUC", "{:.3f}", "w3", PH, "diff | model_a=lr & model_b=rf & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_rf_lo", "Lower end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_low | model_a=lr & model_b=rf & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_lr_minus_rf_hi", "Upper end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_high | model_a=lr & model_b=rf & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_rf_minus_group", "Random forest minus income-group base rate, test PR-AUC (post hoc)", "PR-AUC", "{:.3f}", "w3", PH, "diff | model_a=rf & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_rf_minus_group_lo", "Lower end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_low | model_a=rf & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
c("ph_rf_minus_group_hi", "Upper end of the 95% interval", "PR-AUC", "{:.3f}", "w3", PH, "ci_high | model_a=rf & model_b=group_prior & metric=pr_auc", "", S3 + "8.5", "post hoc")
SG = "results/test_subgroups.csv"
for key, grp in [("high", "High income"), ("um", "Upper middle income"), ("lm", "Lower middle income"), ("low", "Low income")]:
    c(f"sg_prev_{key}", f"Share of test windows that decoupled, {grp}", "%", "{:.0f}", "w3", SG, f"base_rate | grouping=income_group & group={grp}", "x100", S3 + "8.7")
    c(f"sg_roc_{key}", f"Logistic regression test ROC-AUC within {grp}", "ROC-AUC", "{:.2f}", "w3", SG, f"lr_roc_auc | grouping=income_group & group={grp}", "", S3 + "8.7")
    c(f"sg_pos_{key}", f"Decoupling test windows in {grp}", "windows", "{:.0f}", "w3", SG, f"n_positive | grouping=income_group & group={grp}", "", S3 + "8.7")
c("sg_prauc_high", "Logistic regression test PR-AUC within high-income countries", "PR-AUC", "{:.2f}", "w3", SG, "lr_pr_auc | grouping=income_group & group=High income", "", S3 + "8.7")
AB = "results/test_ablation.csv"
for k in ("A", "B", "C"):
    c(f"abl_{k}", f"Test PR-AUC of the logistic regression with feature set {k}", "PR-AUC", "{:.3f}", "w3", AB, f"pr_auc | model=lr & feature_set={k}", "", S3 + "8.8")
RB = "results/test_robustness.csv"
c("rob_excl17_lr", "Test PR-AUC of the logistic regression without start year 2017", "PR-AUC", "{:.3f}", "w3", RB, "pr_auc | variant=exclude t = 2017 (window ends 2020) & model=lr", "", S3 + "8.8")
c("rob_excl17_persist", "Test PR-AUC of persistence without start year 2017", "PR-AUC", "{:.3f}", "w3", RB, "pr_auc | variant=exclude t = 2017 (window ends 2020) & model=persistence", "", S3 + "8.8")
c("rob_small_lr", "Test PR-AUC of the logistic regression without countries under one million people", "PR-AUC", "{:.3f}", "w3", RB, "pr_auc | variant=exclude population < 1 million & model=lr", "", S3 + "8.8")
c("rob_small_persist", "Test PR-AUC of persistence without countries under one million people", "PR-AUC", "{:.3f}", "w3", RB, "pr_auc | variant=exclude population < 1 million & model=persistence", "", S3 + "8.8")
PI = "results/test_permutation_importance.csv"
c("imp_gdp", "Drop in test PR-AUC when income per person is shuffled", "PR-AUC", "{:.3f}", "w3", PI, "importance_mean | feature=ln_gdp_pc", "", S3 + "8.6", "pre-specified")
c("imp_oil", "Drop in test PR-AUC when the oil share of CO2 is shuffled", "PR-AUC", "{:.3f}", "w3", PI, "importance_mean | feature=oil_share", "", S3 + "8.6", "pre-specified")
c("w3_pytest", "Pytest checks passing in the Week 3 repository", "checks", "{:.0f}", "new", "results/reference_pytest.csv", "passed | week=week3", "", "Week 4 (executed here)", "process")

# =============================================================================================== Week 4 (this repository)
N = "Week 4, results/"
c("dec_all_share", "Share of all countries that decoupled between 1990 and 2022", "%", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", "share_decoupled | income_group=All countries", "x100", N + "decoupling_by_income_1990_2022.csv", "descriptive")
c("dec_all_k", "Countries that decoupled between 1990 and 2022", "countries", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", "n_decoupled | income_group=All countries", "", N + "decoupling_by_income_1990_2022.csv", "descriptive")
c("dec_all_n", "Countries compared between 1990 and 2022", "countries", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", "n_countries | income_group=All countries", "", N + "decoupling_by_income_1990_2022.csv", "descriptive")
c("dec_lo_high", "Lower end of the 95% (Wilson) interval for the high-income decoupled share", "%", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", "wilson_lo | income_group=High income", "x100", N + "decoupling_by_income_1990_2022.csv", "descriptive")
c("dec_hi_high", "Upper end of the 95% (Wilson) interval for the high-income decoupled share", "%", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", "wilson_hi | income_group=High income", "x100", N + "decoupling_by_income_1990_2022.csv", "descriptive")
DT = "results/decoupling_over_time.csv"
for key, grp in [("high", "High income"), ("um", "Upper middle income"), ("lm", "Lower middle income"), ("low", "Low income"), ("all", "All countries")]:
    for yr in (1993, 2019):
        c(f"dot_{key}_{yr}", f"Share of {grp} countries decoupling over the 3-year window starting {yr}", "%", "{:.0f}", "new", DT, f"share_decoupled | window_start_year={yr} & income_group={grp}", "x100", N + "decoupling_over_time.csv", "descriptive")
DS = "results/decoupling_over_time_summary.csv"
c("dot_high_mean", "Average share of high-income countries decoupling per three-year window", "%", "{:.0f}", "new", DS, "mean_share_all_windows | income_group=High income", "x100", N + "decoupling_over_time_summary.csv", "descriptive")
c("dot_high_recent", "Average share of high-income countries decoupling per window, windows starting 2010 or later", "%", "{:.0f}", "new", DS, "mean_share_from_2010 | income_group=High income", "x100", N + "decoupling_over_time_summary.csv", "descriptive")
c("dot_high_top", "Windows in which high income has the highest decoupling share of the four groups", "windows", "{:.0f}", "new", DS, "windows_with_highest_share | income_group=High income", "", N + "decoupling_over_time_summary.csv", "descriptive")
c("dot_all_mean", "Average share of all countries decoupling per three-year window", "%", "{:.0f}", "new", DS, "mean_share_all_windows | income_group=All countries", "x100", N + "decoupling_over_time_summary.csv", "descriptive")
c("dot_n_windows", "Window start years shown in the over-time picture", "years", "{:.0f}", "new", DT, "#rows | income_group=All countries", "", N + "decoupling_over_time.csv", "descriptive")
TK = "results/model_skill_top20.csv"
c("top_frac", "Share of windows treated as 'top-scored' in the plain-language metric", "%", "{:.0f}", "new", TK, "top_fraction | model=lr", "x100", N + "model_skill_top20.csv", "post hoc")
c("top_n", "Windows in the top-scored group", "windows", "{:.0f}", "new", TK, "n_top | model=lr", "", N + "model_skill_top20.csv", "post hoc")
c("top_base", "Share of all test windows that decoupled (base rate)", "%", "{:.1f}", "new", TK, "base_rate | model=lr", "x100", N + "model_skill_top20.csv", "post hoc")
for m, nm in [("lr", "logistic regression"), ("rf", "random forest"), ("hgb", "gradient boosting"), ("persistence", "persistence rule")]:
    c(f"top_prec_{m}", f"Precision among the top-scored windows, {nm} (post hoc)", "%", "{:.0f}", "new", TK, f"precision_top | model={m}", "x100", N + "model_skill_top20.csv", "post hoc")
    c(f"top_lo_{m}", f"Lower end of the 95% interval, {nm}", "%", "{:.0f}", "new", TK, f"precision_lo | model={m}", "x100", N + "model_skill_top20.csv", "post hoc")
    c(f"top_hi_{m}", f"Upper end of the 95% interval, {nm}", "%", "{:.0f}", "new", TK, f"precision_hi | model={m}", "x100", N + "model_skill_top20.csv", "post hoc")
    c(f"top_lift_{m}", f"Lift over the base rate, {nm}", "times", "{:.1f}", "new", TK, f"lift_over_base_rate | model={m}", "", N + "model_skill_top20.csv", "post hoc")
VF = "results/verification.csv"
c("ver_n", "Independent recomputation checks run", "checks", "{:.0f}", "new", VF, "#rows |", "", N + "verification.csv", "process")
c("ver_pass", "Recomputation checks that passed", "checks", "{:.0f}", "new", VF, "#rows | result=pass", "", N + "verification.csv", "process")
c("ver_fail", "Recomputation checks that failed", "checks", "{:.0f}", "new", VF, "#rows | result=FAIL", "", N + "verification.csv", "process")
c("ver_rho_diff", "Difference between the original and recomputed rank correlation", "correlation", "{:.1e}", "new", VF, "abs_diff | id=W2-H1-rho", "", N + "verification.csv", "process")
c("ver_rho_new", "Recomputed rank correlation", "correlation", "{:.3f}", "new", VF, "recomputed | id=W2-H1-rho", "", N + "verification.csv", "process")
c("ver_ratio_new", "Recomputed high to lower-income ratio", "times", "{:.1f}", "new", VF, "recomputed | id=W2-H3-ratio", "", N + "verification.csv", "process")
c("ver_prauc_new", "Recomputed logistic regression test PR-AUC", "PR-AUC", "{:.3f}", "new", VF, "recomputed | id=W3-lr-prauc", "", N + "verification.csv", "process")
c("ver_labels_wrong", "Test windows whose saved label differs from the label rebuilt from the panel", "windows", "{:.0f}", "new", VF, "recomputed | id=W3-label-test-mismatches", "", N + "verification.csv", "process")
VT = "results/data_vintage_check.csv"
c("vint_owid_same", "Is the OWID file byte-identical in Weeks 2 and 3 (same sha256)?", "yes/no", "{}", "new", VT, "hash_identical | file=owid-co2-data.csv", "", N + "data_vintage_check.csv", "process")
c("vint_meta_same", "Is the World Bank country-metadata file identical in Weeks 2 and 3 (same sha256)?", "yes/no", "{}", "new", VT, "hash_identical | file=wb_country_metadata.csv", "", N + "data_vintage_check.csv", "process")
c("vint_overlap_rows", "Overlapping 1990-2022 World Bank rows compared between Weeks 2 and 3 (per indicator file)", "rows", "{:,.0f}", "new", VT, "overlap_rows_compared | file=wb_NY.GDP.PCAP.KD.csv", "", N + "data_vintage_check.csv", "process")
c("vint_overlap_diff", "Overlapping World Bank values that differ between Weeks 2 and 3", "values", "{:.0f}", "new", VT, "overlap_values_different | file=wb_NY.GDP.PCAP.KD.csv", "", N + "data_vintage_check.csv", "process")
c("commit_w1", "Week 1 commit used (first 10 characters)", "hash", "{}", "new", "results/lineage.csv", "commit | row_type=repo & week=week1", "first10", N + "lineage.csv", "process")
c("commit_w2", "Week 2 commit used (first 10 characters)", "hash", "{}", "new", "results/lineage.csv", "commit | row_type=repo & week=week2", "first10", N + "lineage.csv", "process")
c("commit_w3", "Week 3 commit used (first 10 characters)", "hash", "{}", "new", "results/lineage.csv", "commit | row_type=repo & week=week3", "first10", N + "lineage.csv", "process")
CR = "results/confidence_ratings.csv"
c("h4_rob_n", "Robustness variants run for H4", "variants", "{:.0f}", "new", CR, "robustness_variants | finding_id=H4", "", N + "confidence_ratings.csv", "process")
c("h4_rob_fail", "H4 robustness variants that did not reach raw p < 0.05", "variants", "{:.0f}", "new", CR, "robustness_failed | finding_id=H4", "", N + "confidence_ratings.csv", "process")
c("h1_rob_n", "Robustness variants run for H1", "variants", "{:.0f}", "new", CR, "robustness_variants | finding_id=H1", "", N + "confidence_ratings.csv", "process")
c("n_rating_high", "Hypotheses H1-H7 rated High", "findings", "{:.0f}", "new", CR, "#rows | kind=hypothesis test & rating=High", "", N + "confidence_ratings.csv", "process")
c("n_rating_moderate", "Hypotheses H1-H7 rated Moderate", "findings", "{:.0f}", "new", CR, "#rows | kind=hypothesis test & rating=Moderate", "", N + "confidence_ratings.csv", "process")
c("n_rating_low", "Hypotheses H1-H7 rated Low", "findings", "{:.0f}", "new", CR, "#rows | kind=hypothesis test & rating=Low", "", N + "confidence_ratings.csv", "process")

# ---- additional claims used by tables and prose
c("w1_consumption_countries", "Countries with consumption-based CO2 in the OWID file", "countries", "{:.0f}", "w1", PROF, "json: owid.coverage_countries_only.consumption_co2.n_countries", "", w1 + "3 and 11", "descriptive")
c("w1_inc_high", "High-income countries in Week 1's joined set", "countries", "{:.0f}", "w1", "report/report_content.md", r"regex: (\d+) high-, \d+ upper-middle", "", w1 + "5", "descriptive")
c("w1_inc_um", "Upper-middle-income countries in Week 1's joined set", "countries", "{:.0f}", "w1", "report/report_content.md", r"regex: \d+ high-, (\d+) upper-middle", "", w1 + "5", "descriptive")
c("w1_inc_lm", "Lower-middle-income countries in Week 1's joined set", "countries", "{:.0f}", "w1", "report/report_content.md", r"regex: upper-middle-, (\d+) lower-middle", "", w1 + "5", "descriptive")
c("w1_inc_low", "Low-income countries in Week 1's joined set", "countries", "{:.0f}", "w1", "report/report_content.md", r"regex: lower-middle- and (\d+) low-income", "", w1 + "5", "descriptive")
c("n_recommendations", "Recommendations in this report", "recommendations", "{:.0f}", "new", "report/_build/tables/recommendations.csv", "#rows |", "", "Week 4, report section 8", "process")
c("cfg_h", "Prediction horizon in years", "years", "{:.0f}", "w3", "results/frozen_config.json", "json: h", "", S3 + "2.3")
c("cfg_pool_start", "First window start year of the training pool", "year", "{:.0f}", "w3", "docs/ml_plan.md", r"regex: \| Pool \(train \+ selection\) \| (\d{4})-", "", S3 + "6.1")
c("w1_skew_log", "Skewness of CO2 per person in 2022 after taking logs", "skewness", "{:.2f}", "w1", "report/report_content.md", r"regex: Skew falls from [\d.]+ to (-?[\d.]+)", "", w1 + "5", "descriptive")
c("cfg_pool_end", "Last window start year in the training pool", "year", "{:.0f}", "w3", "results/frozen_config.json", "json: pool_end", "", S3 + "6.1")
c("cfg_test_first", "First window start year of the test set", "year", "{:.0f}", "w3", "results/frozen_config.json", "json: test_years.0", "", S3 + "6.1")
c("cfg_test_last", "Last window start year of the test set", "year", "{:.0f}", "w3", "results/frozen_config.json", "json: test_years.2", "", S3 + "6.1")
c("abl_nfeat", "Features in the full feature set", "features", "{:.0f}", "w3", AB, "n_features | model=lr & feature_set=C", "", S3 + "8.8")
c("abl_nfeat_A", "Features in the momentum-only set", "features", "{:.0f}", "w3", AB, "n_features | model=lr & feature_set=A", "", S3 + "8.8")
c("sg_n_high", "Test windows from high-income countries", "windows", "{:.0f}", "w3", SG, "n | grouping=income_group & group=High income", "", S3 + "8.7")
c("sg_ctry_high", "High-income countries in the test set", "countries", "{:.0f}", "w3", SG, "n_countries | grouping=income_group & group=High income", "", S3 + "8.7")
for key, grp in [("low", "Low income"), ("lm", "Lower middle income"), ("um", "Upper middle income"), ("high", "High income")]:
    c(f"dec_n_{key}", f"Countries compared for decoupling, {grp}", "countries", "{:.0f}", "new", "results/decoupling_by_income_1990_2022.csv", f"n_countries | income_group={grp}", "", "Week 4 (rebuilt from Week 2's paired table; equals Week 2 Section 6.6)", "descriptive")
c("lr_coef_gdp", "Standardised coefficient of income per person in the logistic regression", "coefficient", "{:.2f}", "w3", "results/lr_standardised_coefficients.csv", "standardised_coefficient | feature=ln_gdp_pc", "", S3 + "8.6")
c("lr_coef_co2", "Standardised coefficient of CO2 per person in the logistic regression", "coefficient", "{:.2f}", "w3", "results/lr_standardised_coefficients.csv", "standardised_coefficient | feature=ln_co2_pc", "", S3 + "8.6")
c("lr_coef_industry", "Standardised coefficient of industry share in the logistic regression", "coefficient", "{:.2f}", "w3", "results/lr_standardised_coefficients.csv", "standardised_coefficient | feature=industry_pct", "", S3 + "8.6")
c("lr_coef_urban", "Standardised coefficient of urbanisation in the logistic regression", "coefficient", "{:.2f}", "w3", "results/lr_standardised_coefficients.csv", "standardised_coefficient | feature=urban_pct", "", S3 + "8.6")
c("imp_urban", "Drop in test PR-AUC when urbanisation is shuffled", "PR-AUC", "{:.3f}", "w3", PI, "importance_mean | feature=urban_pct", "", S3 + "8.6")
c("imp_industry", "Drop in test PR-AUC when industry share is shuffled", "PR-AUC", "{:.3f}", "w3", PI, "importance_mean | feature=industry_pct", "", S3 + "8.6")


def main() -> int:
    seen = set()
    rows = []
    for cl in CLAIMS:
        if cl is None:
            continue
        if cl["claim_id"] in seen:
            raise SystemExit(f"duplicate claim id {cl['claim_id']}")
        seen.add(cl["claim_id"])
        val = resolve(cl["input_copy"], cl["locator"], cl["derivation"])
        disp = cl["fmt"].format(val)
        row = dict(cl)
        row["value"] = repr(float(val)) if not isinstance(val, str) else val
        row["display"] = disp
        rows.append(row)
    cols = ["claim_id", "text", "value", "display", "unit", "fmt", "source_repo", "source_commit", "source_file",
            "input_copy", "locator", "derivation", "originally_reported", "evidence_status"]
    with open(RESULTS / "claims_ledger.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} claims written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
