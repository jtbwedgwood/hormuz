#!/usr/bin/env python3
"""Build the cumulative current-traffic oil-supply scenario chart."""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_m8q_5_current_traffic_oil_scenarios.csv"
OUT_DATA = ROOT / "figures/fig-m8q-current-traffic-cumulative-scenarios-data.csv"
OUT_SVG = ROOT / "figures/fig-m8q-current-traffic-cumulative-scenarios.svg"

HORIZONS = ["2026-09-30", "2026-12-31", "2027-03-31"]
COMPONENTS = [
    ("foregone_counterfactual_stock_build", "Expected stock build did not occur", "#e6a33a"),
    ("government_and_obligated_emergency_release", "Emergency stock release", "#c2410c"),
    ("commercial_and_other_stock_draw", "Commercial / other stock draw", "#7c3aed"),
    ("demand_reduction", "Lower consumption", "#087f75"),
    ("residual_unallocated_adjustment", "Unallocated residual", "#94a3b8"),
]


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="") as handle:
        return list(csv.DictReader(handle))


def find_summary(
    rows: list[dict[str, str]], scenario: str, horizon: str, frame: str, metric: str
) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if row["record_type"] == "horizon_summary"
        and row["scenario_case"] == scenario
        and row["horizon_date"] == horizon
        and row["accounting_frame"] == frame
        and row["metric"] == metric
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one summary row for {scenario=} {horizon=} {frame=} {metric=}; got {len(matches)}"
        )
    return matches[0]


def build_figure_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for horizon in HORIZONS:
        low_loss = float(
            find_summary(rows, "high_supply", horizon, "physical_supply_headline", "net_global_supply_loss")[
                "cumulative_million_bbl"
            ]
        )
        base_loss = float(
            find_summary(rows, "base", horizon, "physical_supply_headline", "net_global_supply_loss")[
                "cumulative_million_bbl"
            ]
        )
        high_loss = float(
            find_summary(rows, "low_supply", horizon, "physical_supply_headline", "net_global_supply_loss")[
                "cumulative_million_bbl"
            ]
        )
        components = {
            metric: float(
                find_summary(rows, "base", horizon, "market_clearing_summary", metric)[
                    "cumulative_million_bbl"
                ]
            )
            for metric, _, _ in COMPONENTS
        }
        if abs(sum(components.values()) - base_loss) > 0.001:
            raise ValueError(f"base accounting bridge does not close for {horizon}")
        if not low_loss < base_loss < high_loss:
            raise ValueError(f"unexpected scenario ordering for {horizon}")

        source_row = find_summary(
            rows, "base", horizon, "physical_supply_headline", "net_global_supply_loss"
        )
        output.append(
            {
                "horizon_date": horizon,
                "cumulative_start_date": "2026-03-01",
                "resilient_low_loss_million_bbl": f"{low_loss:.3f}",
                "base_loss_million_bbl": f"{base_loss:.3f}",
                "stress_high_loss_million_bbl": f"{high_loss:.3f}",
                **{f"base_{metric}_million_bbl": f"{value:.3f}" for metric, value in components.items()},
                "historical_oil_data_through": "2026-06-30",
                "july_oil_status": "forecast/nowcast through 2026-07-31",
                "traffic_observed_through": "2026-07-23",
                "future_traffic_rule": "hold 2026-07-08 through 2026-07-23 average regime after July",
                "source_urls": source_row["source_url"],
                "interpretation": (
                    "Cumulative provisional oil-only scenario; the physical loss range and base market-clearing "
                    "components are two views of the same balance and must not be added together."
                ),
            }
        )
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    with OUT_DATA.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def num(row: dict[str, str], field: str) -> float:
    return float(row[field])


def write_svg(rows: list[dict[str, str]]) -> None:
    width, height = 1440, 900
    plot_x, plot_width = 174, 1135
    scale_max = 5500.0
    ys = [286, 475, 664]
    bar_height = 62
    horizon_labels = ["30 Sep 2026", "31 Dec 2026", "31 Mar 2027"]

    axis: list[str] = []
    for tick in range(0, 5501, 1000):
        x = plot_x + plot_width * tick / scale_max
        axis.append(f'<line x1="{x:.1f}" y1="208" x2="{x:.1f}" y2="715" class="grid"/>')
        axis.append(f'<text x="{x:.1f}" y="748" text-anchor="middle" class="tick">{tick/1000:.0f}</text>')

    marks: list[str] = []
    for row, y, horizon_label in zip(rows, ys, horizon_labels):
        marks.append(f'<text x="72" y="{y+7}" class="horizon">{escape(horizon_label)}</text>')
        cursor = plot_x
        for metric, _, color in COMPONENTS:
            value = num(row, f"base_{metric}_million_bbl")
            segment_width = plot_width * value / scale_max
            marks.append(
                f'<rect x="{cursor:.2f}" y="{y-bar_height/2:.1f}" width="{segment_width:.2f}" '
                f'height="{bar_height}" fill="{color}"/>'
            )
            cursor += segment_width

        low = num(row, "resilient_low_loss_million_bbl")
        base = num(row, "base_loss_million_bbl")
        high = num(row, "stress_high_loss_million_bbl")
        low_x = plot_x + plot_width * low / scale_max
        base_x = plot_x + plot_width * base / scale_max
        high_x = plot_x + plot_width * high / scale_max
        whisker_y = y + 53
        marks.extend(
            [
                f'<line x1="{low_x:.2f}" y1="{whisker_y}" x2="{high_x:.2f}" y2="{whisker_y}" class="range"/>',
                f'<line x1="{low_x:.2f}" y1="{whisker_y-8}" x2="{low_x:.2f}" y2="{whisker_y+8}" class="range"/>',
                f'<line x1="{high_x:.2f}" y1="{whisker_y-8}" x2="{high_x:.2f}" y2="{whisker_y+8}" class="range"/>',
                f'<circle cx="{base_x:.2f}" cy="{whisker_y}" r="7" fill="#172033"/>',
                f'<text x="{base_x+12:.2f}" y="{whisker_y+6}" class="baseLabel">{base/1000:.2f} bn base</text>',
                f'<text x="{low_x:.2f}" y="{whisker_y+31}" text-anchor="middle" class="rangeLabel">{low/1000:.2f}</text>',
                f'<text x="{high_x:.2f}" y="{whisker_y+31}" text-anchor="middle" class="rangeLabel">{high/1000:.2f}</text>',
            ]
        )

    legend: list[str] = []
    x = 72
    for _, label, color in COMPONENTS:
        legend.append(f'<rect x="{x}" y="803" width="18" height="18" rx="2" fill="{color}"/>')
        legend.append(f'<text x="{x+26}" y="817" class="legend">{escape(label)}</text>')
        x += 26 + len(label) * 7.25 + 31

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#f6f7f9"/>
  <rect x="24" y="24" width="1392" height="852" rx="10" fill="#ffffff" stroke="#d8dee8"/>
  <style>
    text{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#172033}}
    .title{{font-size:34px;font-weight:760}} .subtitle{{font-size:18px;font-weight:540;fill:#5d687a}}
    .horizon{{font-size:16px;font-weight:720}} .tick{{font-size:14px;font-weight:600;fill:#64748b}}
    .grid{{stroke:#e2e8f0;stroke-width:1}} .range{{stroke:#172033;stroke-width:2}}
    .baseLabel{{font-size:15px;font-weight:760}} .rangeLabel{{font-size:12px;font-weight:650;fill:#64748b}}
    .legend{{font-size:13px;font-weight:620}} .note{{font-size:14px;font-weight:520;fill:#5d687a}}
  </style>
  <text x="72" y="80" class="title">If today’s low-traffic regime persists, the oil gap keeps compounding</text>
  <text x="72" y="114" class="subtitle">Cumulative net global supply loss from 1 Mar 2026 · billion barrels</text>
  <text x="72" y="151" class="note">Stacked bars show the provisional base-case market accounting; whiskers show resilient-to-stress physical supply cases.</text>
  <text x="72" y="177" class="note">History preserves June’s relaxation. Oil data: Mar–Jun preliminary; Jul forecast/nowcast. Traffic observed through 23 Jul; then held at the 8–23 Jul regime.</text>
  {''.join(axis)}
  {''.join(marks)}
  <text x="{plot_x + plot_width/2:.1f}" y="779" text-anchor="middle" class="tick">Cumulative billion barrels</text>
  {''.join(legend)}
  <text x="72" y="854" class="note">Oil only · no price forecast · residual preserves stock-data discrepancies, cargo timing, and unobserved adjustment. Sources: IEA, EIA, IMF PortWatch; project calculations.</text>
  <metadata>Generated by scripts/build_m8q_4_cumulative_scenario_chart.py from data/derived/hormuz_m8q_5_current_traffic_oil_scenarios.csv.</metadata>
</svg>
'''
    OUT_SVG.write_text(svg)


def main() -> None:
    rows = build_figure_rows(load_rows())
    write_csv(rows)
    write_svg(rows)
    print(f"wrote {OUT_DATA.relative_to(ROOT)} ({len(rows)} horizon rows)")
    print(f"wrote {OUT_SVG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
