#!/usr/bin/env python3
"""Build the CCX supplier-side cushioning figure and source CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv"
OUT_CSV = ROOT / "figures/fig-ccx-supplier-side-cushioning-data.csv"
OUT_SVG = ROOT / "figures/fig-ccx-supplier-side-cushioning.svg"


STYLE = (
    "text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
    "fill:#172033;letter-spacing:0}"
    ".title{font-size:30px;font-weight:760}"
    ".subtitle{font-size:15px;font-weight:560;fill:#5d687a}"
    ".section{font-size:15px;font-weight:760;fill:#172033}"
    ".section_note{font-size:12px;font-weight:560;fill:#5d687a}"
    ".label{font-size:13px;font-weight:720;fill:#172033}"
    ".small{font-size:12px;font-weight:560;fill:#5d687a}"
    ".tiny{font-size:10.5px;font-weight:720;fill:#5d687a}"
    ".pct{font-size:10.5px;font-weight:760;fill:#ffffff}"
    ".axis{font-size:11px;font-weight:560;fill:#5d687a}"
    ".note{font-size:12px;font-weight:560;fill:#5d687a}"
    ".value{font-size:12px;font-weight:720;fill:#172033}"
)

COLORS = {
    "route": "#087f75",
    "route_soft": "#dff3ef",
    "removed": "#b42318",
    "removed_soft": "#fde7e5",
    "delayed": "#b56b12",
    "delayed_soft": "#fff0d6",
    "line": "#d8dee8",
    "ink": "#172033",
    "muted": "#5d687a",
    "panel": "#ffffff",
    "bg": "#f6f7f9",
}

ROUTE_ANCHORS = [
    {
        "country": "Saudi Arabia",
        "figure_label": "Saudi East-West",
        "product": "East-West crude pipeline",
        "commodity_group": "oil liquids",
        "value_text": "5-7 mb/d physical route",
        "mechanism": "bypass capacity",
        "evidence_class": "observed route capacity",
        "source_note": "EIA/Aramco/IEA via kmz.2; near-term spare capacity is tighter than nameplate.",
    },
    {
        "country": "UAE",
        "figure_label": "UAE ADCOP/Fujairah",
        "product": "ADCOP / Fujairah crude route",
        "commodity_group": "oil liquids",
        "value_text": "~0.7 mb/d extra room",
        "mechanism": "bypass capacity",
        "evidence_class": "observed route capacity",
        "source_note": "IEA/EIA/ADNOC via kmz.2; helps UAE crude, not LNG.",
    },
    {
        "country": "Iraq",
        "figure_label": "Iraq-Ceyhan",
        "product": "Kirkuk-Ceyhan northern route",
        "commodity_group": "oil liquids",
        "value_text": "~0.25-0.4 mb/d practical",
        "mechanism": "partial bypass",
        "evidence_class": "observed route capacity",
        "source_note": "EIA/Reuters via kmz.2; does not replace southern Iraqi exports.",
    },
    {
        "country": "Qatar / UAE",
        "figure_label": "Qatar/UAE LNG",
        "product": "LNG export route",
        "commodity_group": "LNG",
        "value_text": "0 practical bypass",
        "mechanism": "no bypass",
        "evidence_class": "observed route constraint",
        "source_note": "IEA/EIA via kmz.2; Qatari/UAE LNG must move by sea through Hormuz.",
    },
]

FIGURE_ROWS = [
    {
        "row_id": "saudi-crude-2026",
        "section": "Route cushion: oil liquids with alternate pipeline or port options",
        "section_note": "Bars show modeled base disrupted share of normal exposed flow; pale remainder is not disrupted in the base case.",
        "mechanism": "rerouted / partly preserved",
        "mechanism_group": "route optionality",
        "color_group": "route",
        "display_product": "crude + condensate",
    },
    {
        "row_id": "uae-crude-products-2026",
        "section": "Route cushion: oil liquids with alternate pipeline or port options",
        "section_note": "Bars show modeled base disrupted share of normal exposed flow; pale remainder is not disrupted in the base case.",
        "mechanism": "rerouted / partly preserved",
        "mechanism_group": "route optionality",
        "color_group": "route",
        "display_product": "crude/products",
    },
    {
        "row_id": "saudi-refined-products-2026",
        "section": "Route cushion: oil liquids with alternate pipeline or port options",
        "section_note": "Bars show modeled base disrupted share of normal exposed flow; pale remainder is not disrupted in the base case.",
        "mechanism": "delayed / rerouted",
        "mechanism_group": "route optionality",
        "color_group": "route",
        "display_product": "refined products",
    },
    {
        "row_id": "uae-refined-products-2026",
        "section": "Route cushion: oil liquids with alternate pipeline or port options",
        "section_note": "Bars show modeled base disrupted share of normal exposed flow; pale remainder is not disrupted in the base case.",
        "mechanism": "rerouted / partly preserved",
        "mechanism_group": "route optionality",
        "color_group": "route",
        "display_product": "refined products",
    },
    {
        "row_id": "qatar-lng-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "removed supply",
        "mechanism_group": "no practical bypass",
        "color_group": "removed",
        "display_product": "LNG",
    },
    {
        "row_id": "uae-lng-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "removed supply",
        "mechanism_group": "no practical bypass",
        "color_group": "removed",
        "display_product": "LNG",
    },
    {
        "row_id": "iraq-crude-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "shut-in / delayed",
        "mechanism_group": "severe route limit",
        "color_group": "removed",
        "display_product": "crude + condensate",
    },
    {
        "row_id": "kuwait-crude-products-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "shut-in / delayed",
        "mechanism_group": "severe route limit",
        "color_group": "removed",
        "display_product": "crude/products",
    },
    {
        "row_id": "qatar-refined-products-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "delayed / removed",
        "mechanism_group": "severe route limit",
        "color_group": "removed",
        "display_product": "LPG/naphtha/products",
    },
    {
        "row_id": "qatar-crude-condensate-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "delayed / removed",
        "mechanism_group": "severe route limit",
        "color_group": "removed",
        "display_product": "crude + condensate",
    },
    {
        "row_id": "iran-crude-condensate-2026",
        "section": "No-bypass or severe route limit: LNG and Gulf oil liquids",
        "section_note": "LNG is the clearest hard-stop case; Iraq/Kuwait/Qatar liquids lack Saudi/UAE-scale bypass.",
        "mechanism": "delayed / removed",
        "mechanism_group": "severe route limit",
        "color_group": "removed",
        "display_product": "crude + condensate",
    },
    {
        "row_id": "qatar-urea-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "delayed export availability",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "urea",
    },
    {
        "row_id": "saudi-urea-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "delayed export availability",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "urea",
    },
    {
        "row_id": "uae-sulphur-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "rerouted / delayed",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "sulphur",
    },
    {
        "row_id": "qatar-ammonia-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "delayed export availability",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "ammonia",
    },
    {
        "row_id": "qatar-sulphur-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "delayed export availability",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "sulphur",
    },
    {
        "row_id": "bahrain-aluminium-2026",
        "section": "Delayed export availability: fertilizer, sulphur, aluminium",
        "section_note": "Annualized non-energy rows are scenario estimates, not cargo-manifest observations.",
        "mechanism": "delayed export availability",
        "mechanism_group": "industrial delay",
        "color_group": "delayed",
        "display_product": "aluminium",
    },
]


def fmt_num(value: float) -> str:
    if value >= 10:
        return f"{value:.0f}"
    if value >= 1:
        return f"{value:.1f}"
    return f"{value:.2f}"


def confidence_short(confidence: str) -> str:
    return {
        "high": "high",
        "medium-high": "med-high",
        "medium": "med",
        "medium-low": "med-low",
        "low-medium": "low-med",
        "low": "low",
    }.get(confidence, confidence)


def mechanism_short(row: dict[str, str]) -> str:
    if row["color_group"] == "route":
        return "route cushion"
    if row["color_group"] == "removed":
        if row["mechanism"] == "removed supply":
            return "removed"
        return "shut-in/delay"
    return "industrial delay"


def load_input() -> dict[str, dict[str, str]]:
    with INPUT.open(newline="") as f:
        return {row["row_id"]: row for row in csv.DictReader(f)}


def commodity_group(product: str, unit: str) -> str:
    p = product.lower()
    if unit == "Bcf/d":
        return "LNG"
    if unit == "mb/d":
        return "oil liquids"
    if "aluminium" in p:
        return "aluminium"
    if "sulphur" in p:
        return "sulphur"
    return "fertilizer"


def build_rows() -> list[dict[str, str]]:
    raw = load_input()
    rows: list[dict[str, str]] = []
    for anchor in ROUTE_ANCHORS:
        rows.append(
            {
                "row_type": "route_anchor",
                "row_id": "",
                "section": "Observed route-capacity anchors",
                "country": anchor["country"],
                "product": anchor["product"],
                "commodity_group": anchor["commodity_group"],
                "baseline_volume": "",
                "baseline_unit": "",
                "base_disrupted_volume": "",
                "disruption_unit": "",
                "base_disrupted_share_of_baseline": "",
                "mechanism": anchor["mechanism"],
                "mechanism_group": anchor["mechanism"],
                "color_group": "removed" if anchor["mechanism"] == "no bypass" else "route",
                "evidence_class": anchor["evidence_class"],
                "confidence": "",
                "value_text": anchor["value_text"],
                "source_basis": anchor["source_note"],
                "method_note": "",
                "double_counting_note": "",
            }
        )

    for spec in FIGURE_ROWS:
        source = raw[spec["row_id"]]
        baseline = float(source["baseline_volume"])
        disrupted = float(source["base_disrupted_volume"])
        share = disrupted / baseline if baseline else 0.0
        rows.append(
            {
                "row_type": "disruption_row",
                "row_id": spec["row_id"],
                "section": spec["section"],
                "country": source["country"],
                "product": spec["display_product"],
                "commodity_group": commodity_group(source["product"], source["baseline_unit"]),
                "baseline_volume": f"{baseline:.6f}",
                "baseline_unit": source["baseline_unit"],
                "base_disrupted_volume": f"{disrupted:.6f}",
                "disruption_unit": source["disruption_unit"],
                "base_disrupted_share_of_baseline": f"{share:.6f}",
                "mechanism": spec["mechanism"],
                "mechanism_group": spec["mechanism_group"],
                "color_group": spec["color_group"],
                "evidence_class": "modeled disruption; mechanism inferred from route constraints",
                "confidence": source["confidence"],
                "value_text": f"{fmt_num(disrupted)} of {fmt_num(baseline)} {source['baseline_unit']}",
                "source_basis": source["source_basis"],
                "method_note": source["method_note"],
                "double_counting_note": source["double_counting_note"],
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    fields = [
        "row_type",
        "row_id",
        "section",
        "country",
        "product",
        "commodity_group",
        "baseline_volume",
        "baseline_unit",
        "base_disrupted_volume",
        "disruption_unit",
        "base_disrupted_share_of_baseline",
        "mechanism",
        "mechanism_group",
        "color_group",
        "evidence_class",
        "confidence",
        "value_text",
        "source_basis",
        "method_note",
        "double_counting_note",
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pill(parts: list[str], x: float, y: float, width: float, color: str, soft: str) -> None:
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="54" rx="8" fill="{soft}" stroke="{color}" stroke-opacity="0.28"/>')


def write_svg(rows: list[dict[str, str]]) -> None:
    width = 1440
    height = 1180
    left = 72
    label_x = 100
    bar_x = 430
    bar_w = 700
    value_x = 1152
    chart_top = 292
    row_h = 36
    bar_h = 16
    section_gap = 58

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{COLORS["bg"]}"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="8" fill="{COLORS["panel"]}" stroke="#dfe4ec"/>',
        f"<style>{STYLE}</style>",
        '<text x="72" y="66" class="title">How Gulf suppliers cushion a Hormuz export shock</text>',
        '<text x="72" y="92" class="subtitle">Pipeline optionality protects some crude flows; LNG and industrial inputs have much thinner route cushions.</text>',
    ]

    parts.append('<text x="72" y="132" class="section">Observed route-capacity anchors</text>')
    anchor_y = 152
    anchor_w = 302
    for idx, anchor in enumerate(ROUTE_ANCHORS):
        x = left + idx * (anchor_w + 20)
        color_key = "removed" if anchor["mechanism"] == "no bypass" else "route"
        pill(parts, x, anchor_y, anchor_w, COLORS[color_key], COLORS[f"{color_key}_soft"])
        parts.append(f'<text x="{x + 16}" y="{anchor_y + 20}" class="tiny">{escape(anchor["evidence_class"].upper())}</text>')
        parts.append(f'<text x="{x + 16}" y="{anchor_y + 39}" class="label">{escape(anchor["figure_label"])}</text>')
        parts.append(f'<text x="{x + anchor_w - 16}" y="{anchor_y + 39}" text-anchor="end" class="value">{escape(anchor["value_text"])}</text>')

    legend_y = 244
    legend = [
        ("route", "base disrupted where route cushion exists"),
        ("removed", "base removed / shut-in or delayed"),
        ("delayed", "annualized industrial export delay"),
    ]
    x = left
    for key, label in legend:
        parts.append(f'<rect x="{x}" y="{legend_y - 12}" width="16" height="16" rx="3" fill="{COLORS[key]}"/>')
        parts.append(f'<rect x="{x + 20}" y="{legend_y - 12}" width="16" height="16" rx="3" fill="{COLORS[key + "_soft"]}" stroke="{COLORS[key]}" stroke-opacity="0.18"/>')
        parts.append(f'<text x="{x + 44}" y="{legend_y + 1}" class="small">{escape(label)}</text>')
        x += 335
    grid_bottom = 1012
    for pct in [0, 25, 50, 75, 100]:
        gx = bar_x + bar_w * pct / 100
        parts.append(f'<line x1="{gx:.1f}" y1="268" x2="{gx:.1f}" y2="{grid_bottom}" stroke="#e8edf3"/>')

    disruption_rows = [r for r in rows if r["row_type"] == "disruption_row"]
    y = chart_top
    current_section = ""
    for r in disruption_rows:
        if r["section"] != current_section:
            if current_section:
                y += section_gap - row_h
            current_section = r["section"]
            section_note = next(spec["section_note"] for spec in FIGURE_ROWS if spec["section"] == current_section)
            parts.append(f'<text x="{left}" y="{y - 18}" class="section">{escape(current_section)}</text>')
            parts.append(f'<text x="{left}" y="{y}" class="section_note">{escape(section_note)}</text>')
            y += 22

        share = min(1.0, float(r["base_disrupted_share_of_baseline"]))
        color_key = r["color_group"]
        color = COLORS[color_key]
        soft = COLORS[f"{color_key}_soft"]
        bar_y = y + 5
        w = share * bar_w

        label = f'{r["country"]} - {r["product"]}'
        parts.append(f'<text x="{label_x}" y="{y + 18}" class="label">{escape(label)}</text>')
        parts.append(f'<text x="{bar_x - 18}" y="{y + 18}" text-anchor="end" class="small">{escape(r["commodity_group"])}</text>')
        parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{soft}"/>')
        parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{color}"/>')
        if w > 38:
            parts.append(
                f'<text x="{bar_x + min(w - 8, w / 2 + 18):.1f}" y="{y + 18}" text-anchor="end" class="pct">{share:.0%}</text>'
            )
        parts.append(f'<text x="{value_x}" y="{y + 13}" class="value">{escape(r["value_text"])}</text>')
        brief = f'{mechanism_short(r)}; {confidence_short(r["confidence"])} conf.'
        parts.append(f'<text x="{value_x}" y="{y + 29}" class="small">{escape(brief)}</text>')
        y += row_h

    axis_y = y + 4
    for pct in [0, 25, 50, 75, 100]:
        x = bar_x + bar_w * pct / 100
        parts.append(f'<text x="{x:.1f}" y="{axis_y + 10}" text-anchor="middle" class="axis">{pct}%</text>')
    parts.append(f'<text x="{bar_x + bar_w / 2}" y="{axis_y + 34}" text-anchor="middle" class="axis">base disrupted share of normal exposed flow</text>')

    note_y = height - 86
    parts.append(f'<rect x="72" y="{note_y - 18}" width="1296" height="1" fill="{COLORS["line"]}"/>')
    parts.append(
        f'<text x="72" y="{note_y + 12}" class="note">Sources: EIA/Vortexa, IEA, EIA, WITS/UN Comtrade, USGS, QAFCO, and project KMZ estimates.</text>'
    )
    parts.append(
        f'<text x="72" y="{note_y + 34}" class="note">Route callouts are observed infrastructure/capacity anchors; bars are modeled base-case disruptions; shut-in/delay labels are inferred from route constraints and traffic severity.</text>'
    )
    parts.append(
        '<metadata>Generated by scripts/build_ccx_supplier_side_cushioning.py from data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv. Units differ across rows; chart compares percentage of each row baseline, not additive volumes.</metadata>'
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
