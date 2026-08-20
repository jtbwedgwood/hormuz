#!/usr/bin/env python3
"""Build the public Strait of Hormuz daily tracker from IMF PortWatch data."""

from __future__ import annotations

import argparse
import csv
from collections import deque
from datetime import date, datetime, timedelta
from math import sqrt
from pathlib import Path
from statistics import mean, stdev


DEFAULT_INPUT = Path("data/external/portwatch/hormuz_daily_chokepoint.csv")
DEFAULT_OUTPUT = Path("data/derived/hormuz_2y7_public_daily_tracker.csv")
DEFAULT_FIGURE = Path("figures/fig-2y7-public-hormuz-daily-transits.svg")
DEFAULT_FIGURE_DATA = Path("figures/fig-2y7-public-hormuz-daily-transits.csv")
DEFAULT_SCENARIO_BASELINE = Path("data/derived/hormuz_m8q_2_current_traffic_scenario.csv")
BASELINE_START = date(2019, 1, 1)
BASELINE_END = date(2024, 12, 31)
SHOCK_DATE = date(2026, 2, 28)
CURRENT_REGIME_START = date(2026, 7, 8)
SCENARIO_HORIZONS = (
    date(2026, 7, 31),
    date(2026, 9, 30),
    date(2026, 12, 31),
    date(2027, 3, 31),
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def rolling_mean(values: list[int], window: int) -> list[float]:
    output: list[float] = []
    buf: deque[int] = deque()
    for value in values:
        buf.append(value)
        if len(buf) > window:
            buf.popleft()
        output.append(mean(buf))
    return output


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def build_tracker(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, float]]:
    rows = sorted(rows, key=lambda row: row["date"])
    baseline = [row for row in rows if BASELINE_START <= parse_date(row["date"]) <= BASELINE_END]
    baseline_total = mean(int(row["n_total"]) for row in baseline)
    baseline_tanker = mean(int(row["n_tanker"]) for row in baseline)
    total_7d = rolling_mean([int(row["n_total"]) for row in rows], 7)
    tanker_7d = rolling_mean([int(row["n_tanker"]) for row in rows], 7)

    output: list[dict[str, object]] = []
    for row, total_roll, tanker_roll in zip(rows, total_7d, tanker_7d):
        n_total = int(row["n_total"])
        n_tanker = int(row["n_tanker"])
        output.append(
            {
                "date": row["date"],
                "n_total": n_total,
                "n_tanker": n_tanker,
                "n_container": int(row["n_container"]),
                "n_dry_bulk": int(row["n_dry_bulk"]),
                "n_general_cargo": int(row["n_general_cargo"]),
                "n_roro": int(row["n_roro"]),
                "n_cargo": int(row["n_cargo"]),
                "capacity_tanker_metric_tons": int(row["capacity_tanker"]),
                "capacity_total_metric_tons": int(row["capacity"]),
                "n_total_7d_avg": round(total_roll, 2),
                "n_tanker_7d_avg": round(tanker_roll, 2),
                "pct_baseline_total": round(100 * n_total / baseline_total, 1),
                "pct_baseline_tanker": round(100 * n_tanker / baseline_tanker, 1),
                "source": "IMF PortWatch Daily_Chokepoints_Data chokepoint6",
                "confidence": "high_for_chokepoint_calls_low_for_cargo_contents",
                "known_unknown_note": (
                    "Known: daily transit calls by broad vessel class. "
                    "Unknown: vessel identity, direction, AIS-dark movements, and actual cargo onboard."
                ),
            }
        )
    metrics = {"baseline_total": baseline_total, "baseline_tanker": baseline_tanker}
    return output, metrics


def build_scenario_baseline(
    rows: list[dict[str, object]], metrics: dict[str, float]
) -> list[dict[str, object]]:
    """Hold the latest low-traffic regime constant for scenario bookkeeping.

    The uncertainty interval is an approximate 95% interval for the regime mean
    (Student-t critical value 2.131 for the initial 16-day window). It captures
    daily sampling variation, not source revisions, AIS gaps, or cargo uncertainty.
    """
    latest = parse_date(str(rows[-1]["date"]))
    regime = [row for row in rows if CURRENT_REGIME_START <= parse_date(str(row["date"])) <= latest]
    if len(regime) < 7:
        raise ValueError("current traffic regime needs at least 7 observations")

    scenario_rows: list[dict[str, object]] = []
    for metric, baseline_key in (("n_total", "baseline_total"), ("n_tanker", "baseline_tanker")):
        values = [float(row[metric]) for row in regime]
        central = mean(values)
        sample_sd = stdev(values)
        # 1.96 is a reasonable large-sample fallback after the initial 16-day window.
        critical_value = 2.131 if len(values) == 16 else 1.96
        margin = critical_value * sample_sd / sqrt(len(values))
        low = max(0.0, central - margin)
        high = central + margin
        baseline = metrics[baseline_key]
        for horizon in SCENARIO_HORIZONS:
            # Once a horizon is observed it belongs in history, not in the
            # forward scenario.  This also removes the superseded July nowcast.
            if horizon <= latest:
                continue
            projection_days = (horizon - latest).days
            scenario_rows.append(
                {
                    "scenario_id": "constant_current_portwatch_traffic",
                    "metric": f"{metric}_calls_per_day",
                    "data_as_of": latest.isoformat(),
                    "current_window_start": CURRENT_REGIME_START.isoformat(),
                    "current_window_end": latest.isoformat(),
                    "current_window_days": len(regime),
                    "current_mean_calls_per_day": round(central, 3),
                    "current_sample_sd_calls_per_day": round(sample_sd, 3),
                    "mean_sampling_low": round(low, 3),
                    "mean_sampling_high": round(high, 3),
                    "2019_2024_baseline_calls_per_day": round(baseline, 3),
                    "current_pct_of_baseline": round(100 * central / baseline, 1),
                    "projection_start": (latest + timedelta(days=1)).isoformat(),
                    "scenario_horizon": horizon.isoformat(),
                    "horizon_role": "future_closure_scenario",
                    "projection_days_after_data_as_of": projection_days,
                    "projected_calls_central": round(central * projection_days, 1),
                    "projected_calls_sampling_low": round(low * projection_days, 1),
                    "projected_calls_sampling_high": round(high * projection_days, 1),
                    "history_treatment": "observed PortWatch history retained through data_as_of, including June relaxation",
                    "assumption": "hold the July 8-through-latest revised mean daily call rate constant after data_as_of",
                    "uncertainty_note": "sampling interval only; excludes revisions, AIS-dark traffic, direction, vessel mix, and cargo onboard",
                    "oil_mapping_note": "vessel calls are not loaded oil volume and must not be converted mechanically to mb/d",
                    "source": "IMF PortWatch Daily_Chokepoints_Data chokepoint6; project calculation",
                }
            )
    return scenario_rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sx(day: date, min_day: date, max_day: date, left: int, width: int) -> float:
    span = (max_day - min_day).days
    return left + width * ((day - min_day).days / span)


def sy(value: float, max_value: float, top: int, height: int) -> float:
    return top + height - height * (value / max_value)


def points(rows: list[dict[str, object]], column: str, max_value: float, min_day: date, max_day: date) -> str:
    left, top, width, height = 72, 72, 1000, 500
    coords = []
    for row in rows:
        day = parse_date(str(row["date"]))
        coords.append(f"{sx(day, min_day, max_day, left, width):.1f},{sy(float(row[column]), max_value, top, height):.1f}")
    return " ".join(coords)


def write_svg(rows: list[dict[str, object]], metrics: dict[str, float], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    min_day = parse_date(str(rows[0]["date"]))
    max_day = parse_date(str(rows[-1]["date"]))
    max_value = max(max(float(row["n_total_7d_avg"]) for row in rows), metrics["baseline_total"]) * 1.08
    left, top, width, height = 72, 72, 1000, 500
    baseline_y = sy(metrics["baseline_total"], max_value, top, height)
    shock_x = sx(SHOCK_DATE, min_day, max_day, left, width)
    latest = rows[-1]

    year_ticks = []
    for year in range(min_day.year, max_day.year + 1):
        tick_day = date(year, 1, 1)
        if min_day <= tick_day <= max_day:
            x = sx(tick_day, min_day, max_day, left, width)
            year_ticks.append(
                f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + height}" stroke="#e5e7eb" stroke-width="1"/>'
                f'<text x="{x:.1f}" y="{top + height + 32}" font-size="16" text-anchor="middle" fill="#374151">{year}</text>'
            )

    y_ticks = []
    for value in [0, 30, 60, 90, 120, 150]:
        if value <= max_value:
            y = sy(value, max_value, top, height)
            y_ticks.append(
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + width}" y2="{y:.1f}" stroke="#eef2f7" stroke-width="1"/>'
                f'<text x="{left - 14}" y="{y + 5:.1f}" font-size="15" text-anchor="end" fill="#374151">{value}</text>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">
  <rect width="1200" height="760" fill="#ffffff"/>
  <text x="72" y="38" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#111827">Daily Strait of Hormuz Transits</text>
  <text x="72" y="62" font-family="Arial, sans-serif" font-size="16" fill="#4b5563">Public IMF PortWatch chokepoint calls, 7-day average; latest observation {latest["date"]}</text>
  <g font-family="Arial, sans-serif">
    {''.join(y_ticks)}
    {''.join(year_ticks)}
    <line x1="{left}" y1="{top}" x2="{left}" y2="{top + height}" stroke="#111827" stroke-width="1.5"/>
    <line x1="{left}" y1="{top + height}" x2="{left + width}" y2="{top + height}" stroke="#111827" stroke-width="1.5"/>
    <line x1="{left}" y1="{baseline_y:.1f}" x2="{left + width}" y2="{baseline_y:.1f}" stroke="#6b7280" stroke-width="2" stroke-dasharray="7 7"/>
    <text x="{left + width - 4}" y="{baseline_y - 8:.1f}" font-size="15" text-anchor="end" fill="#4b5563">2019-2024 average: {metrics["baseline_total"]:.1f}/day</text>
    <line x1="{shock_x:.1f}" y1="{top}" x2="{shock_x:.1f}" y2="{top + height}" stroke="#991b1b" stroke-width="2" stroke-dasharray="5 6"/>
    <text x="{shock_x + 8:.1f}" y="{top + 22}" font-size="15" fill="#991b1b">2026-02-28 shock onset</text>
    <polyline points="{points(rows, "n_total_7d_avg", max_value, min_day, max_day)}" fill="none" stroke="#0f766e" stroke-width="3.5"/>
    <polyline points="{points(rows, "n_tanker_7d_avg", max_value, min_day, max_day)}" fill="none" stroke="#b45309" stroke-width="3"/>
    <rect x="786" y="98" width="286" height="78" fill="#ffffff" stroke="#d1d5db"/>
    <line x1="806" y1="124" x2="850" y2="124" stroke="#0f766e" stroke-width="4"/>
    <text x="862" y="129" font-size="16" fill="#111827">Total transits, 7-day avg</text>
    <line x1="806" y1="154" x2="850" y2="154" stroke="#b45309" stroke-width="4"/>
    <text x="862" y="159" font-size="16" fill="#111827">Tanker transits, 7-day avg</text>
    <text x="72" y="636" font-size="14" fill="#6b7280">Source: IMF PortWatch Daily_Chokepoints_Data, chokepoint6; calculations by project. Caveats: see figures/README.md.</text>
  </g>
</svg>
'''
    path.write_text(svg)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    parser.add_argument("--figure-data", type=Path, default=DEFAULT_FIGURE_DATA)
    parser.add_argument("--scenario-baseline", type=Path, default=DEFAULT_SCENARIO_BASELINE)
    args = parser.parse_args()

    tracker_rows, metrics = build_tracker(load_rows(args.input))
    scenario_rows = build_scenario_baseline(tracker_rows, metrics)
    write_csv(tracker_rows, args.output)
    write_csv(tracker_rows, args.figure_data)
    write_csv(scenario_rows, args.scenario_baseline)
    write_svg(tracker_rows, metrics, args.figure)
    latest = tracker_rows[-1]
    print(f"wrote {len(tracker_rows)} tracker rows to {args.output}")
    print(f"wrote figure to {args.figure}")
    print(f"wrote {len(scenario_rows)} scenario rows to {args.scenario_baseline}")
    print(f"latest {latest['date']}: total={latest['n_total']} tanker={latest['n_tanker']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
