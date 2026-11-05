"""Copy the exact input files this repository uses from the read-only clones in reference/ into data/inputs/.

Writes data/inputs/manifest.csv (source repo, commit, source path, copy path, sha256, bytes). The copy is byte-identical
(the content of `git show <commit>:<path>`, so line endings do not depend on local git settings).
Run:  python src/collect_inputs.py
"""
from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

from common import INPUTS, REF, REPOS, ROOT, git_head, sha256_of

# (week, path inside that repo)
FILES = {
    "week1": [
        "data/processed/profiling/profiling_summary.json",
        "data/processed/profiling/owid_top10_co2_per_capita_2022.csv",
        "data/processed/profiling/owid_coverage_by_year.csv",
        "report/report_content.md",
    ],
    "week2": [
        "data/raw/manifest.json",
        "data/processed/cross_section_2022.csv",
        "data/processed/paired_1990_2022.csv",
        "results/hypothesis_results.csv",
        "results/h6_contingency_and_residuals.csv",
        "results/h2_group_descriptives.csv",
        "results/h4_slopes_by_group.csv",
        "results/h7_coefficients.csv",
        "results/power_mde.csv",
        "results/sample_flow.csv",
        "results/cleaning_log.csv",
        "docs/analysis_plan.md",
    ],
    "week3": [
        "data/raw/manifest.json",
        "data/processed/panel.csv",
        "data/processed/test_predictions.csv",
        "results/frozen_config.json",
        "results/test_run_lock.json",
        "results/test_metrics.csv",
        "results/test_confusion.csv",
        "results/test_posthoc.csv",
        "results/test_paired_differences.csv",
        "results/test_subgroups.csv",
        "results/test_robustness.csv",
        "results/test_ablation.csv",
        "results/test_permutation_importance.csv",
        "results/lr_standardised_coefficients.csv",
        "results/model_selection.csv",
        "results/cv_model_comparison.csv",
        "results/cv_paired_differences.csv",
        "results/label_base_rate_overall.csv",
        "results/label_base_rate_by_year.csv",
        "results/sample_flow.csv",
        "results/reference_check.csv",
        "docs/ml_plan.md",
    ],
}

# Figures reused in the report (copied to figures/reused/ by make_figures.py; listed here only so the manifest records
# their provenance too).
REUSED_FIGURES = {
    "week1": ["figures/fig_profile_missing_heatmap.png", "figures/fig_profile_distributions.png"],
    "week2": ["figures/fig_h2_boxplot_by_income.png", "figures/fig_h6_decoupling_heatmap.png",
              "figures/fig_h4_slopes_by_income.png"],
    "week3": ["figures/fig_label_split_timeline.png", "figures/fig_test_precision_recall.png",
              "figures/fig_importance_coefficients.png"],
}


def committed_bytes(repo_dir, rel: str, commit: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo_dir), "show", f"{commit}:{rel}"], capture_output=True, check=True).stdout


def main() -> int:
    INPUTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for week, rels in FILES.items():
        repo_dir = REF / week
        commit = git_head(repo_dir)
        for rel in rels:
            dst = INPUTS / week / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            # copy the committed blob (not the working tree, whose line endings depend on the local git settings)
            dst.write_bytes(committed_bytes(repo_dir, rel, commit))
            rows.append({"week": week, "source_repo": REPOS[week]["url"], "commit": commit, "source_path": rel,
                         "copy_path": dst.relative_to(ROOT).as_posix(), "sha256": sha256_of(dst),
                         "bytes": dst.stat().st_size, "kind": "input"})
    for week, rels in REUSED_FIGURES.items():
        repo_dir = REF / week
        commit = git_head(repo_dir)
        for rel in rels:
            blob = committed_bytes(repo_dir, rel, commit)
            rows.append({"week": week, "source_repo": REPOS[week]["url"], "commit": commit, "source_path": rel,
                         "copy_path": f"figures/reused/{week}_{Path(rel).name}",
                         "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob), "kind": "reused figure"})
    with open(INPUTS / "manifest.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"copied {sum(r['kind'] == 'input' for r in rows)} input files; manifest has {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
