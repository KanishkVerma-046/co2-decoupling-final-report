# Does Wealth Burn Carbon? Week 4: Comprehensive Project Report and Recommendations

The final task of a four-task data-science virtual internship. The project asks whether richer countries emit more carbon, and whether a country can grow richer while its CO2 emissions per person fall ("decoupling"), using Our World in Data (OWID) CO2 data and World Bank indicators for 1990-2022.

This repository **synthesises Weeks 1 to 3**. It does not repeat their analyses. It:

1. proves where every number comes from (lineage, a claims ledger),
2. recomputes the headline numbers independently,
3. puts the exploration, the statistical tests and the machine-learning model side by side (triangulation) with a fixed confidence rule,
4. adds two small, labelled descriptive analyses,
5. draws new figures for a general audience, and
6. writes the final report for a non-technical audience.

## The four-week project

| Week | Task | Repository | Commit used |
| --- | --- | --- | --- |
| 1 | Data Exploration and Visualization Strategy | https://github.com/KanishkVerma-046/co2-economy-eda-proposal | `cb3a0dfcde6f084e721bf8ceb9f3ad47909433d9` |
| 2 | Statistical Analysis and Hypothesis Testing Framework | https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing | `4348fdd9a01ebed44b0e87bc97eafa8384ca3a2f` |
| 3 | Machine Learning Model Development and Evaluation Plan | https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline | `67d512561a681fde1a5ef1b47b0cae09e986c6c8` |
| 4 | Comprehensive Report and Recommendations (this repository) | https://github.com/KanishkVerma-046/co2-decoupling-final-report | see `git log` |

## Where to look

| Path | What it holds |
| --- | --- |
| `report/report_content.md` | The final report (Markdown, generated). |
| `report/_build/` | Section templates with claim-id placeholders, table templates and `build_report.py`. |
| `report/report_notes.md` | Private notes for the author: items needing attention, figure map, viva questions. |
| `docs/synthesis_plan.md` | The plan, committed before any analysis code. |
| `results/claims_ledger.csv` | Every number in the report: source repository, commit, file and column. |
| `results/lineage.csv`, `results/data_vintage_check.csv` | Commits, data fingerprints and the same-vintage check. |
| `results/verification.csv` | Independent recomputation of the headline numbers. |
| `results/triangulation.csv`, `confidence_ratings.csv`, `evidence_matrix.csv`, `reconciliation.csv`, `recommendations.csv` | The synthesis tables. |
| `results/decoupling_*.csv`, `model_skill_top20.csv` | The new descriptive analyses (the second is post hoc and exploratory). |
| `figures/`, `figures/reused/` | Eight new figures and eight copied from Weeks 1 to 3 with their source recorded. |
| `data/inputs/` | Byte-exact copies of the earlier repositories' files that this repository uses, with `manifest.csv` (commit, path, sha256). |

## How to reproduce

Python 3.13 (developed on 3.13.3, Windows 11).

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/lineage.py
python src/verify_headlines.py
python src/synthesis_tables.py
python src/build_ledger.py
python src/render_tables.py
python src/make_figures.py
python report/_build/build_report.py
pytest
```

On Linux or macOS use `source .venv/bin/activate`. The inputs are already in `data/inputs/`. To refresh them, clone the three earlier repositories into `reference/week1`, `reference/week2` and `reference/week3` (check out the commits above) and run `python src/collect_inputs.py`. `python src/check_references.py` re-verifies the references against the Crossref API and needs internet access.

## Provenance and rules

- **No model was fitted and no earlier test was re-run.** Only saved result files and saved predictions are used. In particular the Week 3 test evaluation (which is locked in its own repository) was not repeated.
- **Numbers come from the ledger.** The report is built from a template; the build stops if a placeholder has no ledger row. A pytest check re-reads every ledger value from its source file.
- **Independent verification.** `src/verify_headlines.py` recomputes the rank correlation and its interval, group ratios, decoupling shares, the Week 3 label, and every test metric with different code from the originals (numpy only for the metrics).
- **Same data vintage.** The OWID file is byte-identical in Weeks 2 and 3, and all overlapping World Bank values are identical. See `results/data_vintage_check.csv`.
- **References** are verified through the Crossref API (`results/reference_check.csv`); those that could not be verified were dropped.
- **Data licences.** OWID and World Bank data are open and must be credited; see the report's reference list for the sources.

## Tests

`pytest` runs the integrity checks in `tests/` (ledger, placeholders, verification tolerances, input hashes, report format, figures, recommendations, word counts, references).
