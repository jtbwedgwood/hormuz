#!/usr/bin/env python3
"""Build the cumulative March-July 2026 global oil accounting figure."""

from __future__ import annotations

import csv
from calendar import monthrange
from math import pi
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
OUT_DATA = ROOT / "data/derived/hormuz_m8q_4_cumulative_global_oil_accounting.csv"
OUT_FIG_DATA = ROOT / "figures/fig-m8q-cumulative-global-oil-accounting-data.csv"
OUT_SVG = ROOT / "figures/fig-m8q-cumulative-global-oil-accounting.svg"

FROZEN_VINTAGE = "2026-02-10"
LATEST_VINTAGE = "2026-07-07"
MONTHS = ["2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]

COLORS = {
    "stock_draw": "#b45309",
    "foregone_build": "#e6a33a",
    "demand": "#087f75",
    "ink": "#172033",
    "muted": "#5d687a",
    "line": "#d8dee8",
    "panel": "#ffffff",
    "bg": "#f6f7f9",
}


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="") as handle:
        return list(csv.DictReader(handle))


def find_value(
    rows: list[dict[str, str]], vintage: str, month: str, metric: str
) -> tuple[float, str, str]:
    matches = [
        row
        for row in rows
        if row["source_family"] == "EIA_STEO"
        and row["publication_vintage"] == vintage
        and row["observation_month"] == month
        and row["metric"] == metric
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {vintage=} {month=} {metric=}, got {len(matches)}")
    row = matches[0]
    return float(row["value"]), row["status"], row["citation"]


def build_monthly(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for month in MONTHS:
        year, month_number = map(int, month.split("-"))
        days = monthrange(year, month_number)[1]
        pre_supply, _, pre_citation = find_value(rows, FROZEN_VINTAGE, month, "global_liquids_supply")
        pre_demand, _, _ = find_value(rows, FROZEN_VINTAGE, month, "global_liquids_consumption")
        latest_supply, status, latest_citation = find_value(rows, LATEST_VINTAGE, month, "global_liquids_supply")
        latest_demand, demand_status, _ = find_value(rows, LATEST_VINTAGE, month, "global_liquids_consumption")
        if demand_status != status:
            raise ValueError(f"supply/demand status mismatch for {month}")

        pre_balance = pre_supply - pre_demand
        latest_balance = latest_supply - latest_demand
        supply_shortfall = (pre_supply - latest_supply) * days
        demand_reduction = (pre_demand - latest_demand) * days
        foregone_build = pre_balance * days
        actual_draw = -latest_balance * days
        accounted = demand_reduction + foregone_build + actual_draw
        residual = supply_shortfall - accounted
        if abs(residual) > 0.01:
            raise ValueError(f"accounting does not close for {month}: {residual}")
        if min(supply_shortfall, demand_reduction, foregone_build, actual_draw) < 0:
            raise ValueError(f"unexpected negative accounting component for {month}")

        output.append(
            {
                "observation_month": month,
                "days": str(days),
                "latest_status": status,
                "frozen_vintage": FROZEN_VINTAGE,
                "latest_vintage": LATEST_VINTAGE,
                "frozen_supply_mb_d": f"{pre_supply:.6f}",
                "latest_supply_mb_d": f"{latest_supply:.6f}",
                "frozen_demand_mb_d": f"{pre_demand:.6f}",
                "latest_demand_mb_d": f"{latest_demand:.6f}",
                "frozen_implied_build_mb_d": f"{pre_balance:.6f}",
                "latest_implied_balance_mb_d": f"{latest_balance:.6f}",
                "cumulative_supply_shortfall_million_bbl": f"{supply_shortfall:.3f}",
                "cumulative_lower_consumption_million_bbl": f"{demand_reduction:.3f}",
                "cumulative_foregone_expected_build_million_bbl": f"{foregone_build:.3f}",
                "cumulative_actual_implied_draw_million_bbl": f"{actual_draw:.3f}",
                "arithmetic_residual_million_bbl": f"{residual:.6f}",
                "source_urls": f"{pre_citation}|{latest_citation}",
                "interpretation": (
                    "EIA petroleum and other liquid fuels; arithmetic comparison of the frozen February STEO "
                    "with the July STEO vintage. This is a global balance revision, not a causal estimate that "
                    "every difference was caused by Hormuz."
                ),
            }
        )
    return output


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def total(rows: list[dict[str, str]], field: str) -> float:
    return sum(float(row[field]) for row in rows)


def fmt_million(value: float) -> str:
    return f"{value:,.0f}m bbl"


def write_svg(rows: list[dict[str, str]]) -> None:
    supply = total(rows, "cumulative_supply_shortfall_million_bbl")
    demand = total(rows, "cumulative_lower_consumption_million_bbl")
    foregone = total(rows, "cumulative_foregone_expected_build_million_bbl")
    draw = total(rows, "cumulative_actual_implied_draw_million_bbl")
    components = [
        ("Implied inventory draw", draw, COLORS["stock_draw"]),
        ("Expected stock build did not occur", foregone, COLORS["foregone_build"]),
        ("Lower consumption", demand, COLORS["demand"]),
    ]
    if abs(supply - sum(value for _, value, _ in components)) > 0.1:
        raise ValueError("cumulative accounting does not close")

    width, height = 1440, 760
    cx, cy, radius = 350, 355, 142
    circumference = 2 * pi * radius
    previous_pct = 0.0
    arcs: list[str] = []
    legend: list[str] = []
    for index, (label, value, color) in enumerate(components):
        pct = 100 * value / supply
        arc_length = circumference * pct / 100
        offset = circumference * previous_pct / 100
        arcs.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{color}" stroke-width="54" stroke-dasharray="{arc_length:.4f} {circumference-arc_length:.4f}" '
            f'stroke-dashoffset="{-offset:.4f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        y = 225 + index * 118
        legend.extend(
            [
                f'<rect x="690" y="{y-20}" width="24" height="24" rx="3" fill="{color}"/>',
                f'<text x="730" y="{y}" class="label">{escape(label)}</text>',
                f'<text x="730" y="{y+34}" class="value">{fmt_million(value)} · {pct:.1f}%</text>',
            ]
        )
        previous_pct += pct

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="{COLORS['bg']}"/>
  <rect x="24" y="24" width="1392" height="712" rx="10" fill="{COLORS['panel']}" stroke="{COLORS['line']}"/>
  <style>
    text{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:{COLORS['ink']}}}
    .title{{font-size:34px;font-weight:760}} .subtitle{{font-size:18px;font-weight:540;fill:{COLORS['muted']}}}
    .label{{font-size:19px;font-weight:720}} .value{{font-size:24px;font-weight:760}}
    .centerBig{{font-size:37px;font-weight:800}} .centerSmall{{font-size:15px;font-weight:650;fill:{COLORS['muted']}}}
    .note{{font-size:14px;font-weight:520;fill:{COLORS['muted']}}}
  </style>
  <text x="72" y="80" class="title">How the global oil balance absorbed 1.72 billion fewer barrels of supply</text>
  <text x="72" y="114" class="subtitle">Cumulative 1 March–31 July 2026 versus EIA’s frozen February forecast</text>
  {''.join(arcs)}
  <circle cx="{cx}" cy="{cy}" r="104" fill="#ffffff"/>
  <text x="{cx}" y="{cy-4}" text-anchor="middle" class="centerBig">{supply/1000:.2f} bn</text>
  <text x="{cx}" y="{cy+26}" text-anchor="middle" class="centerSmall">barrels of lower supply</text>
  {''.join(legend)}
  <line x1="72" y1="608" x2="1368" y2="608" stroke="{COLORS['line']}"/>
  <text x="72" y="642" class="note">Accounting through 31 Jul 2026 · Mar–Jun preliminary estimates · Jul forecast completed 1 Jul · EIA July STEO released 7 Jul</text>
  <text x="72" y="672" class="note">Identity: lower supply = lower consumption + canceled expected stock build + implied stock draw. Values use petroleum and other liquids.</text>
  <text x="72" y="702" class="note">This is a forecast-vintage global balance comparison, not proof that every revision was caused by Hormuz. Source: EIA STEO Feb and Jul 2026; calculations by project.</text>
  <metadata>Generated by scripts/build_m8q_4_cumulative_oil_accounting.py from data/derived/hormuz_m8q_1_monthly_oil_balance.csv.</metadata>
</svg>
'''
    OUT_SVG.write_text(svg)


def main() -> None:
    rows = build_monthly(load_rows())
    write_csv(rows, OUT_DATA)
    write_csv(rows, OUT_FIG_DATA)
    write_svg(rows)
    supply = total(rows, "cumulative_supply_shortfall_million_bbl")
    print(f"wrote {OUT_DATA.relative_to(ROOT)} ({len(rows)} monthly rows)")
    print(f"wrote {OUT_FIG_DATA.relative_to(ROOT)} and {OUT_SVG.relative_to(ROOT)}")
    print(f"cumulative supply shortfall through 2026-07-31: {supply:.1f} million barrels")


if __name__ == "__main__":
    main()
