"""Verify every candidate reference through the Crossref REST API (title, journal, year, volume, pages, DOI).

Writes results/reference_check.csv. A reference is VERIFIED only if Crossref returns a record for the DOI whose title
matches the expected title (normalised) and whose year matches. Anything else is DROPPED and is not cited in the report.
Run:  python src/check_references.py
"""
from __future__ import annotations

import re
import sys
import time

import pandas as pd
import requests

from common import RESULTS

# key, DOI, expected title (as I remember it), expected year, why it is cited
CANDIDATES = [
    ("GrossmanKrueger1995", "10.2307/2118443", "Economic Growth and the Environment", 1995, "Environmental Kuznets curve idea"),
    ("Stern2004", "10.1016/j.worlddev.2004.03.004", "The Rise and Fall of the Environmental Kuznets Curve", 2004, "Evidence for the Kuznets curve for carbon is weak"),
    ("Haberl2020", "10.1088/1748-9326/ab842a", "A systematic review of the evidence on decoupling of GDP, resource use and GHG emissions, part II: synthesizing the insights", 2020, "Decoupling is not a falling climate footprint"),
    ("LeQuere2019", "10.1038/s41558-019-0419-7", "Drivers of declining CO2 emissions in 18 developed economies", 2019, "Decoupling in rich countries"),
    ("Peters2011", "10.1073/pnas.1006388108", "Growth in emission transfers via international trade from 1990 to 2008", 2011, "Emissions embodied in trade"),
    ("DavisCaldeira2010", "10.1073/pnas.0906974107", "Consumption-based accounting of CO2 emissions", 2010, "Production vs consumption accounting"),
    ("Hubacek2021", "10.1016/j.adapen.2021.100074", "Evidence of decoupling consumption-based CO2 emissions from economic growth", 2021, "Consumption-based decoupling"),
    ("Robinson1950", "10.2307/2087176", "Ecological Correlations and the Behavior of Individuals", 1950, "Ecological fallacy"),
    ("Spearman1904", "10.2307/1412159", "The Proof and Measurement of Association between Two Things", 1904, "Rank correlation"),
    ("BenjaminiHochberg1995", "10.1111/j.2517-6161.1995.tb02031.x", "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing", 1995, "Multiple testing"),
    ("Efron1979", "10.1214/aos/1176344552", "Bootstrap Methods: Another Look at the Jackknife", 1979, "Bootstrap"),
    ("Wilson1927", "10.1080/01621459.1927.10502953", "Probable Inference, the Law of Succession, and Statistical Inference", 1927, "Interval for a proportion"),
    ("Shmueli2010", "10.1214/10-STS330", "To Explain or to Predict?", 2010, "Prediction is not explanation"),
    ("Breiman2001", "10.1023/A:1010933404324", "Random Forests", 2001, "Random forest"),
    ("Friedman2001", "10.1214/aos/1013203451", "Greedy function approximation: A gradient boosting machine", 2001, "Gradient boosting"),
    ("ZouHastie2005", "10.1111/j.1467-9868.2005.00503.x", "Regularization and Variable Selection Via the Elastic Net", 2005, "Elastic net"),
    ("SaitoRehmsmeier2015", "10.1371/journal.pone.0118432", "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets", 2015, "PR curves under imbalance"),
    ("ChiccoJurman2020", "10.1186/s12864-019-6413-7", "The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation", 2020, "MCC"),
    ("BergmeirBenitez2012", "10.1016/j.ins.2011.12.028", "On the use of cross-validation for time series predictor evaluation", 2012, "Time-aware validation"),
    ("KapoorNarayanan2023", "10.1016/j.patter.2023.100804", "Leakage and the reproducibility crisis in machine-learning-based science", 2023, "Leakage"),
    ("Wilkinson2016", "10.1038/sdata.2016.18", "The FAIR Guiding Principles for scientific data management and stewardship", 2016, "Data governance"),
    ("ClevelandMcGill1984", "10.1080/01621459.1984.10478080", "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods", 1984, "Which visual encodings are read accurately"),
    ("Wong2011", "10.1038/nmeth.1618", "Points of view: Color blindness", 2011, "Colour-blind-safe design"),
    ("Anscombe1973", "10.1080/00031305.1973.10478966", "Graphs in Statistical Analysis", 1973, "Always plot the data"),
    ("HarrowerBrewer2003", "10.1179/000870403235002042", "ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps", 2003, "Colour schemes"),
    ("Holm1979", "", "A simple sequentially rejective multiple test procedure", 1979, "Holm correction (Crossref has no record of the original)"),
]


def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)  # Crossref titles can carry markup such as <sub>2</sub>
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def first(x):
    return x[0] if isinstance(x, list) and x else ""


def main() -> int:
    rows = []
    sess = requests.Session()
    sess.headers["User-Agent"] = "co2-final-report-reference-check/1.0"
    for key, doi, title, year, why in CANDIDATES:
        row = {"key": key, "expected_doi": doi, "expected_title": title, "expected_year": year, "why_cited": why}
        if not doi:
            # try a title search for the original; drop if not found
            r = sess.get("https://api.crossref.org/works", params={"query.bibliographic": f"{title} Holm 1979 Scandinavian Journal of Statistics", "rows": 5}, timeout=30)
            hit = None
            if r.ok:
                for it in r.json()["message"]["items"]:
                    t = norm(first(it.get("title", [""])))
                    yr = (it.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0]
                    if t == norm(title) and yr == year:
                        hit = it
            row.update({"status": "VERIFIED" if hit else "DROPPED (no matching Crossref record)"})
            if hit:
                doi = hit["DOI"]
            rows.append(row)
            continue
        for attempt in range(3):
            try:
                r = sess.get(f"https://api.crossref.org/works/{doi}", timeout=30)
                break
            except requests.RequestException:
                time.sleep(2)
                r = None
        if r is None or not r.ok:
            row["status"] = f"DROPPED (Crossref HTTP {None if r is None else r.status_code})"
            rows.append(row)
            continue
        m = r.json()["message"]
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", first(m.get("title", [])))).strip()
        yr = (m.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0]
        authors = "; ".join(f"{a.get('family', '')}, {a.get('given', '')}".strip(", ") for a in m.get("author", []))
        ok_title = norm(t) == norm(title)
        ok_year = yr == year
        row.update({"crossref_doi": m.get("DOI"), "title": t, "authors": authors, "container": first(m.get("container-title", [])),
                    "year": yr, "volume": m.get("volume", ""), "issue": m.get("issue", ""), "pages": m.get("page", m.get("article-number", "")),
                    "title_match": ok_title, "year_match": ok_year,
                    "doi_match": (m.get("DOI", "").lower() == doi.lower()),
                    "status": "VERIFIED" if (ok_title and ok_year) else "DROPPED (title or year differs from Crossref)"})
        rows.append(row)
        time.sleep(0.3)
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "reference_check.csv", index=False, lineterminator="\n")
    print(df[["key", "status", "year", "container"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
