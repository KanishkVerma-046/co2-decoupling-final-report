## 2. Introduction

| In short |
| --- |
| This project asks whether richer countries emit more carbon, and whether growth and falling emissions can go together. It was built in four steps: plan, test, predict, and (this report) check and combine. The report is written for managers first and technical readers second. |

### 2.1 The problem

Carbon dioxide from burning fossil fuels and making cement is the largest single human cause of climate change. Countries differ enormously in how much they emit, how rich they are, and how their energy is produced. A long-running idea says that countries pollute more as they grow richer, then less once they are rich enough. Economists call this the environmental Kuznets curve [@GrossmanKrueger1995]. Later reviews found that the evidence for carbon dioxide is weak and depends on the sample and the method [@Stern2004]. This project tests the question with open data rather than assuming an answer.

The question is harder than it looks. Totals are dominated by a few very large economies. Per-person values are dominated by a few very small, fuel-exporting ones. The two data sources name countries differently. Much of the history is missing. A careless analysis would produce a confident but wrong headline.

### 2.2 Why it matters

An organisation that wants to set priorities, report progress or decide where to look first needs to know three things. Is income a useful way to group countries? Is the growth-without-extra-carbon outcome rare or common? And can a model tell in advance which countries are heading that way? Wrong answers are costly in both directions. Treating income as destiny hides the countries that break the pattern. Trusting a weak model sends effort to the wrong places.

### 2.3 Who this report is for, and how to read it

The first audience is a manager who needs the answer, the confidence in it and the next steps. The second is a technical reviewer who needs to see how every number was produced. The report serves both by putting a plain-English summary at the start of each method section, and by moving the detail into tables, figures and appendices.

**Table 2.1: Where to start, by type of reader.**

| Reader | Start with | Then read |
| --- | --- | --- |
| Manager or sponsor | Sections 1 and 11 | Sections 5.4, 7 and 8 |
| Analyst who will reuse the results | Sections 3 and 5 | Sections 4, 9 and 10 |
| Technical reviewer | Sections 4 and 5.5 | Appendices A and B |
| Anyone meeting a new term | Section 2.5 | Appendix C |

### 2.4 The four-week project at a glance

The work was done in four steps. Each step used the earlier ones as its starting point and kept its own repository, listed with commit hashes in Appendix A.

![Figure 2.1: The four steps of the project, from planning to this synthesis. Read from left to right: each box says what the step asked, what it did and what came out. Source: Week 4 synthesis.](../figures/fig_journey.png)

- **Week 1: plan the exploration.** It chose two open datasets, found and fixed their quirks on paper, set out {w1_n_questions} questions and the charts that would answer them, and profiled the real data. The full exploratory analysis was planned but not run.
- **Week 2: test the claims.** It wrote an analysis plan before opening the data, then ran {n_hypotheses} hypothesis tests ({n_confirmatory} confirmatory, one exploratory) with corrections for running several tests at once.
- **Week 3: try to predict decoupling.** It built a model that predicts, for a country in a given year, whether decoupling will happen over the next {cfg_h} years. The design was fixed in advance and the final test was run once.
- **Week 4: check, combine and advise.** This report recomputes the key numbers, compares the three sets of results, rates the evidence and turns it into recommendations.

### 2.5 A short glossary

The terms below are used throughout. A longer list is in Appendix C.

**Table 2.2: Terms used in this report.**

| Term | What it means here |
| --- | --- |
| CO2 per person | Tonnes of carbon dioxide from fossil fuels and cement produced inside a country in a year, divided by its population. |
| Income per person | Economic output per person in constant 2015 US dollars (World Bank GDP per person). |
| Decoupling | Always *absolute* decoupling: CO2 per person falls while income per person rises. |
| Income group | The World Bank's four classes: low, lower-middle, upper-middle and high income (current classification). |
| Production-based emissions | Emissions counted where the carbon is released, not where the goods are used. |
| Rank correlation | A score for how well the order of countries on one measure matches their order on another: high means a close match, zero means none. |
| Hypothesis test | A procedure that asks whether a pattern is larger than chance alone would produce. |
| Confidence interval | A range that is likely to contain the true value; wide means uncertain. |
| PR-AUC | A score between zero and one for how well a model puts true cases near the top of its list. A model with no skill scores the share of true cases. |
| Base rate | The share of cases that are true to begin with (here, the share of windows in which decoupling happens). |
| Post hoc | Decided after the results were seen, so treated as exploratory. |
