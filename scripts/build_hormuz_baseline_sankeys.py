#!/usr/bin/env python3
"""Build baseline Hormuz oil and LNG origin/destination Sankey figures."""

from __future__ import annotations

import csv
import math
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]

OIL_TOTAL_URL = "https://www.eia.gov/todayinenergy/images/2025.06.16/fig1.xlsx"
OIL_URL = "https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx"
LNG_URL = "https://www.eia.gov/todayinenergy/images/2025.06.24/fig2.xlsx"

OIL_CSV = ROOT / "figures/fig-kmz-oil-hormuz-baseline-sankey-data.csv"
OIL_SVG = ROOT / "figures/fig-kmz-oil-hormuz-baseline-sankey.svg"
LNG_CSV = ROOT / "figures/fig-kmz-lng-hormuz-baseline-sankey-data.csv"
LNG_SVG = ROOT / "figures/fig-kmz-lng-hormuz-baseline-sankey.svg"

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

FIGURE_STYLE = (
    "text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
    "fill:#172033;letter-spacing:0}"
    ".title{font-size:30px;font-weight:760}"
    ".label{font-size:15px;font-weight:740}"
    ".small{font-size:13px;font-weight:560;fill:#5d687a}"
    ".total{font-size:14px;font-weight:720;fill:#172033}"
    ".note{font-size:13px;font-weight:560;fill:#5d687a}"
)

PRODUCT_PROXY_SOURCES = {
    "Saudi Arabia": "https://www.eia.gov/international/analysis/country/SAU",
    "United Arab Emirates": "https://www.eia.gov/international/content/analysis/countries_long/United_Arab_Emirates/uae_2023.pdf",
    "Iraq": "https://www.eia.gov/international/analysis/country/irq",
    "Qatar": "https://www.eia.gov/international/analysis/country/QAT",
    "Iran": "https://www.eia.gov/international/content/analysis/countries_long/Iran/pdf/Iran%20CAB%202024.pdf",
    "Kuwait": "https://www.eia.gov/international/analysis/country/kwt",
}

PRODUCT_PROXY_VALUES = {
    # Country product-export proxies from hormuz-kmz.1. The route-total product
    # control comes from EIA/Vortexa fig1; Kuwait is the balancing residual.
    "Saudi Arabia": 1.300,
    "United Arab Emirates": 1.500,
    "Iraq": 0.479,
    "Qatar": 0.805,
    "Iran": 1.000,
}


def download(url: str) -> Path:
    path = Path(tempfile.gettempdir()) / Path(url).name
    urllib.request.urlretrieve(url, path)
    return path


def col_to_number(col: str) -> int:
    number = 0
    for ch in col:
        number = number * 26 + ord(ch.upper()) - ord("A") + 1
    return number


def split_cell(ref: str) -> tuple[int, int]:
    col = "".join(ch for ch in ref if ch.isalpha())
    row = int("".join(ch for ch in ref if ch.isdigit()))
    return row, col_to_number(col)


def read_xlsx_cells(path: Path) -> dict[tuple[int, int], str]:
    with ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//a:t", NS)))

        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        cells: dict[tuple[int, int], str] = {}
        for cell in root.findall(".//a:sheetData/a:row/a:c", NS):
            value = cell.find("a:v", NS)
            text = "" if value is None else value.text or ""
            if cell.get("t") == "s" and text:
                text = shared[int(text)]
            cells[split_cell(cell.get("r", ""))] = text
        return cells


def table_from_cells(
    cells: dict[tuple[int, int], str],
    start_row: int,
    end_row: int,
    value_col: int,
    name_col: int = 1,
) -> list[tuple[str, float]]:
    rows = []
    for row in range(start_row, end_row + 1):
        name = cells.get((row, name_col), "").strip()
        value = float(cells.get((row, value_col), "0") or 0)
        if name and value > 0:
            rows.append((normalize_name(name), value))
    return rows


def group_rows(rows: list[tuple[str, float]], keep: set[str], grouped_name: str) -> list[tuple[str, float]]:
    output: list[tuple[str, float]] = []
    grouped = 0.0
    for name, value in rows:
        if name in keep:
            output.append((name, value))
        else:
            grouped += value
    if grouped > 0:
        output.append((grouped_name, grouped))
    return output


def fold_row(rows: list[tuple[str, float]], name_to_fold: str, target_name: str) -> list[tuple[str, float]]:
    output: list[tuple[str, float]] = []
    folded = 0.0
    for name, value in rows:
        if name == name_to_fold:
            folded += value
        elif name == target_name:
            output.append((name, value + folded))
            folded = 0.0
        else:
            output.append((name, value))
    if folded:
        output.append((target_name, folded))
    return output


def normalize_name(name: str) -> str:
    fixes = {
        "SAUDI ARABIA": "Saudi Arabia",
        "UNITED ARAB EMIRATES": "United Arab Emirates",
        "IRAQ": "Iraq",
        "KUWAIT": "Kuwait",
        "QATAR": "Qatar",
        "IRAN": "Iran",
        "other": "Other",
        "other Asia": "Other Asia",
        "other Europe": "Other Europe",
    }
    return fixes.get(name, name)


def write_link_csv(
    path: Path,
    commodity: str,
    unit: str,
    year: str,
    url: str,
    origins: list[tuple[str, float]],
    destinations: list[tuple[str, float]],
) -> None:
    fields = [
        "figure_id",
        "commodity",
        "year",
        "flow_side",
        "source",
        "target",
        "value",
        "unit",
        "source_url",
        "caveat",
    ]
    rows: list[dict[str, str]] = []
    figure_id = path.stem.replace("-data", "")
    caveat = "Origin totals and destination totals are separate EIA/Vortexa aggregates; links are not country-pair cargo matches."
    for name, value in origins:
        rows.append(
            {
                "figure_id": figure_id,
                "commodity": commodity,
                "year": year,
                "flow_side": "origin_to_hormuz",
                "source": name,
                "target": "Strait of Hormuz",
                "value": f"{value:.6f}",
                "unit": unit,
                "source_url": url,
                "caveat": caveat,
            }
        )
    for name, value in destinations:
        rows.append(
            {
                "figure_id": figure_id,
                "commodity": commodity,
                "year": year,
                "flow_side": "hormuz_to_destination",
                "source": "Strait of Hormuz",
                "target": name,
                "value": f"{value:.6f}",
                "unit": unit,
                "source_url": url,
                "caveat": caveat,
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_oil_csv(
    path: Path,
    origins: list[dict[str, float | str]],
    destinations: list[dict[str, float | str]],
) -> None:
    fields = [
        "figure_id",
        "commodity",
        "product_group",
        "year",
        "flow_side",
        "source",
        "target",
        "value",
        "unit",
        "source_url",
        "caveat",
    ]
    figure_id = path.stem.replace("-data", "")
    rows: list[dict[str, str]] = []
    for row in origins + destinations:
        rows.append(
            {
                "figure_id": figure_id,
                "commodity": "oil and petroleum products",
                "product_group": str(row["product_group"]),
                "year": "2024",
                "flow_side": str(row["flow_side"]),
                "source": str(row["source"]),
                "target": str(row["target"]),
                "value": f"{float(row['value']):.6f}",
                "unit": "mb/d",
                "source_url": str(row["source_url"]),
                "caveat": str(row["caveat"]),
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt(value: float, unit: str) -> str:
    if value >= 1:
        return f"{value:.1f} {unit}"
    return f"{value:.2f} {unit}"


def fmt_component(value: float) -> str:
    if value >= 1:
        return f"{value:.1f}"
    return f"{value:.2f}"


def node_layout(rows: list[tuple[str, float]], top: float, height: float, min_gap: float) -> dict[str, tuple[float, float]]:
    total = sum(value for _name, value in rows)
    usable = height - min_gap * (len(rows) - 1)
    scale = usable / total
    y = top
    layout = {}
    for name, value in rows:
        h = value * scale
        layout[name] = (y, h)
        y += h + min_gap
    return layout


def band_path(
    x1: float,
    y1_top: float,
    y1_bottom: float,
    x2: float,
    y2_top: float,
    y2_bottom: float,
) -> str:
    dx = (x2 - x1) * 0.55
    return (
        f"M {x1:.1f} {y1_top:.1f} "
        f"C {x1 + dx:.1f} {y1_top:.1f}, {x2 - dx:.1f} {y2_top:.1f}, {x2:.1f} {y2_top:.1f} "
        f"L {x2:.1f} {y2_bottom:.1f} "
        f"C {x2 - dx:.1f} {y2_bottom:.1f}, {x1 + dx:.1f} {y1_bottom:.1f}, {x1:.1f} {y1_bottom:.1f} "
        "Z"
    )


def row_value(rows: list[tuple[str, float]], name: str) -> float:
    for row_name, value in rows:
        if row_name == name:
            return value
    return 0.0


def scaled_component(
    node_y: float,
    node_h: float,
    component_value: float,
    node_total: float,
) -> tuple[float, float]:
    if component_value <= 0 or node_total <= 0:
        return node_y, 0.0
    return node_y, component_value / node_total * node_h


def product_origin_allocation(product_total: float, country_order: list[str]) -> dict[str, float]:
    product = {country: 0.0 for country in country_order}
    proxy_sum = 0.0
    for country, value in PRODUCT_PROXY_VALUES.items():
        if country in product:
            product[country] = value
            proxy_sum += value

    residual = product_total - proxy_sum
    if residual < -0.01:
        raise ValueError(
            f"Product proxy sum {proxy_sum:.3f} exceeds EIA product total {product_total:.3f}"
        )
    if "Kuwait" in product:
        product["Kuwait"] += max(0.0, residual)
    elif "Other" in product:
        product["Other"] += max(0.0, residual)
    return product


def draw_product_overlay(parts: list[str], d: str, opacity: float = 0.46) -> None:
    parts.append(f'<path d="{d}" fill="url(#productHatch)" opacity="{opacity:.2f}"/>')


def draw_oil_sankey(
    path: Path,
    crude_origins: list[tuple[str, float]],
    product_origins: dict[str, float],
    crude_destinations: list[tuple[str, float]],
    crude_total: float,
    product_total: float,
    oil_total: float,
) -> None:
    width, height = 1440, 980
    top, chart_h = 122, 746
    left_x, mid_x, right_x = 250, 708, 1018
    node_w = 22

    origin_totals = [(name, value + product_origins.get(name, 0.0)) for name, value in crude_origins]
    destination_rows = crude_destinations + [("Refined/LPG destinations not public", product_total)]

    left = node_layout(origin_totals, top, chart_h, 22)
    right = node_layout(destination_rows, top, chart_h, 24)

    crude_mid_y = top
    crude_mid_h = crude_total / oil_total * chart_h
    product_mid_y = crude_mid_y + crude_mid_h
    product_mid_h = product_total / oil_total * chart_h

    colors = [
        "#087f75",
        "#315c99",
        "#b56b12",
        "#6d5bd0",
        "#b42318",
        "#2f7d48",
        "#6b7280",
        "#2084a0",
        "#8c5a2b",
    ]
    origin_color = {name: colors[i % len(colors)] for i, (name, _value) in enumerate(origin_totals)}
    dest_color = {name: colors[(i + 3) % len(colors)] for i, (name, _value) in enumerate(crude_destinations)}
    product_color = "#7c8798"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f6f7f9"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="8" fill="#ffffff" stroke="#dfe4ec"/>',
        "<defs>",
        '<pattern id="productHatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">',
        '<line x1="0" y1="0" x2="0" y2="8" stroke="#172033" stroke-opacity="0.48" stroke-width="2"/>',
        "</pattern>",
        "</defs>",
        f"<style>{FIGURE_STYLE}</style>",
        '<text x="72" y="64" class="title">Oil Flows through the Strait of Hormuz, 2024</text>',
        '<rect x="932" y="52" width="34" height="12" fill="#315c99" opacity="0.45"/>',
        '<text x="976" y="63" class="small">crude/condensate</text>',
        '<rect x="932" y="74" width="34" height="12" fill="#7c8798" opacity="0.24"/>',
        '<rect x="932" y="74" width="34" height="12" fill="url(#productHatch)" opacity="0.58"/>',
        '<text x="976" y="85" class="small">refined products/LPG</text>',
    ]

    crude_cursor = crude_mid_y
    product_cursor = product_mid_y
    for name, crude_value in crude_origins:
        product_value = product_origins.get(name, 0.0)
        node_total = crude_value + product_value
        y, h = left[name]
        crude_y, crude_h = scaled_component(y, h, crude_value, node_total)
        product_y = crude_y + crude_h
        product_h = scaled_component(y, h, product_value, node_total)[1]

        if crude_value > 0:
            mid_top = crude_cursor
            mid_bottom = crude_cursor + crude_value / crude_total * crude_mid_h
            d = band_path(left_x + node_w, crude_y, crude_y + crude_h, mid_x, mid_top, mid_bottom)
            parts.append(f'<path d="{d}" fill="{origin_color[name]}" opacity="0.34"/>')
            crude_cursor = mid_bottom

        if product_value > 0:
            mid_top = product_cursor
            mid_bottom = product_cursor + product_value / product_total * product_mid_h
            d = band_path(left_x + node_w, product_y, product_y + product_h, mid_x, mid_top, mid_bottom)
            parts.append(f'<path d="{d}" fill="{origin_color[name]}" opacity="0.18"/>')
            draw_product_overlay(parts, d, 0.38)
            product_cursor = mid_bottom

    crude_dest_cursor = crude_mid_y
    for name, value in crude_destinations:
        y, h = right[name]
        mid_top = crude_dest_cursor
        mid_bottom = crude_dest_cursor + value / crude_total * crude_mid_h
        d = band_path(mid_x + node_w, mid_top, mid_bottom, right_x, y, y + h)
        parts.append(f'<path d="{d}" fill="{dest_color[name]}" opacity="0.34"/>')
        crude_dest_cursor = mid_bottom

    product_dest_y, product_dest_h = right["Refined/LPG destinations not public"]
    d = band_path(
        mid_x + node_w,
        product_mid_y,
        product_mid_y + product_mid_h,
        right_x,
        product_dest_y,
        product_dest_y + product_dest_h,
    )
    parts.append(f'<path d="{d}" fill="{product_color}" opacity="0.18"/>')
    draw_product_overlay(parts, d, 0.40)

    for name, total_value in origin_totals:
        crude_value = row_value(crude_origins, name)
        product_value = product_origins.get(name, 0.0)
        y, h = left[name]
        crude_y, crude_h = scaled_component(y, h, crude_value, total_value)
        product_y = crude_y + crude_h
        product_h = scaled_component(y, h, product_value, total_value)[1]
        if crude_h > 0:
            parts.append(
                f'<rect x="{left_x}" y="{crude_y:.1f}" width="{node_w}" height="{crude_h:.1f}" '
                f'fill="{origin_color[name]}"/>'
            )
        if product_h > 0:
            parts.append(
                f'<rect x="{left_x}" y="{product_y:.1f}" width="{node_w}" height="{product_h:.1f}" '
                f'fill="{origin_color[name]}" opacity="0.45"/>'
            )
            parts.append(
                f'<rect x="{left_x}" y="{product_y:.1f}" width="{node_w}" height="{product_h:.1f}" '
                f'fill="url(#productHatch)" opacity="0.70"/>'
            )
        parts.append(f'<text x="{left_x - 14}" y="{y + h / 2 - 4:.1f}" class="label" text-anchor="end">{escape(name)}</text>')
        if product_value > 0:
            component_label = f"{fmt_component(crude_value)} crude + {fmt_component(product_value)} prod"
        else:
            component_label = f"{fmt_component(crude_value)} crude"
        parts.append(f'<text x="{left_x - 14}" y="{y + h / 2 + 13:.1f}" class="small" text-anchor="end">{escape(component_label)} mb/d</text>')

    parts.append(f'<rect x="{mid_x}" y="{crude_mid_y:.1f}" width="{node_w}" height="{crude_mid_h:.1f}" fill="#172033"/>')
    parts.append(f'<rect x="{mid_x}" y="{product_mid_y:.1f}" width="{node_w}" height="{product_mid_h:.1f}" fill="#7c8798"/>')
    parts.append(f'<rect x="{mid_x}" y="{product_mid_y:.1f}" width="{node_w}" height="{product_mid_h:.1f}" fill="url(#productHatch)" opacity="0.75"/>')
    parts.append(f'<text x="{mid_x + node_w / 2:.1f}" y="{top + chart_h + 28:.1f}" class="total" text-anchor="middle">{fmt(oil_total, "mb/d")}</text>')

    for name, value in crude_destinations:
        y, h = right[name]
        parts.append(f'<rect x="{right_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" fill="{dest_color[name]}"/>')
        parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 - 4:.1f}" class="label">{escape(name)}</text>')
        parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 + 13:.1f}" class="small">{fmt(value, "mb/d")}</text>')

    y, h = product_dest_y, product_dest_h
    parts.append(f'<rect x="{right_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" fill="{product_color}" opacity="0.55"/>')
    parts.append(f'<rect x="{right_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" fill="url(#productHatch)" opacity="0.70"/>')
    parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 - 4:.1f}" class="label">Refined/LPG</text>')
    parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 + 13:.1f}" class="small">destination split not public</text>')
    parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 + 30:.1f}" class="small">{fmt(product_total, "mb/d")}</text>')

    parts.append(f'<rect x="72" y="916" width="{width - 144}" height="1" fill="#d8dee8"/>')
    parts.append('<text x="72" y="944" class="note">Source: EIA/Vortexa</text>')
    metadata = (
        "Figure generated by scripts/build_hormuz_baseline_sankeys.py; commodity=oil and petroleum products; "
        f"crude_source={OIL_URL}; total_product_source={OIL_TOTAL_URL}; unit=mb/d; year=2024. "
        "Product origin split is indicative and destination split is not public in EIA figure data."
    )
    parts.append(f"<metadata>{escape(metadata)}</metadata>")
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n")


def draw_sankey(
    path: Path,
    title: str,
    commodity: str,
    unit: str,
    url: str,
    origins: list[tuple[str, float]],
    destinations: list[tuple[str, float]],
) -> None:
    width, height = 1440, 980
    top, chart_h = 108, 760
    left_x, mid_x, right_x = 250, 708, 1018
    node_w = 22
    source_total = sum(v for _n, v in origins)
    dest_total = sum(v for _n, v in destinations)
    total = (source_total + dest_total) / 2
    left = node_layout(origins, top, chart_h, 24)
    right = node_layout(destinations, top, chart_h, 31)
    mid_h = chart_h
    mid_y = top

    colors = [
        "#087f75",
        "#315c99",
        "#b56b12",
        "#6d5bd0",
        "#b42318",
        "#2f7d48",
        "#6b7280",
        "#2084a0",
        "#8c5a2b",
    ]
    origin_color = {name: colors[i % len(colors)] for i, (name, _value) in enumerate(origins)}
    dest_color = {name: colors[(i + 3) % len(colors)] for i, (name, _value) in enumerate(destinations)}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f6f7f9"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="8" fill="#ffffff" stroke="#dfe4ec"/>',
        f"<style>{FIGURE_STYLE}</style>",
        f'<text x="72" y="66" class="title">{escape(title)}</text>',
    ]

    origin_cursor = mid_y
    for name, value in origins:
        y, h = left[name]
        mid_top = origin_cursor
        mid_bottom = origin_cursor + value / source_total * mid_h
        parts.append(
            f'<path d="{band_path(left_x + node_w, y, y + h, mid_x, mid_top, mid_bottom)}" '
            f'fill="{origin_color[name]}" opacity="0.34"/>'
        )
        origin_cursor = mid_bottom

    dest_cursor = mid_y
    for name, value in destinations:
        y, h = right[name]
        mid_top = dest_cursor
        mid_bottom = dest_cursor + value / dest_total * mid_h
        parts.append(
            f'<path d="{band_path(mid_x + node_w, mid_top, mid_bottom, right_x, y, y + h)}" '
            f'fill="{dest_color[name]}" opacity="0.34"/>'
        )
        dest_cursor = mid_bottom

    for name, value in origins:
        y, h = left[name]
        parts.append(f'<rect x="{left_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" fill="{origin_color[name]}"/>')
        parts.append(f'<text x="{left_x - 14}" y="{y + h / 2 - 4:.1f}" class="label" text-anchor="end">{escape(name)}</text>')
        parts.append(f'<text x="{left_x - 14}" y="{y + h / 2 + 13:.1f}" class="small" text-anchor="end">{fmt(value, unit)}</text>')

    parts.append(f'<rect x="{mid_x}" y="{mid_y:.1f}" width="{node_w}" height="{mid_h:.1f}" fill="#172033"/>')
    parts.append(f'<text x="{mid_x + node_w / 2:.1f}" y="{mid_y + mid_h + 28:.1f}" class="total" text-anchor="middle">{fmt(total, unit)}</text>')

    for name, value in destinations:
        y, h = right[name]
        parts.append(f'<rect x="{right_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" fill="{dest_color[name]}"/>')
        parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 - 4:.1f}" class="label">{escape(name)}</text>')
        parts.append(f'<text x="{right_x + node_w + 14}" y="{y + h / 2 + 13:.1f}" class="small">{fmt(value, unit)}</text>')

    parts.append(f'<rect x="72" y="916" width="{width - 144}" height="1" fill="#d8dee8"/>')
    parts.append('<text x="72" y="944" class="note">Source: EIA/Vortexa</text>')
    metadata = (
        f"Figure generated by scripts/build_hormuz_baseline_sankeys.py; commodity={commodity}; "
        f"source={url}; unit={unit}; year=2024."
    )
    parts.append(f"<metadata>{escape(metadata)}</metadata>")
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n")


def build_oil() -> None:
    cells = read_xlsx_cells(download(OIL_URL))
    total_cells = read_xlsx_cells(download(OIL_TOTAL_URL))
    crude_origins = table_from_cells(cells, 3, 9, 6)
    crude_destinations = table_from_cells(cells, 17, 25, 6)
    oil_total = float(total_cells[(4, 7)])
    crude_total = float(total_cells[(5, 7)])
    product_total = float(total_cells[(6, 7)])
    if not math.isclose(sum(value for _name, value in crude_origins), crude_total, rel_tol=0, abs_tol=0.01):
        raise ValueError("Origin crude total does not match EIA fig1 crude/condensate total")
    if not math.isclose(sum(value for _name, value in crude_destinations), crude_total, rel_tol=0, abs_tol=0.01):
        raise ValueError("Destination crude total does not match EIA fig1 crude/condensate total")
    crude_destinations = fold_row(crude_destinations, "Saudi Arabia", "Other")

    country_order = [name for name, _value in crude_origins]
    product_origins = product_origin_allocation(product_total, country_order)
    if not math.isclose(sum(product_origins.values()), product_total, rel_tol=0, abs_tol=0.01):
        raise ValueError("Product origin allocation does not match EIA fig1 product total")

    origin_rows: list[dict[str, float | str]] = []
    dest_rows: list[dict[str, float | str]] = []
    crude_caveat = (
        "EIA/Vortexa crude/condensate origin totals and destination totals are separate aggregates; "
        "links are not country-pair cargo matches."
    )
    product_caveat = (
        "Product/LPG origin split combines EIA's 2024 route-total petroleum-products flow with country "
        "product-export proxies from hormuz-kmz.1; Kuwait is the residual needed to reconcile to the EIA "
        "route total. Use as an indicative visual allocation, not cargo-level accounting."
    )
    for country, value in crude_origins:
        origin_rows.append(
            {
                "product_group": "crude oil and condensate",
                "flow_side": "origin_to_hormuz",
                "source": country,
                "target": "Strait of Hormuz",
                "value": value,
                "source_url": OIL_URL,
                "caveat": crude_caveat,
            }
        )
        product_value = product_origins.get(country, 0.0)
        if product_value > 0:
            product_sources = [OIL_TOTAL_URL]
            if country in PRODUCT_PROXY_SOURCES:
                product_sources.append(PRODUCT_PROXY_SOURCES[country])
            origin_rows.append(
                {
                    "product_group": "refined products/LPG",
                    "flow_side": "origin_to_hormuz",
                    "source": country,
                    "target": "Strait of Hormuz",
                    "value": product_value,
                    "source_url": "|".join(product_sources),
                    "caveat": product_caveat,
                }
            )
    for destination, value in crude_destinations:
        dest_rows.append(
            {
                "product_group": "crude oil and condensate",
                "flow_side": "hormuz_to_destination",
                "source": "Strait of Hormuz",
                "target": destination,
                "value": value,
                "source_url": OIL_URL,
                "caveat": crude_caveat,
            }
        )
    dest_rows.append(
        {
            "product_group": "refined products/LPG",
            "flow_side": "hormuz_to_destination",
            "source": "Strait of Hormuz",
            "target": "Refined/LPG destinations not public",
            "value": product_total,
            "source_url": OIL_TOTAL_URL,
            "caveat": (
                "EIA fig1 provides the 2024 petroleum-products total through Hormuz, but the public workbook "
                "does not provide destination-country splits for refined products/LPG."
            ),
        }
    )

    write_oil_csv(OIL_CSV, origin_rows, dest_rows)
    draw_oil_sankey(
        OIL_SVG,
        crude_origins,
        product_origins,
        crude_destinations,
        crude_total,
        product_total,
        oil_total,
    )


def build_lng() -> None:
    cells = read_xlsx_cells(download(LNG_URL))
    origins = group_rows(table_from_cells(cells, 3, 6, 6), {"Qatar", "United Arab Emirates"}, "Other origins")
    destinations = table_from_cells(cells, 14, 22, 6)
    write_link_csv(LNG_CSV, "liquefied natural gas", "Bcf/d", "2024", LNG_URL, origins, destinations)
    draw_sankey(
        LNG_SVG,
        "LNG Flow through the Strait of Hormuz, 2024",
        "liquefied natural gas",
        "Bcf/d",
        LNG_URL,
        origins,
        destinations,
    )


def validate_csv(path: Path) -> None:
    with path.open(newline="") as f:
        rows = list(csv.reader(f))
    widths = {len(row) for row in rows}
    if len(widths) != 1:
        raise ValueError(f"{path} has inconsistent row widths: {sorted(widths)}")
    if len(rows) <= 1:
        raise ValueError(f"{path} has no data rows")


def main() -> int:
    build_oil()
    build_lng()
    for path in [OIL_CSV, LNG_CSV]:
        validate_csv(path)
    for path in [OIL_SVG, LNG_SVG]:
        if not path.read_text().lstrip().startswith("<svg"):
            raise ValueError(f"{path} is not an SVG")
    print(f"wrote {OIL_CSV.relative_to(ROOT)} and {OIL_SVG.relative_to(ROOT)}")
    print(f"wrote {LNG_CSV.relative_to(ROOT)} and {LNG_SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
