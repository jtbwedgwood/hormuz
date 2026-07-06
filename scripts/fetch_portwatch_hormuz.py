#!/usr/bin/env python3
"""Fetch IMF PortWatch daily Strait of Hormuz chokepoint data."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


ARCGIS_QUERY_URL = (
    "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/"
    "Daily_Chokepoints_Data/FeatureServer/0/query"
)

FIELDS = [
    "date",
    "year",
    "month",
    "day",
    "portid",
    "portname",
    "n_container",
    "n_dry_bulk",
    "n_general_cargo",
    "n_roro",
    "n_tanker",
    "n_cargo",
    "n_total",
    "capacity_container",
    "capacity_dry_bulk",
    "capacity_general_cargo",
    "capacity_roro",
    "capacity_tanker",
    "capacity_cargo",
    "capacity",
]


def query_page(offset: int, page_size: int) -> dict:
    params = {
        "where": "portid='chokepoint6'",
        "outFields": ",".join(FIELDS),
        "orderByFields": "date ASC",
        "returnGeometry": "false",
        "f": "json",
        "resultOffset": str(offset),
        "resultRecordCount": str(page_size),
    }
    url = f"{ARCGIS_QUERY_URL}?{urlencode(params)}"
    with urlopen(url, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload


def fetch_all(page_size: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    offset = 0
    while True:
        payload = query_page(offset, page_size)
        features = payload.get("features", [])
        rows.extend(feature["attributes"] for feature in features)
        if not payload.get("exceededTransferLimit") and len(features) < page_size:
            break
        offset += len(features)
        if not features:
            break
    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/external/portwatch/hormuz_daily_chokepoint.csv"),
        help="CSV path to write",
    )
    parser.add_argument("--page-size", type=int, default=2000)
    args = parser.parse_args()

    rows = fetch_all(args.page_size)
    write_csv(rows, args.output)
    if rows:
        print(f"wrote {len(rows)} rows to {args.output}")
        print(f"date range: {rows[0]['date']} to {rows[-1]['date']}")
    else:
        print(f"wrote 0 rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
