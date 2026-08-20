#!/usr/bin/env python3
"""Build the p2k.5 frozen-February versus July forward oil-balance audit.

The EIA balance is petroleum and other liquid fuels production less
consumption.  A positive value is an *implied* stock build, not an observed
inventory movement and not a deliverable reserve.  The seasonal/structural
split is an exact within-vintage decomposition: each calendar year's
day-weighted mean is labelled structural and each month's deviation from that
mean is labelled seasonal.  It is descriptive, not a causal seasonal model.
"""

from __future__ import annotations

import calendar
import csv
import io
import re
import urllib.request
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_5_foregone_build_capacity.csv"
HISTORICAL = ROOT / "data/derived/hormuz_m8q_4_cumulative_global_oil_accounting.csv"
FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
IEA_SURPLUS_URL = (
    "https://www.iea.org/commentaries/"
    "as-oil-market-surplus-keeps-rising-something-s-got-to-give"
)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

FIELDS = [
    "row_id", "record_type", "vintage", "period", "period_start", "period_end",
    "days", "supply_mb_d", "demand_mb_d", "implied_balance_mb_d",
    "structural_balance_mb_d", "seasonal_deviation_mb_d",
    "implied_balance_million_bbl", "cumulative_from_july_million_bbl",
    "physical_supply_shortfall_million_bbl", "active_adjustment_burden_million_bbl",
    "incremental_burden_vs_frozen_february_million_bbl",
    "pct_increase_vs_frozen_february_active_burden", "source_urls", "confidence",
    "method", "interpretation", "caveat",
]

PERIODS = {
    "march_june_2026": (date(2026, 3, 1), date(2026, 6, 30)),
    "july_december_2026": (date(2026, 7, 1), date(2026, 12, 31)),
    "august_december_2026": (date(2026, 8, 1), date(2026, 12, 31)),
    "july_september_2026": (date(2026, 7, 1), date(2026, 9, 30)),
    "august_september_2026": (date(2026, 8, 1), date(2026, 9, 30)),
    "october_december_2026": (date(2026, 10, 1), date(2026, 12, 31)),
    "calendar_2027": (date(2027, 1, 1), date(2027, 12, 31)),
}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def workbook_rows(workbook: bytes, sheet_number: int) -> dict[str, dict[str, str]]:
    """Return XLSX rows keyed by the EIA mnemonic in column A."""
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = [
            "".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t"))
            for item in strings_root.findall("m:si", NS)
        ]
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
        output: dict[str, dict[str, str]] = {}
        for row_node in root.findall(".//m:row", NS):
            cells: dict[str, str] = {}
            for cell in row_node.findall("m:c", NS):
                value = cell.find("m:v", NS)
                column = re.match(r"[A-Z]+", cell.attrib["r"])
                if value is None or column is None:
                    continue
                raw = value.text or ""
                cells[column.group()] = strings[int(raw)] if cell.attrib.get("t") == "s" else raw
            if cells.get("A"):
                output[cells["A"]] = cells
        return output


def find_table(workbook: bytes, sheets: list[int], mnemonic: str) -> dict[str, dict[str, str]]:
    for sheet in sheets:
        rows = workbook_rows(workbook, sheet)
        if mnemonic in rows:
            return rows
    raise ValueError(f"Could not find {mnemonic} in sheets {sheets}")


def excel_column(number: int) -> str:
    value = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        value = chr(65 + remainder) + value
    return value


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(**values: object) -> dict[str, str]:
    output = {field: "" for field in FIELDS}
    for key, value in values.items():
        output[key] = fmt(value)
    return output


def extract_months(workbook: bytes) -> list[dict[str, object]]:
    supply = find_table(workbook, [7, 5], "papr_world")["papr_world"]
    demand = find_table(workbook, [9, 8], "patc_world")["patc_world"]
    output: list[dict[str, object]] = []
    # EIA's AY:BV cells are January 2026 through December 2027.
    for offset in range(24):
        year, month = 2026 + offset // 12, offset % 12 + 1
        column = excel_column(51 + offset)  # AY is Excel column 51.
        supply_value, demand_value = float(supply[column]), float(demand[column])
        output.append({
            "year": year, "month": month, "date": date(year, month, 1),
            "days": calendar.monthrange(year, month)[1], "supply": supply_value,
            "demand": demand_value, "balance": supply_value - demand_value,
        })
    return output


def weighted_rate(items: list[dict[str, object]]) -> float:
    days = sum(int(item["days"]) for item in items)
    return sum(float(item["balance"]) * int(item["days"]) for item in items) / days


def volume(items: list[dict[str, object]]) -> float:
    return sum(float(item["balance"]) * int(item["days"]) for item in items)


def historical_bridge() -> dict[str, float]:
    with HISTORICAL.open(newline="") as handle:
        rows = [item for item in csv.DictReader(handle) if item["observation_month"] <= "2026-06"]
    if len(rows) != 4:
        raise ValueError("Expected exactly March-June rows in the historical bridge")
    return {
        "supply_shortfall": sum(float(item["cumulative_supply_shortfall_million_bbl"]) for item in rows),
        "lower_consumption": sum(float(item["cumulative_lower_consumption_million_bbl"]) for item in rows),
        "expected_build": sum(float(item["cumulative_foregone_expected_build_million_bbl"]) for item in rows),
        "actual_draw": sum(float(item["cumulative_actual_implied_draw_million_bbl"]) for item in rows),
        "days": sum(int(item["days"]) for item in rows),
    }


def build() -> list[dict[str, str]]:
    paths = {
        "frozen_february_2026": (FEB_URL, extract_months(download(FEB_URL))),
        "postshock_july_2026": (JUL_URL, extract_months(download(JUL_URL))),
    }
    rows: list[dict[str, str]] = []
    period_values: dict[tuple[str, str], tuple[float, float]] = {}

    for vintage, (source_url, items) in paths.items():
        annual_rates = {
            year: weighted_rate([item for item in items if item["year"] == year])
            for year in (2026, 2027)
        }
        cumulative = 0.0
        for item in items:
            year, month = int(item["year"]), int(item["month"])
            balance, days = float(item["balance"]), int(item["days"])
            monthly_volume = balance * days
            if (year, month) >= (2026, 7):
                cumulative += monthly_volume
            rows.append(row(
                row_id=f"monthly-{vintage}-{year}-{month:02d}", record_type="monthly_path",
                vintage=vintage, period=f"{year}-{month:02d}",
                period_start=date(year, month, 1).isoformat(),
                period_end=date(year, month, days).isoformat(), days=days,
                supply_mb_d=float(item["supply"]), demand_mb_d=float(item["demand"]),
                implied_balance_mb_d=balance, structural_balance_mb_d=annual_rates[year],
                seasonal_deviation_mb_d=balance - annual_rates[year],
                implied_balance_million_bbl=monthly_volume,
                cumulative_from_july_million_bbl=cumulative if (year, month) >= (2026, 7) else None,
                source_urls=source_url, confidence="high_arithmetic_medium_forecast",
                method="EIA world petroleum and other liquid fuels production minus consumption. Structural is the vintage/year day-weighted mean; seasonal deviation is monthly balance minus that mean.",
                interpretation="Positive is an implied build; negative is an implied draw.",
                caveat="Implied balance is not an observed stock series. Seasonal deviation is an exact descriptive decomposition, not an estimated normal seasonal effect.",
            ))

        for year in (2026, 2027):
            selected = [item for item in items if item["year"] == year]
            rows.append(row(
                row_id=f"annual-{vintage}-{year}", record_type="annual_structural_summary",
                vintage=vintage, period=str(year), period_start=f"{year}-01-01",
                period_end=f"{year}-12-31", days=sum(int(item["days"]) for item in selected),
                implied_balance_mb_d=annual_rates[year], structural_balance_mb_d=annual_rates[year],
                seasonal_deviation_mb_d=0.0, implied_balance_million_bbl=volume(selected),
                source_urls=source_url, confidence="high_arithmetic_medium_forecast",
                method="Day-weighted calendar-year mean of the monthly implied EIA balances.",
                interpretation="The annual mean is the structural component used in the monthly decomposition.",
                caveat="A forecast surplus can prompt production, demand or storage-capacity adjustments and therefore need not materialize.",
            ))

        for label, (start, end) in PERIODS.items():
            selected = [item for item in items if start <= item["date"] <= end]
            period_values[(vintage, label)] = (weighted_rate(selected), volume(selected))
            rows.append(row(
                row_id=f"period-{vintage}-{label}", record_type="period_summary",
                vintage=vintage, period=label, period_start=start.isoformat(), period_end=end.isoformat(),
                days=sum(int(item["days"]) for item in selected), implied_balance_mb_d=weighted_rate(selected),
                implied_balance_million_bbl=volume(selected), source_urls=source_url,
                confidence="high_arithmetic_medium_forecast",
                method="Sum of monthly implied balances multiplied by calendar days.",
                interpretation="Net implied build if positive and net implied draw if negative.",
                caveat="Netting hides sequencing; consult monthly rows and the July-September versus October-December summaries.",
            ))

    bridge = historical_bridge()
    frozen_active = bridge["supply_shortfall"] - bridge["expected_build"]
    scenarios = [
        ("frozen_february_surplus", bridge["expected_build"] / bridge["days"]),
        ("balanced_prewar_market", 0.0),
        ("tight_prewar_market_1mbd_draw", -1.0),
        ("tight_prewar_market_2mbd_draw", -2.0),
    ]
    for label, baseline_rate in scenarios:
        expected_balance_volume = baseline_rate * bridge["days"]
        active_burden = bridge["supply_shortfall"] - expected_balance_volume
        incremental = active_burden - frozen_active
        rows.append(row(
            row_id=f"counterfactual-{label}", record_type="historical_counterfactual_sensitivity",
            vintage="scenario", period=label, period_start="2026-03-01", period_end="2026-06-30",
            days=bridge["days"], implied_balance_mb_d=baseline_rate,
            implied_balance_million_bbl=expected_balance_volume,
            physical_supply_shortfall_million_bbl=bridge["supply_shortfall"],
            active_adjustment_burden_million_bbl=active_burden,
            incremental_burden_vs_frozen_february_million_bbl=incremental,
            pct_increase_vs_frozen_february_active_burden=100 * incremental / frozen_active,
            source_urls=f"{HISTORICAL.relative_to(ROOT)} | {FEB_URL}",
            confidence="high_arithmetic_low_counterfactual",
            method="Hold the March-June physical supply shortfall fixed and replace the pre-shock expected balance. Required active adjustment equals physical shortfall minus the counterfactual expected balance.",
            interpretation="Active adjustment means lower consumption and/or actual inventory draw; foregone accumulation is excluded.",
            caveat="Sensitivity, not a claim that the same disruption, production response and demand path would occur in a differently balanced market.",
        ))

    # Source/context record: it makes the structural interpretation auditable
    # without introducing an additional numerical series into the balance.
    rows.append(row(
        row_id="context-iea-october-2025-surplus", record_type="source_context",
        vintage="prewar_context", period="2025-2026 outlook", source_urls=IEA_SURPLUS_URL,
        confidence="high_for_quoted_context",
        method="Qualitative corroboration; not added to EIA arithmetic.",
        interpretation="IEA reported a 1.9 mb/d January-September 2025 surplus and said the 2026 overhang was approaching 4 mb/d, driven by OPEC+ and non-OPEC+ supply growth against tepid demand.",
        caveat="IEA and EIA balances use different vintages and should not be numerically combined.",
    ))

    july_aug_sep = period_values[("postshock_july_2026", "august_september_2026")]
    july_q4 = period_values[("postshock_july_2026", "october_december_2026")]
    july_2027 = period_values[("postshock_july_2026", "calendar_2027")]
    rows.extend([
        row(
            row_id="verdict-durable-buffer-credit", record_type="durability_verdict",
            vintage="postshock_july_2026", period="as_of_2026-08-05",
            implied_balance_million_bbl=0.0, source_urls=JUL_URL,
            confidence="medium_for_zero_credit_low_for_forward_path",
            method="Buffer-balance-sheet treatment: do not credit forecast accumulation as an already-held stock or engineering capacity.",
            interpretation="Defensible durable foregone-build headroom is zero. The historical 396.078 mb was a one-time avoided accumulation; later forecast surpluses are conditional flow sensitivities.",
            caveat="Zero durable credit does not mean EIA forecasts no future surplus; it prevents a forecast surplus from being represented as a banked reserve.",
        ),
        row(
            row_id="verdict-near-term-july-path", record_type="durability_verdict",
            vintage="postshock_july_2026", period="2026-08-01/2026-09-30",
            period_start="2026-08-01", period_end="2026-09-30", days=61,
            implied_balance_mb_d=july_aug_sep[0], implied_balance_million_bbl=july_aug_sep[1],
            source_urls=JUL_URL, confidence="high_arithmetic_medium_forecast",
            method="July STEO implied balance for August and September.",
            interpretation="The current post-shock path requires a further draw, so it supplies no near-term foregone-build cushion.",
            caveat="Both months were forecasts as of the July 2026 STEO.",
        ),
        row(
            row_id="verdict-later-surplus-sensitivities", record_type="durability_verdict",
            vintage="postshock_july_2026", period="Q4_2026_and_calendar_2027",
            implied_balance_mb_d=july_2027[0], implied_balance_million_bbl=july_2027[1],
            source_urls=JUL_URL, confidence="high_arithmetic_low_durability_inference",
            method="July STEO: Q4 2026 implied build is separately recorded in interpretation; numeric fields report calendar 2027.",
            interpretation=f"Conditional surplus returns in Q4 2026 ({july_q4[1]:.3f} mb, {july_q4[0]:.3f} mb/d) and expands in 2027, but should be a scenario sensitivity rather than base-case buffer capacity.",
            caveat="The July path embeds reopening and recovery assumptions. Continued current-level Strait traffic would invalidate its Gulf supply path; the February path is even staler.",
        ),
    ])

    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
