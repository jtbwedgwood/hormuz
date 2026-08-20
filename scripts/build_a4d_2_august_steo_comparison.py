#!/usr/bin/env python3
"""Build the August STEO refresh audit against frozen February and July vintages."""

from __future__ import annotations

import calendar
import csv
import io
import math
import re
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_a4d_2_august_steo_comparison.csv"
FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
AUG_URL = "https://www.eia.gov/outlooks/steo/archives/aug26_base.xlsx"
AUG_PDF = "https://www.eia.gov/outlooks/steo/archives/aug26.pdf"
IEA_ROUTE = "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
MONTHS = {
    "2026-03": ("BA", 31), "2026-04": ("BB", 30), "2026-05": ("BC", 31),
    "2026-06": ("BD", 30), "2026-07": ("BE", 31),
}
FRAMES = {
    "march_june": ["2026-03", "2026-04", "2026-05", "2026-06"],
    "march_july": list(MONTHS),
}
COUNTRIES = {
    "papr_US": "United States", "papr_BR": "Brazil", "papr_RS": "Russia",
    "papr_GY": "Guyana", "papr_MX": "Mexico", "papr_AR": "Argentina",
    "papr_CA": "Canada", "papr_MY": "Malaysia", "papr_IN": "India",
    "papr_NO": "Norway", "papr_MU": "Oman",
}
REGIONAL_IDS = [
    "t3b_papr_r01", "t3b_papr_r02", "t3b_papr_r03", "t3b_papr_r04",
    "t3b_papr_r06", "t3b_papr_r07",
]
BASELINE_YEARS = [2017, 2018, 2019, 2023, 2024, 2025]

# August STEO Table 1. March-May is a single period-average rate.
GULF_SHUTINS = {
    "Kuwait": (1.400, 1.250, 0.950), "United Arab Emirates": (1.450, 0.000, 0.000),
    "Iran": (0.110, 0.580, 0.100), "Iraq": (2.820, 2.530, 1.860),
    "Qatar": (0.450, 0.420, 0.350), "Bahrain": (0.120, 0.150, 0.130),
    "Saudi Arabia": (2.500, 2.550, 2.070),
}

FIELDS = [
    "row_id", "record_type", "frame", "period_start", "period_end", "days",
    "metric", "geography", "august_value", "july_value", "delta_vs_july",
    "unit", "frozen_vintage", "comparison_vintage", "data_status", "source_url",
    "source_locator", "method", "interpretation", "confidence", "caveat",
]


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def workbook_rows(workbook: bytes, sheet: int) -> dict[str, dict[str, str]]:
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = [
            "".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t"))
            for item in strings_root.findall("m:si", NS)
        ]
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet}.xml"))
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


def blank(**values: object) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    for key, value in values.items():
        if key not in row:
            raise KeyError(key)
        row[key] = f"{value:.6f}".rstrip("0").rstrip(".") if isinstance(value, float) else str(value)
    return row


def volume(first: dict[str, str], second: dict[str, str], months: list[str]) -> float:
    return sum((float(first[MONTHS[m][0]]) - float(second[MONTHS[m][0]])) * MONTHS[m][1] for m in months)


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    fraction = position - lower
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def build() -> list[dict[str, str]]:
    books = {name: download(url) for name, url in {"feb": FEB_URL, "jul": JUL_URL, "aug": AUG_URL}.items()}
    supply = {name: workbook_rows(book, 7)["papr_world"] for name, book in books.items()}
    demand = {name: workbook_rows(book, 9)["patc_world"] for name, book in books.items()}
    country = {name: workbook_rows(book, 6) for name, book in books.items()}
    rows: list[dict[str, str]] = []

    headline_by_frame: dict[str, dict[str, float]] = {}
    for frame, months in FRAMES.items():
        days = sum(MONTHS[m][1] for m in months)
        values: dict[str, dict[str, float]] = {}
        for vintage in ("jul", "aug"):
            shortfall = volume(supply["feb"], supply[vintage], months)
            reduction = volume(demand["feb"], demand[vintage], months)
            foregone = sum(
                (float(supply["feb"][MONTHS[m][0]]) - float(demand["feb"][MONTHS[m][0]])) * MONTHS[m][1]
                for m in months
            )
            draw = sum(
                (float(demand[vintage][MONTHS[m][0]]) - float(supply[vintage][MONTHS[m][0]])) * MONTHS[m][1]
                for m in months
            )
            if abs(shortfall - reduction - foregone - draw) > 1e-6:
                raise ValueError(f"headline identity failed for {frame} {vintage}")
            values[vintage] = {
                "global_supply_shortfall": shortfall,
                "global_consumption_reduction": reduction,
                "foregone_expected_inventory_build": foregone,
                "implied_inventory_draw": draw,
            }
        headline_by_frame[frame] = values["aug"]
        for metric in values["aug"]:
            rows.append(blank(
                row_id=f"headline-{frame}-{metric}", record_type="headline_component",
                frame=frame, period_start="2026-03-01", period_end=f"{months[-1]}-{MONTHS[months[-1]][1]:02d}",
                days=days, metric=metric, geography="World", august_value=values["aug"][metric],
                july_value=values["jul"][metric], delta_vs_july=values["aug"][metric] - values["jul"][metric],
                unit="million_bbl", frozen_vintage="2026-02-10", comparison_vintage="2026-08-11",
                data_status="preliminary_estimates", source_url=f"{FEB_URL} | {JUL_URL} | {AUG_URL}",
                source_locator="Tables 3c and 3e, monthly World total rows",
                method="Calendar-day integration of matched monthly February-minus-target STEO values; implied balance is production minus consumption.",
                interpretation="Forecast-vintage accounting identity; not proof that every revision was caused by Hormuz.",
                confidence="high_for_arithmetic_medium_for_measurement",
                caveat="EIA labels past-month international values estimates, which remain revisable.",
            ))

    # Make the quoted frozen-February monthly build range directly auditable.
    feb_builds = [float(supply["feb"][MONTHS[m][0]]) - float(demand["feb"][MONTHS[m][0]]) for m in FRAMES["march_june"]]
    rows.append(blank(
        row_id="frozen-february-monthly-build-range-march-june", record_type="counterfactual_context",
        frame="march_june", period_start="2026-03-01", period_end="2026-06-30", days=122,
        metric="frozen_february_expected_monthly_build_range", geography="World",
        august_value=max(feb_builds), july_value=min(feb_builds), unit="mb/d_max_and_min",
        frozen_vintage="2026-02-10", comparison_vintage="not_applicable", data_status="frozen_forecast",
        source_url=FEB_URL, source_locator="Tables 3c and 3e, World total, March-June 2026",
        method="Maximum is in august_value; minimum is in july_value because the schema otherwise stores vintage comparisons.",
        interpretation=f"Frozen February expected builds ranged from {min(feb_builds):.3f} to {max(feb_builds):.3f} mb/d (2.4-3.9 mb/d rounded).",
        confidence="high_for_arithmetic", caveat="This was a forecast of implied balance, not observed or physically reserved inventory.",
    ))

    for frame, months in FRAMES.items():
        days = sum(MONTHS[m][1] for m in months)
        for row_id, label in COUNTRIES.items():
            aug_revision = -volume(country["feb"][row_id], country["aug"][row_id], months)
            jul_revision = -volume(country["feb"][row_id], country["jul"][row_id], months)
            rows.append(blank(
                row_id=f"country-{frame}-{row_id.removeprefix('papr_').lower()}", record_type="country_supply_revision",
                frame=frame, period_start="2026-03-01", period_end=f"{months[-1]}-{MONTHS[months[-1]][1]:02d}", days=days,
                metric="petroleum_and_other_liquids_production_revision", geography=label,
                august_value=aug_revision, july_value=jul_revision, delta_vs_july=aug_revision-jul_revision,
                unit="million_bbl", frozen_vintage="2026-02-10", comparison_vintage="2026-08-11",
                data_status="preliminary_estimates", source_url=f"{FEB_URL} | {JUL_URL} | {AUG_URL}",
                source_locator=f"Table 3b row {row_id}", method="Target vintage minus frozen-February monthly production, integrated by calendar days.",
                interpretation="Positive is additional production relative to the frozen forecast; this is a revision, not causal attribution.",
                confidence="medium_high_for_revision_low_for_causality", caveat="Country estimates remain revisable.",
            ))

    # Recompute r3v.5's ordinary-revision distribution on matched February-August
    # historical vintage pairs. Reusing its February-July distribution here would
    # mismatch the target vintage.
    baseline_values: dict[str, list[float]] = {frame: [] for frame in FRAMES}
    baseline_sources: list[str] = []
    for year in BASELINE_YEARS:
        suffix = str(year)[2:]
        feb_url = f"https://www.eia.gov/outlooks/steo/archives/feb{suffix}_base.xlsx"
        aug_url = f"https://www.eia.gov/outlooks/steo/archives/aug{suffix}_base.xlsx"
        feb_book, aug_book = download(feb_url), download(aug_url)
        feb_world = find_table(feb_book, [7, 5], "papr_world")["papr_world"]
        aug_world = find_table(aug_book, [7, 5], "papr_world")["papr_world"]
        feb_russia = find_table(feb_book, [6], "papr_RS")["papr_RS"]
        aug_russia = find_table(aug_book, [6], "papr_RS")["papr_RS"]
        for frame, months in FRAMES.items():
            world_revision = volume(feb_world, aug_world, months)
            russia_revision = volume(feb_russia, aug_russia, months)
            baseline_values[frame].append(world_revision-russia_revision)
        baseline_sources.extend([feb_url, aug_url])
    for frame, months in FRAMES.items():
        russia_shortfall = volume(country["feb"]["papr_RS"], country["aug"]["papr_RS"], months)
        ex_russia = headline_by_frame[frame]["global_supply_shortfall"] - russia_shortfall
        p10 = percentile(baseline_values[frame], 0.10)
        p90 = percentile(baseline_values[frame], 0.90)
        low = ex_russia - p90
        high = ex_russia - p10
        rows.append(blank(
            row_id=f"attribution-{frame}-supply-central-band", record_type="causal_plausibility_band",
            frame=frame, period_start="2026-03-01", period_end=f"{months[-1]}-{MONTHS[months[-1]][1]:02d}",
            days=sum(MONTHS[m][1] for m in months), metric="hormuz_plausible_supply_effect_central_band",
            geography="World excluding Russia", august_value=low, july_value=high, unit="million_bbl_low_and_high",
            frozen_vintage="2026-02-10", comparison_vintage="2026-08-11", data_status="bounded_attribution",
            source_url=" | ".join([FEB_URL, AUG_URL, *baseline_sources]),
            source_locator=f"February-August 2017-19 and 2023-25 {frame} world-ex-Russia p10/p90",
            method="Remove Russia from the August world shortfall, then subtract the matched historical February-August p90/p10 signed ordinary-revision bounds (linear Type-7 interpolation).",
            interpretation=f"Preferred causal-plausibility range is {low:.1f}-{high:.1f} million barrels; not an identified treatment effect.",
            confidence="medium_for_band_low_for_causal_precision", caveat="Small historical sample; ordinary revisions may correlate with shock-era news.",
        ))

    # Table 1 replaces the July report's monthly country table with March-May average, June, and July estimates.
    for country_name, (mar_may, june, july) in GULF_SHUTINS.items():
        cumulative = mar_may * 92 + june * 30 + july * 31
        for period, rate, days, start, end in [
            ("march_may", mar_may, 92, "2026-03-01", "2026-05-31"),
            ("june", june, 30, "2026-06-01", "2026-06-30"),
            ("july", july, 31, "2026-07-01", "2026-07-31"),
        ]:
            rows.append(blank(
                row_id=f"gulf-{country_name.lower().replace(' ', '_')}-{period}", record_type="gulf_country_crude_shutin",
                frame=period, period_start=start, period_end=end, days=days, metric="closure_related_crude_production_shutin",
                geography=country_name, august_value=rate, unit="mb/d", comparison_vintage="2026-08-11",
                data_status="estimated", source_url=AUG_PDF, source_locator="Table 1, p. 6",
                method="Direct EIA transcription; March-May is one average, not three monthly observations.",
                interpretation="Closure-related crude production shut-in.", confidence="high_for_source_medium_for_measurement",
                caveat="Crude only; excludes condensates and NGLs.",
            ))
        rows.append(blank(
            row_id=f"gulf-{country_name.lower().replace(' ', '_')}-march-july-cumulative", record_type="gulf_country_crude_shutin_summary",
            frame="march_july", period_start="2026-03-01", period_end="2026-07-31", days=153,
            metric="cumulative_closure_related_crude_production_shutin", geography=country_name,
            august_value=cumulative, unit="million_bbl", comparison_vintage="2026-08-11", data_status="estimated",
            source_url=AUG_PDF, source_locator="Table 1, p. 6", method="March-May average times 92 days plus June times 30 and July times 31.",
            interpretation="Country cumulative through July.", confidence="medium_high", caveat="Crude only; estimates remain revisable.",
        ))

    gulf_total = 10.050 * 92 + 7.480 * 30 + 5.460 * 31
    rows.append(blank(
        row_id="gulf-total-march-july-cumulative", record_type="gulf_crude_shutin_total", frame="march_july",
        period_start="2026-03-01", period_end="2026-07-31", days=153,
        metric="cumulative_closure_related_crude_production_shutin", geography="Affected Gulf producers",
        august_value=gulf_total, unit="million_bbl", comparison_vintage="2026-08-11", data_status="estimated",
        source_url=AUG_PDF, source_locator="Table 1 total row, p. 6", method="10.050 mb/d times 92 days plus 7.480 times 30 plus 5.460 times 31.",
        interpretation="1,318.26 million barrels of estimated crude shut-ins through July using EIA's published total row.", confidence="medium_high",
        caveat="The published March-May total exceeds the seven displayed country rows by 1.2 mb/d; crude only and not additive to the global shortfall.",
    ))
    country_gulf_total = sum((mar_may * 92 + june * 30 + july * 31) for mar_may, june, july in GULF_SHUTINS.values())
    rows.append(blank(
        row_id="gulf-country-vs-total-discrepancy", record_type="source_reconciliation",
        frame="march_july", period_start="2026-03-01", period_end="2026-07-31", days=153,
        metric="published_total_minus_displayed_country_rows", geography="Affected Gulf producers",
        august_value=gulf_total-country_gulf_total, unit="million_bbl", comparison_vintage="2026-08-11",
        data_status="published_source_discrepancy", source_url=AUG_PDF, source_locator="Table 1, p. 6",
        method="Published total-row integration minus the sum of the seven displayed country rows. The entire difference is in the March-May average: 10.050 versus 8.850 mb/d.",
        interpretation="EIA's displayed country rows do not reconcile to its March-May aggregate; preserve both rather than inventing a country allocation.",
        confidence="high_for_arithmetic_low_for_explanation", caveat="Could reflect omitted production or a report-table error; EIA does not explain it in the report.",
    ))

    # Restate the only period-matched route bridge supported by the existing public reconstruction.
    non_me_june = sum(volume(country["aug"][row_id], country["feb"][row_id], FRAMES["march_june"]) for row_id in REGIONAL_IDS)
    oman_june = volume(country["aug"]["papr_MU"], country["feb"]["papr_MU"], FRAMES["march_june"])
    nongulf_june = non_me_june + oman_june
    missing, bypass = 1924.60, 362.10
    shortfall = headline_by_frame["march_june"]["global_supply_shortfall"]
    residual = missing - bypass - nongulf_june - shortfall
    for metric, value, method in [
        ("gross_missing_hormuz_transit", missing, "Existing public route reconstruction: 20 mb/d prewar less March-May 2.7 mb/d and June 8.9 mb/d."),
        ("incremental_bypass", bypass, "Existing named-route reconstruction above a 3.8 mb/d prewar baseline."),
        ("non_gulf_and_oman_supply_revision", nongulf_june, "August-minus-February complete non-Middle-East Table 3b regional revisions plus Oman."),
        ("global_supply_shortfall", shortfall, "Frozen-February less August world production."),
        ("route_taxonomy_timing_residual", residual, "Missing transit minus incremental bypass minus non-Gulf/Oman supply minus global supply shortfall."),
    ]:
        rows.append(blank(
            row_id=f"route-bridge-march-june-{metric}", record_type="route_bridge", frame="march_june",
            period_start="2026-03-01", period_end="2026-06-30", days=122, metric=metric,
            geography="World", august_value=value, unit="million_bbl", frozen_vintage="2026-02-10",
            comparison_vintage="2026-08-11", data_status="mixed_estimate_and_revision",
            source_url=f"{FEB_URL} | {AUG_URL} | {IEA_ROUTE}", source_locator="STEO Tables 3b/3c; public route reconstruction",
            method=method, interpretation="Bridge identity: missing transit - bypass - non-Gulf/Oman supply = shortfall + residual.",
            confidence="medium_for_arithmetic_low_for_route_measurement",
            caveat="Route flow and production use different taxonomies and timing; residual is diagnostic, not allocable barrels.",
        ))

    for metric, value, unit, interpretation in [
        ("july_crude_shutins", 5.5, "mb/d", "EIA assesses July production shut-ins averaged about 5.5 mb/d."),
        ("q3_crude_shutins_forecast", 6.573, "mb/d", "Higher than July STEO because severe Hormuz constraints persist through August."),
        ("q4_crude_shutins_forecast", 4.200, "mb/d", "Flows are assumed to increase slowly from September."),
        ("q1_2027_crude_shutins_forecast", 1.637, "mb/d", "Most production is assumed largely restored in 1Q27."),
        ("end_2027_ongoing_disruption", 0.6, "mb/d", "About 0.6 mb/d remains disrupted through end-2027."),
    ]:
        rows.append(blank(
            row_id=f"forward-assumption-{metric}", record_type="forward_assumption", frame="forward",
            metric=metric, geography="Affected Gulf producers", august_value=value, unit=unit,
            comparison_vintage="2026-08-11", data_status="estimate_or_forecast_as_named", source_url=AUG_PDF,
            source_locator="Overview p. 2; Global Oil Markets pp. 5-6; Table 1 p. 6",
            method="Direct report transcription.", interpretation=interpretation, confidence="high_for_eia_assumption",
            caveat="Conditional forecast assumption, not a physical capacity guarantee.",
        ))

    rows.append(blank(
        row_id="frame-recommendation-march-july", record_type="editorial_recommendation", frame="march_july",
        period_start="2026-03-01", period_end="2026-07-31", days=153, metric="recommended_primary_historical_frame",
        geography="World", august_value=1.0, unit="boolean_1_yes", comparison_vintage="2026-08-11",
        data_status="recommendation", source_url=f"{AUG_URL} | {AUG_PDF}", source_locator="August forecast completed 6 August; July values are past-month estimates",
        method="Prefer the longest common frame whose terminal month is estimated rather than forecast and which includes the renewed July escalation.",
        interpretation="Switch the blog's primary frame to March-July; retain March-June as a sensitivity and bridge-comparison frame.",
        confidence="high_for_framing", caveat="July and earlier international values are preliminary estimates, not final observations.",
    ))
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    if not rows or len({row["row_id"] for row in rows}) != len(rows):
        raise ValueError("empty output or duplicate row_id")
    for frame in FRAMES:
        headline = {row["metric"]: float(row["august_value"]) for row in rows if row["record_type"] == "headline_component" and row["frame"] == frame}
        if abs(headline["global_supply_shortfall"] - headline["global_consumption_reduction"] - headline["foregone_expected_inventory_build"] - headline["implied_inventory_draw"]) > 1e-5:
            raise ValueError(f"output identity failed for {frame}")
    gulf = [row for row in rows if row["row_id"] == "gulf-total-march-july-cumulative"]
    if len(gulf) != 1 or abs(float(gulf[0]["august_value"]) - 1318.26) > 1e-6:
        raise ValueError("Gulf total failed")


def main() -> None:
    rows = build()
    validate(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
