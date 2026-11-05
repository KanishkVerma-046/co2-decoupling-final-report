# Does Wealth Burn Carbon? Comprehensive Data Science Project Report and Recommendations

*Week 4 Task - Comprehensive Data Science Project Report and Recommendations (synthesis of the Week 1, Week 2 and Week 3 work)*

---

## 1. Executive summary

### 1.1 The question

Do richer countries burn more carbon? And can a country grow richer while its carbon emissions per person fall? This report calls the second outcome *decoupling* (carbon dioxide, or CO2, per person goes down while income per person goes up). It combines three earlier pieces of work on about {h1_n} countries between 1990 and 2022, using open data from Our World in Data and the World Bank.

### 1.2 What we did

In Week 1 we planned the exploration and checked the data. In Week 2 we wrote down {n_hypotheses} claims before looking at the results and tested them. In Week 3 we built a machine-learning model that predicts which countries will decouple over the next three years, and tested it once on years it had never seen. In this final week we recomputed the headline numbers with different code ({ver_pass} of {ver_n} checks agree), traced every number to a source file, and rated how far each finding can be trusted.

### 1.3 Five key findings

![Figure 1.1: The five headline numbers, each with a one-line meaning and a confidence badge. Read the badge first: it says how far the number can be trusted. Source: Week 4 synthesis of Weeks 1 to 3.](../figures/fig_findings_glance.png)

- **Richer countries emit more per person.** The rank correlation between income and CO2 per person is {h1_rho} (a perfect match would score one and no link zero). *High confidence.*
- **The gap is large.** High-income countries emit about {h3_ratio} times as much CO2 per person as lower-middle and low-income countries combined. *High confidence.*
- **Decoupling is mostly a high-income story.** Between 1990 and 2022, {dec_pct_high}% of high-income countries decoupled, against {dec_pct_low}% to {dec_pct_um}% in the other groups. Still, {dec_notdec_pct_high}% of high-income countries did not. *High confidence.*
- **Most high-income countries cut emissions per person.** The median fall was {h5_median_abs}% and CO2 per person fell in {h5_fell} of {h5_n} countries, but the effect is moderate and the study was only just large enough to detect it. *Moderate confidence.*
- **The model ranks better than a simple rule, but it is not a decision tool.** Its ranking score was {test_prauc2_lr} against {test_prauc2_persistence} for a rule that copies the recent past (a model with no skill scores about {test_prauc2_prior}, the share of true cases). At its fixed cut-off it flagged almost every window. *Moderate confidence.*

### 1.4 Five recommendations

The full list of {n_recommendations} recommendations, with evidence, next steps and success measures, is in Section 8. The five that matter most:

- **R1.** Use income groups as a starting lens, not a verdict, and always show how many countries break the group pattern. *High confidence.*
- **R2.** Measure decoupling over multi-year windows and report CO2 counted where it is produced next to CO2 counted where goods are consumed. *Moderate confidence.*
- **R3.** Do not use the Week 3 model for yes/no decisions. Use it only as a ranking aid, with its precision shown next to the base rate. *Moderate confidence.*
- **R5.** Treat the finding that the income-emissions link is flatter at high income as provisional until it is repeated. *Low confidence in the finding.*
- **R6.** Pin data versions, store checksums and refresh once a year with a change report. *High confidence.*

These are evidence-informed analytical recommendations. Policy decisions would need evidence about cause and effect, which this project does not provide.

### 1.5 The biggest caveat

All results describe patterns across countries, not causes. CO2 is counted where it is produced, so a rich country can look as if it decoupled because the goods it buys are now made, and the carbon emitted, elsewhere. The report cannot tell how much of the measured decoupling is of this kind.

### 1.6 How to read the rest of this report

Managers can read Sections 1, 5.4, 7, 8 and 11. Technical readers will want Sections 3 to 5, 9 and the appendices. Method sections open with a short plain-English summary, and every number can be traced through the claims ledger (Appendix B).
