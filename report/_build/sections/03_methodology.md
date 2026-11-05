## 4. Methodology

### 4.1 Data cleaning and preparation

| In short |
| --- |
| The data were cleaned by written rules, each tied to a measured problem. Nothing that matters for the result was filled in, and every dropped or changed row was logged. |

Section 3.2 lists the rules. Three design choices deserve explanation, because they shape every later result.

*Why not fill in missing values?* CO2 and income are the two things the project studies. Guessing them would partly manufacture the relationship being tested. Where gaps were small and in secondary variables (industry share, for example), Week 3 compared four ways of filling them and found the choice made no real difference: all four scored within one standard error of each other for every model.

*Why logarithms?* Both CO2 per person and income per person are very uneven: a few countries are far above the rest. Plotted or averaged on their raw scale, those few dominate. On a logarithmic scale, each step up is a multiplication (ten times, for example) rather than an addition, which spreads countries out evenly and turns the income-emissions pattern into something close to a straight line. Week 1's profiling measured this: the skew of raw CO2 per person in 2022 was {w1_skew_raw}, against {w1_skew_log} after taking logs.

*Why ranks?* Rank-based statistics ask only whether the order of countries agrees, so one extreme value, such as Qatar's {w1_top_emitter_value} tonnes per person, cannot dominate.

### 4.2 Exploratory analysis and visualisation strategy (Week 1)

| In short |
| --- |
| Week 1 matched each question to a chart type and wrote down colour and accessibility rules before drawing anything. It also ran a first profile of both datasets. The planned exploratory analysis was not carried out in full; the pictures in Section 5.1 execute the parts that matter most. |

Week 1 defined {w1_n_questions} questions, from "how have emissions changed since 1990?" to "how sensitive are the main findings to data choices?". Each question was paired with a method and a chart, such as a log-log scatter for income against emissions and a quadrant plot for decoupling. Colour rules were fixed up front: one hue for magnitude, two hues with a neutral middle for change, never colour alone to carry meaning, no dual-axis charts, and axis labels that say when a scale is logarithmic.

Week 1's real contribution was measurement. The profiling quantified the missing data, found the country-name mismatches and showed why logarithms are needed (Figure 4.1).

![Figure 4.1: Distributions of CO2 per person in 2022 (left) and the joined 2022 preview on logarithmic axes (right). Look at how the raw distribution has a long right tail while the logarithmic one is far more balanced; this is why the report uses log scales. Source: Week 1, fig_profile_distributions.png, commit {commit_w1}.](../figures/reused/week1_fig_profile_distributions.png)

An honest note on scope: Week 1 was a plan, backed by profiling and a preliminary rank correlation. It did not produce the exploratory findings it planned. This report fills the gap in two ways: Weeks 2 and 3 supply the tests and the model, and Section 5.1 draws the three most important planned pictures (income against emissions, decoupling by group, decoupling over time) from the saved Week 2 and Week 3 data.

### 4.3 Statistical testing framework (Week 2)

| In short |
| --- |
| The claims were written down before the data were opened. Each was tested with a method suited to skewed data, corrected for running several tests at once, and reported with an effect size and an interval rather than a bare yes or no. |

**Pre-specification.** The analysis plan was committed to version control before any test was run. It fixed the hypotheses, the direction of each, the sample, the test and the decision rule. This guards against the quiet habit of trying many analyses and reporting the one that worked.

**The hypotheses.** Seven in all. H1 to H6 were confirmatory; H7 was exploratory and sits outside the correction.

- H1: richer countries emit more CO2 per person (rank correlation).
- H2 and H3: CO2 per person differs across the four income groups, and high-income countries emit more than lower-middle and low-income countries together.
- H4: the slope of the income-emissions line differs by income group.
- H5: CO2 per person fell in high-income countries between 1990 and 2022.
- H6: decoupling depends on income group.
- H7 (exploratory): industry share and urbanisation add explanatory power beyond income.

**Why these tests.** Because the data are skewed, the primary tests rely on ranks or on corrections for uneven spread: Spearman's rank correlation [@Spearman1904] for H1, the Kruskal-Wallis test for H2, Welch's t-test for H3, an interaction test with robust standard errors for H4, the Wilcoxon signed-rank test for the paired comparison in H5, and a chi-square test for H6. Each has a companion test run for comparison, so a result does not depend on one method's assumptions.

**Multiple testing.** Running six tests, each at the usual 5% error level, gives a much higher chance than 5% that at least one false alarm slips through. The Holm procedure adjusts the six p-values so that the chance of any false alarm across the whole set stays at 5%. It is never less powerful than the simpler Bonferroni method.

**Effect sizes and intervals.** A p-value says only that a pattern is unlikely to be chance. It does not say how big the pattern is. Every result is therefore reported with an effect size and a 95% interval from a bootstrap, which re-draws the sample many times to see how much the answer moves [@Efron1979].

**Power.** The plan computed the smallest effect each design could detect with 80% power. For H5 the observed effect was just below it ({h5_dz} against a minimum of {h5_mde}), which is why H5 is rated Moderate in Section 5.4.

**Robustness.** Each confirmatory test was re-run with PPP income, without countries under one million people, without oil and gas exporters, and with permutation tests. Only H4 changed meaningfully.

### 4.4 Machine learning (Week 3)

| In short |
| --- |
| The model answers one question: for a country in a given year, will CO2 per person fall while income per person rises over the next three years? It was built so that it never sees the future, compared with simple baselines, and evaluated once on years it had not touched. |

**The label.** For a country and a start year, the label says *decoupling* if CO2 per person is lower and income per person higher {cfg_h} years later, and *no decoupling* otherwise. This is the same absolute decoupling as in Week 2, applied to a rolling window. {w3_all_rows} windows were eligible across the training pool and test set, from {w3_pool_countries} countries.

**The features.** {abl_nfeat} measures known at the start of the window: income level and recent growth, population, urbanisation, industry share, CO2 per person and how it changed over the last one, three and five years, energy use, and the coal, oil and gas shares of CO2. Year, country identity and income group were left out on purpose: the first two let a model memorise, and the third is circular with income.

**The models.** Three were tried: an elastic-net logistic regression [@ZouHastie2005] (a simple, penalised formula), a random forest [@Breiman2001] and gradient boosting [@Friedman2001] (both ensembles of decision trees). Two baselines gave a yardstick: a *persistence rule* (predict decoupling if it happened over the previous three years) and a *base-rate rule* (always predict the average).

**Time-aware validation.** Random shuffling would let a model learn from the future. Instead, windows starting in {cfg_pool_start}-{cfg_pool_end} formed a pool for training and tuning, and the years {cfg_test_first}-{cfg_test_last} were held back for the final test. A gap of {cfg_h} years sat between them so that no training window overlapped the test period (Figure 4.2). Inside the pool, models were scored with rolling-origin validation: train on the past, validate on the next block, repeat.

![Figure 4.2: How the decoupling label and the data split were built. Read it from left to right: a window looks ahead three years, a gap separates training from testing, and the test years come last. Source: Week 3, fig_label_split_timeline.png, commit {commit_w3}.](../figures/reused/week3_fig_label_split_timeline.png)

**Choosing a model.** The rule, set in advance, was to take the model with the best cross-validated PR-AUC unless a simpler one was within one standard error of it. PR-AUC (area under the precision-recall curve) suits this task because decoupling windows are the minority: it measures how well true cases are ranked near the top and has a clear no-skill line [@SaitoRehmsmeier2015]. The random forest scored highest ({cv_prauc_rf}) but the logistic regression ({cv_prauc_lr}) cleared the cut-off ({cv_cutoff}), so it was chosen. A cut-off for turning scores into yes or no was fixed by maximising F1 on out-of-fold predictions; it came to {thr_lr}.

**Metrics and uncertainty.** Besides PR-AUC, the report uses ROC-AUC, precision, recall, F1 and the Matthews correlation coefficient (MCC), which stays honest when classes are unbalanced [@ChiccoJurman2020]. Intervals come from a bootstrap that re-draws whole countries, because windows from one country are not independent.

**One test run.** After the configuration was frozen, the test years were scored once; a lock file blocks a second run. Later comparisons read the saved predictions only and are labelled post hoc.

### 4.5 Quality assurance

| In short |
| --- |
| Quality was built in at four levels: plans written first, automated tests, a ledger that ties every number to a file, and an independent recomputation of the headline numbers. |

- **Pre-specified plans.** Weeks 2 and 3 each committed their plan before touching data or models, and logged every later deviation.
- **Pytest suites.** Week 2 reports {w2_pytest_reported} checks and Week 3 reports {w3_pytest}. Run here from fresh clones, Week 3 passes all of them and Week 2 passes {w2_pytest_passed} of {w2_pytest_reported}; the one failure is the line-ending issue in Section 3.4.
- **A claims ledger.** Every number in this report is a row in `results/claims_ledger.csv` with its source repository, commit, file and column. The report is built from a template with placeholders, so a number cannot drift from its evidence.
- **Independent verification.** `src/verify_headlines.py` recomputes the headline numbers from saved data and saved predictions with different code (Section 5.5).
