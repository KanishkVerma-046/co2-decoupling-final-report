"""Independent re-implementation of the Week 3 decoupling label, built only from the saved panel.

Rule (from Week 3's committed plan): for country c and window start year t,
  y = 1 if CO2pc(t+3) < CO2pc(t) and GDPpc(t+3) > GDPpc(t), else 0,
and a row is eligible only if CO2pc and GDPpc are strictly positive at t and at t+3.
Window start years 1993-2019. Split (from the plan): pool 1993-2013, purge gap 2014-2016 (unused by the model),
test 2017-2019.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

H = 3
POOL_END = 2013
TEST_YEARS = (2017, 2018, 2019)


def build_labels(panel: pd.DataFrame, first_t: int = 1993, last_t: int = 2019) -> pd.DataFrame:
    p = panel[["iso3", "year", "co2_pc", "gdp_pc", "income_group", "region", "population"]].copy()
    p["year"] = p["year"].astype(int)
    now = p.rename(columns={"co2_pc": "co2_t", "gdp_pc": "gdp_t"})
    fut = p[["iso3", "year", "co2_pc", "gdp_pc"]].copy()
    fut["year"] = fut["year"] - H
    fut = fut.rename(columns={"co2_pc": "co2_f", "gdp_pc": "gdp_f"})
    m = now.merge(fut, on=["iso3", "year"], how="left")
    m = m[(m["year"] >= first_t) & (m["year"] <= last_t)]
    ok = (m[["co2_t", "gdp_t", "co2_f", "gdp_f"]].notna().all(axis=1)
          & (m["co2_t"] > 0) & (m["gdp_t"] > 0) & (m["co2_f"] > 0) & (m["gdp_f"] > 0))
    m = m[ok].copy()
    m["y"] = ((m["co2_f"] < m["co2_t"]) & (m["gdp_f"] > m["gdp_t"])).astype(int)
    m["split"] = np.where(m["year"] <= POOL_END, "pool", np.where(m["year"].isin(TEST_YEARS), "test", "purge gap"))
    return m.rename(columns={"year": "t"}).reset_index(drop=True)
