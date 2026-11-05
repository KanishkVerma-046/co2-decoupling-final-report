# Synthesis plan (Week 4): written and committed before any analysis code

**Status.** This plan was written after cloning Weeks 1-3 read-only and reading their reports, notes, plans and result files, and before writing any new analysis code. Nothing new had been computed at this point. Everything below is fixed now; changes go only in the dated "Deviations" section at the end, never above it.

**Project.** "Does Wealth Burn Carbon?" Final report that synthesises Weeks 1-3 for a non-technical audience (managers) and a technical audience (reviewers).

## 1. What this repository does and does not do

It does: (a) prove where every number comes from (lineage and a claims ledger), (b) independently recompute the headline numbers, (c) put the three weeks side by side (triangulation), (d) add two small, clearly labelled descriptive analyses, (e) draw new figures for a general audience, (f) write the report.

It does not: fit or tune any model, re-run the Week 3 test evaluation, download new data, run new hypothesis tests, or make causal claims. Only saved result files and saved predictions are used.

## 2. Inputs

Copied by `src/collect_inputs.py` from the three clones into `data/inputs/week1|week2|week3/` together with `data/inputs/manifest.csv` (source repo, commit hash, source path, sha256 of the copy). The clones are read at the commit hash recorded in `results/lineage.csv`.

## 3. Lineage and consistency (`results/lineage.csv`, `results/data_vintage_check.csv`)

- One row per earlier repo: URL, commit hash, commit date, contribution, number of pytest checks (counted from the test files, and executed where the suite installs quickly), and for every raw data file the sha256 recorded in that repo's manifest.
- Vintage check: compare the sha256 of the OWID file and of each World Bank file across Weeks 1-3. Equal hash = same file. Different hash = report plainly. Because the World Bank files in Week 2 and Week 3 were requested for different year ranges (1990-2022 versus 1988-2022), a different hash alone does not prove different values; where both raw files are committed, compare the overlapping rows value by value and report the number of differing values. Week 1 stores no manifest or raw files, so its vintage is checked only through the counts it reported (rows, columns, file size, snapshot date).
- If any mismatch exists, explain how it could affect comparisons across weeks.

## 4. Independent verification (`src/verify_headlines.py` -> `results/verification.csv`)

Recompute with code that is different from the original, from saved processed data or saved predictions only. Columns: quantity, original value, recomputed value, absolute difference, tolerance, pass or fail.

| Quantity | Source file | Method used here | Tolerance |
|---|---|---|---|
| Spearman rho, GDP per person vs CO2 per person, 2022 (n) | Week 2 `cross_section_2022.csv` | ranks with `scipy.stats.rankdata`, then Pearson on ranks (not `spearmanr`) | 1e-9 |
| Bootstrap 95% interval of rho | same | own bootstrap, 10,000 resamples, a different seed | 0.02 on each end (resampling noise) |
| Ratio of high-income to lower-middle plus low-income CO2 per person (geometric means) | same | `groupby` on log10 values, pooled group mean | 1e-6 |
| Group medians of CO2 per person | same | `groupby().median()` | 1e-9 |
| Decoupled share by income group, and counts | Week 2 `paired_1990_2022.csv` | recompute decoupling from the 1990 and 2022 values themselves, not from the saved flag | 1e-9 |
| High-income median change 1990-2022 and number that fell | same | direct from values | 1e-6 |
| High-income log-log slope | same | `numpy.polyfit` on log10 values | 1e-6 |
| Week 3 labels, base rates (overall, pool, test, by year) | Week 3 `panel.csv` | rebuild the label from CO2 and GDP at t and t+3 with the stated eligibility rule; compare with the saved labels in the saved predictions | exact |
| Test PR-AUC, ROC-AUC, F1, MCC, precision, recall, confusion matrix per model | Week 3 `test_predictions.csv` + `frozen_config.json` thresholds | own step-wise average precision, rank-based ROC-AUC, confusion counts with numpy (not scikit-learn) | 1e-9 |

Any mismatch is reported in the final message and in the report's limitations section.

## 5. Reconciliation of definitions (`results/reconciliation.csv`)

A table of definitional differences across weeks, filled from the reports and result files: unit of analysis, "decoupling" definition (Week 2 compares 1990 and 2022 levels; Week 3 uses rolling 3-year windows), sample sizes and exclusions, income-group vintage, GDP series, CO2 series, year ranges. The report explains in plain words why two different "decoupling" percentages are not in conflict.

## 6. Triangulation and the confidence rule (`results/triangulation.csv`, `results/confidence_ratings.csv`)

Questions: (Q-A) does income relate to emissions per person; (Q-B) do income groups differ; (Q-C) have rich countries decoupled; (Q-D) what predicts decoupling; (Q-E) do structural drivers matter. For each: what Week 1 (exploration and planning), Week 2 (tests) and Week 3 (model) said, whether they agree, and a confidence rating.

**Rule, fixed now.** Ratings come from evidence in the repositories, not from how interesting a finding is.

- **High:** (1) pre-specified in a plan committed before the analysis; (2) every pre-specified robustness variant agrees in direction and has raw p < 0.05; (3) Holm-adjusted p < 0.01 for confirmatory tests, or a pre-specified paired interval that excludes zero for model comparisons; (4) not flagged by its own repository as under-powered; (5) supported by at least one other week's evidence or an independent period.
- **Moderate:** pre-specified and supported, but at least one of the High conditions is not met while at most one robustness variant fails (for example a modest effect, a flagged power limit, a single hold-out period, or a dependence on a documented choice).
- **Low:** exploratory or post hoc; or two or more robustness variants fail; or the evidence is only a planning-stage smoke test.

The counts of robustness variants run and passed are computed from Week 2's `hypothesis_results.csv` by `src/synthesis_tables.py`, so the High/Moderate/Low label for H1-H6 is mechanical. Model-based and exploratory claims are rated by the same rule, with the reasons written next to them.

## 7. New descriptive analyses (clearly labelled as new, descriptive, not tests)

1. **Decoupling share over time by income group.** From Week 3's panel: for each window start year t = 1993-2019 and each income group, the share of eligible countries whose CO2 per person fell and GDP per person rose over the next three years. Test years (2017-2019) are marked; the purge-gap years 2014-2016 are drawn but marked as not used by the model. Caveat drawn on the figure and in the text: income groups are the current World Bank classification.
2. **Plain-language model-skill metric (post hoc, exploratory, not pre-specified).** From Week 3's saved test predictions only: precision among the top 20% highest-scored test windows (ties broken by a fixed rule written in the code), compared with the 24.9% base rate, for the logistic regression, random forest, gradient boosting and the persistence rule. Country-clustered bootstrap intervals (resampling whole countries). No refitting, no change to any frozen choice. The 20% cut is a presentation choice fixed here, not tuned.

## 8. Figures (PNG, 200 dpi, colour-blind-safe, one style, height at most 0.8 x width, readable at 16 cm wide)

New: (1) project journey Weeks 1-4; (2) key findings at a glance with confidence badges; (3) income versus CO2 per person for a general audience (from Week 2's cross-section); (4) decoupling share by income group; (5) decoupling over time by income group; (6) model skill in plain language (PR-AUC with intervals against the no-skill line, plus top-20% precision, marked post hoc); (7) evidence-strength matrix; (8) recommendations roadmap.
Reused (copied with credit to source week and file): 6-8 of the strongest from Weeks 1-3.
Every figure gets a caption that says what to look at and what it means. No placeholder text.

## 9. Recommendation framework

Every recommendation carries: ID, recommendation, evidence (claim ids), confidence (same rule; a recommendation cannot be rated higher than the weakest evidence it rests on), audience, concrete next step, success measure, caveat. Recommendations are evidence-informed analytical advice. Policy decisions would need causal evidence this project does not provide, and the report says so. A recommendation about how to use the ML model cannot rest on a post hoc result alone for a High rating.

## 10. Report constraints

Body prose 6,000-7,500 words; executive summary about 450-600 words; plain English; "decoupling" always means absolute decoupling. Every number comes from `results/claims_ledger.csv` through `report/_build/build_report.py`. References are verified through Crossref or dropped. No hours tables.

## 11. Quality gates (pytest, at least 12 checks)

Ledger ids unique and all template placeholders resolve; every ledger value matches its source cell; verification tolerances met; no placeholder text; table rows have consistent cell counts; LF endings; figures exist and are not tall; every recommendation has an evidence link and a confidence rating; no High claim rests only on a post hoc or exploratory result; bare numbers in the template are limited to an allow-list.

## Deviations

(none yet)
