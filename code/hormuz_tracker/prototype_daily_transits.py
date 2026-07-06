#!/usr/bin/env python3
"""Prototype daily Strait of Hormuz transit counter.

Input is a normalized AIS-position CSV. The script detects vessel track segments
that cross a configured line and aggregates unique crossings by UTC date,
direction, and vessel class. It is intentionally dependency-free so it can run
against exports from multiple AIS providers.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator


DEFAULT_LINE_A = (26.24, 56.50)
DEFAULT_LINE_B = (26.56, 56.50)


@dataclass(frozen=True)
class Position:
    vessel_id: str
    timestamp_utc: datetime
    lat: float
    lon: float
    vessel_class: str
    ship_type: str = ""
    sog_knots: float | None = None
    source: str = ""


@dataclass(frozen=True)
class Crossing:
    vessel_id: str
    timestamp_utc: datetime
    direction: str
    vessel_class: str
    source: str


def parse_timestamp(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def read_positions(path: Path) -> list[Position]:
    positions: list[Position] = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vessel_id = first_present(row, "vessel_id", "imo", "mmsi")
            if not vessel_id:
                raise ValueError("Each row must include vessel_id, imo, or mmsi")
            sog = row.get("sog_knots") or row.get("speed_knots") or ""
            positions.append(
                Position(
                    vessel_id=vessel_id,
                    timestamp_utc=parse_timestamp(required(row, "timestamp_utc")),
                    lat=float(required(row, "lat")),
                    lon=float(required(row, "lon")),
                    vessel_class=(row.get("vessel_class") or "unknown").strip().lower(),
                    ship_type=(row.get("ship_type") or "").strip(),
                    sog_knots=float(sog) if sog else None,
                    source=(row.get("source") or "").strip(),
                )
            )
    return positions


def first_present(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def required(row: dict[str, str], key: str) -> str:
    value = (row.get(key) or "").strip()
    if not value:
        raise ValueError(f"Missing required column: {key}")
    return value


def side_of_line(lat: float, lon: float, line_a: tuple[float, float], line_b: tuple[float, float]) -> float:
    ay, ax = line_a
    by, bx = line_b
    return (bx - ax) * (lat - ay) - (by - ay) * (lon - ax)


def interpolate_crossing_time(
    before: Position,
    after: Position,
    line_a: tuple[float, float],
    line_b: tuple[float, float],
) -> datetime:
    before_side = abs(side_of_line(before.lat, before.lon, line_a, line_b))
    after_side = abs(side_of_line(after.lat, after.lon, line_a, line_b))
    total = before_side + after_side
    if total == 0:
        return after.timestamp_utc
    fraction = before_side / total
    elapsed = after.timestamp_utc - before.timestamp_utc
    return before.timestamp_utc + fraction * elapsed


def normalize_direction(
    before: Position,
    after: Position,
    line_a: tuple[float, float],
    line_b: tuple[float, float],
    gulf_side: str,
) -> str:
    before_side = side_of_line(before.lat, before.lon, line_a, line_b)
    after_side = side_of_line(after.lat, after.lon, line_a, line_b)
    entered_positive_side = after_side > before_side
    if gulf_side == "positive":
        return "inbound_to_gulf" if entered_positive_side else "outbound_from_gulf"
    return "inbound_to_gulf" if not entered_positive_side else "outbound_from_gulf"


def iter_crossings(
    positions: Iterable[Position],
    line_a: tuple[float, float],
    line_b: tuple[float, float],
    gulf_side: str,
    max_gap_hours: float,
    min_sog_knots: float,
) -> Iterator[Crossing]:
    by_vessel: dict[str, list[Position]] = {}
    for position in positions:
        by_vessel.setdefault(position.vessel_id, []).append(position)

    max_gap_seconds = max_gap_hours * 3600
    for vessel_id, track in by_vessel.items():
        track.sort(key=lambda p: p.timestamp_utc)
        last_crossing: datetime | None = None
        for before, after in zip(track, track[1:]):
            gap = (after.timestamp_utc - before.timestamp_utc).total_seconds()
            if gap <= 0 or gap > max_gap_seconds:
                continue
            if before.sog_knots is not None and after.sog_knots is not None:
                if max(before.sog_knots, after.sog_knots) < min_sog_knots:
                    continue
            before_side = side_of_line(before.lat, before.lon, line_a, line_b)
            after_side = side_of_line(after.lat, after.lon, line_a, line_b)
            if before_side == 0 or after_side == 0 or before_side * after_side > 0:
                continue
            crossing_time = interpolate_crossing_time(before, after, line_a, line_b)
            if last_crossing and (crossing_time - last_crossing).total_seconds() < 6 * 3600:
                continue
            last_crossing = crossing_time
            yield Crossing(
                vessel_id=vessel_id,
                timestamp_utc=crossing_time,
                direction=normalize_direction(before, after, line_a, line_b, gulf_side),
                vessel_class=after.vessel_class or before.vessel_class or "unknown",
                source=after.source or before.source,
            )


def aggregate_daily(crossings: Iterable[Crossing]) -> list[dict[str, str | int]]:
    counts: dict[tuple[str, str, str], set[str]] = {}
    for crossing in crossings:
        day = crossing.timestamp_utc.date().isoformat()
        key = (day, crossing.direction, crossing.vessel_class)
        counts.setdefault(key, set()).add(crossing.vessel_id)

    rows: list[dict[str, str | int]] = []
    for (day, direction, vessel_class), vessels in sorted(counts.items()):
        rows.append(
            {
                "date_utc": day,
                "direction": direction,
                "vessel_class": vessel_class,
                "transit_count": len(vessels),
                "unique_vessels": len(vessels),
                "coverage_flag": "prototype_unvalidated",
            }
        )
    return rows


def write_daily_counts(rows: list[dict[str, str | int]], path: Path) -> None:
    fieldnames = ["date_utc", "direction", "vessel_class", "transit_count", "unique_vessels", "coverage_flag"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_lat_lon(value: str) -> tuple[float, float]:
    lat, lon = value.split(",", maxsplit=1)
    return float(lat), float(lon)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Normalized AIS-position CSV")
    parser.add_argument("--output", required=True, type=Path, help="Daily transit count CSV to write")
    parser.add_argument("--line-a", default=f"{DEFAULT_LINE_A[0]},{DEFAULT_LINE_A[1]}", help="Crossing line endpoint lat,lon")
    parser.add_argument("--line-b", default=f"{DEFAULT_LINE_B[0]},{DEFAULT_LINE_B[1]}", help="Crossing line endpoint lat,lon")
    parser.add_argument(
        "--gulf-side",
        choices=["positive", "negative"],
        default="positive",
        help="Which side of the crossing line is the Persian Gulf side",
    )
    parser.add_argument("--max-gap-hours", type=float, default=6.0, help="Ignore consecutive positions farther apart than this")
    parser.add_argument("--min-sog-knots", type=float, default=1.0, help="Minimum observed speed to count a crossing")
    args = parser.parse_args()

    line_a = parse_lat_lon(args.line_a)
    line_b = parse_lat_lon(args.line_b)
    positions = read_positions(args.input)
    crossings = list(iter_crossings(positions, line_a, line_b, args.gulf_side, args.max_gap_hours, args.min_sog_knots))
    write_daily_counts(aggregate_daily(crossings), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
