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
    "text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
    "fill:#172033;letter-spacing:0}"
    ".title{font-size:30px;font-weight:760}"
    ".label{font-size:15px;font-weight:740}"
    ".small{font-size:13px;font-weight:560;fill:#5d687a}"
    ".total{font-size:14px;font-weight:720;fill:#172033}"
    ".note{font-size:13px;font-weight:560;fill:#5d687a}"
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
    origins = table_from_cells(cells, 3, 9, 6)
    destinations = table_from_cells(cells, 17, 25, 6)
    write_link_csv(OIL_CSV, "crude oil and condensate", "mb/d", "2024", OIL_URL, origins, destinations)
    draw_sankey(
        OIL_SVG,
        "Oil Flow through the Strait of Hormuz, 2024",
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
