#!/usr/bin/env python3
"""Build the supplier-side cushioning figure and its evidence table."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OIL_INPUT = ROOT / "figures/fig-kmz-oil-hormuz-baseline-sankey-data.csv"
LNG_INPUT = ROOT / "figures/fig-kmz-lng-hormuz-baseline-sankey-data.csv"
OUT_CSV = ROOT / "figures/fig-ccx-supplier-side-cushioning-data.csv"
OUT_SVG = ROOT / "figures/fig-ccx-supplier-side-cushioning.svg"

OIL_ORDER = [
    "Saudi Arabia",
    "United Arab Emirates",
    "Iraq",
    "Kuwait",
    "Qatar",
    "Iran",
    "Other",
]
LNG_ORDER = ["Qatar", "United Arab Emirates"]

# Recoverable volumes are incremental shares of the Hormuz-routed baseline that
# can use an operational non-Hormuz route during a sustained effective closure.
ESTIMATES = {
    ("oil", "Saudi Arabia"): {
        "recoverable": 4.0,
        "confidence": "medium",
        "method": "Midpoint of IEA's 3-5 mb/d early-2026 spare East-West range; capped below the 5 mb/d export portion of the 7 mb/d system.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz|https://www.aramco.com/en/news-media/news/2026/aramco-announces-first-quarter-2026-results",
    },
    ("oil", "United Arab Emirates"): {
        "recoverable": 0.7,
        "confidence": "medium-high",
        "method": "IEA estimate of incremental room in ADCOP above roughly 1.1 mb/d already routed to Fujairah.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz|https://www.eia.gov/todayinenergy/detail.php?id=67804",
    },
    ("oil", "Iraq"): {
        "recoverable": 0.3,
        "confidence": "medium",
        "method": "Rounded near-term northern export capacity via Turkiye; southern Basra exports have no operational connection to it.",
        "sources": "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock|https://www.eia.gov/international/analysis/countries/IRQ/",
    },
    ("oil", "Iran"): {
        "recoverable": 0.05,
        "confidence": "low",
        "method": "Rounded observed average from two reported Jask cargoes over roughly three months; far below its nameplate capacity.",
        "sources": "https://www.eia.gov/international/content/analysis/special_topics/World_Oil_Transit_Chokepoints/|https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz",
    },
    ("oil", "Kuwait"): {
        "recoverable": 0.0,
        "confidence": "high",
        "method": "No operational non-Hormuz export route; storage only delays production and refinery cuts.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz",
    },
    ("oil", "Qatar"): {
        "recoverable": 0.0,
        "confidence": "high",
        "method": "No operational non-Hormuz route for Qatar's crude, condensate, LPG, or refined products.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz",
    },
    ("oil", "Other"): {
        "recoverable": 0.0,
        "confidence": "low",
        "method": "Residual Sankey origin is not country-resolved; no separately evidenced operational bypass is assigned.",
        "sources": "https://www.eia.gov/todayinenergy/detail.php?id=65504",
    },
    ("LNG", "Qatar"): {
        "recoverable": 0.0,
        "confidence": "high",
        "method": "No route can deliver Qatar LNG from Ras Laffan to the global market without transiting Hormuz.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz|https://www.iea.org/reports/gas-market-report-q3-2026/executive-summary",
    },
    ("LNG", "United Arab Emirates"): {
        "recoverable": 0.0,
        "confidence": "high",
        "method": "No route can deliver UAE LNG from Das Island to the global market without transiting Hormuz.",
        "sources": "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz|https://adnocgas.ae/en/Our-Operations/LNG",
    },
}

COLORS = {
    "oil": "#087f75",
    "oil_soft": "#dff3ef",
    "lng": "#315c99",
    "lng_soft": "#e3ebf7",
    "ink": "#172033",
    "muted": "#5d687a",
    "line": "#d8dee8",
    "grid": "#e8edf3",
    "panel": "#ffffff",
    "bg": "#f6f7f9",
}

STYLE = (
    "text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
    "fill:#172033;letter-spacing:0}"
    ".title{font-size:32px;font-weight:760}"
    ".section{font-size:16px;font-weight:760;text-transform:uppercase}"
    ".label{font-size:15px;font-weight:720}"
    ".small{font-size:13px;font-weight:560;fill:#5d687a}"
    ".axis{font-size:11px;font-weight:560;fill:#5d687a}"
    ".note{font-size:13px;font-weight:560;fill:#5d687a}"
    ".value{font-size:14px;font-weight:720}"
)


def load_origin_totals(path: Path) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["flow_side"] == "origin_to_hormuz":
                totals[row["source"]] += float(row["value"])
    return dict(totals)


def build_rows() -> list[dict[str, str | float]]:
    oil = load_origin_totals(OIL_INPUT)
    lng = load_origin_totals(LNG_INPUT)
    rows: list[dict[str, str | float]] = []
    for section, order, totals, unit in (
        ("oil", OIL_ORDER, oil, "mb/d"),
        ("LNG", LNG_ORDER, lng, "Bcf/d"),
    ):
        for supplier in order:
            baseline = totals[supplier]
            estimate = ESTIMATES[(section, supplier)]
            recoverable = float(estimate["recoverable"])
            if recoverable > baseline:
                raise ValueError(f"recoverable volume exceeds baseline for {supplier}")
            rows.append(
                {
                    "section": section,
                    "supplier": supplier,
                    "baseline_volume": f"{baseline:.6f}",
                    "recoverable_volume": f"{recoverable:.6f}",
                    "unrecoverable_volume": f"{baseline - recoverable:.6f}",
                    "recoverable_share": f"{recoverable / baseline if baseline else 0.0:.6f}",
                    "unit": unit,
                    "confidence": estimate["confidence"],
                    "method": estimate["method"],
                    "sources": estimate["sources"],
                }
            )
    return rows


def display_number(value: float) -> str:
    if value == 0:
        return "0"
    if value >= 1:
        return f"{value:.1f}"
    return f"{value:.2f}"


def write_csv(rows: list[dict[str, str | float]]) -> None:
    fields = [
        "section",
        "supplier",
        "baseline_volume",
        "recoverable_volume",
        "unrecoverable_volume",
        "recoverable_share",
        "unit",
        "confidence",
        "method",
        "sources",
    ]
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_svg(rows: list[dict[str, str | float]]) -> None:
    width, height = 1440, 820
    left, label_x = 72, 96
    bar_x, bar_w, bar_h = 360, 690, 20
    value_x = 1080
    chart_top, row_h = 190, 44
    oil_rows = [row for row in rows if row["section"] == "oil"]
    lng_rows = [row for row in rows if row["section"] == "LNG"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{COLORS["bg"]}"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="8" fill="{COLORS["panel"]}" stroke="#dfe4ec"/>',
        "<defs>",
        '<pattern id="oilHatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">',
        f'<line x1="0" y1="0" x2="0" y2="8" stroke="{COLORS["oil"]}" stroke-opacity="0.30" stroke-width="2"/>',
        "</pattern>",
        '<pattern id="lngHatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">',
        f'<line x1="0" y1="0" x2="0" y2="8" stroke="{COLORS["lng"]}" stroke-opacity="0.30" stroke-width="2"/>',
        "</pattern>",
        "</defs>",
        f"<style>{STYLE}</style>",
        '<text x="72" y="70" class="title">How Gulf suppliers cushion a Hormuz export shock</text>',
        f'<rect x="72" y="106" width="30" height="14" rx="2" fill="{COLORS["oil"]}"/>',
        '<text x="112" y="118" class="small">recoverable</text>',
        f'<rect x="222" y="106" width="30" height="14" rx="2" fill="{COLORS["oil_soft"]}"/>',
        '<rect x="222" y="106" width="30" height="14" rx="2" fill="url(#oilHatch)"/>',
        '<text x="262" y="118" class="small">unrecoverable</text>',
    ]

    grid_top, grid_bottom = 154, 672
    for pct in (0, 25, 50, 75, 100):
        x = bar_x + bar_w * pct / 100
        parts.append(f'<line x1="{x:.1f}" y1="{grid_top}" x2="{x:.1f}" y2="{grid_bottom}" stroke="{COLORS["grid"]}"/>')

    def add_section(section_rows: list[dict[str, str | float]], y: float, section: str) -> float:
        color_key = "oil" if section == "oil" else "lng"
        soft_key = f"{color_key}_soft"
        section_label = "OIL" if section == "oil" else "LNG"
        parts.append(f'<text x="{left}" y="{y}" class="section" fill="{COLORS[color_key]}">{section_label}</text>')
        y += 20
        for row in section_rows:
            share = float(row["recoverable_share"])
            recoverable_w = bar_w * share
            bar_y = y + 6
            supplier = str(row["supplier"])
            if supplier == "United Arab Emirates":
                supplier = "UAE"
            parts.append(f'<text x="{label_x}" y="{y + 22}" class="label">{escape(supplier)}</text>')
            parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{COLORS[soft_key]}"/>')
            parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="url(#{color_key}Hatch)"/>')
            if recoverable_w:
                parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{recoverable_w:.1f}" height="{bar_h}" rx="3" fill="{COLORS[color_key]}"/>')
            value = f'~{display_number(float(row["recoverable_volume"]))} of {display_number(float(row["baseline_volume"]))} {row["unit"]}'
            parts.append(f'<text x="{value_x}" y="{y + 22}" class="value">{escape(value)}</text>')
            y += row_h
        return y

    y = add_section(oil_rows, chart_top, "oil")
    y += 22
    y = add_section(lng_rows, y, "LNG")

    axis_y = 694
    for pct in (0, 25, 50, 75, 100):
        x = bar_x + bar_w * pct / 100
        parts.append(f'<text x="{x:.1f}" y="{axis_y}" text-anchor="middle" class="axis">{pct}%</text>')
    parts.append(f'<text x="{bar_x + bar_w / 2}" y="{axis_y + 24}" text-anchor="middle" class="axis">share of normal Hormuz-routed exports</text>')
    parts.append(f'<rect x="72" y="756" width="1296" height="1" fill="{COLORS["line"]}"/>')
    parts.append('<text x="72" y="785" class="note">Sources: EIA/Vortexa, IEA, Aramco and ADNOC</text>')
    parts.append(
        '<metadata>Generated by scripts/build_ccx_supplier_side_cushioning.py from the two EIA/Vortexa baseline Sankey data files; methodology and uncertainty are documented in docs/hormuz-supplier-side-cushioning.md.</metadata>'
    )
    parts.append("</svg>")
    OUT_SVG.write_text("\n".join(parts) + "\n")


def main() -> None:
    rows = build_rows()
    write_csv(rows)
    write_svg(rows)
    print(f"wrote {OUT_CSV.relative_to(ROOT)} and {OUT_SVG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
