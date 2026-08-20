#!/usr/bin/env python3
"""Build a country/month ledger of non-Gulf oil-supply revisions for March-July 2026."""

from __future__ import annotations

import csv
import io
import re
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_7_nongulf_supply_ledger.csv"

FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
AUG_URL = "https://www.eia.gov/outlooks/steo/archives/aug26_base.xlsx"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEA_JUNE = "https://www.iea.org/reports/oil-market-report-june-2026"
IEA_COMMENTARY = "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"
IEA_ACTION = "https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions"

MONTHS = {
    "2026-03": ("BA", 31),
    "2026-04": ("BB", 30),
    "2026-05": ("BC", 31),
    "2026-06": ("BD", 30),
    "2026-07": ("BE", 31),
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

REGIONS = {
    "papr_CA": ("Canada", "North America", "non_gulf"),
    "papr_MX": ("Mexico", "North America", "non_gulf"),
    "papr_US": ("United States", "North America", "non_gulf"),
    "papr_AR": ("Argentina", "Central and South America", "non_gulf"),
    "papr_BR": ("Brazil", "Central and South America", "non_gulf"),
    "papr_CO": ("Colombia", "Central and South America", "non_gulf"),
    "papr_GY": ("Guyana", "Central and South America", "non_gulf"),
    "papr_NO": ("Norway", "Europe", "non_gulf"),
    "papr_UK": ("United Kingdom", "Europe", "non_gulf"),
    "papr_AJ": ("Azerbaijan", "Eurasia", "non_gulf"),
    "papr_KZ": ("Kazakhstan", "Eurasia", "non_gulf"),
    "papr_RS": ("Russia", "Eurasia", "non_gulf"),
    "papr_MU": ("Oman", "Middle East", "regional_non_hormuz_route"),
    "papr_AO": ("Angola", "Africa", "non_gulf"),
    "papr_EG": ("Egypt", "Africa", "non_gulf"),
    "papr_CH": ("China", "Asia and Oceania", "non_gulf"),
    "papr_IN": ("India", "Asia and Oceania", "non_gulf"),
    "papr_ID": ("Indonesia", "Asia and Oceania", "non_gulf"),
    "papr_MY": ("Malaysia", "Asia and Oceania", "non_gulf"),
}

GROUP_IDS = {
    "papr_nonopec": "Non-OPEC total",
    "t3b_papr_r01": "North America total",
    "t3b_papr_r02": "Central and South America total",
    "t3b_papr_r03": "Europe total",
    "t3b_papr_r04": "Eurasia total",
    "t3b_papr_r05": "Middle East total",
    "t3b_papr_r06": "Africa total",
    "t3b_papr_r07": "Asia and Oceania total",
}

FIELDS = [
    "row_id", "record_type", "country", "region", "route_exposure_class", "period",
    "days", "metric", "taxonomy", "february_forecast_mb_per_day",
    "august_vintage_mb_per_day", "revision_mb_per_day", "revision_million_bbl",
    "cumulative_revision_million_bbl", "source_value_unit", "accounting_eligible", "data_status",
    "publication_vintage", "confidence", "source_url", "source_detail",
    "interpretation", "double_counting_note",
]


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t")) for item in root.findall("m:si", NS)]


def extract_sheet_rows(workbook: bytes, sheet_number: int) -> dict[str, dict[str, float | str]]:
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        strings = shared_strings(archive)
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
        rows: dict[str, dict[str, float | str]] = {}
        for row_node in root.findall(".//m:row", NS):
            cells: dict[str, str] = {}
            for cell in row_node.findall("m:c", NS):
                value = cell.find("m:v", NS)
                if value is None:
                    continue
                column = re.match(r"[A-Z]+", cell.attrib["r"])
                if column is None:
                    continue
                raw = value.text or ""
                cells[column.group()] = strings[int(raw)] if cell.attrib.get("t") == "s" else raw
            row_id = cells.get("A", "")
            if not row_id:
                continue
            parsed: dict[str, float | str] = {"label": cells.get("B", "")}
            valid = True
            for month, (column, _) in MONTHS.items():
                try:
                    parsed[month] = float(cells[column])
                except (KeyError, ValueError):
                    valid = False
            if valid:
                rows[row_id] = parsed
        return rows


def blank_row(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    for key, value in values.items():
        if isinstance(value, float):
            result[key] = f"{value:.6f}".rstrip("0").rstrip(".")
        else:
            result[key] = str(value)
    return result


def build() -> list[dict[str, str]]:
    feb_book = download(FEB_URL)
    aug_book = download(AUG_URL)
    feb = extract_sheet_rows(feb_book, 6)  # STEO Table 3b, non-OPEC total liquids
    aug = extract_sheet_rows(aug_book, 6)
    feb_3c = extract_sheet_rows(feb_book, 7)  # accounting reconciliation groups
    aug_3c = extract_sheet_rows(aug_book, 7)

    rows: list[dict[str, str]] = []
    cumulative: dict[str, float] = defaultdict(float)
    country_totals: dict[str, float] = {}

    for eia_id, (country, region, exposure) in REGIONS.items():
        if eia_id not in feb or eia_id not in aug:
            raise ValueError(f"Missing common EIA row {eia_id}")
        for month, (_, days) in MONTHS.items():
            frozen = float(feb[eia_id][month])
            updated = float(aug[eia_id][month])
            rate = updated - frozen
            volume = rate * days
            cumulative[eia_id] += volume
            rows.append(blank_row(
                row_id=f"m8q7-{eia_id.removeprefix('papr_').lower()}-{month.replace('-', '')}",
                record_type="country_month",
                country=country,
                region=region,
                route_exposure_class=exposure,
                period=month,
                days=days,
                metric="petroleum_and_other_liquid_fuels_production_revision",
                taxonomy="petroleum_and_other_liquid_fuels",
                february_forecast_mb_per_day=frozen,
                august_vintage_mb_per_day=updated,
                revision_mb_per_day=rate,
                revision_million_bbl=volume,
                cumulative_revision_million_bbl=cumulative[eia_id],
                source_value_unit="mb/d; million_bbl after calendar-day conversion",
                accounting_eligible="yes",
                data_status="preliminary_estimate" if month < "2026-07" else "forecast",
                publication_vintage="2026-08-11 (forecast completed 2026-08-06)",
                confidence="medium_high",
                source_url=f"{FEB_URL}|{AUG_URL}",
                source_detail="EIA STEO Table 3b; August vintage minus frozen February vintage for the same country/month.",
                interpretation="Positive values are extra production relative to the frozen forecast; negative values are additional shortfalls. They are cushions/revisions, not a causal Hormuz attribution.",
                double_counting_note="Do not add a country's exports or IEA collective-action commitment to this production revision without an overlap reconciliation.",
            ))
        country_totals[eia_id] = cumulative[eia_id]
        rows.append(blank_row(
            row_id=f"m8q7-{eia_id.removeprefix('papr_').lower()}-mar-jul-summary",
            record_type="country_period_summary",
            country=country,
            region=region,
            route_exposure_class=exposure,
            period="2026-03-01/2026-07-31",
            days=153,
            metric="cumulative_petroleum_and_other_liquid_fuels_production_revision",
            taxonomy="petroleum_and_other_liquid_fuels",
            revision_million_bbl=country_totals[eia_id],
            cumulative_revision_million_bbl=country_totals[eia_id],
            source_value_unit="million_bbl",
            accounting_eligible="yes",
            data_status="March-July preliminary estimates",
            publication_vintage="2026-08-11 (forecast completed 2026-08-06)",
            confidence="medium_high",
            source_url=f"{FEB_URL}|{AUG_URL}",
            source_detail="Sum of five monthly EIA vintage differences times calendar days.",
            interpretation="Signed cumulative production revision versus the frozen February forecast.",
            double_counting_note="This summary is the sum of the country-month rows and must not be added to them.",
        ))

    # Regional totals retain countries omitted from Table 3b, but the Middle East
    # total has a cross-vintage classification break and is context only.
    region_totals: dict[str, float] = {}
    for eia_id, label in GROUP_IDS.items():
        total = sum((float(aug[eia_id][m]) - float(feb[eia_id][m])) * days for m, (_, days) in MONTHS.items())
        region_totals[label] = total
        classification_break = label in {"Non-OPEC total", "Middle East total"}
        rows.append(blank_row(
            row_id=f"m8q7-group-{eia_id.lower()}-mar-jul",
            record_type="regional_reconciliation",
            country=label,
            region=label,
            route_exposure_class="mixed",
            period="2026-03-01/2026-07-31",
            days=153,
            metric="cumulative_petroleum_and_other_liquid_fuels_production_revision",
            taxonomy="petroleum_and_other_liquid_fuels",
            revision_million_bbl=total,
            cumulative_revision_million_bbl=total,
            source_value_unit="million_bbl",
            accounting_eligible="context_only" if classification_break else "yes_after_overlap_check",
            data_status="March-July preliminary estimates",
            publication_vintage="2026-08-11 (forecast completed 2026-08-06)",
            confidence="low_for_cross_vintage_comparison" if classification_break else "medium_high",
            source_url=f"{FEB_URL}|{AUG_URL}",
            source_detail="EIA STEO Table 3b regional aggregate, August vintage minus frozen February vintage.",
            interpretation=("Composition/classification changed across vintages; do not interpret this group delta as a geographic supply response."
                            if classification_break else "Regional cross-check including EIA countries not separately displayed."),
            double_counting_note="Contains the named country rows in the same region; never add both.",
        ))

    positive = sum(value for value in country_totals.values() if value > 0)
    negative = sum(value for value in country_totals.values() if value < 0)
    net = positive + negative
    for name, value, interpretation in [
        ("identified_positive_additions", positive, "Gross positive revisions among common named non-Gulf and Oman rows."),
        ("identified_negative_revisions", negative, "Offsetting negative revisions among the same common named rows."),
        ("identified_named_net", net, "Net of positive and negative revisions among common named rows; not the full world outside-Gulf residual."),
    ]:
        rows.append(blank_row(
            row_id=f"m8q7-summary-{name}", record_type="ledger_summary", country="Named supplier ledger",
            region="World excluding Hormuz-dependent Gulf producers", route_exposure_class="non_gulf_and_oman",
            period="2026-03-01/2026-07-31", days=153, metric=name,
            taxonomy="petroleum_and_other_liquid_fuels", revision_million_bbl=value,
            cumulative_revision_million_bbl=value, accounting_eligible="yes_as_ledger_subtotal",
            source_value_unit="million_bbl",
            data_status="March-July preliminary estimates", publication_vintage="2026-08-11",
            confidence="medium", source_url=f"{FEB_URL}|{AUG_URL}",
            source_detail="Arithmetic over common named country rows in EIA STEO Table 3b.",
            interpretation=interpretation,
            double_counting_note="Subtotal of country rows; not additive to its components or regional totals.",
        ))

    americas = region_totals["North America total"] + region_totals["Central and South America total"]
    other_non_middle_east = sum(region_totals[name] for name in [
        "Europe total", "Eurasia total", "Africa total", "Asia and Oceania total"
    ])
    non_middle_east = americas + other_non_middle_east
    for name, value, interpretation in [
        ("americas_complete_regional_revision", americas, "Complete EIA Americas regional revision; includes countries not separately displayed in Table 3b."),
        ("other_non_middle_east_regional_revision", other_non_middle_east, "Complete Europe, Eurasia, Africa, and Asia/Oceania regional revision, net of positive and negative countries."),
        ("non_middle_east_complete_regional_net", non_middle_east, "Complete net revision outside EIA's Middle East region; the cleanest EIA estimate of the non-Middle-East production cushion."),
    ]:
        rows.append(blank_row(
            row_id=f"m8q7-summary-{name}", record_type="ledger_summary", country="Regional supply ledger",
            region="Outside Middle East", route_exposure_class="non_middle_east",
            period="2026-03-01/2026-07-31", days=153, metric=name,
            taxonomy="petroleum_and_other_liquid_fuels", revision_million_bbl=value,
            cumulative_revision_million_bbl=value, accounting_eligible="yes_as_regional_subtotal",
            source_value_unit="million_bbl",
            data_status="March-July preliminary estimates", publication_vintage="2026-08-11",
            confidence="medium_high_for_revision_low_for_hormuz_attribution", source_url=f"{FEB_URL}|{AUG_URL}",
            source_detail="Arithmetic over non-overlapping EIA STEO Table 3b regional aggregates.",
            interpretation=interpretation,
            double_counting_note="Subtotal of regional rows; do not add to country rows or its component regions.",
        ))

    # Exact Table 3c identity. It is retained to show scale and the unallocated
    # remainder, not to pretend that OPEC+ is a clean Gulf/non-Gulf boundary.
    identity_ids = {
        "papr_world": "World total revision",
        "papr_opecplus": "OPEC+ total revision",
        "papr_us": "United States revision",
        "papr_nonopecplus_xus": "Non-OPEC+ excluding United States revision",
    }
    identity_values: dict[str, float] = {}
    for eia_id, label in identity_ids.items():
        value = sum((float(aug_3c[eia_id][m]) - float(feb_3c[eia_id][m])) * days for m, (_, days) in MONTHS.items())
        identity_values[eia_id] = value
        rows.append(blank_row(
            row_id=f"m8q7-global-identity-{eia_id}", record_type="global_accounting_reconciliation",
            country=label, region="World", route_exposure_class="mixed", period="2026-03-01/2026-07-31",
            days=153, metric="cumulative_petroleum_and_other_liquid_fuels_production_revision",
            taxonomy="petroleum_and_other_liquid_fuels", revision_million_bbl=value,
            cumulative_revision_million_bbl=value, accounting_eligible="reconciliation_only",
            source_value_unit="million_bbl",
            data_status="March-July preliminary estimates", publication_vintage="2026-08-11",
            confidence="high_for_arithmetic_low_for_hormuz_attribution", source_url=f"{FEB_URL}|{AUG_URL}",
            source_detail="EIA STEO Table 3c exact classification identity.",
            interpretation="This closes the global forecast revision but OPEC+ is not a clean Gulf boundary and membership/classification changed across vintages.",
            double_counting_note="Reconciliation frame only; do not add to country or regional rows.",
        ))
    closed = identity_values["papr_opecplus"] + identity_values["papr_us"] + identity_values["papr_nonopecplus_xus"]
    if abs(closed - identity_values["papr_world"]) > 0.01:
        raise ValueError("Table 3c world identity does not close")

    # Non-additive primary-source cross-checks and policy commitments.
    context_rows = [
        ("iea-americas-growth-revision", "forecast_cross_check", "Americas", "annual_2026", "annual_supply_growth_forecast_revision", 0.6, "mb/d", IEA_MAY, "2026-05-13", "postshock_forecast_revision",
         "IEA said expected 2026 Americas supply growth was revised up by more than 0.6 mb/d since the start of the year, to 1.5 mb/d.",
         "context_only", "Lower-bound annual growth revision; compare with, do not add to, the monthly EIA Americas revisions."),
        ("iea-atlantic-export-shift", "trade_flow_context", "Atlantic Basin to East of Suez", "since_2026-02_to_2026-06-17", "change_in_crude_exports", 3.5, "mb/d", IEA_JUNE, "2026-06-17", "observed_estimate",
         "IEA attributed the rise to robust Americas growth plus steep US SPR releases; its commentary named the US, Kazakhstan, Brazil and Venezuela as the biggest output gains.",
         "no", "Mixes production, government stocks and cargo redirection; never use 3.5 mb/d as incremental production."),
        ("iea-us-may-exports", "trade_flow_context", "United States", "2026-05", "total_crude_and_petroleum_product_exports", 13.1, "mb/d", IEA_COMMENTARY, "2026-06-22", "observed_estimate",
         "IEA reported record May exports, nearly one-quarter above May 2025, supported by production plus industry and government stock draws.",
         "no", "Export level, not increment; includes products and stock draw already represented elsewhere."),
        ("iea-canada-production-commitment", "policy_production_commitment", "Canada", "announced_2026-03-19", "collective_action_production_increase", 23.6, "million_bbl", IEA_ACTION, "2026-03-19", "provisional_commitment",
         "IEA's provisional collective-action table classified Canada's full contribution as a production increase.",
         "no_until_observed", "Announcement is not measured output; compare with, do not add to, the August-vintage EIA production revision."),
        ("iea-mexico-production-commitment", "policy_production_commitment", "Mexico", "announced_2026-03-19", "collective_action_production_increase", 3.9, "million_bbl", IEA_ACTION, "2026-03-19", "provisional_commitment",
         "IEA's provisional collective-action table classified Mexico's full contribution as a production increase.",
         "no_separate_addition", "Likely overlaps the EIA March-July production revision; do not add both."),
    ]
    for row_id, record_type, country, period, metric, value, unit, url, vintage, status, detail, eligible, note in context_rows:
        rows.append(blank_row(
            row_id=row_id, record_type=record_type, country=country, region="", route_exposure_class="mixed",
            period=period, metric=metric, taxonomy="total_oil_or_source_definition",
            revision_mb_per_day=value if unit == "mb/d" else "",
            revision_million_bbl=value if unit == "million_bbl" else "",
            source_value_unit=unit, accounting_eligible=eligible, data_status=status,
            publication_vintage=vintage,
            confidence="medium", source_url=url, source_detail=detail,
            interpretation="Primary-source cross-check or mechanism evidence; not a country production-accounting row.",
            double_counting_note=note,
        ))

    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
