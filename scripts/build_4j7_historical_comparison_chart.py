#!/usr/bin/env python3
"""Build the 4J7 historical shock comparison figure from ranking score tables."""

from __future__ import annotations

import csv
import math
import re
from collections import defaultdict
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
CASE_SCORES = ROOT / "data/derived/hormuz_4j7_4_case_ranking_scores.csv"
PRODUCT_SCORES = ROOT / "data/derived/hormuz_4j7_4_hormuz_product_ranking_scores.csv"
OUT_CSV = ROOT / "figures/fig-4j7-historical-shock-comparison-data.csv"
OUT_SVG = ROOT / "figures/fig-4j7-historical-shock-comparison.svg"

DIMENSION_COLUMNS = [
    ("realized_or_exposed_disruption_share", "flow", "Flow exposed/lost"),
    ("disruption_intensity", "intensity", "Intensity"),
    ("route_substitution_constraint", "route", "Route"),
    ("spare_capacity_buffer", "spare", "Spare"),
    ("inventory_cover", "stocks", "Stocks"),
    ("strategic_response_offset", "policy", "Policy"),
    ("real_price_response", "price", "Price"),
    ("shipping_insurance_channel", "shipping", "Freight"),
]

CASE_GROUP_LABELS = {
    "current_hormuz": "Current Hormuz exposure scenarios",
    "primary_oil_shock": "Historical oil supply and allocation shocks",
    "control_oil_shock": "Historical oil supply and allocation shocks",
    "control_oil_products_logistics_shock": "Historical oil supply and allocation shocks",
    "route_shipping": "Route/logistics analogues",
}

CASE_GROUP_ORDER = {
    "current_hormuz": 0,
    "primary_oil_shock": 1,
    "control_oil_shock": 1,
    "control_oil_products_logistics_shock": 1,
    "route_shipping": 2,
}

CASE_GROUP_COLORS = {
    "current_hormuz": "#8b2f2f",
    "primary_oil_shock": "#2f6f73",
    "control_oil_shock": "#2f6f73",
    "control_oil_products_logistics_shock": "#2f6f73",
    "route_shipping": "#7d5a1f",
}

CONFIDENCE_MARKERS = {
    "high": "solid",
    "medium_high": "solid",
    "medium": "solid",
    "low": "hollow",
    "speculative": "hollow",
}

TEXT_STYLE = (
    "text{font-family:Arial,Helvetica,sans-serif;fill:#202020}"
    ".title{font-size:30px;font-weight:700}"
    ".subtitle{font-size:16px;fill:#4a4a4a}"
    ".section{font-size:14px;font-weight:700;fill:#4a4a4a;text-transform:uppercase}"
    ".label{font-size:13px}"
    ".small{font-size:11px;fill:#555}"
    ".axis{font-size:11px;fill:#555}"
    ".note{font-size:11px;fill:#626262}"
    ".tiny{font-size:10px;fill:#666}"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def score_value(value: str) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text.upper() == "NA":
        return None
    return float(text)


def first_number(text: str) -> str:
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text or "")
    return match.group(0) if match else ""


def summarize_rows(rows: list[dict[str, str]], panel: str) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["case_id"]].append(row)

    output: list[dict[str, str]] = []
    for case_id, case_rows in grouped.items():
        first = case_rows[0]
        dim_scores: dict[str, str] = {}
        dim_caveats: list[str] = []
        disrupted_share = ""
        peak_price = ""
        duration_days = ""
        source_urls: list[str] = []
        caveats: list[str] = []
        confidences: set[str] = set()
        score_statuses: set[str] = set()

        for row in case_rows:
            dim = row["dimension"]
            dim_scores[dim] = row["score_0_4"].strip()
            if dim == "realized_or_exposed_disruption_share":
                disrupted_share = first_number(row["raw_input_values"])
            if dim == "real_price_response":
                peak_price = first_number(row["raw_input_values"])
            if dim == "duration_recovery_shape":
                duration_days = first_number(row["raw_input_values"])
            if row.get("caveat"):
                dim_caveats.append(f"{dim}: {row['caveat']}")
                caveats.append(row["caveat"])
            if row.get("source_urls_or_local_paths"):
                source_urls.append(row["source_urls_or_local_paths"])
            if row.get("confidence"):
                confidences.add(row["confidence"])
            if row.get("score_status"):
                score_statuses.add(row["score_status"])

        row_out: dict[str, str] = {
            "panel": panel,
            "case_id": case_id,
            "case_name": first["case_name"],
            "case_group": first["case_group"],
            "case_group_label": CASE_GROUP_LABELS.get(first["case_group"], first["case_group"]),
            "commodity_scope": first["commodity_scope"],
            "normalized_score_0_100": f"{float(first['normalized_score_0_100']):.2f}",
            "rank_within_source_table": first["rank_within_table"],
            "score_status": "|".join(sorted(score_statuses)),
            "confidence": first["confidence"],
            "all_dimension_confidences": "|".join(sorted(confidences)),
            "display_label": display_label(first, panel),
            "disrupted_or_exposed_share_pct_label": disrupted_share,
            "duration_days_label": duration_days,
            "peak_real_price_change_pct_label": peak_price,
            "source_score_table": str(
                CASE_SCORES.relative_to(ROOT) if panel == "comparison_case" else PRODUCT_SCORES.relative_to(ROOT)
            ),
            "source_urls_or_local_paths": " || ".join(dict.fromkeys(source_urls)),
            "caveats": " || ".join(dict.fromkeys(caveats)),
            "dimension_caveats": " || ".join(dict.fromkeys(dim_caveats)),
        }
        for dim, short, _label in DIMENSION_COLUMNS:
            raw = dim_scores.get(dim, "")
            row_out[f"{short}_score_0_4"] = raw
            parsed = score_value(raw)
            row_out[f"{short}_score_0_100"] = "" if parsed is None else f"{25 * parsed:.1f}"
        output.append(row_out)
    return output


def display_label(row: dict[str, str], panel: str) -> str:
    if panel == "hormuz_product_channel":
        return row["commodity_scope"]
    if row["case_group"] == "current_hormuz":
        return f"Hormuz: {row['commodity_scope']}"
    return row["case_name"]


def write_figure_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "panel",
        "case_id",
        "case_name",
        "case_group",
        "case_group_label",
        "commodity_scope",
        "display_label",
        "normalized_score_0_100",
        "rank_within_source_table",
        "score_status",
        "confidence",
        "all_dimension_confidences",
        "disrupted_or_exposed_share_pct_label",
        "duration_days_label",
        "peak_real_price_change_pct_label",
    ]
    for _dim, short, _label in DIMENSION_COLUMNS:
        fields.extend([f"{short}_score_0_4", f"{short}_score_0_100"])
    fields.extend(["source_score_table", "source_urls_or_local_paths", "caveats", "dimension_caveats"])
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt_score(value: str) -> str:
    score = float(value)
    return f"{score:.0f}" if score.is_integer() else f"{score:.1f}"


def svg_text(x: float, y: float, text: str, cls: str = "label", anchor: str | None = None) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}"{anchor_attr}>{escape(text)}</text>'


def svg_wrapped_text(
    x: float,
    y: float,
    text: str,
    width_chars: int,
    cls: str = "note",
    line_height: int = 14,
) -> list[str]:
    lines = wrap(text, width=width_chars, break_long_words=False)
    return [svg_text(x, y + i * line_height, line, cls=cls) for i, line in enumerate(lines)]


def chart_label(text: str, limit: int = 43) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def dimension_rect(
    x: float,
    y: float,
    width: float,
    height: float,
    score: str,
    color: str,
    low_confidence: bool,
) -> list[str]:
    parsed = score_value(score)
    if parsed is None:
        return [
            f'<line x1="{x + 3:.1f}" y1="{y + height / 2:.1f}" x2="{x + width - 3:.1f}" y2="{y + height / 2:.1f}" stroke="#b7b7b7" stroke-width="1"/>',
            svg_text(x + width / 2, y + height - 2, "n/a", cls="tiny", anchor="middle"),
        ]
    fill_w = width * parsed / 4
    opacity = "0.55" if low_confidence else "0.78"
    return [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="2" fill="#eeeeee"/>',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{fill_w:.1f}" height="{height:.1f}" rx="2" fill="{color}" opacity="{opacity}"/>',
        svg_text(x + width / 2, y + height + 11, f"{parsed:g}", cls="tiny", anchor="middle"),
    ]


def write_svg(comparison_rows: list[dict[str, str]], product_rows: list[dict[str, str]]) -> None:
    width = 1600
    height = 1080
    left = 58
    label_w = 300
    score_x = left + label_w + 20
    score_w = 320
    dim_x = score_x + score_w + 44
    dim_w = 42
    dim_gap = 8
    product_x = 1190
    product_score_w = 260
    top = 164
    row_h = 34
    bar_h = 13
    max_score = 100

    rows = sorted(
        comparison_rows,
        key=lambda r: (
            CASE_GROUP_ORDER.get(r["case_group"], 9),
            -float(r["normalized_score_0_100"]),
            r["display_label"],
        ),
    )
    product_rows = sorted(product_rows, key=lambda r: -float(r["normalized_score_0_100"]))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f"<style>{TEXT_STYLE}</style>",
        '<defs><pattern id="lowConfidenceHatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#ffffff" stroke-width="1.2"/></pattern></defs>',
        svg_text(left, 46, "How Hormuz differs from earlier oil and shipping shocks", cls="title"),
        svg_text(
            left,
            76,
            "Rubric severity score from 4J7.4 ranking tables, 0-100. Scores combine exposure, persistence, buffers, route constraint, price response, and freight channels.",
            cls="subtitle",
        ),
        svg_text(
            left,
            101,
            "Route closures, sanctions rerouting, infrastructure outages, and current Hormuz exposure scenarios are separated below; the score is not a barrel-equivalent loss.",
            cls="subtitle",
        ),
    ]

    legend_y = 126
    legend_items = [
        ("#8b2f2f", "current exposure/scenario"),
        ("#2f6f73", "oil supply/allocation shock"),
        ("#7d5a1f", "route/logistics analogue"),
    ]
    lx = left
    for color, label in legend_items:
        parts.append(f'<rect x="{lx:.1f}" y="{legend_y - 11:.1f}" width="16" height="12" fill="{color}" opacity="0.78"/>')
        parts.append(svg_text(lx + 22, legend_y, label, cls="small"))
        lx += 205
    parts.append(f'<circle cx="{lx + 8:.1f}" cy="{legend_y - 5:.1f}" r="6" fill="#ffffff" stroke="#333" stroke-width="1.7"/>')
    parts.append(svg_text(lx + 22, legend_y, "hollow marker = low confidence/proxy", cls="small"))

    parts.append(svg_text(left, top - 26, "Historical comparison rows", cls="section"))
    parts.append(svg_text(score_x, top - 26, "Normalized severity score", cls="section"))
    for i, (_dim, _short, label) in enumerate(DIMENSION_COLUMNS):
        x = dim_x + i * (dim_w + dim_gap)
        for j, line in enumerate(wrap(label, width=9)):
            parts.append(svg_text(x + dim_w / 2, top - 44 + j * 11, line, cls="tiny", anchor="middle"))

    axis_y = top - 10
    for tick in [0, 25, 50, 75, 100]:
        x = score_x + score_w * tick / max_score
        parts.append(f'<line x1="{x:.1f}" y1="{axis_y:.1f}" x2="{x:.1f}" y2="{top + len(rows) * row_h + 40:.1f}" stroke="#eeeeee"/>')
        parts.append(svg_text(x, axis_y - 5, str(tick), cls="axis", anchor="middle"))

    y = top
    previous_group = None
    section_seen: set[str] = set()
    for row in rows:
        group = row["case_group"]
        group_label = row["case_group_label"]
        if group_label != previous_group:
            if group_label in section_seen:
                y += 10
            if previous_group is not None:
                y += 14
            parts.append(svg_text(left, y + 2, group_label, cls="section"))
            section_seen.add(group_label)
            previous_group = group_label
            y += 22

        score = float(row["normalized_score_0_100"])
        color = CASE_GROUP_COLORS.get(group, "#555555")
        low_conf = CONFIDENCE_MARKERS.get(row["confidence"], "solid") == "hollow"
        bar_w = score_w * score / max_score
        parts.append(f'<line x1="{score_x:.1f}" y1="{y + 7:.1f}" x2="{score_x + score_w:.1f}" y2="{y + 7:.1f}" stroke="#e5e5e5" stroke-width="10" stroke-linecap="round"/>')
        parts.append(f'<line x1="{score_x:.1f}" y1="{y + 7:.1f}" x2="{score_x + bar_w:.1f}" y2="{y + 7:.1f}" stroke="{color}" stroke-width="10" stroke-linecap="round" opacity="0.82"/>')
        marker_fill = "#ffffff" if low_conf else color
        parts.append(f'<circle cx="{score_x + bar_w:.1f}" cy="{y + 7:.1f}" r="7" fill="{marker_fill}" stroke="{color}" stroke-width="2"/>')
        if low_conf:
            parts.append(f'<circle cx="{score_x + bar_w:.1f}" cy="{y + 7:.1f}" r="5" fill="url(#lowConfidenceHatch)" opacity="0.9"/>')

        label = chart_label(row["display_label"])
        if row["confidence"] in {"low", "speculative"}:
            label = f"{label} (low conf.)"
        parts.append(svg_text(left, y + 10, label, cls="label"))
        sub = f"rank {row['rank_within_source_table']} | {row['commodity_scope']} | conf: {row['confidence']}"
        parts.append(svg_text(left, y + 25, sub, cls="tiny"))
        parts.append(svg_text(score_x + score_w + 9, y + 11, fmt_score(row["normalized_score_0_100"]), cls="label"))

        for i, (_dim, short, _label) in enumerate(DIMENSION_COLUMNS):
            x = dim_x + i * (dim_w + dim_gap)
            parts.extend(dimension_rect(x, y - 1, dim_w, bar_h, row[f"{short}_score_0_4"], color, low_conf))
        y += row_h

    product_top = top
    parts.append(svg_text(product_x, product_top - 26, "Current Hormuz product/channel rows", cls="section"))
    parts.append(svg_text(product_x, product_top - 9, "Same rubric, sorted by product exposure score", cls="small"))
    for tick in [0, 50, 100]:
        x = product_x + product_score_w * tick / 100
        parts.append(f'<line x1="{x:.1f}" y1="{product_top + 8:.1f}" x2="{x:.1f}" y2="{product_top + len(product_rows) * 54 + 16:.1f}" stroke="#eeeeee"/>')
        parts.append(svg_text(x, product_top + 3, str(tick), cls="axis", anchor="middle"))

    py = product_top + 24
    for row in product_rows:
        score = float(row["normalized_score_0_100"])
        color = "#8b2f2f"
        low_conf = CONFIDENCE_MARKERS.get(row["confidence"], "solid") == "hollow"
        w = product_score_w * score / 100
        parts.append(svg_text(product_x, py, row["display_label"], cls="label"))
        parts.append(svg_text(product_x, py + 15, f"rank {row['rank_within_source_table']} | conf: {row['confidence']}", cls="tiny"))
        parts.append(f'<rect x="{product_x:.1f}" y="{py + 22:.1f}" width="{product_score_w:.1f}" height="10" rx="2" fill="#e9e9e9"/>')
        parts.append(f'<rect x="{product_x:.1f}" y="{py + 22:.1f}" width="{w:.1f}" height="10" rx="2" fill="{color}" opacity="0.78"/>')
        marker_fill = "#ffffff" if low_conf else color
        parts.append(f'<circle cx="{product_x + w:.1f}" cy="{py + 27:.1f}" r="6" fill="{marker_fill}" stroke="{color}" stroke-width="1.8"/>')
        parts.append(svg_text(product_x + product_score_w + 12, py + 31, fmt_score(row["normalized_score_0_100"]), cls="label"))
        py += 54

    note_y = 978
    notes = [
        "Caveat: Current Hormuz rows are exposure/scenario rankings, not observed realized losses. Do not sum product rows; crude, refined products, LPG/NGLs, petrochemicals, fertilizer inputs, sulphur, aluminium, and freight channels overlap.",
        "Source: data/derived/hormuz_4j7_4_case_ranking_scores.csv and data/derived/hormuz_4j7_4_hormuz_product_ranking_scores.csv; underlying IEA, EIA, World Bank/IMF, UN/industry and project-derived tables listed in the score files; calculations by author. Accessed 2026-07-06.",
        "Low-conf. labels and hollow markers indicate low-confidence/proxy rows. Dimension cells show 0-4 rubric scores; n/a means the score table did not carry a meaningful value for that dimension.",
    ]
    for note in notes:
        for line in svg_wrapped_text(left, note_y, note, width_chars=190, cls="note", line_height=14):
            parts.append(line)
            note_y += 14
        note_y += 4

    metadata = (
        "Figure ID: fig-4j7-historical-shock-comparison; author/script: "
        "scripts/build_4j7_historical_comparison_chart.py; generated from 4J7.4 ranking score tables; "
        "unit: normalized severity score 0-100 plus dimension rubric scores 0-4."
    )
    parts.append(f"<metadata>{escape(metadata)}</metadata>")
    parts.append("</svg>")
    OUT_SVG.write_text("\n".join(parts) + "\n")


def validate_outputs() -> None:
    missing = [path for path in [OUT_CSV, OUT_SVG] if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing output(s): {', '.join(str(p) for p in missing)}")
    if OUT_CSV.stat().st_size <= 0 or OUT_SVG.stat().st_size <= 0:
        raise ValueError("one or more outputs are empty")
    with OUT_CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("figure data CSV has no rows")
    if not OUT_SVG.read_text().lstrip().startswith("<svg"):
        raise ValueError("SVG output does not start with <svg")
    if any(math.isnan(float(row["normalized_score_0_100"])) for row in rows):
        raise ValueError("NaN score found in figure data")


def main() -> int:
    comparison_rows = summarize_rows(read_csv(CASE_SCORES), "comparison_case")
    product_rows = summarize_rows(read_csv(PRODUCT_SCORES), "hormuz_product_channel")
    write_figure_csv(comparison_rows + product_rows)
    write_svg(comparison_rows, product_rows)
    validate_outputs()
    print(f"wrote {OUT_CSV.relative_to(ROOT)} ({len(comparison_rows) + len(product_rows)} rows)")
    print(f"wrote {OUT_SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
