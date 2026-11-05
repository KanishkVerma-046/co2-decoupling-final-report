## 7. Discussion

| In short |
| --- |
| Across countries, wealth and carbon go together, strongly. Among the richest countries the link has loosened, and most have cut emissions per person. But the cut is partial, may partly reflect imported emissions, and cannot be predicted well. |

### 7.1 What the evidence says about "does wealth burn carbon"

Across countries, yes, and strongly: a rank correlation of {h1_rho}, an income-group gap of about {h3_ratio} times, and income per person as the strongest feature in the predictive model. These come from different weeks and methods, and they agree: it is the most secure finding in the project.

Within the richest countries the answer is more nuanced. The majority of high-income countries cut CO2 per person between 1990 and 2022 ({h5_fell} of {h5_n}), and nearly two in three decoupled outright ({dec_pct_high}%). So wealth does not *have to* burn carbon: nearly two in three of the richest economies show that income can grow while emissions per person fall. But {dec_notdec_pct_high}% of them did not, and the median fall was {h5_median_abs}%. Decoupling is common among the rich, not automatic, and rare elsewhere.

### 7.2 Decoupling is real, but partial and measured one way

**It is measured on production-based emissions.** The data count CO2 emitted inside each country. A country that closes a steel mill and buys steel abroad lowers its own count and raises someone else's. Research on trade-embodied emissions found that emissions from the production of traded goods grew strongly between 1990 and 2008, and that some of the stabilisation of emissions in developed countries was linked to growing imports from developing ones [@Peters2011]. Other studies report falling production-based emissions in a group of developed economies [@LeQuere2019] and decoupling of consumption-based emissions from growth [@Hubacek2021]. This project did not test how much of the measured decoupling is of the imported kind. A systematic review of the decoupling literature separates absolute from relative decoupling and asks whether the decoupling seen is enough for climate targets [@Haberl2020]; a fall in emissions per person is therefore not the same as a climate-safe path.

**It depends on the window.** Over the whole period, {dec_all_share}% of all countries decoupled; in the training period, {w3_pool_rate}% of three-year windows did. High-income countries decouple in {dot_high_mean}% of windows on average. Any single number needs its definition beside it.

**It describes countries, not people.** A country-level pattern says nothing about whether a richer household emits more. Treating a group average as a fact about each member is the ecological fallacy [@Robinson1950].

### 7.3 What the weak machine-learning result means

The model is a useful *teaching* result, not a *forecasting* tool. It does what the plan asked: it beats the persistence rule with an interval that excludes zero. But at its fixed cut-off it flags almost everything, a free rule that uses only a country's income group ranks about as well, and a country's recent history alone predicts almost nothing about the next three years. In plain terms, the model's skill is mostly Week 2's finding expressed as a formula. Prediction and explanation are different jobs [@Shmueli2010]; this model does the first modestly and the second not at all.

The forest's and boosting's test-set advantage is a lead, not a finding: it was seen after the test set was opened.

### 7.4 How robust each conclusion is

Section 5.4 rates each conclusion. The income link, the group gap and the concentration of decoupling in high-income countries are High: they hold in every check and agree across weeks, though the gap is partly built in because groups are defined from income, and the decoupling share depends on a two-year comparison. The high-income fall is Moderate: it holds in every check but is moderate in size and only just detectable. The flatter slope and the structural drivers are Low. The model's edge over persistence is Moderate: the interval excludes zero, but the gain is modest and the test period was shaped by the pandemic.

### 7.5 What would change the conclusions

- **Consumption-based data** showing that most of the high-income decoupling disappears would weaken the central optimism; data showing it persists would strengthen it.
- **A later test period** in which the forest keeps its lead, or all models fall to the base rate, would settle the post hoc question.
- **Income groups by year** would change which countries sit in which group.
- **A different baseline year** would change who counts as decoupled, especially for economies that collapsed or restructured around 1990.
- **Data revisions** to income or emissions could move individual countries.

## 8. Recommendations

| In short |
| --- |
| There are {n_recommendations} recommendations. Each has an evidence link, a confidence rating, an owner, a next step and a measure of success. Three are ready to start now. These are evidence-informed analytical recommendations; policy decisions would need evidence about cause and effect that this project does not provide. |

### 8.1 How to read the recommendations

The confidence column is the weakest rating among the findings in the Section 5.4 evidence matrix that the recommendation rests on, or, for the two process recommendations, the rating of an observation made and verified in this project. A Low rating means the underlying finding is weak, which is itself the reason for the recommendation (R5), or that the recommended action is a test, not a conclusion (R4, R8). The table is wide; the paragraphs below say the same in plain language.

**Table 8.1: Prioritised recommendations.**

[[table:recommendations]]

![Figure 8.1: The recommendations in three groups, read from left to right: ready to start, needing a small piece of new work, and needing new data or a new test. Look at the badge on each card: it is the confidence in the evidence behind that recommendation. Source: Week 4 synthesis.](../figures/fig_roadmap.png)

### 8.2 The recommendations in plain language

**R1. Use income groups as a starting lens, not a verdict.** Income group separates emissions per person ({med_low} tonnes in the poorest group, {med_high} in the richest) and decoupling ({dec_pct_low}% to {dec_pct_high}%). But {dec_notdec_pct_high}% of high-income countries did not decouple, and the model's ranking within groups is weak. Show counts and the share that break the pattern in every group chart.

**R2. Track decoupling over several years, and with two kinds of emissions.** Two-year comparisons and three-year windows give different numbers ({dec_pct_high}% against an average of {dot_high_mean}%), so report more than one window length. Report emissions counted where they are produced next to emissions counted where goods are consumed; only {w1_consumption_countries} countries have the consumption series, so start there. The rating is Moderate because the need for the second measure rests on outside research, not on a test here.

**R3. Do not use the model for yes/no decisions.** Its cut-off flags nearly everything and a free income-group rule does about as well. If a shortlist is needed, take the top-scored windows and show their precision with an interval. Never present a model flag as a prediction that a country *will* decouple.

**R4. Test the forest and boosting models on later data.** They scored higher on the test years (forest {test_prauc_rf}, boosting {test_prauc_hgb}, against {test_prauc_lr}), but only after the fact. Freeze them, write the plan first, and score once on later windows. Until then the lead is a hypothesis.

**R5. Treat the slope-difference finding as provisional.** Of {h4_rob_n} robustness checks, {h4_rob_fail} did not reach the usual significance level, and the extra variance explained is only {h4_dr2}. Do not build on it until it is replicated.

**R6. Pin data versions, hash raw files and refresh once a year.** The lineage check worked because Weeks 2 and 3 saved fingerprints, and it found a real weakness: Week 2's checksum test fails on a fresh clone because of line endings. Store checksums that survive line-ending changes, record income classification by year, and re-run the lineage check at every refresh.

**R7. Show uncertainty and write the plan first.** Here the habit paid off: the plan stopped a post hoc model swap, and the intervals showed that the median fall in high-income emissions ({h5_ci_lo}% to {h5_ci_hi}%) and the model's score ({test_prauc_lo_lr} to {test_prauc_hi_lr}) are both wide. Use one format for every headline (number, interval, badge) and commit the plan before the results.

**R8. Study structural drivers properly.** Industry share adds explanatory power beyond income in the exploratory test ({h7_dr2} of variance) and oil share matters to the model ({imp_oil}), but urbanisation is inconsistent across weeks. A pre-specified study on a country-year panel with energy-mix shares is the natural next step.

## 9. Limitations

| In short |
| --- |
| The main limits are the data definitions (production-based CO2, current income groups), the unit of analysis (countries, not people), and the sample (few countries, overlapping windows, one pandemic-affected test period). No verification mismatches were found, but verification checks arithmetic, not definitions. |

- **Production-based emissions.** CO2 is counted where it is emitted, and only from fossil fuels and cement. Imports of carbon-intensive goods, land use and other greenhouse gases are not counted.
- **Current income groups.** The 2026 World Bank classification is applied to all years. Countries that moved between groups are placed in their current one, so each group mixes histories.
- **Circular income groups.** Groups are defined from income, so group comparisons partly restate the income result, and any model that sorts by group inherits it.
- **Ecological fallacy.** Everything describes countries. Nothing here says what a richer person or household emits.
- **Association, not cause.** No design here can separate the effect of income from fuel endowment, climate, trade, policy or institutions.
- **Dependence between windows.** Consecutive windows from one country share two of three years, and neighbouring countries share markets and technology, so effective sample sizes are smaller than nominal ones. Re-drawing whole countries in the bootstrap reduces this but does not remove it.
- **One test period.** The test windows end in 2020 to 2022 and were shaped by the pandemic. Dropping the first test year raised every score but kept the order.
- **A binary, strict label.** A tiny fall counts the same as a large one, and the end-point comparison is sensitive to the start year.
- **Single data vintage.** Both sources are revised. This project used one download.
- **Week 1 was a plan.** The planned exploration was not run in full, so the first lens in the triangulation is thin. Section 5.1 executes only the three most important planned charts.
- **Verification.** All {ver_n} recomputation checks agree with the originals ({ver_fail} mismatches). One finding outside the numbers: Week 2's own checksum test fails on a fresh clone because of line endings (Section 3.4).
- **Not done.** No consumption-based or causal analysis, no new data, no calibration inside folds, no retraining of any model and no re-run of the Week 3 test evaluation.

## 10. Future work and improvements

In rough order of value for effort:

1. **Add consumption-based emissions** for the countries that have them, and repeat the decoupling comparison on both measures (R2).
2. **Replicate the slope-difference test** on a later year, with the original plan (R5).
3. **Score the forest and boosting models once** on windows beyond the test years, with a plan written first (R4).
4. **Build a country-year panel for structural drivers**, adding OWID's energy-mix shares and a separate treatment of urbanisation (R8).
5. **Use income classifications by year** and compare the group results with those from the current classification.
6. **Replace the binary label with a continuous one** (the size of the change in emissions), and test whether the weak result owes something to the strict yes/no definition.
7. **Add calibration inside the cross-validation folds**, so that predicted probabilities can be read as probabilities.
8. **Automate the data refresh** with the lineage check and a change report (R6).
9. **Run the planned exploratory analysis in full**, including the fuel-mix and carbon-intensity charts that Week 1 specified but did not draw.

## 11. Conclusions

Does wealth burn carbon? Across countries, yes: richer countries emit far more CO2 per person, with a rank correlation of {h1_rho} and high-income countries emitting about {h3_ratio} times as much as lower-middle and low-income countries combined. These findings are rated High confidence: they were specified in advance, survive every robustness check and are echoed by the model.

But wealth does not have to burn carbon. Between 1990 and 2022, {dec_pct_high}% of high-income countries cut CO2 per person while growing, against {dec_pct_low}% to {dec_pct_um}% elsewhere. Emissions per person fell in {h5_fell} of {h5_n} high-income countries, by a median of {h5_median_abs}%. Moderate confidence is appropriate for the size of that fall; the direction is clear, the amount is not. And more than a third of high-income countries did not decouple.

Three limits keep this answer cautious. The emissions are counted where the carbon is released, so some of the decoupling may be imported. Nothing here shows that wealth *causes* either the emissions or the decoupling. And the attempt to predict who will decouple next gave a modest result: the model ranks countries better than a simple rule ({test_prauc_lr} against {test_prauc_persistence}), but it is not a decision tool, and much of what it knows is that rich countries decouple more often.

For decision makers, the practical conclusions are these. Use income as a starting lens, not a verdict (R1). Measure decoupling in more than one way (R2). Use the model, if at all, as a ranking aid (R3). Treat the weaker findings as provisional (R5). Keep the data and the plans traceable (R6, R7). The project's strongest asset is not any single number but the discipline behind it: plans written first, one locked test, independent checks, and a ledger that ties every number to its source.

## 12. References

[[references]]

*Data sources (web resources, not journal articles).* Our World in Data, *CO2 and greenhouse gas emissions data* (`owid-co2-data.csv`), https://github.com/owid/co2-data. World Bank, *World Development Indicators* via the Indicators API v2, https://api.worldbank.org/v2/. Both were downloaded on the dates recorded in the Week 2 and Week 3 manifests.

*Earlier work in this project (cited by repository and commit, not as publications).* Week 1: https://github.com/KanishkVerma-046/co2-economy-eda-proposal, commit {commit_w1}. Week 2: https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing, commit {commit_w2}. Week 3: https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline, commit {commit_w3}.
