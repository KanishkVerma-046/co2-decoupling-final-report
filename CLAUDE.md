# CLAUDE.md - project instructions

## Context (short)

Week 4 (final) task of a four-task data-science virtual internship: a comprehensive, plain-English report with recommendations that synthesises Weeks 1-3 of the project **"Does Wealth Burn Carbon?"** (CO2 per person versus economic development, 1990-2022; Our World in Data CO2 dataset + World Bank indicators).

| Week | Repo | Contribution |
|---|---|---|
| 1 | https://github.com/KanishkVerma-046/co2-economy-eda-proposal | EDA and visualisation plan, preliminary data profiling |
| 2 | https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing | Pre-specified hypotheses H1-H7 (H1-H6 confirmatory, Holm) |
| 3 | https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline | Leakage-safe ML for 3-year-ahead decoupling |
| 4 | this repo (`co2-decoupling-final-report`) | Synthesis, verification, figures, final report |

The report is submitted as a Word file. A separate assistant converts `report/report_content.md` to .docx, so the Markdown must follow the format limits below.

## Repository layout

```
README.md, CLAUDE.md, requirements.txt
docs/synthesis_plan.md      written and committed BEFORE any analysis code
src/collect_inputs.py       copies the exact input files from reference/weekN into data/inputs with a sha256 manifest
src/lineage.py              results/lineage.csv, results/data_vintage_check.csv
src/verify_headlines.py     independent recomputation -> results/verification.csv
src/synthesis_tables.py     triangulation, confidence ratings, decoupling over time, model-skill metric, reconciliation
src/build_ledger.py         results/claims_ledger.csv (every number used in the report)
src/make_figures.py         new figures (figures/*.png) and reused-figure copies (figures/reused/*.png)
tests/                      pytest checks
data/inputs/                small copies of inputs, with provenance (manifest)
results/                    all CSV outputs
report/report_content.md    generated report (do not edit by hand)
report/_build/              report_template.md + build_report.py ({claim_id} placeholders)
report/report_notes.md      private notes for the author (not for submission)
reference/                  git-ignored read-only clones of Weeks 1-3
```

## Hard rules

- Never invent numbers, citations, hours or results. Report conflicts and gaps. Honest, modest findings are presented as they are.
- Do not re-fit models or re-run the Week 3 test evaluation. Use saved result files and saved predictions only.
- No placeholders ("TODO", "TBD", "author to enter", "lorem") in the report, figures or README.
- Every reference is verified through the Crossref API (title, journal, year, volume/pages, DOI); unverifiable ones are dropped. Earlier project work is cited by repo URL and commit hash.
- No effort or hours tables.
- "Decoupling" always means absolute decoupling: CO2 per person falls while GDP per person rises.
- Keep commands and paths cross-platform (pathlib; no bash-only scripts). Windows 11, Python 3.13.

## Numbers in the report

**Numbers in the report come from `results/claims_ledger.csv` via `report/_build/build_report.py`.** The template `report/_build/report_template.md` contains `{claim_id}` placeholders; the build fails loudly if an id is missing. Never type a result number directly into the template.

## Markdown format limits (the converter)

Only `##` and `###` headings, paragraphs, pipe tables, `- ` bullets, numbered lists, code fences, bold, italic, inline code, links. No blockquotes, HTML, footnotes or nested lists. Callouts are one-column pipe tables (header row = title, one body row). No `|` inside a table cell. Figures: `![Figure 5.1: caption.](../figures/fig_name.png)`; reused figures live in `../figures/reused/`. Table captions: a bold paragraph directly above the table, `**Table 5.1: caption.**`. LF line endings.
