## Appendix A. Repository map and how to reproduce

The four repositories and the exact commits read for this report:

- Week 1: https://github.com/KanishkVerma-046/co2-economy-eda-proposal, commit {commit_w1}.
- Week 2: https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing, commit {commit_w2}.
- Week 3: https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline, commit {commit_w3}.
- Week 4: https://github.com/KanishkVerma-046/co2-decoupling-final-report (this report; its commit is shown in its own history).

**Table A.1: Layout of the Week 4 repository.**

| Path | What it holds |
| --- | --- |
| `docs/synthesis_plan.md` | The plan, committed before any analysis code: what is verified, the confidence rule, the figures, the recommendation framework. |
| `data/inputs/` | Byte-exact copies of the files used from Weeks 1 to 3, with `manifest.csv` (source repository, commit, path, sha256). |
| `src/` | `collect_inputs.py`, `lineage.py`, `verify_headlines.py`, `synthesis_tables.py`, `build_ledger.py`, `render_tables.py`, `check_references.py`, `make_figures.py`. |
| `results/` | Every output table: lineage, vintage check, verification, confidence ratings, triangulation, reconciliation, ledger, decoupling tables, model-skill table. |
| `figures/` and `figures/reused/` | Eight new figures and eight copied from Weeks 1 to 3. |
| `report/_build/` | The section templates with claim-id placeholders and `build_report.py`. |
| `report/report_content.md` | This report, generated. |
| `tests/` | Pytest checks on the ledger, the build, the figures and the report. |

**To reproduce this repository** (Windows or any system with Python 3.13):

```
git clone https://github.com/KanishkVerma-046/co2-decoupling-final-report
cd co2-decoupling-final-report
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
git clone https://github.com/KanishkVerma-046/co2-economy-eda-proposal reference/week1
git clone https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing reference/week2
git clone https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline reference/week3
git -C reference/week1 checkout <Week 1 commit above>
git -C reference/week2 checkout <Week 2 commit above>
git -C reference/week3 checkout <Week 3 commit above>
python src/collect_inputs.py
python src/lineage.py
python src/verify_headlines.py
python src/synthesis_tables.py
python src/build_ledger.py
python src/render_tables.py
python src/check_references.py
python src/make_figures.py
python report/_build/build_report.py
pytest
```

The inputs are already stored in `data/inputs/`, so the clones are needed only to refresh them. The reference check needs internet access. On Linux or macOS replace the activation line with `source .venv/bin/activate`.

**To reproduce the earlier weeks**, follow the commands in their READMEs. In outline: Week 2 runs `src/acquire.py`, `src/clean.py`, `src/tests.py`, `src/make_figures.py` and `pytest`. Week 3 runs `src/acquire.py`, `src/clean.py`, `src/features.py`, `src/evaluate_cv.py`, `src/evaluate_test.py` (once only; a lock file blocks repeats), `src/posthoc_test_analysis.py`, `src/make_figures.py` and `pytest`. This report did not re-run any of these; it reads their saved results and ran their pytest suites only.

## Appendix B. Claims ledger excerpt

Every number in this report is a row in `results/claims_ledger.csv`: a claim id, a plain-language statement, the value, its unit, the source repository and commit, the source file, the column or key, and where it was first reported. The report text holds placeholders (a claim id such as `h1_rho` in curly brackets) that the build script fills from the ledger and refuses to build if an id is missing. The table below shows the most important claims; the full ledger holds the rest.

**Table B.1: Selected claims from the ledger.**

[[table:ledger_excerpt]]

## Appendix C. Glossary

**Table C.1: Terms in plain English.**

| Term | Meaning |
| --- | --- |
| Absolute decoupling | CO2 per person falls while income per person rises. The only kind of decoupling this report uses. |
| Aggregate | A region or group such as "World" or "High income countries", not a country. Removed before analysis. |
| Base rate | The share of cases that are true to begin with. A model with no skill scores about this. |
| Bootstrap | Re-drawing the sample many times, with replacement, to see how much a result moves. |
| Calibration | Whether a predicted probability of, say, a third really means that a third of such cases happen. |
| Circular (income groups) | Groups are defined from income, so using them to explain income-related outcomes partly repeats the question. |
| Claims ledger | The table that ties every number in the report to a source file and column. |
| Confidence badge | A High, Moderate or Low label from the rule in Section 5.4. |
| Confidence interval | A range likely to contain the true value. Here, 95% unless stated. |
| Consumption-based emissions | Emissions counted where goods are used rather than where they are made. |
| Cross-validation | Scoring a model on parts of the data it was not trained on. Here the parts are in time order. |
| Decoupling window | A start year and the three years that follow it. |
| Ecological fallacy | Treating a pattern across groups as if it held for each member. |
| Effect size | How big a difference or relationship is, as opposed to whether it is detectable. |
| F1 | A score that combines precision and recall. |
| GDP per person | Economic output per person; here in constant 2015 US dollars. |
| Holm correction | A way to adjust p-values when several tests are run, keeping the overall false-alarm rate under control. |
| Leakage | Information from the future reaching a model during training, which flatters its score. |
| MCC | Matthews correlation coefficient: a fair score for yes/no predictions when one class is rarer. |
| Persistence rule | Predict that a country decouples if it decoupled over the previous three years. |
| Post hoc | Decided after the results were seen. Exploratory by definition. |
| PPP | Purchasing power parity: income adjusted for local prices. Used as a check. |
| PR-AUC | Area under the precision-recall curve: how well a model ranks true cases near the top. |
| Precision | Of the cases flagged, the share that were truly positive. |
| Production-based emissions | Emissions counted where the carbon is released. |
| Rank correlation | How well the order of countries on one measure matches their order on another. |
| Recall | Of the true cases, the share that were flagged. |
| ROC-AUC | The chance that a random true case is scored above a random false one. |
| Robustness check | Re-running an analysis under a different reasonable choice to see if the answer holds. |
| sha256 | A fingerprint of a file; any change to the file changes the fingerprint. |
| Test set | Data held back until the end and used once to judge the final model. |
| Vintage | The version of a dataset at the time it was downloaded. |

## Appendix D. List of figures

**Table D.1: Every figure, with its source.**

| Figure | What it shows | New or reused | Source file |
| --- | --- | --- | --- |
| 1.1 | Key findings at a glance | New | `figures/fig_findings_glance.png` |
| 2.1 | The four-step project journey | New | `figures/fig_journey.png` |
| 3.1 | Missing data by variable and decade | Reused, Week 1 | `figures/reused/week1_fig_profile_missing_heatmap.png` |
| 4.1 | Skewed and logarithmic distributions | Reused, Week 1 | `figures/reused/week1_fig_profile_distributions.png` |
| 4.2 | Label construction and data split | Reused, Week 3 | `figures/reused/week3_fig_label_split_timeline.png` |
| 5.1 | Income against CO2 per person, 2022 | New | `figures/fig_income_vs_co2.png` |
| 5.2 | Decoupling by income group, 1990-2022 | New | `figures/fig_decoupling_by_group.png` |
| 5.3 | Decoupling over time by income group | New | `figures/fig_decoupling_over_time.png` |
| 5.4 | CO2 per person by income group | Reused, Week 2 | `figures/reused/week2_fig_h2_boxplot_by_income.png` |
| 5.5 | Decoupling counts by income group | Reused, Week 2 | `figures/reused/week2_fig_h6_decoupling_heatmap.png` |
| 5.6 | Income-emissions slopes by group | Reused, Week 2 | `figures/reused/week2_fig_h4_slopes_by_income.png` |
| 5.7 | Model skill in plain language | New | `figures/fig_model_skill.png` |
| 5.8 | Precision-recall curves on the test years | Reused, Week 3 | `figures/reused/week3_fig_test_precision_recall.png` |
| 5.9 | Permutation importance and coefficients | Reused, Week 3 | `figures/reused/week3_fig_importance_coefficients.png` |
| 5.10 | Evidence-strength matrix | New | `figures/fig_evidence_matrix.png` |
| 8.1 | Recommendations roadmap | New | `figures/fig_roadmap.png` |

The Week 2 effect-size forest plot was considered for reuse but is taller than the page limit set for this report, so it is not included.

## Appendix E. Questions a manager might ask

**1. In one sentence, what did you find?** Richer countries emit far more CO2 per person, and most high-income countries have managed to cut emissions per person while growing, but the cut is partial, may partly reflect imported emissions and cannot be predicted well.

**2. How sure are you?** It depends on the finding, and the report says so for each one. The income-emissions link and the group gap are rated High; the size of the high-income fall and the model's ranking skill are rated Moderate; the slope difference and the structural-driver findings are rated Low (Section 5.4).

**3. Is {dec_pct_high}% of rich countries decoupling a good result?** It is a good sign, but it is a two-year comparison of production-based emissions. Over three-year windows the average share is {dot_high_mean}%, and {dec_notdec_pct_high}% of high-income countries did not decouple at all between 1990 and 2022.

**4. Why do you keep saying "production-based"?** Because the data count carbon where it is released. A country that imports goods made with fossil fuels abroad looks cleaner than its consumption deserves. This project cannot say how much of the decoupling is of this kind.

**5. Can we use the model to pick which countries to target?** Not as a yes/no tool. At its fixed cut-off it flagged almost every window. As a ranking aid it is modestly better than a simple rule, and an income-group rule does about as well. If you need a shortlist, take the top-scored windows and show how often they were right ({top_prec_lr}%, against a base rate of {top_base}%).

**6. Why not switch to the random forest, which scored higher?** Because it scored higher only after the test set had been opened. Choosing a model by looking at the test result turns the test into part of the training. We report the lead and recommend a fresh test (R4).

**7. What does "significant after correction" mean?** When you run several tests, some will look significant by luck. The Holm correction raises the bar to account for that. All {n_confirmatory} confirmatory tests cleared it, but the margins differ a lot; the effect sizes and ratings carry the real message.

**8. Why is the slope finding rated Low when it passed the test?** Because {h4_rob_fail} of {h4_rob_n} of its robustness checks did not reach the usual significance level, and the extra variance it explains is only {h4_dr2}. A result that depends on which countries are in the sample should be repeated before it is relied on.

**9. Are the numbers in this report reliable?** Every number is traced to a source file through a ledger, and {ver_pass} of {ver_n} headline numbers were recomputed independently and matched. That shows the arithmetic is right. It does not show the definitions are the best possible.

**10. Does this show that wealth causes emissions?** No. Everything here is an association between countries. Income, industry, fuel, climate, trade and policy are tangled together, and no design in this project separates them.

**11. What would you do first with this?** Start with R1, R6 and R7: they are ready now, need no new data and have High confidence. Then add consumption-based emissions (R2).

**12. Where is the biggest remaining risk?** The definition of decoupling. A different start year, a different window, or a consumption-based measure could move the headline numbers. That is why R2 asks for more than one measure.
