# Notes for the author (NOT for submission)

## 1. Items needing your attention first

1. **Week 1 never ran its planned exploratory analysis.** It is a plan with real profiling and a preliminary rank correlation. The report says so (Sections 4.2, 5.1, 9) and draws the three most important planned pictures from Week 2 and Week 3 data. The "exploration" lens in the triangulation is therefore thin. If a marker expects a full EDA, this is the gap to point at.
2. **Week 2's own checksum test fails on a fresh clone (1 of 25 checks).** The cause is line endings: the manifest hashes were taken from Windows (CRLF) files, but Git stored the World Bank CSVs with LF. Restoring CRLF reproduces every recorded hash (`results/data_vintage_check.csv`). No data values are affected. The report states this plainly (Section 3.4, R6). A one-line fix for the Week 2 repository would be a `.gitattributes` entry that marks `data/raw/**` as binary; I did not touch the earlier repositories.
3. **All three earlier repositories carry commit dates on the same calendar day** (see `results/lineage.csv`). The report therefore speaks of four *steps* or *weeks* as the task structure and gives no dates and no hours. The brief says the task takes roughly 30 to 35 hours; I did not write any hours or effort table because you have not logged hours. Expect a marker who reads `git log` to notice the dates.
4. **Body prose is 6,979 words** (limit 6,000 to 7,500, excluding the executive summary, tables, code, figure lines, captions, references and appendices). The executive summary is 587 words (limit 450 to 600). The whole file is about 17,044 words including tables and appendices. The "In short" callouts are one-column tables and are excluded from the body count; if your college counts them, the body is roughly 650 words higher and over the limit. Trim Section 6 or Section 8.2 first.
5. **One recommended figure is missing.** Week 2's effect-size forest plot is taller than wide (ratio above 1), which breaks the "height at most 0.8 x width" rule, so it is not reused. The eight reused figures are listed in Appendix D. The reused figures keep their original look (fonts and palettes differ slightly from the new ones).
6. **References.** Of 26 candidate references, 25 were verified through the Crossref API (title, journal, year, volume, pages, DOI; see `results/reference_check.csv`) and 19 of them are cited. Holm (1979) was dropped: Crossref returns no record for the original paper, so the Holm correction is explained without a citation. Four of the verified papers are cited for what their titles and (where Crossref supplies one) abstracts say, not for details I read in the full text: Le Quéré et al. (2019) and Hubacek et al. (2021) by title only, Haberl et al. (2020) by the opening of its abstract, Peters et al. (2011) by its abstract. Check the wording in Section 7.2 if a marker is strict. OWID and the World Bank are cited as web data sources, not as Crossref items. Earlier work is cited by repository and commit.
7. **Colour-blind check.** The categorical colours used (blue, vermilion, orange) pass the palette validator. The four-step blue ramp for income groups does *not* pass the validator's strict test for telling categories apart (adjacent steps too close), so those figures also use marker shapes and direct labels. Light-blue and orange marks are below 3:1 contrast against white; labels and a table view carry the same information.
8. **Nothing was pushed.** Commands are at the end of this file.
9. **Not done, by design:** no model was re-fitted, the Week 3 test run was not repeated, and no new hypothesis tests were run. The only new numbers are descriptive: decoupling by group and over time, and the post hoc "top-scored fifth" precision.

## 2. Figure-to-section map

| Figure | File | Section |
| --- | --- | --- |
| 1.1 Key findings at a glance | `figures/fig_findings_glance.png` | 1.3 |
| 2.1 Project journey | `figures/fig_journey.png` | 2.4 |
| 3.1 Missing data heat map (Week 1) | `figures/reused/week1_fig_profile_missing_heatmap.png` | 3.2 |
| 4.1 Distributions (Week 1) | `figures/reused/week1_fig_profile_distributions.png` | 4.2 |
| 4.2 Label and split timeline (Week 3) | `figures/reused/week3_fig_label_split_timeline.png` | 4.4 |
| 5.1 Income vs CO2 per person | `figures/fig_income_vs_co2.png` | 5.1 |
| 5.2 Decoupling by income group | `figures/fig_decoupling_by_group.png` | 5.1 |
| 5.3 Decoupling over time | `figures/fig_decoupling_over_time.png` | 5.1 |
| 5.4 CO2 per person by group (Week 2) | `figures/reused/week2_fig_h2_boxplot_by_income.png` | 5.2 |
| 5.5 Decoupling counts (Week 2) | `figures/reused/week2_fig_h6_decoupling_heatmap.png` | 5.2 |
| 5.6 Slopes by group (Week 2) | `figures/reused/week2_fig_h4_slopes_by_income.png` | 5.2 |
| 5.7 Model skill | `figures/fig_model_skill.png` | 5.3 |
| 5.8 Precision-recall curves (Week 3) | `figures/reused/week3_fig_test_precision_recall.png` | 5.3 |
| 5.9 Importance and coefficients (Week 3) | `figures/reused/week3_fig_importance_coefficients.png` | 5.3 |
| 5.10 Evidence matrix | `figures/fig_evidence_matrix.png` | 5.4 |
| 8.1 Recommendations roadmap | `figures/fig_roadmap.png` | 8.1 |

Paste the images by hand where the report has `![Figure ...](../figures/...)`. The Markdown also carries table captions as bold lines directly above each table.

## 3. Statements in the report that do NOT come from a ledger row

Every number comes from the ledger. These statements are *words*, not numbers, and rest on something else:

- **Descriptions of the methods of Weeks 1 to 3** (Section 4) are summarised from those repositories' plans and reports (`docs/analysis_plan.md`, `docs/ml_plan.md`, report text), not from a results file. Examples: which test was used for which hypothesis; the list of model features; the rolling-origin validation and the one-standard-error rule.
- **"Every pair of groups differs after correction"** and **"the effect is no smaller with PPP income, without small countries or oil exporters" (H6)** are read from `results/hypothesis_results.csv` and Week 2's post hoc table, but are not separate ledger rows.
- **Qualitative size words** such as "about a third", "nearly two in three" and "more than a third" are rounded readings of ledger values (32%, 64%, 36%).
- **The literature statements** in Sections 2.1 and 7.2 (environmental Kuznets curve; trade-embodied emissions; the decoupling review; the ecological fallacy; prediction versus explanation) paraphrase the verified papers as described in item 6 above.
- **"Imported emissions may explain part of the decoupling"** is background knowledge, not a result of this project. The report says that this project did not test it.
- **The roadmap phases (Do now, Do next, Explore later)** and the "next step" and "success measure" columns are my judgements, not results.
- **The statement that the Week 2 checksum failure is a line-ending effect** was verified here: `results/data_vintage_check.csv` shows each committed file matches its manifest hash only after LF is converted to CRLF.

## 4. Verification and lineage outcome

- **Lineage.** OWID file: same sha256 in Weeks 2 and 3 (True). World Bank country metadata: same sha256 (True). The four shared World Bank indicator files differ in hash only because the year range requested differs, and all 8,778 overlapping rows per file have identical values (0 differences). Week 1 stored no manifest; its reported file size, shape and missing-data rates agree with Weeks 2 and 3.
- **Pytest in the earlier repositories** (run on fresh clones at the recorded commits): Week 2, 24 passed and 1 failed (line endings); Week 3, 31 passed on a clone made with `core.autocrlf=false`. On a default Windows clone Week 3 shows two failures that are also line-ending effects (raw-file hash and an LF-endings check).
- **Independent recomputation.** 99 checks, 99 pass, 0 fail. The largest differences are bootstrap interval ends (different random seed, tolerance 0.02) and two quantities that the earlier repositories printed to one or two decimals. The Week 3 label rebuilt from the panel matches all 594 saved test labels and every year's counts.
- **Conflicts between weeks.** None in the numbers. The apparent conflicts are definitions (Section 3.5): two-end-year decoupling against three-year windows; countries against windows; different samples per test; Week 1's preliminary correlation (0.857 on 197 countries) against Week 2's (0.855 on 198).

## 5. Decisions I made (log)

- **Confidence rule applied mechanically** (`src/synthesis_tables.py`). H4 comes out Low because 2 of 6 of its robustness variants do not reach raw p below 0.05 (the rule says two or more failures means Low). H5 comes out Moderate because Week 2 flags it as under-powered. H1, H2, H3 and H6 come out High. The model-comparison findings were rated by the same conditions with the reasons written beside them (`results/confidence_ratings.csv`).
- **Two process findings (P1, P2) are rated High** because they were observed directly and verified by scripts in this repository. Recommendations R6 and R7 rest on them.
- **A recommendation's confidence is the weakest rating among the findings it rests on** (`src/render_tables.py`). A Low rating on R4, R5 or R8 is intended: it says the action is a test or a caution, not a conclusion.
- **Executive summary lists five of the 8 recommendations** (R1, R2, R3, R5, R6).
- **Week 3's "post hoc" label** is kept for anything computed after the test set was opened, including the new top-scored-fifth metric. The 20% cut was fixed in the plan before it was computed.
- **Data sources are cited as web resources**; only publications went through Crossref.

## 6. Twelve likely viva questions

1. **Why did you not rerun the earlier analyses?** The task is a synthesis. Re-running the Week 3 test would break its one-run rule. Instead I recomputed the headline numbers from saved data with different code and checked that they agree.
2. **How do you know the three weeks used the same data?** The OWID file has the same fingerprint in Weeks 2 and 3, and all overlapping World Bank values are identical. Week 1 saved no fingerprint, but its counts and missing-data rates match.
3. **Why are there two different "decoupling" percentages?** One compares each country's 1990 and 2022 values (64% of high-income countries); the other counts three-year windows (an average of 37% of high-income countries per window). They answer different questions.
4. **How was confidence rated, and could you have rated it differently?** By a rule fixed in advance: pre-specification, robustness checks, adjusted p-value, power warning and support from another week. The H-ratings are mechanical from Week 2's results file.
5. **Why is the slope finding rated Low when it was significant?** Because 2 of 6 robustness checks did not reach the usual significance level and the extra variance explained is only 0.010.
6. **Why not switch to the random forest?** It scored higher only after the test set was opened. Choosing a model by the test result makes the test part of the selection.
7. **Is the model useful?** As a ranking aid, modestly (0.390 against 0.284 for persistence). As a yes/no tool, no: it flags nearly everything at its frozen threshold, and an income-group rule scores 0.379.
8. **What is PR-AUC and why use it?** The area under the precision-recall curve. It suits a task where the true cases are the minority, and it has a clear no-skill line (the base rate).
9. **What does production-based mean and why does it matter?** CO2 is counted where it is emitted. A country can look cleaner by importing goods made elsewhere. This project did not test how much of the decoupling is of that kind.
10. **What is the ecological fallacy?** Treating a pattern across countries as if it held for the people in them. Everything here is country-level.
11. **Why are the income groups a problem?** They are defined from income, so group comparisons partly restate the income result, and the current classification is applied to all years.
12. **What would you do next?** Add consumption-based emissions (R2), replicate the slope result (R5), score the forest and boosting models once on later data (R4), and fix the checksum handling (R6).

## 7. Push commands (nothing has been pushed)

Create an empty repository named `co2-decoupling-final-report` on GitHub first (no README, no licence), then from the project folder:

```
git remote add origin https://github.com/KanishkVerma-046/co2-decoupling-final-report.git
git branch -M main
git push -u origin main
```
