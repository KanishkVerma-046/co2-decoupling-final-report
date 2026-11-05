## 5. Results

### 5.1 What the data look like

| In short |
| --- |
| Richer countries emit more per person and high-income countries are the ones that mostly decouple, but even among them only about a third decouple in a typical three-year window. The lower-income groups show no clear trend. |

**Income and emissions.** Figure 5.1 plots every country in 2022: income per person across, CO2 per person up, both on logarithmic scales. The dots rise from lower left to upper right, and the orange trend line captures most of the pattern. The rank correlation is {h1_rho} (95% interval {h1_ci_lo} to {h1_ci_hi}, {h1_n} countries). Two features deserve attention. The spread around the line is wide: at similar incomes, CO2 per person differs by a factor of ten or more, which is where fuel mix, climate and industry come in. The cloud also flattens among the richest countries, a hint (tested as H4 in Section 5.2) that more income no longer means proportionally more carbon there.

![Figure 5.1: Income per person and CO2 per person in 2022 for {h1_n} countries, on logarithmic scales, coloured by income group. Look at the straight upward trend and at the wide vertical spread within each group. Source: Week 2 cross-section table (cross_section_2022.csv), redrawn in Week 4.](../figures/fig_income_vs_co2.png)

**Decoupling by group, 1990 to 2022.** Figure 5.2 compares each country's 1990 and 2022 values. The bars rise sharply with income. In the high-income group {dec_k_high} of {dec_n_high} countries ({dec_pct_high}%, 95% interval {dec_lo_high}% to {dec_hi_high}%) cut CO2 per person while their income grew. In the other groups the shares are {dec_pct_low}% ({dec_k_low} of {dec_n_low}), {dec_pct_lm}% ({dec_k_lm} of {dec_n_lm}) and {dec_pct_um}% ({dec_k_um} of {dec_n_um}). Across all {dec_all_n} countries compared, {dec_all_share}% decoupled. The low-income interval is wide because the group is small.

![Figure 5.2: Share of countries whose CO2 per person fell while income per person rose between 1990 and 2022, by income group, with 95% intervals. Look at the step up at the high-income bar and at the dashed line for all countries. Source: Week 4, rebuilt from Week 2's paired table.](../figures/fig_decoupling_by_group.png)

**Decoupling over time.** Figure 5.3 asks the same question for every three-year window from {cfg_pool_start} to {cfg_test_last}. The high-income line rises from {dot_high_1993}% in the first window to {dot_high_2019}% in the last, with large swings in between. In a typical window {dot_high_mean}% of high-income countries decouple ({dot_high_recent}% in windows starting since 2010), and high income has the highest share of the four groups in {dot_high_top} of {dot_n_windows} windows. For all countries the share rose from {dot_all_1993}% to {dot_all_2019}%. The lower groups show no steady trend: low income goes from {dot_low_1993}% to {dot_low_2019}% and lower-middle income from {dot_lm_1993}% to {dot_lm_2019}%. Windows starting in {cfg_test_first} to {cfg_test_last} end in the pandemic years, so the right-hand end should be read with care.

![Figure 5.3: Share of countries decoupling in each three-year window, by income group. Look at the dark high-income line, which sits above the rest in most windows, and at the grey and blue bands that mark the years Week 3 left unused and the test years. Source: Week 4, built from Week 3's panel with the label rebuilt independently.](../figures/fig_decoupling_over_time.png)

These figures are descriptive. The next two sections ask whether the patterns could be chance, and whether they predict anything.

### 5.2 Statistical tests

| In short |
| --- |
| All six confirmatory tests were significant after correction, but they are not equally strong. Income, group differences and decoupling by group are robust. The decline in high-income emissions is moderate. The difference in slope is fragile. |

**Table 5.1: Primary results of the seven hypotheses (Week 2), with the confidence rule applied to each.**

[[table:hypothesis_summary]]

**Income and emissions (H1 to H3).** The H1 rank correlation of {h1_rho} survives every check: with PPP income ({h1_rho_ppp}, {h1_rho_ppp_n} countries), without countries under one million people ({h1_rho_small}) and without oil and gas exporters ({h1_rho_oil}). Median CO2 per person rises at every step up the income ladder, from {med_low} tonnes in low-income countries to {med_lm}, {med_um} and {med_high} tonnes (Figure 5.4). Every pair of groups differs after correction. High-income countries emit about {h3_ratio} times as much per person as lower-middle and low-income countries combined, a gap that holds without small countries ({h3_ratio_small} times) and without oil and gas exporters ({h3_ratio_oil} times). The standardised effect (Cohen's d of {h3_d}) is unusually large, partly because groups are defined from income.

![Figure 5.4: CO2 per person in 2022 by income group, on a logarithmic scale, with individual countries and box summaries. Look at how little the boxes overlap. Source: Week 2, fig_h2_boxplot_by_income.png, commit {commit_w2}.](../figures/reused/week2_fig_h2_boxplot_by_income.png)

**Decoupling by group (H6).** The share of countries that decoupled rises from {dec_pct_low}% in low-income countries to {dec_pct_high}% in high-income ones, and the chi-square test rejects independence (Cramer's V = {h6_v}, interval {h6_v_lo} to {h6_v_hi}). The odds of decoupling in a high-income country are about {h6_or} times those elsewhere (interval {h6_or_lo} to {h6_or_hi}), and the effect is no smaller with PPP income or without small countries or oil exporters. Figure 5.5 shows where the table departs from independence: high-income countries decouple far more often than expected, every other group less often.

![Figure 5.5: Counts of decoupled and not-decoupled countries by income group, with the count expected if group made no difference in brackets. The colour shows the standardised residual: look for the strong cells in the high-income row. Source: Week 2, fig_h6_decoupling_heatmap.png, commit {commit_w2}.](../figures/reused/week2_fig_h6_decoupling_heatmap.png)

**Did high-income emissions fall (H5)?** Yes, moderately. Among {h5_n} high-income countries with data in both years, the median change in CO2 per person was a fall of {h5_median_abs}% (95% interval {h5_ci_lo}% to {h5_ci_hi}%), and it fell in {h5_fell} countries. The result holds without small countries (median {h5_median_small}%) and without oil exporters ({h5_median_oil}%). Two cautions. The effect size ({h5_rbc}) has an interval ending at {h5_rbc_hi}, close to zero. And the design could detect a paired effect of {h5_mde}, but the observed effect was {h5_dz}, so the evidence is real but not overwhelming (adjusted p = {h5_p_holm}).

**The weakest result: do slopes differ (H4)?** The test says yes (adjusted p = {h4_p_holm}), but the extra variance explained is only {h4_dr2} of the total, about one percent. The estimated slopes run from {slope_low} for low-income countries down to {slope_high} for high-income ones: among poorer countries a doubling of income goes with a near-proportional rise in emissions, while among the richest the link is nearly flat (Figure 5.6). But {h4_rob_fail} of the {h4_rob_n} robustness checks did not reach the usual significance level: without small countries the p-value is {h4_p_small} and the planned label-permutation check gives {h4_p_labelperm}. The honest summary is: there is some evidence of a flatter slope at high income, but it depends on which countries are included. This is why it is rated Low and recommended for replication (R5).

![Figure 5.6: Income and CO2 per person by income group, each with its own fitted line. Look at how the high-income line is much flatter than the others. Source: Week 2, fig_h4_slopes_by_income.png, commit {commit_w2}.](../figures/reused/week2_fig_h4_slopes_by_income.png)

**Structural drivers (H7, exploratory).** Adding industry share and urbanisation to income raises the share of variance explained from {h7_r2_gdp} to {h7_r2_full} (an extra {h7_dr2}, {h7_n} countries). Industry carries the effect: each extra percentage point of industry in the economy goes with about {h7_industry_pct}% more CO2 per person at the same income. Urbanisation shows no clear effect once income and industry are accounted for (the interval runs from {h7_urban_lo} to {h7_urban_hi}). Because this analysis was exploratory and its p-values were not corrected, it is rated Low.

### 5.3 Machine learning

| In short |
| --- |
| The model puts decoupling windows nearer the top of its list than a simple rule does, but not by much. Used as a yes/no classifier it is close to useless. A free rule that just uses a country's income group does about as well, and two other models scored higher after the fact. |

**Setting.** Of the {w3_pool_rows} windows in the training pool, {w3_pool_pos} ({w3_pool_rate}%) were decoupling windows. In the test set, {w3_test_pos} of {w3_test_rows} ({w3_test_rate}%) were. A model with no skill would therefore score a PR-AUC of about {test_prauc2_prior} on the test set.

**Main result.** The chosen logistic regression scored a test PR-AUC of {test_prauc_lr} (95% interval {test_prauc_lo_lr} to {test_prauc_hi_lr}), against {test_prauc_persistence} for the persistence rule. The paired difference was {test_diff_persist} (interval {test_diff_persist_lo} to {test_diff_persist_hi}), which excludes zero, so the pre-specified success criterion for ranking was met. In cross-validation the model's score was lower ({cv_prauc_lr}), so there is no sign that tuning inflated the test score. Pooled out-of-fold predictions showed the same advantage over persistence ({cv_lr_minus_persist}, interval {cv_lr_minus_persist_lo} to {cv_lr_minus_persist_hi}).

**Table 5.2: Test results for all models (start years {cfg_test_first} to {cfg_test_last}; precision, recall, F1 and MCC at each model's frozen threshold).**

[[table:test_metrics]]

![Figure 5.7: Left: ranking skill of each model on the test years, with the no-skill line. Right: of the highest-scored windows, the share that really decoupled (a post hoc, exploratory view added in Week 4). Look at how all models sit above the base rate, and at how wide the intervals are. Source: Week 3 test results, redrawn in Week 4.](../figures/fig_model_skill.png)

**As a yes/no classifier it fails.** At its frozen threshold the logistic regression flagged {test_fp_lr} windows that did not decouple as decoupling and cleared only {test_tn_lr}, while catching {test_tp_lr} of the {w3_test_pos} true cases. Its precision ({test_prec_lr}) was about the base rate and its MCC was {test_mcc_lr} (interval {test_mcc_lo_lr} to {test_mcc_hi_lr}), lower than the persistence rule's {test_mcc_persistence}. The threshold rule, which maximises F1, drifts to "flag almost everything" when a model separates the classes only weakly. Week 3 pre-specified this rule and kept it.

**Much of the skill is income.** In a post hoc check, a rule that gives each window the training-period base rate of its income group scored a PR-AUC of {ph_group_prior}. The logistic regression's advantage over it was {ph_lr_minus_group} (interval {ph_lr_minus_group_lo} to {ph_lr_minus_group_hi}), which is indistinguishable from nothing. In plain terms, what the linear model mostly learned is the Week 2 finding that richer countries decouple more often. Within income groups its ranking is weak; for lower-middle-income countries its ROC-AUC was {sg_roc_lm}, below the {test_roc_prior} of a coin flip. Among the subgroups, the share of windows that decoupled ranges from {sg_prev_low}% (low income) to {sg_prev_high}% (high income).

**Two other models scored higher, after the fact.** The random forest scored {test_prauc_rf} and gradient boosting {test_prauc_hgb}. The logistic regression minus the forest was {ph_lr_minus_rf} (interval {ph_lr_minus_rf_lo} to {ph_lr_minus_rf_hi}), and the forest beat the income-group rule by {ph_rf_minus_group} (interval {ph_rf_minus_group_lo} to {ph_rf_minus_group_hi}), which hints at structure beyond income. These comparisons are post hoc. Switching to the forest after seeing the test set would turn the test set into a selection tool, so the pre-specified choice stands and the forest result is a lead for the next round (R4).

**A plain-language view (post hoc).** Table 5.3 asks a simpler question: if you took only the top {top_frac}% of windows by model score ({top_n} windows), how many would really decouple? The base rate is {top_base}%.

**Table 5.3: Precision among the top-scored {top_frac}% of test windows (post hoc, exploratory, not pre-specified).**

[[table:top20]]

The logistic regression's top-scored fifth was right {top_prec_lr}% of the time, about {top_lift_lr} times the base rate. The persistence rule's top fifth was right {top_prec_persistence}%. This is a more intuitive way to see the same modest ranking gain; the {top_frac}% cut was fixed in advance for presentation and was not tuned.

**What the model leans on.** Shuffling income per person in the test data cost {imp_gdp} of PR-AUC, the largest drop of any feature, followed by the oil share of CO2 ({imp_oil}). Urbanisation mattered in cross-validation but not on the test set ({imp_urban}). Using recent changes in CO2 and income alone, the model scored {abl_A}, no better than the base rate; adding economic structure raised it to {abl_B} and fuel mix to {abl_C}. A country's recent trajectory says almost nothing about its next three years.

![Figure 5.8: Precision-recall curves on the test years. The dotted line is the base rate; the cross is the persistence rule. Look at how close the curves lie to each other and to the dotted line over much of their range. Source: Week 3, fig_test_precision_recall.png, commit {commit_w3}.](../figures/reused/week3_fig_test_precision_recall.png)

![Figure 5.9: Left: how much the test score falls when each feature is shuffled. Right: the largest standardised coefficients of the logistic regression. Look at income per person at the top of both panels. Source: Week 3, fig_importance_coefficients.png, commit {commit_w3}.](../figures/reused/week3_fig_importance_coefficients.png)

Robustness did not change the order. Without the first test year, whose window ends in 2020, the logistic regression scored {rob_excl17_lr} against {rob_excl17_persist} for persistence. Without countries under one million people it scored {rob_small_lr} against {rob_small_persist}.

### 5.4 Triangulation: where the three lenses agree and where they do not

| In short |
| --- |
| Income is the common thread: all three weeks point to it. Beyond income, the evidence thins out. Each finding is rated High, Moderate or Low by a fixed rule, not by how interesting it is. |

Three kinds of evidence are laid side by side in Table 5.4: the Week 1 exploration, the Week 2 tests and the Week 3 model.

**Table 5.4: The project's main questions, what each week said, and how far the answer can be trusted.**

[[table:triangulation]]

**The confidence rule.** The rule was fixed before the analysis. *High*: pre-specified; every pre-specified robustness check agrees; the corrected p-value is below 0.01 (or a paired interval for a model comparison excludes zero); the repository raised no power warning; and another week's evidence backs it. *Moderate*: pre-specified and supported, but at least one of those conditions fails and no more than one robustness check does. *Low*: exploratory, post hoc, planning-stage only, or two or more robustness checks fail. For tests H1 to H6 the counts are computed from Week 2's results file, so the rating is mechanical.

**Table 5.5: The rule applied to every finding.**

[[table:confidence]]

Of the seven hypotheses, {n_rating_high} are rated High, {n_rating_moderate} Moderate and {n_rating_low} Low. Figure 5.10 shows which lens supports which finding.

![Figure 5.10: Evidence matrix. Rows are findings; columns show which week supports each (filled = pre-specified result, half-filled = partial, exploratory or post hoc, hollow = planned only, dash = none) and the confidence rating. Look for rows that depend on a single week. Source: Week 4 synthesis.](../figures/fig_evidence_matrix.png)

Where the lenses agree, the agreement is on income. Where they disagree, it is about detail: Week 2 finds no clear urbanisation effect while Week 3's model leans on it in cross-validation, and the forest's test-set advantage, seen only after the fact, contradicts the rule that chose the logistic regression. None of these disagreements overturns a headline finding; each is why a related finding is rated lower.

### 5.5 Independent verification

| In short |
| --- |
| The headline numbers were recomputed with different code from saved data. All checks agree with the originals. |

`src/verify_headlines.py` recomputed {ver_n} quantities from the saved processed data and saved predictions, with code written independently of the earlier repositories: rank correlation from ranks, its interval from a new bootstrap, decoupling flags rebuilt from the 1990 and 2022 values, the Week 3 label rebuilt from the panel, and every test metric and confusion matrix recomputed from the saved predictions at the frozen thresholds. Of {ver_n} checks, {ver_pass} passed and {ver_fail} failed.

**Table 5.6: Selected verification checks. Tolerances are set before running: exact for counts and exact formulas, 0.02 for bootstrap interval ends because a different random seed changes them slightly.**

[[table:verification]]

The rank correlation ({ver_rho_new}), the ratio ({ver_ratio_new}) and the test PR-AUC ({ver_prauc_new}) all reproduce, and {ver_labels_wrong} of the {w3_test_rows} test windows have a saved label that differs from the independently rebuilt one. The checks verify arithmetic and consistency. They do not prove the underlying data are right, or that the definitions are the best ones.
