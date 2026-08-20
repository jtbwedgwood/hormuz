#!/usr/bin/env python3
"""Build the mid-August U.S. SPR and commercial-petroleum stock ledger.

Positive changes mean a stock draw; negative changes mean a stock build.  The
cutoff is the 7 August 2026 week released by EIA on 12 August, the latest weekly
observation available at the project's 18 August research cutoff.
"""

from __future__ import annotations

import csv
import tempfile
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_a4d_5_us_weekly_stocks.csv"
CUTOFF = pd.Timestamp("2026-08-07")
START = pd.Timestamp("2026-02-27")
RECENT_START = pd.Timestamp("2026-06-26")
RELEASE_DATE = "2026-08-12"

SERIES = {
    "spr": (
        "https://www.eia.gov/dnav/pet/hist_xls/WCSSTUS1w.xls",
        "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1",
    ),
    "commercial": (
        "https://www.eia.gov/dnav/pet/hist_xls/WTESTUS1w.xls",
        "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1",
    ),
}

FIELDS = [
    "week_ending",
    "spr_million_bbl",
    "commercial_petroleum_ex_spr_million_bbl",
    "spr_signed_draw_since_2026_02_27_million_bbl",
    "commercial_signed_draw_since_2026_02_27_million_bbl",
    "spr_signed_draw_since_2026_06_26_million_bbl",
    "commercial_signed_draw_since_2026_06_26_million_bbl",
    "spr_average_draw_rate_since_2026_06_26_mb_per_day",
    "commercial_average_draw_rate_since_2026_06_26_mb_per_day",
    "source_release_date",
    "spr_source_url",
    "commercial_source_url",
    "sign_convention",
]


def read_series(download_url: str) -> pd.Series:
    with tempfile.NamedTemporaryFile(suffix=".xls") as handle:
        request = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            handle.write(response.read())
            handle.flush()
        frame = pd.read_excel(handle.name, sheet_name="Data 1", header=None)
    dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce", format="mixed")
    values = pd.to_numeric(frame.iloc[:, 1], errors="coerce") / 1000.0
    series = pd.Series(values.values, index=dates).dropna().sort_index()
    return series.loc[(series.index >= START) & (series.index <= CUTOFF)]


def fmt(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def main() -> None:
    spr = read_series(SERIES["spr"][0])
    commercial = read_series(SERIES["commercial"][0])
    assert spr.index.equals(commercial.index)
    assert spr.index[-1] == CUTOFF
    assert START in spr.index and RECENT_START in spr.index

    rows: list[dict[str, str]] = []
    for observation_date in spr.index:
        elapsed = (observation_date - RECENT_START).days
        spr_recent_draw = spr.loc[RECENT_START] - spr.loc[observation_date]
        commercial_recent_draw = commercial.loc[RECENT_START] - commercial.loc[observation_date]
        rows.append(
            {
                "week_ending": observation_date.date().isoformat(),
                "spr_million_bbl": fmt(spr.loc[observation_date]),
                "commercial_petroleum_ex_spr_million_bbl": fmt(commercial.loc[observation_date]),
                "spr_signed_draw_since_2026_02_27_million_bbl": fmt(
                    spr.loc[START] - spr.loc[observation_date]
                ),
                "commercial_signed_draw_since_2026_02_27_million_bbl": fmt(
                    commercial.loc[START] - commercial.loc[observation_date]
                ),
                "spr_signed_draw_since_2026_06_26_million_bbl": fmt(spr_recent_draw),
                "commercial_signed_draw_since_2026_06_26_million_bbl": fmt(
                    commercial_recent_draw
                ),
                "spr_average_draw_rate_since_2026_06_26_mb_per_day": (
                    fmt(spr_recent_draw / elapsed) if elapsed > 0 else ""
                ),
                "commercial_average_draw_rate_since_2026_06_26_mb_per_day": (
                    fmt(commercial_recent_draw / elapsed) if elapsed > 0 else ""
                ),
                "source_release_date": RELEASE_DATE,
                "spr_source_url": SERIES["spr"][1],
                "commercial_source_url": SERIES["commercial"][1],
                "sign_convention": "positive_is_draw_negative_is_build",
            }
        )

    latest = rows[-1]
    assert latest["spr_million_bbl"] == "298.694"
    assert latest["commercial_petroleum_ex_spr_million_bbl"] == "1236.468"
    assert latest["spr_signed_draw_since_2026_06_26_million_bbl"] == "26.961"
    assert latest["commercial_signed_draw_since_2026_06_26_million_bbl"] == "-34.898"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows through {CUTOFF.date()})")


if __name__ == "__main__":
    main()
