#!/usr/bin/env python3
"""Audit whether China's 2026 STEO demand revision is hidden destocking.

The key distinction is between final product use and non-OECD ``apparent
consumption``.  China does not submit product-stock levels to JODI, so the
official apparent-demand identity cannot reveal a product-stock draw.  The
output therefore separates observed accounting components from an explicitly
low-confidence reclassification sensitivity.
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
OUT = ROOT / "data/derived/hormuz_p2k_4_china_demand_reclassification.csv"

FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
JODI_2025_URL = (
    "https://www.jodidata.org/_resources/files/downloads/oil-data/annual-csv/"
    "secondary/2025.csv"
)
JODI_2026_URL = (
    "https://www.jodidata.org/_resources/files/downloads/oil-data/annual-csv/"
    "secondary/secondaryyear2026.csv"
)
JODI_DEFINITION_URL = (
    "https://www.jodidata.org/oil/support/user-guide/"
    "data-available-in-the-jodi-oil-world-database.aspx"
)
JODI_COMPLETENESS_URL = (
    "https://www.egnret.ewg.apec.org/sites/default/files/2023-04/"
    "day2/2%20Report%20on%20JODI%20Data%20Submissions%20in%20APEC-final.pdf"
)
EIA_APPARENT_DEMAND_URL = "https://www.eia.gov/todayinenergy/detail.php?id=63764"
EIA_STEO_URL = "https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf"
AP_ANALYST_URL = (
    "https://apnews.com/article/oil-gasoline-demand-iran-us-iea-report-"
    "de45ede94f992da07d35a8b737fdeacf"
)
COMMERCIAL_DRAW_URL = (
    "https://www.energyconnects.com/news/oil/2026/june/"
    "china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/"
)

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
MONTH_COLUMNS = {"2026-03": "BA", "2026-04": "BB", "2026-05": "BC", "2026-06": "BD", "2026-07": "BE"}

FIELDS = [
    "row_id", "record_type", "period_start", "period_end", "month", "metric",
    "value_2026", "comparison_value", "difference", "reclass_low",
    "reclass_base", "reclass_high", "unit", "status", "confidence",
    "source_url", "method", "interpretation", "accounting_treatment", "caveat",
]

NBS_RUNS = {
    "2026-03": (61.67, -2.2, "https://www.stats.gov.cn/english/PressRelease/202604/t20260417_1963350.html"),
    "2026-04": (54.65, -5.8, "https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html"),
    "2026-05": (53.72, -9.1, "https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html"),
    "2026-06": (51.24, -17.7, "https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html"),
}

# GACC totals reported in Reuters-derived coverage. June's 2025 comparison is
# reconstructed from the reported H1 and Jan-May cumulative percentage changes.
CUSTOMS_EXPORTS = {
    "2026-03": (4.60, -11.5, "https://uk.marketscreener.com/news/china-s-march-refined-oil-shipments-fall-after-export-ban-ce7e50d3db80f422"),
    "2026-04": (3.12, -38.0, "https://www.investing.com/news/economy-news/chinas-refined-oil-exports-drop-38-in-april-amid-fuel-restrictions-93CH-4695002"),
    "2026-05": (3.37, -23.6, "https://www.bairdmaritime.com/shipping/tankers/export-rules-cool-down-china-refined-oil-shipments-in-may"),
}
JUNE_EXPORTS_URL = "https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def workbook_rows(workbook: bytes, sheet_number: int) -> dict[str, dict[str, str]]:
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


def demand_table(workbook: bytes) -> dict[str, dict[str, str]]:
    for sheet in (9, 8):
        table = workbook_rows(workbook, sheet)
        if "patc_ch" in table:
            return table
    raise ValueError("China demand mnemonic patc_ch not found")


def jodi_rows(data: bytes) -> dict[tuple[str, str, str], float | None]:
    output: dict[tuple[str, str, str], float | None] = {}
    text = io.StringIO(data.decode("utf-8-sig"))
    for row in csv.DictReader(text):
        if row["REF_AREA"] != "CN" or row["UNIT_MEASURE"] != "KBBL":
            continue
        if row["TIME_PERIOD"] not in {"2025-03", "2025-04", "2025-05", "2026-03", "2026-04", "2026-05"}:
            continue
        raw = row["OBS_VALUE"]
        output[(row["TIME_PERIOD"], row["ENERGY_PRODUCT"], row["FLOW_BREAKDOWN"])] = (
            None if raw in {"", "-", "x"} else float(raw) / 1000.0
        )
    return output


def fmt(value: float | str | None) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.6f}".rstrip("0").rstrip(".")


def row(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    for key, value in values.items():
        result[key] = fmt(value)  # type: ignore[arg-type]
    return result


def month_bounds(month: str) -> tuple[str, str]:
    days = calendar.monthrange(int(month[:4]), int(month[-2:]))[1]
    return f"{month}-01", f"{month}-{days:02d}"


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    feb = demand_table(fetch(FEB_URL))["patc_ch"]
    jul = demand_table(fetch(JUL_URL))["patc_ch"]
    eia_gaps: dict[str, float] = {}
    for month, column in MONTH_COLUMNS.items():
        start, end = month_bounds(month)
        days = calendar.monthrange(2026, int(month[-2:]))[1]
        feb_value, jul_value = float(feb[column]), float(jul[column])
        gap = (feb_value - jul_value) * days
        eia_gaps[month] = gap
        rows.append(row(
            row_id=f"eia-demand-revision-{month}", record_type="counterfactual_demand_revision",
            period_start=start, period_end=end, month=month,
            metric="petroleum_and_other_liquid_fuels_consumption_below_february_path",
            value_2026=jul_value, comparison_value=feb_value, difference=gap, unit="mb/d_and_million_bbl_difference",
            status="preliminary" if month != "2026-07" else "forecast", confidence="medium_high_for_vintage_arithmetic",
            source_url=f"{FEB_URL} | {JUL_URL}",
            method="July STEO mb/d compared with frozen February STEO mb/d; difference multiplied by calendar days.",
            interpretation="Positive difference is lower EIA consumption than forecast in February; it is not automatically final-use destruction.",
            accounting_treatment="Historical denominator for March-June; July is excluded from the historical reclassification test.",
            caveat="Includes ordinary forecast revision and all contemporaneous shocks. China is non-OECD apparent consumption.",
        ))

    historical_gap = sum(eia_gaps[m] for m in MONTH_COLUMNS if m != "2026-07")
    headline_gap = sum(eia_gaps.values())
    rows.append(row(
        row_id="eia-demand-revision-march-june-cumulative", record_type="counterfactual_demand_revision",
        period_start="2026-03-01", period_end="2026-06-30", metric="historical_china_demand_revision",
        difference=historical_gap, unit="million_bbl", status="march_june_preliminary", confidence="medium_high_for_vintage_arithmetic",
        source_url=f"{FEB_URL} | {JUL_URL}", method="Sum of monthly March-June rows.",
        interpretation="The relevant historical denominator is 90.943 mb, not the 119.992 mb March-July headline.",
        accounting_treatment="Use for the observed-window reclassification sensitivity.",
        caveat="Preliminary estimates can be revised.",
    ))
    rows.append(row(
        row_id="eia-demand-revision-march-july-headline", record_type="counterfactual_demand_revision",
        period_start="2026-03-01", period_end="2026-07-31", metric="published_project_china_demand_revision_headline",
        difference=headline_gap, unit="million_bbl", status="march_june_preliminary_july_forecast",
        confidence="medium_high_for_vintage_arithmetic", source_url=f"{FEB_URL} | {JUL_URL}",
        method="Sum of monthly March-July rows.", interpretation="Matches the 119.992 mb upstream headline.",
        accounting_treatment="Do not treat July's 29.049 mb forecast as observed destocking.",
        caveat="One quarter of the headline is a forecast month.",
    ))

    # EIA explains that Chinese gasoline apparent demand is refinery production
    # plus imports minus exports because China does not publish stock changes.
    rows.append(row(
        row_id="method-eia-china-apparent-demand", record_type="methodology",
        period_start="2026-03-01", period_end="2026-06-30", metric="non_oecd_apparent_consumption_stock_treatment",
        unit="text", status="official_methodology", confidence="high", source_url=f"{EIA_APPARENT_DEMAND_URL} | {EIA_STEO_URL}",
        method="EIA describes non-OECD consumption as apparent consumption; for Chinese gasoline it explicitly uses refinery production plus imports minus exports because stock changes are unavailable.",
        interpretation="An unobserved product-stock draw can make final use exceed measured apparent demand.",
        accounting_treatment="This creates a plausible reclassification channel but does not quantify it.",
        caveat="EIA does not publish a complete product-by-product China STEO model bridge, so the gasoline explanation is the clearest public example rather than proof that every liquid is constructed identically.",
    ))

    jodi = jodi_rows(fetch(JODI_2025_URL))
    jodi.update(jodi_rows(fetch(JODI_2026_URL)))
    flows = {
        "REFGROUT": "refinery_output",
        "TOTIMPSB": "product_imports",
        "TOTEXPSB": "product_exports",
        "TOTDEMO": "apparent_product_demand",
        "STOCKCH": "reported_product_stock_change",
    }
    for month in ("03", "04", "05"):
        current_period, prior_period = f"2026-{month}", f"2025-{month}"
        start, end = month_bounds(current_period)
        for flow, metric in flows.items():
            current = jodi.get((current_period, "TOTPRODS", flow))
            prior = jodi.get((prior_period, "TOTPRODS", flow))
            difference = None if current is None or prior is None else current - prior
            stock_unreported = flow == "STOCKCH"
            rows.append(row(
                row_id=f"jodi-{metric}-{current_period}", record_type="official_apparent_product_balance",
                period_start=start, period_end=end, month=current_period, metric=metric,
                value_2026=current, comparison_value=prior, difference=difference, unit="million_bbl",
                status="not_submitted_encoded_zero" if stock_unreported else "official_submission",
                confidence="high_for_reported_arithmetic_low_for_final_use",
                source_url=f"{JODI_2025_URL} | {JODI_2026_URL} | {JODI_COMPLETENESS_URL}",
                method="China JODI secondary-products submission in thousand barrels, divided by 1,000; difference is 2026 minus 2025.",
                interpretation=("China does not submit product-stock levels/changes; zero must not be read as observed no change." if stock_unreported else
                                "A component of the mechanical apparent-product balance, not a final-sales series."),
                accounting_treatment=("Missing observation; do not use zero as evidence against destocking." if stock_unreported else
                                      "Diagnostic only; nested inside apparent demand."),
                caveat="JODI documents missing/inaccurate non-OECD inventories; China closing-stock fields are blank and the stock-change zero is a not-submitted encoding.",
            ))

    rows.append(row(
        row_id="jodi-apparent_product_demand-2026-06", record_type="official_apparent_product_balance",
        period_start="2026-06-01", period_end="2026-06-30", month="2026-06",
        metric="apparent_product_demand", unit="million_bbl", status="china_june_not_submitted_at_2026_08_04_update",
        confidence="high_for_unavailability", source_url=f"{JODI_2026_URL} | {JODI_COMPLETENESS_URL}",
        method="Availability check against the JODI annual 2026 secondary-products file updated 2026-08-04.",
        interpretation="The independent public apparent-product balance ends in May; June cannot be filled without proprietary or later data.",
        accounting_treatment="Retain EIA's preliminary June value and NBS/customs diagnostics; do not impute a June JODI demand observation.",
        caveat="A later JODI update may add or revise June.",
    ))

    product_names = {
        "LPG": "lpg", "NAPHTHA": "naphtha", "GASOLINE": "motor_and_aviation_gasoline",
        "KEROSENE": "kerosene_including_jet", "GASDIES": "gas_and_diesel_oil",
        "RESFUEL": "residual_fuel_oil", "ONONSPEC": "other_oil_products",
    }
    for product, name in product_names.items():
        current = sum(jodi[(f"2026-{month}", product, "TOTDEMO")] or 0.0 for month in ("03", "04", "05"))
        prior = sum(jodi[(f"2025-{month}", product, "TOTDEMO")] or 0.0 for month in ("03", "04", "05"))
        rows.append(row(
            row_id=f"jodi-product-demand-composition-{name}-march-may", record_type="apparent_demand_composition",
            period_start="2026-03-01", period_end="2026-05-31", metric=f"apparent_demand_{name}",
            value_2026=current, comparison_value=prior, difference=current - prior, unit="million_bbl",
            status="official_submission", confidence="medium_for_direction_low_for_final_use",
            source_url=f"{JODI_2025_URL} | {JODI_2026_URL} | {JODI_DEFINITION_URL}",
            method="Sum of China JODI product demand for March-May; difference is 2026 minus 2025.",
            interpretation="Product composition diagnostic inside the mechanical apparent-demand total.",
            accounting_treatment="Non-additive memo breakdown; never combine with total-product demand.",
            caveat="Stock changes are unreported and other oil products combine refinery gas, ethane, petroleum coke, lubricants, bitumen and additional products.",
        ))

    for month, (actual_mt, yoy_pct, source) in NBS_RUNS.items():
        start, end = month_bounds(month)
        prior_mt = actual_mt / (1.0 + yoy_pct / 100.0)
        shortfall_mt = prior_mt - actual_mt
        low, base, high = shortfall_mt * 7.1, shortfall_mt * 7.33, shortfall_mt * 7.5
        rows.append(row(
            row_id=f"nbs-refinery-run-shortfall-{month}", record_type="refinery_layer_observation",
            period_start=start, period_end=end, month=month, metric="refinery_throughput_below_prior_year",
            value_2026=actual_mt, comparison_value=prior_mt, difference=base,
            reclass_low=low, reclass_base=base, reclass_high=high, unit="million_metric_tons_and_million_bbl_equivalent",
            status="official_observation_converted", confidence="medium_high", source_url=source,
            method="NBS reported level and comparable-coverage y/y rate imply prior-year tonnes; converted at 7.1/7.33/7.5 bbl per tonne.",
            interpretation="Gross crude-processing contraction; it is much larger than the EIA demand revision and cannot be equated to final-use reduction.",
            accounting_treatment="Memo diagnostic only; never add to demand or inventory totals.",
            caveat="Crude throughput is upstream of product use and NBS coverage is industrial enterprises above the designated size.",
        ))

    nbs_rows = [item for item in rows if item["row_id"].startswith("nbs-refinery-run-shortfall-2026-")]
    rows.append(row(
        row_id="nbs-refinery-run-shortfall-march-june-cumulative", record_type="refinery_layer_observation",
        period_start="2026-03-01", period_end="2026-06-30", metric="refinery_throughput_below_prior_year",
        difference=sum(float(item["difference"]) for item in nbs_rows),
        reclass_low=sum(float(item["reclass_low"]) for item in nbs_rows),
        reclass_base=sum(float(item["reclass_base"]) for item in nbs_rows),
        reclass_high=sum(float(item["reclass_high"]) for item in nbs_rows),
        unit="million_bbl_equivalent", status="official_observations_converted", confidence="medium_high",
        source_url=" | ".join(value[2] for value in NBS_RUNS.values()),
        method="Sum of monthly NBS year-on-year crude-processing shortfalls.",
        interpretation="The roughly 155 mb gross run shortfall exceeds the 90.943 mb EIA demand revision, proving that throughput is not a final-consumption measure.",
        accounting_treatment="Memo diagnostic only; never add to demand or inventory totals.",
        caveat="Year-on-year comparator and crude-to-barrel conversion range.",
    ))

    # Broad refined-product exports retained domestically versus 2025.
    export_rows: dict[str, tuple[float, float, str]] = dict(CUSTOMS_EXPORTS)
    h1_2026, h1_yoy = 23.59, -13.2
    jan_may_2026, jan_may_yoy = 19.23, -12.0
    june_2025 = h1_2026 / (1 + h1_yoy / 100) - jan_may_2026 / (1 + jan_may_yoy / 100)
    june_yoy = (4.36 / june_2025 - 1) * 100
    export_rows["2026-06"] = (4.36, june_yoy, JUNE_EXPORTS_URL)
    export_retention_base = 0.0
    for month, (actual_mt, yoy_pct, source) in export_rows.items():
        start, end = month_bounds(month)
        prior_mt = actual_mt / (1.0 + yoy_pct / 100.0)
        retained_mt = prior_mt - actual_mt
        low, base, high = retained_mt * 7.3, retained_mt * 7.8, retained_mt * 8.3
        export_retention_base += base
        rows.append(row(
            row_id=f"customs-export-retention-{month}", record_type="refining_export_layer_observation",
            period_start=start, period_end=end, month=month, metric="refined_product_exports_below_prior_year",
            value_2026=actual_mt, comparison_value=prior_mt, difference=base,
            reclass_low=low, reclass_base=base, reclass_high=high, unit="million_metric_tons_and_million_bbl_equivalent",
            status="customs_reported" if month != "2026-06" else "derived_from_reported_cumulatives",
            confidence="medium_high", source_url=source,
            method="Reported broad refined-product export volume and y/y change; 7.3/7.8/8.3 bbl per tonne mixed-product conversion. June comparison is derived from H1 and Jan-May cumulative disclosures.",
            interpretation="Barrels retained for domestic availability; export policy insulated consumers as refinery output fell.",
            accounting_treatment="Not destocking and not additional global supply. Lower exports raise apparent domestic demand relative to a no-control case.",
            caveat="Broad customs category includes marine fuel and aviation/Hong Kong flows; it is not identical to clean-fuel exports or domestic sales.",
        ))

    rows.append(row(
        row_id="customs-export-retention-march-june-cumulative", record_type="refining_export_layer_observation",
        period_start="2026-03-01", period_end="2026-06-30", metric="refined_products_retained_by_lower_exports",
        difference=export_retention_base, reclass_low=export_retention_base * 7.3 / 7.8,
        reclass_base=export_retention_base, reclass_high=export_retention_base * 8.3 / 7.8,
        unit="million_bbl_equivalent", status="reported_and_derived_cumulative", confidence="medium",
        source_url=" | ".join(v[2] for v in export_rows.values()),
        method="Sum of four monthly broad-product export shortfalls versus 2025.",
        interpretation="About 35 mb of product availability was preserved at home by lower exports; this explains insulation, not consumption destruction.",
        accounting_treatment="Context only. It is already embedded with a positive sign in apparent consumption and must not be reclassified as inventory draw.",
        caveat="Mixed-product conversion and year-on-year counterfactual.",
    ))

    rows.append(row(
        row_id="analyst-road-fuel-demand-loss", record_type="independent_final_use_crosscheck",
        period_start="2026-03-01", period_end="2026-06-30", metric="gasoline_and_diesel_final_use_loss_rate",
        reclass_low=0.5, reclass_base=0.55, reclass_high=0.6, unit="mb/d",
        status="attributed_analyst_estimate", confidence="low_medium", source_url=AP_ANALYST_URL,
        method="Contemporaneous AP quotation of Daniel Sternoff/CGEP estimate of 0.5-0.6 mb/d gasoline-and-diesel losses since the crisis began.",
        interpretation="Material road-fuel use did decline; the whole EIA revision cannot plausibly be relabeled destocking.",
        accounting_treatment="Used only to bound a high reclassification sensitivity, not as an additive ledger row.",
        caveat="Analyst estimate, not a monthly official sales series; counterfactual may differ from February STEO.",
    ))
    rows.append(row(
        row_id="analyst-commercial-crude-draw", record_type="inventory_crosscheck",
        period_start="2026-05-08", period_end="2026-06-07", metric="commercial_operational_crude_stock_draw",
        difference=25.0, unit="million_bbl", status="attributed_analyst_estimate", confidence="medium",
        source_url=COMMERCIAL_DRAW_URL,
        method="Bloomberg-syndicated reporting citing Vortexa, Kpler, Energy Aspects and Kayrros.",
        interpretation="Supports commercial/operational flexibility but is crude inventory, not proof of missing final product use.",
        accounting_treatment="Inventory memo row; never use as direct demand reclassification.",
        caveat="Ownership and product/crude boundary are unresolved; aggregate IEA tank estimates also show a March build and June draw.",
    ))

    # High sensitivity: after crediting the low end (0.5 mb/d) of the independent
    # road-fuel loss estimate over 122 days, at most ~30 mb of the 90.943 mb EIA
    # historical revision remains available for *all* other mechanisms. Assigning
    # that entire remainder to hidden product destocking is intentionally generous.
    days_historical = 122
    high_reclass = max(0.0, historical_gap - 0.5 * days_historical)
    base_reclass = high_reclass / 2.0
    positive_gap = sum(max(0.0, eia_gaps[m]) for m in eia_gaps if m != "2026-07")
    for month in ("2026-03", "2026-04", "2026-05", "2026-06"):
        start, end = month_bounds(month)
        weight = max(0.0, eia_gaps[month]) / positive_gap
        rows.append(row(
            row_id=f"inventory-reclassification-{month}", record_type="low_confidence_reclassification_sensitivity",
            period_start=start, period_end=end, month=month, metric="eia_demand_revision_potentially_hidden_product_destocking",
            comparison_value=eia_gaps[month], reclass_low=0.0, reclass_base=base_reclass * weight,
            reclass_high=high_reclass * weight, unit="million_bbl", status="scenario_not_observation", confidence="low",
            source_url=f"{AP_ANALYST_URL} | {EIA_APPARENT_DEMAND_URL} | {JODI_COMPLETENESS_URL}",
            method="Cumulative scenario allocated across months proportional to positive EIA demand-revision gaps.",
            interpretation="Timing allocation is mechanical because public product-stock data do not exist.",
            accounting_treatment="If used, move from China demand revision to opaque inventory/reconciliation; total absorption is unchanged.",
            caveat="Not a measured monthly stock path.",
        ))

    rows.append(row(
        row_id="inventory-reclassification-march-june-cumulative", record_type="integration_handoff",
        period_start="2026-03-01", period_end="2026-06-30", metric="historical_china_demand_to_inventory_reclassification",
        comparison_value=historical_gap, reclass_low=0.0, reclass_base=base_reclass,
        reclass_high=high_reclass, unit="million_bbl", status="recommended_sensitivity_not_observation", confidence="low",
        source_url=f"{AP_ANALYST_URL} | {EIA_APPARENT_DEMAND_URL} | {JODI_2026_URL} | {JODI_COMPLETENESS_URL}",
        method="Low=zero because no public product-stock draw is observed. High=90.943 mb historical EIA gap minus 61.0 mb implied by the low end of the 0.5-0.6 mb/d road-fuel loss estimate over 122 days. Base is the midpoint, not a statistical estimate.",
        interpretation="Use 0/14.972/29.943 mb only as an accounting sensitivity. Evidence does not justify saying that 15 mb was actually drawn from product stocks.",
        accounting_treatment="Subtract the selected value from the China demand-revision slice and add it to opaque inventory/reconciliation. Do not add it to observed global inventories; total absorption must remain unchanged.",
        caveat="The road-fuel estimate and STEO revision do not share a perfectly matched counterfactual; the high case is deliberately generous.",
    ))
    rows.append(row(
        row_id="inventory-reclassification-march-july-headline", record_type="integration_handoff",
        period_start="2026-03-01", period_end="2026-07-31", metric="headline_china_demand_to_inventory_reclassification",
        comparison_value=headline_gap, reclass_low=0.0, reclass_base=base_reclass,
        reclass_high=high_reclass, unit="million_bbl", status="historical_allowance_only_july_unclassified", confidence="low",
        source_url=f"{FEB_URL} | {JUL_URL} | {AP_ANALYST_URL} | {JODI_COMPLETENESS_URL}",
        method="Carries the March-June reclassification sensitivity unchanged against the 119.992 mb March-July headline; no July stock claim is made.",
        interpretation="Of the 119.992 mb headline, 29.049 mb is July forecast and receives no destocking reclassification before data arrive.",
        accounting_treatment="Same nested move as the historical row; total absorption unchanged.",
        caveat="Do not extrapolate the historical stock sensitivity into July without a product-stock or final-sales observation.",
    ))

    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    if abs(historical_gap - 90.943186747) > 1e-6 or abs(headline_gap - 119.992047) > 1e-6:
        raise ValueError("EIA vintage denominators changed")
    if abs(sum(float(item["reclass_base"]) for item in rows if item["row_id"].startswith("inventory-reclassification-2026-")) - base_reclass) > 1e-5:
        raise ValueError("Monthly base reclassification does not close")
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
