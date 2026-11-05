## 3. Data and lineage

| In short |
| --- |
| Two open datasets were joined on country codes and cleaned with written rules. The same OWID file and the same World Bank values were used in Weeks 2 and 3, and Week 1's reported counts are consistent with them. The three weeks use different definitions of "decoupling" and different samples, so their numbers must not be mixed without the translation given in Section 3.5. |

### 3.1 Sources and what they measure

**Our World in Data (OWID) CO2 dataset.** One file of {w1_owid_rows} rows and {w1_owid_cols} columns ({w1_owid_mb} MB), covering {w1_owid_year_min} to {w1_owid_year_max}. It holds {w1_owid_entities} entities, of which {w1_owid_countries} are countries and {w1_owid_non_countries} are regions, groups or special categories. The key measure is CO2 per person from fossil fuels and industry, counted where the carbon is released (production-based).

**World Bank World Development Indicators.** Downloaded through the public API: income per person (GDP per person, constant 2015 US dollars), population, the urban share of the population and industry's share of GDP, plus the metadata that assigns each country to an income group. The download holds {w1_wb_entities} entities, of which {w1_wb_aggregates} are regional or income-group aggregates.

Both sources are open (OWID and the World Bank state that their data may be reused with credit). The analysis window is 1990 to 2022, chosen in Week 1 because CO2 and population are nearly complete from 1990, OWID's own GDP column stops in 2022, and 1990 is a common baseline year.

### 3.2 Cleaning rules

Each rule answers a problem measured in Week 1's profiling, not a generic checklist. The rules were written in Week 1, applied in Week 2 and ported unchanged to Week 3.

**Table 3.1: The cleaning rules and what they affected.**

| Rule | Why | What it affected |
| --- | --- | --- |
| Remove aggregates (regions, income groups, "World") | Counting a region and its countries double counts emissions. | {w2_owid_aggregates} OWID entities and {w2_wb_aggregates} World Bank aggregates. |
| Join on the three-letter ISO3 country code, never on names | Names differ: "Egypt" against "Egypt, Arab Rep.". | {w1_iso_matched} countries matched on codes against {w1_name_matched} on names, so a name join would have lost {w1_name_lost}. |
| One manual crosswalk for Kosovo | It has a code at the World Bank but none in OWID. | {w2_kosovo_rows} rows re-keyed. |
| Never fill in CO2 or income | They are the outcome and the main driver; filling them in would invent the pattern under study. | Rows missing either are dropped from that analysis only, and counted. |
| Keep zero CO2 values but exclude them from logarithms | Zeros are real in the early record of two territories, but a logarithm is undefined. | {w2_log_guard_rows} country-years. |
| One income series: World Bank GDP per person, constant 2015 US dollars | OWID's own GDP column is missing for {w1_window_owid_gdp_missing}% of country-years in the window, against {w1_window_wb_gdp_missing}% at the World Bank. | Used throughout; the PPP series is a check only. |
| Restrict to 1990-2022 | CO2 is missing for only {w1_window_co2_missing}% of country-years in this window. | Week 3 reads 1988-1989 as look-back only. |

![Figure 3.1: Share of country-year rows with a missing value, by variable and decade, in the OWID file (countries only). Look at how the pale cells cluster in the early decades: missingness depends far more on time than on the variable, which is why the study starts in 1990. Source: Week 1, fig_profile_missing_heatmap.png, commit {commit_w1}.](../figures/reused/week1_fig_profile_missing_heatmap.png)

### 3.3 How many countries entered each analysis

Every test and every model uses only the countries that have the variables it needs. Nobody is dropped silently: each step is counted in the earlier repositories' sample-flow tables, reproduced below.

**Table 3.2: Sample flow in Weeks 2 and 3 (counts as reported by those weeks).**

[[table:sample_flow]]

In Week 2 the income-and-emissions test started with {w2_entities} country entities and kept {h1_n} after removing {w2_no_co2_2022} without CO2 in 2022 and {w2_no_gdp_2022} without income. In Week 3 the table starts from country-years, not countries, and ends with {w3_flow_end} eligible three-year windows, of which {w3_all_rows} fall in the training pool or the test set. The remainder start in the three years between them, which Week 3 deliberately left unused.

### 3.4 Lineage and consistency across the weeks

This report rests on three earlier repositories. Table 3.3 gives the exact commit read for each one.

**Table 3.3: The earlier work this report draws on.**

[[table:lineage]]

A synthesis is only valid if the weeks used the same data. We compared the raw-file fingerprints (sha256 hashes) that Weeks 2 and 3 recorded, and then compared the overlapping values directly.

**Table 3.4: Whether the weeks used the same data vintage.**

[[table:vintage]]

The outcome, stated plainly:

- **OWID: identical.** The file has the same fingerprint in Weeks 2 and 3. Week 1 recorded no fingerprint, but its reported file size and shape match.
- **World Bank: same values.** The files differ in fingerprint only because Week 2 requested 1990-2022 and Week 3 requested 1988-2022. For every overlapping row ({vint_overlap_rows} rows per indicator file) the values are identical ({vint_overlap_diff} differences). Week 1's missing-data rates for three indicators agree with Week 2's cleaning log to two decimals.
- **One tooling problem, no data problem.** Week 2's own checksum test fails on a fresh clone ({w2_pytest_failed} of {w2_pytest_reported} checks), because its World Bank files were fingerprinted with Windows line endings and stored with Unix ones. Restoring the line endings reproduces the recorded fingerprints. Section 8 turns this into a recommendation.

Had the vintages differed, the weeks' numbers would not be comparable: a revised income value changes a country's rank, its income group and whether it counts as decoupled. Because they match, differences between weeks can be traced to definitions, not data.

### 3.5 Reconciling definitions across the weeks

The weeks answer related but different questions, so some numbers look inconsistent when they are not. The clearest case is decoupling. Week 2 asks whether a country's CO2 per person was lower, and income per person higher, in 2022 than in 1990: one comparison over {dec_all_n} countries, with {dec_all_share}% of them decoupling. Week 3 asks the same question over any three-year window and counts windows, not countries: about {w3_pool_rate}% of windows in the training period decoupled and {w3_test_rate}% in the test years. Short windows catch a country in a bad year; the long comparison hides the ups and downs between the two end years.

**Table 3.5: Definitional differences between the weeks, and how this report treats them.**

[[table:reconciliation]]

Two further points. First, Week 1's preliminary rank correlation ({w1_smoke_rho3} on {w1_smoke_n} countries) and Week 2's ({h1_rho} on {h1_n}) differ only because Week 2 includes one more country; Week 1's figure was a smoke test and is used only as a consistency check. Second, the income-group counts differ between weeks because the samples differ, not because the classification does. Throughout, the current World Bank classification is applied to all years, which is a limitation (Section 9).
