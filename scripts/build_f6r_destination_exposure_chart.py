#!/usr/bin/env python3
"""Build the F6R importer exposure / adjustment chart from derived CSVs."""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
F6R5 = ROOT / "data/derived/hormuz_f6r_5_replacement_demand_response.csv"
OUT_CSV = ROOT / "figures/fig-f6r-crude-importer-adjustment-data.csv"
OUT_SVG = ROOT / "figures/fig-f6r-crude-importer-adjustment.svg"


ORDER = ["China", "India", "Japan", "South Korea", "Europe and Mediterranean", "United States"]
COLORS = {
    "replacement_supply_base": "#2f6f73",
    "inventory_draw_base": "#b5832d",
    "demand_destruction_base": "#8f4f6f",
    "residual_or_other_base": "#c8c8c8",
}
LABELS = {
    "replacement_supply_base": "replacement supply",
    "inventory_draw_base": "inventory draw",
    "demand_destruction_base": "demand reduction",
    "residual_or_other_base": "unresolved / other",
}


def parse_exposure_mb_d(text: str) -> float:
    token = text.split(" mb/d", 1)[0].split()[-1]
    return float(token)


def load_rows() -> list[dict[str, str]]:
    with F6R5.open(newline="") as f:
        rows = list(csv.DictReader(f))
    crude = [
        r
        for r in rows
        if r["unit_or_band"] == "mb/d flow-equivalent"
        and r["product_or_channel"]
        in {
            "crude oil and condensate",
            "crude oil and refined products",
            "crude oil and petroleum liquids",
        }
        and r["importer_or_region"] in ORDER
    ]
    by_name = {r["importer_or_region"]: r for r in crude}
    output = []
    for name in ORDER:
        r = by_name[name]
        exposure = parse_exposure_mb_d(r["shock_exposure"])
        repl = float(r["replacement_supply_base"])
        inv = float(r["inventory_draw_base"])
        demand = float(r["demand_destruction_base"])
        residual = max(0.0, exposure - repl - inv - demand)
        output.append(
            {
                "importer_or_region": name,
                "exposure_mb_d": f"{exposure:.3f}",
                "replacement_supply_base": f"{repl:.3f}",
                "inventory_draw_base": f"{inv:.3f}",
                "demand_destruction_base": f"{demand:.3f}",
                "residual_or_other_base": f"{residual:.3f}",
                "confidence": r["confidence"],
                "source_urls": r["source_urls"],
                "caveats": r["caveats"],
            }
        )
    return output


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "importer_or_region",
        "exposure_mb_d",
        "replacement_supply_base",
        "inventory_draw_base",
        "demand_destruction_base",
        "residual_or_other_base",
        "confidence",
        "source_urls",
        "caveats",
    ]
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_svg(rows: list[dict[str, str]]) -> None:
    width = 1180
    height = 740
    margin_left = 210
    chart_top = 138
    row_h = 66
    bar_h = 26
    chart_w = 820
    max_x = 5.0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#202020}.title{font-size:28px;font-weight:700}.sub{font-size:15px;fill:#4a4a4a}.label{font-size:15px}.small{font-size:12px;fill:#555}.axis{font-size:12px;fill:#555}.note{font-size:11px;fill:#666}</style>',
        '<text x="54" y="52" class="title">How major importers cushion Hormuz crude exposure</text>',
        '<text x="54" y="80" class="sub">Base-case flow-equivalent adjustment for direct crude/product exposure, mb/d. Values are scenario estimates, not cargo accounting.</text>',
    ]

    legend_x = 54
    legend_y = 110
    for key in ["replacement_supply_base", "inventory_draw_base", "demand_destruction_base", "residual_or_other_base"]:
        parts.append(f'<rect x="{legend_x}" y="{legend_y - 12}" width="16" height="16" fill="{COLORS[key]}"/>')
        parts.append(f'<text x="{legend_x + 22}" y="{legend_y + 1}" class="small">{escape(LABELS[key])}</text>')
        legend_x += 170

    axis_y = chart_top + len(rows) * row_h + 18
    for tick in range(0, 6):
        x = margin_left + tick / max_x * chart_w
        parts.append(f'<line x1="{x:.1f}" y1="{chart_top - 18}" x2="{x:.1f}" y2="{axis_y - 20}" stroke="#e7e7e7"/>')
        parts.append(f'<text x="{x:.1f}" y="{axis_y}" text-anchor="middle" class="axis">{tick}</text>')
    parts.append(f'<text x="{margin_left + chart_w / 2}" y="{axis_y + 25}" text-anchor="middle" class="axis">mb/d</text>')

    for i, r in enumerate(rows):
        y = chart_top + i * row_h
        name = r["importer_or_region"]
        exposure = float(r["exposure_mb_d"])
        parts.append(f'<text x="{margin_left - 14}" y="{y + 20}" text-anchor="end" class="label">{escape(name)}</text>')
        parts.append(f'<text x="{margin_left - 14}" y="{y + 39}" text-anchor="end" class="small">{exposure:.2f} mb/d exposed</text>')
        x0 = margin_left
        for key in ["replacement_supply_base", "inventory_draw_base", "demand_destruction_base", "residual_or_other_base"]:
            val = float(r[key])
            w = val / max_x * chart_w
            if w > 0:
                parts.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{COLORS[key]}"/>')
                if w > 34:
                    parts.append(
                        f'<text x="{x0 + w / 2:.1f}" y="{y + 18}" text-anchor="middle" class="small" fill="#202020">{val:.2g}</text>'
                    )
            x0 += w
        x_exposure = margin_left + exposure / max_x * chart_w
        parts.append(f'<line x1="{x_exposure:.1f}" y1="{y - 5}" x2="{x_exposure:.1f}" y2="{y + bar_h + 5}" stroke="#111" stroke-width="2"/>')
    parts.append('<text x="54" y="650" class="note">Black tick marks show the direct 2024 route-exposure baseline for each importer/region. Stacked colors show base-case adjustment channels from the F6R.5 matrix.</text>')
    parts.append('<text x="54" y="670" class="note">Source: F6R importer exposure and replacement/demand-response matrices; EIA/Vortexa, METI, Government of India, EU Commission, S49 reserve tables; calculations by author. Accessed 2026-07-06.</text>')
    parts.append('<text x="54" y="690" class="note">Caveat: replacement, inventory, and demand buckets are inferred scenario allocations; do not sum with LNG, LPG, fertilizer, sulfur, or aluminium rows.</text>')
    parts.append("</svg>")
    OUT_SVG.write_text("\n".join(parts) + "\n")


def main() -> None:
    rows = load_rows()
    write_csv(rows)
    write_svg(rows)
    print(f"wrote {OUT_CSV.relative_to(ROOT)} and {OUT_SVG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
