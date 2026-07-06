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

OIL_URL = "https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx"
LNG_URL = "https://www.eia.gov/todayinenergy/images/2025.06.24/fig2.xlsx"

OIL_CSV = ROOT / "figures/fig-kmz-oil-hormuz-baseline-sankey-data.csv"
OIL_SVG = ROOT / "figures/fig-kmz-oil-hormuz-baseline-sankey.svg"
LNG_CSV = ROOT / "figures/fig-kmz-lng-hormuz-baseline-sankey-data.csv"
LNG_SVG = ROOT / "figures/fig-kmz-lng-hormuz-baseline-sankey.svg"

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

FIGURE_STYLE = (
    "text{font-family:Arial,Helvetica,sans-serif;fill:#111827}"
    ".title{font-size:28px;font-weight:700}"
    ".sub{font-size:16px;fill:#4b5563}"
    ".label{font-size:14px;font-weight:700}"
    ".small{font-size:12px;fill:#4b5563}"
    ".note{font-size:12px;fill:#6b7280}"
)


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


def cubic_path(x1: float, y1: float, x2: float, y2: float) -> str:
    dx = (x2 - x1) * 0.55
    return f"M {x1:.1f} {y1:.1f} C {x1 + dx:.1f} {y1:.1f}, {x2 - dx:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}"


def draw_sankey(
    path: Path,
    title: str,
    subtitle: str,
    commodity: str,
    unit: str,
    url: str,
    origins: list[tuple[str, float]],
    destinations: list[tuple[str, float]],
) -> None:
    width, height = 1400, 760
    top, chart_h = 120, 500
    left_x, mid_x, right_x = 210, 690, 1010
    node_w = 18
    source_total = sum(v for _n, v in origins)
    dest_total = sum(v for _n, v in destinations)
    total = (source_total + dest_total) / 2
    max_width = 46
    stroke_scale = max_width / max(max(value for _name, value in origins), max(value for _name, value in destinations))
    left = node_layout(origins, top, chart_h, 11)
    right = node_layout(destinations, top, chart_h, 8)
    mid_h = chart_h * 0.86
    mid_y = top + (chart_h - mid_h) / 2

    colors = ["#0f766e", "#2563eb", "#b45309", "#7c3aed", "#dc2626", "#15803d", "#6b7280", "#0891b2", "#9333ea"]
    origin_color = {name: colors[i % len(colors)] for i, (name, _value) in enumerate(origins)}
    dest_color = {name: colors[(i + 3) % len(colors)] for i, (name, _value) in enumerate(destinations)}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f"<style>{FIGURE_STYLE}</style>",
        f'<text x="72" y="42" class="title">{escape(title)}</text>',
        f'<text x="72" y="68" class="sub">{escape(subtitle)}</text>',
        '<text x="72" y="96" class="small">Exporter totals</text>',
        f'<text x="{mid_x + node_w / 2:.1f}" y="96" class="small" text-anchor="middle">Strait of Hormuz</text>',
        f'<text x="{width - 72}" y="96" class="small" text-anchor="end">Destination totals</text>',
    ]

    origin_cursor = mid_y
    for name, value in origins:
        y, h = left[name]
        stroke_w = max(2.0, value * stroke_scale)
        parts.append(
            f'<path d="{cubic_path(left_x + node_w, y + h / 2, mid_x, origin_cursor + value / source_total * mid_h / 2)}" '
            f'stroke="{origin_color[name]}" stroke-width="{stroke_w:.1f}" fill="none" opacity="0.34" stroke-linecap="round"/>'
        )
        origin_cursor += value / source_total * mid_h

    dest_cursor = mid_y
    for name, value in destinations:
        y, h = right[name]
        stroke_w = max(2.0, value * stroke_scale)
        parts.append(
            f'<path d="{cubic_path(mid_x + node_w, dest_cursor + value / dest_total * mid_h / 2, right_x, y + h / 2)}" '
            f'stroke="{dest_color[name]}" stroke-width="{stroke_w:.1f}" fill="none" opacity="0.34" stroke-linecap="round"/>'
        )
        dest_cursor += value / dest_total * mid_h

    for name, value in origins:
        y, h = left[name]
        parts.append(f'<rect x="{left_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" rx="3" fill="{origin_color[name]}"/>')
        parts.append(f'<text x="{left_x - 10}" y="{y + h / 2 - 3:.1f}" class="label" text-anchor="end">{escape(name)}</text>')
        parts.append(f'<text x="{left_x - 10}" y="{y + h / 2 + 13:.1f}" class="small" text-anchor="end">{fmt(value, unit)}</text>')

    parts.append(f'<rect x="{mid_x}" y="{mid_y:.1f}" width="{node_w}" height="{mid_h:.1f}" rx="4" fill="#374151"/>')
    parts.append(f'<text x="{mid_x + node_w / 2:.1f}" y="{mid_y + mid_h + 26:.1f}" class="label" text-anchor="middle">Total {fmt(total, unit)}</text>')

    for name, value in destinations:
        y, h = right[name]
        parts.append(f'<rect x="{right_x}" y="{y:.1f}" width="{node_w}" height="{h:.1f}" rx="3" fill="{dest_color[name]}"/>')
        parts.append(f'<text x="{right_x + node_w + 10}" y="{y + h / 2 - 3:.1f}" class="label">{escape(name)}</text>')
        parts.append(f'<text x="{right_x + node_w + 10}" y="{y + h / 2 + 13:.1f}" class="small">{fmt(value, unit)}</text>')

    diff = abs(source_total - dest_total)
    parts.append(f'<rect x="72" y="654" width="{width - 144}" height="1" fill="#e5e7eb"/>')
    parts.append(
        '<text x="72" y="682" class="note">Source: EIA Today in Energy figure data based on Vortexa; 2024 annual average; calculations by project. Caveats: see figures/README.md.</text>'
    )
    parts.append(
        f'<text x="72" y="704" class="note">Origin and destination totals are separate aggregates, not country-pair cargo matching. Rounding gap: {diff:.3f} {unit}.</text>'
    )
    metadata = (
        f"Figure generated by scripts/build_hormuz_baseline_sankeys.py; commodity={commodity}; "
        f"source={url}; unit={unit}; year=2024."
    )
    parts.append(f"<metadata>{escape(metadata)}</metadata>")
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n")


def build_oil() -> None:
    cells = read_xlsx_cells(download(OIL_URL))
    origins = table_from_cells(cells, 3, 9, 6)
    destinations = table_from_cells(cells, 17, 25, 6)
    write_link_csv(OIL_CSV, "crude oil and condensate", "mb/d", "2024", OIL_URL, origins, destinations)
    draw_sankey(
        OIL_SVG,
        "2024 Hormuz Oil Flow Baseline",
        "Crude oil and condensate moving through Hormuz, by origin and destination market",
        "crude oil and condensate",
        "mb/d",
        OIL_URL,
        origins,
        destinations,
    )


def build_lng() -> None:
    cells = read_xlsx_cells(download(LNG_URL))
    origins = group_rows(table_from_cells(cells, 3, 6, 6), {"Qatar", "United Arab Emirates"}, "Other origins")
    destinations = table_from_cells(cells, 14, 22, 6)
    write_link_csv(LNG_CSV, "liquefied natural gas", "Bcf/d", "2024", LNG_URL, origins, destinations)
    draw_sankey(
        LNG_SVG,
        "2024 Hormuz LNG Flow Baseline",
        "Liquefied natural gas moving through Hormuz, by origin and destination market",
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
