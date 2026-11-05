"""Shared paths and small helpers for the Week 4 synthesis repository."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference"
INPUTS = ROOT / "data" / "inputs"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
REUSED = FIGURES / "reused"
REPORT = ROOT / "report"

REPOS = {
    "week1": {"name": "co2-economy-eda-proposal",
              "url": "https://github.com/KanishkVerma-046/co2-economy-eda-proposal",
              "title": "Week 1, Data Exploration and Visualization Strategy"},
    "week2": {"name": "co2-gdp-hypothesis-testing",
              "url": "https://github.com/KanishkVerma-046/co2-gdp-hypothesis-testing",
              "title": "Week 2, Statistical Analysis and Hypothesis Testing Framework"},
    "week3": {"name": "co2-decoupling-ml-pipeline",
              "url": "https://github.com/KanishkVerma-046/co2-decoupling-ml-pipeline",
              "title": "Week 3, Machine Learning Model Development and Evaluation Plan"},
}

INCOME_ORDER = ["Low income", "Lower middle income", "Upper middle income", "High income"]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head(repo_dir: Path) -> str:
    return subprocess.run(["git", "-C", str(repo_dir), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()


def git_date(repo_dir: Path) -> str:
    return subprocess.run(["git", "-C", str(repo_dir), "log", "-1", "--format=%cI"], capture_output=True, text=True,
                          check=True).stdout.strip()


def commits() -> dict[str, str]:
    """Commit hash of each reference clone (read from the clones; also recorded in data/inputs/manifest.csv)."""
    return {k: git_head(REF / k) for k in REPOS}
