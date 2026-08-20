#!/usr/bin/env python3
"""Country-resolve the March-June 2026 demand-vintage gap.

The EIA February-to-July STEO difference exists only for selected countries and
seven regions.  This builder therefore preserves three distinct evidence types:

1. exact STEO country/region vintage differences;
2. JODI March-May year-on-year apparent-product-demand cross-checks; and
3. explicitly low-fidelity, baseline-share allocations that close the otherwise
   unresolved Middle East, Asia/Oceania and Africa regional buckets.

The allocations are accounting scaffolds, not observations or causal estimates.
"""

from __future__ import annotations

import calendar
import csv
import io
import re
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_10_country_demand_resolution.csv"
M8Q8 = ROOT / "data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv"
P2K3 = ROOT / "data/derived/hormuz_p2k_3_demand_cost_tier_matrix.csv"

FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
EIA_RANKING_URL = (
    "https://www.eia.gov/international/rankings/country/PRI?"
    "aid=2&f=A&pid=5&u=0&v=none&y=01%2F01%2F2024"
)
JODI_2025_URL = (
    "https://www.jodidata.org/_resources/files/downloads/oil-data/annual-csv/"
    "secondary/2025.csv"
)
JODI_2026_URL = (
    "https://www.jodidata.org/_resources/files/downloads/oil-data/annual-csv/"
    "secondary/secondaryyear2026.csv"
)
JODI_GUIDE_URL = (
    "https://www.jodidata.org/oil/support/user-guide/"
    "data-available-in-the-jodi-oil-world-database.aspx"
)

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
MONTH_COLUMNS = {"2026-03": "BA", "2026-04": "BB", "2026-05": "BC", "2026-06": "BD"}
BASELINE_2024_COLUMNS = ["AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL"]

FIELDS = [
    "row_id", "record_type", "region", "country", "parent_row_id",
    "period_start", "period_end", "period_role", "value_low_million_bbl",
    "value_base_million_bbl", "value_high_million_bbl", "unit",
    "baseline_2024_mb_per_day", "share_of_parent_pct", "allocation_method",
    "fidelity", "evidence_status", "jodi_march_may_gap_million_bbl",
    "jodi_months_available", "current_cost_tier", "source_url", "source_row_ids",
    "method", "interpretation", "caveat", "double_counting_rule",
]

# EIA International Energy Statistics 2024 petroleum-and-other-liquids
# consumption ranking, mb/d.  Qatar is the same portal's 2024 country value.
BASELINE_MBD = {
    "Saudi Arabia": 3.631, "Iran": 1.970, "Iraq": 1.061,
    "United Arab Emirates": 0.878, "Kuwait": 0.419, "Qatar": 0.276,
    "South Korea": 2.515, "Taiwan": 0.871, "Singapore": 1.482,
    "Indonesia": 1.627, "Thailand": 1.372, "Vietnam": 0.555,
    "Malaysia": 0.747, "Australia": 1.145, "Philippines": 0.473,
    "Egypt": 0.953, "South Africa": 0.612, "Nigeria": 0.493,
    "Algeria": 0.457, "Kenya": 0.116,
}

JODI_CODES = {
    "Saudi Arabia": "SA", "Iran": "IR", "Iraq": "IQ",
    "United Arab Emirates": "AE", "Kuwait": "KW", "Qatar": "QA",
    "South Korea": "KR", "Taiwan": "TW", "Singapore": "SG",
    "Indonesia": "ID", "Thailand": "TH", "Vietnam": "VN",
    "Malaysia": "MY", "Australia": "AU", "Philippines": "PH",
    "Egypt": "EG", "South Africa": "ZA", "Nigeria": "NG",
    "Algeria": "DZ", "Kenya": "KE",
}

COST_TIER = {
    "Saudi Arabia": "2", "United Arab Emirates": "2", "Iran": "3",
    "Iraq": "3", "Kuwait": "3", "Qatar": "3", "Other Middle East": "2_to_3",
    "South Korea": "2_to_3", "Taiwan": "unknown", "Singapore": "1",
    "Indonesia": "1_to_2", "Thailand": "2", "Vietnam": "unknown",
    "Malaysia": "2", "Australia": "unknown", "Philippines": "1_to_3_mixed",
    "Other Asia and Oceania": "unknown", "Egypt": "2", "South Africa": "unknown",
    "Nigeria": "2_to_3", "Algeria": "2_to_3", "Kenya": "3",
    "Other Africa": "2_to_3",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    unknown = set(values) - set(FIELDS)
    if unknown:
        raise ValueError(f"Unknown fields: {sorted(unknown)}")
    result.update({key: fmt(value) for key, value in values.items()})
    return result


def workbook_rows(workbook: bytes, sheet_number: int = 9) -> dict[str, dict[str, str]]:
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
                match = re.match(r"[A-Z]+", cell.attrib["r"])
                if value is None or match is None:
                    continue
                raw = value.text or ""
                cells[match.group()] = strings[int(raw)] if cell.attrib.get("t") == "s" else raw
            if cells.get("A"):
                output[cells["A"]] = cells
        return output


def annual_2024_rate(item: dict[str, str]) -> float:
    return sum(
        float(item[column]) * calendar.monthrange(2024, month)[1]
        for month, column in enumerate(BASELINE_2024_COLUMNS, start=1)
    ) / 366


def steo_gap(feb: dict[str, str], july: dict[str, str]) -> float:
    return sum(
        (float(feb[column]) - float(july[column])) * calendar.monthrange(2026, int(month[-2:]))[1]
        for month, column in MONTH_COLUMNS.items()
    )


def jodi_totals(data: bytes) -> dict[tuple[str, str], float | None]:
    output: dict[tuple[str, str], float | None] = {}
    for item in csv.DictReader(io.StringIO(data.decode("utf-8-sig"))):
        if item["UNIT_MEASURE"] != "KBBL" or item["ENERGY_PRODUCT"] != "TOTPRODS":
            continue
        if item["FLOW_BREAKDOWN"] != "TOTDEMO":
            continue
        if item["TIME_PERIOD"] not in {
            "2025-03", "2025-04", "2025-05", "2026-03", "2026-04", "2026-05"
        }:
            continue
        raw = item["OBS_VALUE"]
        output[(item["REF_AREA"], item["TIME_PERIOD"])] = (
            None if raw in {"", "-", "x"} else float(raw) / 1000.0
        )
    return output


def jodi_crosscheck(country: str, values: dict[tuple[str, str], float | None]) -> tuple[float | None, str]:
    code = JODI_CODES[country]
    differences: list[float] = []
    months: list[str] = []
    for month in ("03", "04", "05"):
        prior = values.get((code, f"2025-{month}"))
        current = values.get((code, f"2026-{month}"))
        if prior is None or current is None:
            continue
        # A zero current total against material prior demand is a missing/not-
        # submitted encoding for this purpose, not a 100% demand collapse.
        if current == 0 and prior > 1:
            continue
        differences.append(prior - current)
        months.append(month)
    return (sum(differences), ",".join(months)) if differences else (None, "")


def existing_korea_imputation() -> float:
    with M8Q8.open(newline="") as handle:
        rows = [
            item for item in csv.DictReader(handle)
            if item["row_id"].startswith("korea-demand-inference-2026")
            and item["observation_month"] in MONTH_COLUMNS
        ]
    if len(rows) != 4:
        raise ValueError("Expected four March-June South Korea imputation rows")
    return sum(float(item["value_base"]) for item in rows)


def add_allocation_rows(
    rows: list[dict[str, str]], *, region: str, parent_id: str, parent_value: float,
    countries: list[str], region_baseline: float, method_name: str,
    jodi: dict[tuple[str, str], float | None], source_ids: str,
) -> None:
    named_baseline = sum(BASELINE_MBD[country] for country in countries)
    other_name = f"Other {region}"
    other_baseline = region_baseline - named_baseline
    if other_baseline <= 0:
        raise ValueError(f"Non-positive other-country baseline for {region}: {other_baseline}")
    weights = {country: BASELINE_MBD[country] for country in countries}
    weights[other_name] = other_baseline
    if abs(sum(weights.values()) - region_baseline) > 1e-9:
        raise ValueError(f"Baseline weights do not close for {region}")
    allocated = 0.0
    for country, weight in weights.items():
        # Publish a ledger that closes at its displayed six-decimal precision.
        # The residual "Other" row absorbs only the sub-barrel rounding dust.
        value = (
            round(parent_value - allocated, 6)
            if country == other_name
            else round(parent_value * weight / region_baseline, 6)
        )
        allocated += value
        gap, months = (None, "") if country == other_name else jodi_crosscheck(country, jodi)
        rows.append(row(
            row_id=f"allocation-{re.sub(r'[^a-z0-9]+', '-', region.lower()).strip('-')}-"
                   f"{re.sub(r'[^a-z0-9]+', '-', country.lower()).strip('-')}",
            record_type="project_country_allocation", region=region, country=country,
            parent_row_id=parent_id, period_start="2026-03-01", period_end="2026-06-30",
            period_role="matched_historical_preliminary", value_base_million_bbl=value,
            unit="million_bbl", baseline_2024_mb_per_day=weight,
            share_of_parent_pct=100 * value / parent_value,
            allocation_method=method_name, fidelity="low_project_imputation",
            evidence_status="regional_counterfactual_allocated_by_pre_shock_consumption_share",
            jodi_march_may_gap_million_bbl=gap, jodi_months_available=months,
            current_cost_tier=COST_TIER[country],
            source_url=f"{EIA_RANKING_URL} | {FEB_URL} | {JUL_URL} | {JODI_2025_URL} | {JODI_2026_URL}",
            source_row_ids=source_ids,
            method="Allocate the matched EIA regional February-to-July vintage gap in proportion to EIA 2024 petroleum-and-other-liquids consumption. JODI March-May year-on-year apparent-product demand is a non-additive cross-check only.",
            interpretation="A closing country scaffold for pressure-location analysis, not an observed country demand loss.",
            caveat="Neutral baseline-share allocation ignores unequal outage severity, trade, inventories, ordinary revision and product mix. JODI uses a different year-on-year counterfactual and often has missing stock data.",
            double_counting_rule=f"Nested inside {parent_id}; use country allocations or the parent, never both.",
        ))


def build() -> list[dict[str, str]]:
    feb = workbook_rows(fetch(FEB_URL))
    july = workbook_rows(fetch(JUL_URL))
    jodi = jodi_totals(fetch(JODI_2025_URL))
    jodi.update(jodi_totals(fetch(JODI_2026_URL)))
    rows: list[dict[str, str]] = []

    specs = {
        "patc_world": ("World", "World", "headline"),
        "patc_r01": ("North America", "North America", "region"),
        "patc_r02": ("Central and South America", "Central and South America", "region"),
        "patc_r03": ("Europe", "Europe", "region"),
        "patc_r04": ("Eurasia", "Eurasia", "region"),
        "patc_r05": ("Middle East", "Middle East", "region"),
        "patc_r06": ("Africa", "Africa", "region"),
        "patc_r07": ("Asia and Oceania", "Asia and Oceania", "region"),
        "patc_ch": ("Asia and Oceania", "China", "country"),
        "patc_in": ("Asia and Oceania", "India", "country"),
        "patc_ja": ("Asia and Oceania", "Japan", "country"),
        "patc_br": ("Central and South America", "Brazil", "country"),
        "patc_rs": ("Eurasia", "Russia", "country"),
    }
    exact: dict[str, float] = {}
    for mnemonic, (region, country, level) in specs.items():
        value = steo_gap(feb[mnemonic], july[mnemonic])
        exact[mnemonic] = value
        parent = "" if level == "headline" else (
            "exact-world" if level == "region" else f"exact-region-{re.sub(r'[^a-z0-9]+', '-', region.lower()).strip('-')}"
        )
        rows.append(row(
            row_id="exact-world" if level == "headline" else
                   (f"exact-region-{re.sub(r'[^a-z0-9]+', '-', region.lower()).strip('-')}" if level == "region" else
                    f"exact-country-{country.lower().replace(' ', '-') }"),
            record_type=f"eia_{level}_vintage_difference", region=region, country=country,
            parent_row_id=parent, period_start="2026-03-01", period_end="2026-06-30",
            period_role="matched_historical_preliminary", value_low_million_bbl=value,
            value_base_million_bbl=value, value_high_million_bbl=value, unit="million_bbl",
            allocation_method="direct_EIA_STEO_country_or_region_row", fidelity="medium_high_arithmetic_low_causal",
            evidence_status="published_forecast_vintage_difference", source_url=f"{FEB_URL} | {JUL_URL}",
            source_row_ids=f"demand-{mnemonic}-202603 through 202606",
            method="Frozen February STEO minus July-vintage consumption for March-June, multiplied by calendar days.",
            interpretation="Positive means consumption below the frozen February path; July forecast is excluded.",
            caveat="The vintage difference includes ordinary revisions and contemporaneous shocks and is not a controlled causal estimate.",
            double_counting_rule=("World equals the seven region rows." if level == "headline" else
                                  "Country rows are nested inside their region; region rows are nested inside World."),
        ))

    world_regions = sum(exact[key] for key in ["patc_r01", "patc_r02", "patc_r03", "patc_r04", "patc_r05", "patc_r06", "patc_r07"])
    if abs(world_regions - exact["patc_world"]) > 2e-5:
        raise ValueError(f"Regional gaps do not close to world: {world_regions} vs {exact['patc_world']}")

    # Middle East: no STEO country rows.  Allocate the whole matched regional gap.
    add_allocation_rows(
        rows, region="Middle East", parent_id="exact-region-middle-east",
        parent_value=exact["patc_r05"],
        countries=["Saudi Arabia", "Iran", "Iraq", "United Arab Emirates", "Kuwait", "Qatar"],
        region_baseline=annual_2024_rate(july["patc_r05"]),
        method_name="neutral_2024_consumption_share_allocation",
        jodi=jodi, source_ids="p2k.3 mena-iraq-kuwait-qatar | mena-saudi-uae | mena-iran",
    )

    # Asia/Oceania: remove exact China/India/Japan first.  South Korea remains
    # the existing 24.4 mb March-June project imputation and is never added twice.
    asia_residual = exact["patc_r07"] - exact["patc_ch"] - exact["patc_in"] - exact["patc_ja"]
    rows.append(row(
        row_id="residual-asia-oceania-ex-china-india-japan", record_type="arithmetic_residual",
        region="Asia and Oceania", country="Asia and Oceania excluding China India and Japan",
        parent_row_id="exact-region-asia-and-oceania", period_start="2026-03-01", period_end="2026-06-30",
        period_role="matched_historical_preliminary", value_low_million_bbl=asia_residual,
        value_base_million_bbl=asia_residual, value_high_million_bbl=asia_residual, unit="million_bbl",
        allocation_method="parent_minus_exact_named_countries", fidelity="medium_high_arithmetic_low_causal",
        evidence_status="arithmetic_residual", source_url=f"{FEB_URL} | {JUL_URL}",
        source_row_ids="exact-country-china | exact-country-india | exact-country-japan",
        method="Asia/Oceania regional vintage gap minus exact STEO China, India and Japan gaps.",
        interpretation="Matched March-June unresolved Asian denominator; it is 115.375 mb, not the 146.2 mb March-July figure.",
        caveat="Still contains ordinary revision and all unlisted Asia/Oceania countries.",
        double_counting_rule="Use this residual or its country allocations, never both.",
    ))
    korea_value = existing_korea_imputation()
    korea_jodi, korea_months = jodi_crosscheck("South Korea", jodi)
    rows.append(row(
        row_id="allocation-asia-and-oceania-south-korea", record_type="existing_country_imputation",
        region="Asia and Oceania", country="South Korea",
        parent_row_id="residual-asia-oceania-ex-china-india-japan", period_start="2026-03-01", period_end="2026-06-30",
        period_role="matched_historical_preliminary", value_base_million_bbl=korea_value, unit="million_bbl",
        baseline_2024_mb_per_day=BASELINE_MBD["South Korea"], share_of_parent_pct=100 * korea_value / asia_residual,
        allocation_method="existing_m8q8_project_imputation", fidelity="low_project_imputation",
        evidence_status="project_imputation_with_partial_JODI_crosscheck",
        jodi_march_may_gap_million_bbl=korea_jodi, jodi_months_available=korea_months,
        current_cost_tier=COST_TIER["South Korea"],
        source_url=f"{M8Q8.relative_to(ROOT)} | {JODI_2025_URL} | {JODI_2026_URL}",
        source_row_ids="korea-demand-inference-202603 through 202606 | p2k.3 korea-petrochemical-refining",
        method="Retain the existing 6.2/6.0/6.2/6.0 mb monthly imputation. JODI's 36.83 mb March-May year-on-year apparent-product contraction is a differently defined cross-check, not a replacement.",
        interpretation="South Korea remains a nested 24.4 mb imputation; public evidence confirms deep contraction but not the same frozen-February counterfactual.",
        caveat="JODI apparent demand includes trade, refinery and missing-stock mechanics; June was unavailable at the cutoff.",
        double_counting_rule="Inside the 115.375 mb Asia residual. Subtract before allocating the remainder and never add to the parent.",
    ))
    asia_remainder = asia_residual - korea_value
    asia_region_baseline = annual_2024_rate(july["patc_r07"])
    exact_named_baseline = 16.371 + 5.599 + 3.140 + BASELINE_MBD["South Korea"]
    residual_after_korea_baseline = asia_region_baseline - exact_named_baseline
    add_allocation_rows(
        rows, region="Asia and Oceania", parent_id="residual-asia-oceania-after-south-korea",
        parent_value=asia_remainder,
        countries=["Taiwan", "Singapore", "Indonesia", "Thailand", "Vietnam", "Malaysia", "Australia", "Philippines"],
        region_baseline=residual_after_korea_baseline,
        method_name="neutral_2024_consumption_share_after_exact_and_korea",
        jodi=jodi,
        source_ids="p2k.3 Southeast Asia country cells; South Korea already removed",
    )
    rows.append(row(
        row_id="residual-asia-oceania-after-south-korea", record_type="arithmetic_residual",
        region="Asia and Oceania", country="Residual after South Korea",
        parent_row_id="residual-asia-oceania-ex-china-india-japan", period_start="2026-03-01", period_end="2026-06-30",
        period_role="matched_historical_preliminary", value_base_million_bbl=asia_remainder, unit="million_bbl",
        allocation_method="asia_residual_minus_existing_korea_imputation", fidelity="medium_arithmetic_low_allocation",
        evidence_status="arithmetic_residual", source_url=str(M8Q8.relative_to(ROOT)),
        source_row_ids="allocation-asia-and-oceania-south-korea",
        method="Subtract 24.4 mb South Korea imputation from the matched 115.375 mb residual.",
        interpretation="Denominator allocated across Taiwan, Singapore, Indonesia, Thailand, Vietnam, Malaysia, Australia, Philippines and other Asia/Oceania.",
        caveat="The country split below is a baseline-share scaffold.",
        double_counting_rule="Use this row or its allocations, never both.",
    ))

    # Africa is not required for exact closure of the two largest buckets, but
    # resolving it improves the subsequent demand-pressure landing scenarios.
    add_allocation_rows(
        rows, region="Africa", parent_id="exact-region-africa", parent_value=exact["patc_r06"],
        countries=["Egypt", "South Africa", "Nigeria", "Algeria", "Kenya"],
        region_baseline=annual_2024_rate(july["patc_r06"]),
        method_name="neutral_2024_consumption_share_allocation", jodi=jodi,
        source_ids="p2k.3 africa-egypt-conservation | africa-transport-food | africa-kenya-lpg | africa-south-africa",
    )

    rows.append(row(
        row_id="method-jodi-comparability", record_type="methodology", region="Global", country="JODI-covered countries",
        period_start="2026-03-01", period_end="2026-05-31", period_role="crosscheck_only", unit="text",
        allocation_method="none", fidelity="varies_by_country", evidence_status="official_apparent_product_demand_crosscheck",
        source_url=f"{JODI_2025_URL} | {JODI_2026_URL} | {JODI_GUIDE_URL}",
        method="For valid TOTPRODS/TOTDEMO submissions, calculate 2025 minus 2026 March-May apparent-product demand. Exclude missing and implausible zero encodings.",
        interpretation="Useful for direction and scale, but not a February-STEO counterfactual and not necessarily final use.",
        caveat="Stock coverage, refinery/trade treatment and submission completeness vary; June was not available at build time.",
        double_counting_rule="JODI values are memo cross-checks embedded in allocation rows; never add them to EIA gaps.",
    ))

    # Closing checks for each allocated parent.
    groups = {
        "exact-region-middle-east": exact["patc_r05"],
        "residual-asia-oceania-after-south-korea": asia_remainder,
        "exact-region-africa": exact["patc_r06"],
    }
    for parent, expected in groups.items():
        actual = sum(
            float(item["value_base_million_bbl"])
            for item in rows
            if item["record_type"] == "project_country_allocation" and item["parent_row_id"] == parent
        )
        if abs(actual - expected) > 1e-5:
            raise ValueError(f"{parent} allocations do not close: {actual} vs {expected}")
    if abs(korea_value + asia_remainder - asia_residual) > 1e-6:
        raise ValueError("South Korea nesting does not close")
    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
