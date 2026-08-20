#!/usr/bin/env python3
"""Build the revision-aware February-August 2026 oil-balance source panel."""

from __future__ import annotations

import csv
import io
import tempfile
import urllib.request
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"

FIELDS = [
    "row_id",
    "observation_month",
    "observation_period",
    "publication_vintage",
    "source",
    "source_family",
    "counterfactual_role",
    "status",
    "metric",
    "geography",
    "value",
    "unit",
    "definition",
    "taxonomy",
    "confidence",
    "citation",
    "notes",
]

EIA_VINTAGES = {
    "2026-02-10": "feb26",
    "2026-03-10": "mar26",
    "2026-04-07": "apr26",
    "2026-05-12": "may26",
    "2026-06-09": "jun26",
    "2026-07-07": "jul26",
    "2026-08-11": "aug26",
}
MONTH_COLUMNS = {
    "2026-02": "AZ",
    "2026-03": "BA",
    "2026-04": "BB",
    "2026-05": "BC",
    "2026-06": "BD",
    "2026-07": "BE",
    "2026-08": "BF",
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def eia_url(slug: str) -> str:
    return f"https://www.eia.gov/outlooks/steo/archives/{slug}_base.xlsx"


def extract_row(workbook: bytes, sheet_number: int, row_number: int = 6) -> dict[str, float]:
    """Read cached numeric cells from a simple XLSX row using the stdlib."""
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
        row = root.find(f'.//m:row[@r="{row_number}"]', NS)
        if row is None:
            raise ValueError(f"missing row {row_number} in sheet {sheet_number}")
        values: dict[str, float] = {}
        for cell in row.findall("m:c", NS):
            reference = cell.attrib["r"]
            column = reference.removesuffix(str(row_number))
            value = cell.find("m:v", NS)
            if column in MONTH_COLUMNS.values() and value is not None:
                values[column] = float(value.text)
        return values


def row(
    row_id: str,
    observation_month: str,
    observation_period: str,
    publication_vintage: str,
    source: str,
    source_family: str,
    counterfactual_role: str,
    status: str,
    metric: str,
    geography: str,
    value: float,
    unit: str,
    definition: str,
    taxonomy: str,
    confidence: str,
    citation: str,
    notes: str = "",
) -> dict[str, str]:
    return {
        "row_id": row_id,
        "observation_month": observation_month,
        "observation_period": observation_period,
        "publication_vintage": publication_vintage,
        "source": source,
        "source_family": source_family,
        "counterfactual_role": counterfactual_role,
        "status": status,
        "metric": metric,
        "geography": geography,
        "value": f"{value:.6f}".rstrip("0").rstrip("."),
        "unit": unit,
        "definition": definition,
        "taxonomy": taxonomy,
        "confidence": confidence,
        "citation": citation,
        "notes": notes,
    }


def build_eia_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="hormuz-m8q1-") as temp_dir:
        for vintage, slug in EIA_VINTAGES.items():
            url = eia_url(slug)
            local = Path(temp_dir) / f"{slug}_base.xlsx"
            urllib.request.urlretrieve(url, local)
            workbook = local.read_bytes()
            supply = extract_row(workbook, 7)
            demand = extract_row(workbook, 9)
            vintage_month = vintage[:7]
            role = "frozen_prewar_forecast" if slug == "feb26" else "postshock_vintage"
            for observation_month, column in MONTH_COLUMNS.items():
                status = "forecast" if observation_month >= vintage_month else "preliminary_estimate"
                suffix = observation_month.replace("-", "")
                values = {
                    "global_liquids_supply": supply[column],
                    "global_liquids_consumption": demand[column],
                    "implied_global_inventory_change": supply[column] - demand[column],
                }
                definitions = {
                    "global_liquids_supply": "EIA world petroleum and other liquid fuels production.",
                    "global_liquids_consumption": "EIA world petroleum and other liquid fuels consumption.",
                    "implied_global_inventory_change": (
                        "Arithmetic supply less consumption from the same EIA vintage; positive is a stock build "
                        "and negative is a stock draw."
                    ),
                }
                for metric, value in values.items():
                    rows.append(
                        row(
                            f"eia_{slug}_{suffix}_{metric}",
                            observation_month,
                            observation_month,
                            vintage,
                            f"EIA STEO {slug[:3].title()} 2026",
                            "EIA_STEO",
                            role,
                            status,
                            metric,
                            "World",
                            value,
                            "mb/d",
                            definitions[metric],
                            "petroleum_and_other_liquid_fuels",
                            "high" if metric != "implied_global_inventory_change" else "medium_high",
                            url,
                            (
                                "EIA archive Table 3c row 'World total' and Table 3e row 'World total'. "
                                "Past-month values remain estimates subject to revision; the workbook groups estimates and forecasts."
                            ),
                        )
                    )
    return rows


def build_eia_narrative_rows() -> list[dict[str, str]]:
    """Add official July STEO outage anchors not contained in Tables 3c/3e."""
    url = "https://www.eia.gov/outlooks/steo/report/global_oil.php"
    specs = [
        (
            "eia_jul_may_middle_east_crude_shutin",
            "2026-05",
            11.2,
            "preliminary_estimate",
            "Peak May Middle East crude-production shut-ins assessed in the July STEO.",
        ),
        (
            "eia_jul_jun_middle_east_crude_shutin",
            "2026-06",
            8.3,
            "preliminary_estimate",
            "Average June Middle East crude-production shut-ins after flows resumed.",
        ),
    ]
    return [
        row(
            row_id,
            observation_month,
            observation_month,
            "2026-07-07",
            "EIA STEO July 2026",
            "EIA_STEO",
            "postshock_vintage",
            status,
            "middle_east_crude_production_shutin",
            "Middle East",
            value,
            "mb/d",
            definition,
            "crude_oil",
            "medium_high",
            url,
            "Keep separate from IEA total-oil Gulf/pre-war loss estimates, which include a broader liquids taxonomy.",
        )
        for row_id, observation_month, value, status, definition in specs
    ]


def build_iea_rows() -> list[dict[str, str]]:
    february = "https://www.iea.org/reports/oil-market-report-february-2026"
    march = "https://www.iea.org/reports/oil-market-report-march-2026"
    april = "https://www.iea.org/reports/oil-market-report-april-2026"
    may = "https://www.iea.org/reports/oil-market-report-may-2026"
    june = "https://www.iea.org/reports/oil-market-report-june-2026"
    july = "https://www.iea.org/reports/oil-market-report-july-2026"
    commentary = (
        "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"
    )
    specs = [
        # February OMR pre-war annual outlook anchors. These are period forecasts, not monthly levels.
        ("iea_feb_2026_supply", "2026-02", "2026 calendar-year average", "2026-02-12", "IEA OMR February 2026", "forecast", "global_oil_supply", "World", 108.6, "mb/d", "Forecast 2026 average world oil supply.", "total_oil", "high", february, "Frozen pre-war annual anchor; do not substitute for the monthly February level."),
        ("iea_feb_2026_demand_growth", "2026-02", "2026 calendar-year change", "2026-02-12", "IEA OMR February 2026", "forecast", "global_oil_demand_change_yoy", "World", 0.85, "mb/d", "Forecast 2026 year-on-year change in global oil demand.", "total_oil", "high", february, "Annual growth, not a monthly demand level."),
        ("iea_feb_2026_runs", "2026-02", "2026 calendar-year average", "2026-02-12", "IEA OMR February 2026", "forecast", "global_refinery_crude_throughput", "World", 84.6, "mb/d", "Forecast 2026 average refinery crude throughput.", "crude_throughput", "high", february, "Annual average forecast."),
        # March OMR early shock estimates, subsequently revised as monthly observations arrived.
        ("iea_mar_mar_supply_change", "2026-03", "2026-03", "2026-03-12", "IEA OMR March 2026", "forecast", "global_oil_supply_change_mom", "World", -8.0, "mb/d", "Projected March change in global oil supply from February.", "total_oil", "medium", march, "April OMR later estimated a 10.1 mb/d decline."),
        ("iea_mar_current_gulf_cut", "2026-03", "point in time at publication", "2026-03-12", "IEA OMR March 2026", "point_in_time_estimate", "affected_gulf_output_loss_vs_prewar", "Gulf producers", 10.0, "mb/d", "At least 10 mb/d of total oil production curtailed in Gulf countries.", "total_oil", "medium", march, "Lower bound comprising at least 8 mb/d crude and 2 mb/d condensates/NGLs."),
        ("iea_mar_current_gulf_crude_cut", "2026-03", "point in time at publication", "2026-03-12", "IEA OMR March 2026", "point_in_time_estimate", "affected_gulf_output_loss_vs_prewar", "Gulf producers", 8.0, "mb/d", "At least 8 mb/d of crude production curtailed.", "crude_oil", "medium", march, "Component of the total-oil cut; do not add to the 10 mb/d headline."),
        ("iea_mar_current_gulf_ngl_cut", "2026-03", "point in time at publication", "2026-03-12", "IEA OMR March 2026", "point_in_time_estimate", "affected_gulf_output_loss_vs_prewar", "Gulf producers", 2.0, "mb/d", "At least 2 mb/d of condensates and NGL production curtailed.", "condensates_and_ngls", "medium", march, "Component of the total-oil cut; do not add to the 10 mb/d headline."),
        ("iea_mar_marapr_demand_revision", "2026-03", "2026-03-01/2026-04-30 average", "2026-03-12", "IEA OMR March 2026", "forecast_revision", "global_oil_demand_revision_vs_prior", "World", -1.0, "mb/d", "Average revision to March-April global demand versus the February OMR.", "total_oil", "medium", march, "IEA says around/more than 1 mb/d; rounded shock-era forecast revision."),
        # April OMR: first preliminary March observation and contemporaneous April run estimate.
        ("iea_apr_mar_supply", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "global_oil_supply", "World", 97.0, "mb/d", "IEA total oil supply.", "total_oil", "high", april, "First post-shock monthly supply estimate."),
        ("iea_apr_mar_supply_mom", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "global_oil_supply_change_mom", "World", -10.1, "mb/d", "Change from February global oil supply.", "total_oil", "high", april, "Largest monthly fall in the IEA series at publication."),
        ("iea_apr_mar_inventory", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "observed_inventory_change", "World", -85.0, "million_barrels", "Observed total oil inventory change; negative is a draw.", "crude_and_products_observed", "medium", april, "Superseded by the May OMR estimate of -129 mb."),
        ("iea_apr_mar_inventory_exgulf", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "observed_inventory_change", "World excluding Middle East Gulf", -205.0, "million_barrels", "Observed stock change outside the Middle East Gulf.", "crude_and_products_observed", "medium", april, "Do not add to the world total; Gulf stocks moved in the opposite direction."),
        ("iea_apr_mar_gulf_floating", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "floating_inventory_change", "Middle East Gulf", 100.0, "million_barrels", "Change in floating crude and oil-product storage.", "crude_and_products", "medium", april, "Explains why missing exports were not identical to production loss."),
        ("iea_apr_mar_gulf_onshore", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "onshore_crude_inventory_change", "Middle East Gulf", 20.0, "million_barrels", "Change in onshore crude stocks.", "crude", "medium", april, "Gulf stock build."),
        ("iea_apr_mar_china_crude", "2026-03", "2026-03", "2026-04-14", "IEA OMR April 2026", "preliminary_estimate", "onshore_crude_inventory_change", "China", 40.0, "million_barrels", "Change in crude held in tanks.", "crude", "medium", april, "Does not identify government versus commercial ownership."),
        ("iea_apr_apr_runs", "2026-04", "2026-04", "2026-04-14", "IEA OMR April 2026", "current_month_estimate", "global_refinery_crude_throughput", "World", 77.2, "mb/d", "Global refinery crude throughput.", "crude_throughput", "medium", april, "About 6 mb/d of cuts at Middle East and feedstock-constrained Asian refineries."),
        # May OMR revisions and April observations.
        ("iea_may_mar_inventory", "2026-03", "2026-03", "2026-05-13", "IEA OMR May 2026", "revised_preliminary_estimate", "observed_inventory_change", "World", -129.0, "million_barrels", "Observed total oil inventory change; negative is a draw.", "crude_and_products_observed", "medium_high", may, "Revises the April OMR estimate of -85 mb."),
        ("iea_may_mar_onland", "2026-03", "2026-03", "2026-05-13", "IEA OMR May 2026", "revised_preliminary_estimate", "onshore_inventory_change", "World", -12.0, "million_barrels", "Observed on-land stock change.", "crude_and_products_observed", "medium", may, "May OMR publishes a matched global split: oil on water fell 117 mb; the separate 100 mb Middle East Gulf floating build is nested within the global result."),
        ("iea_may_mar_water", "2026-03", "2026-03", "2026-05-13", "IEA OMR May 2026", "revised_preliminary_estimate", "oil_on_water_change", "World", -117.0, "million_barrels", "Observed global oil-on-water change.", "crude_and_products_observed", "medium", may, "Supersedes use of the regional +100 mb Middle East Gulf floating-storage build as if it were the global change."),
        ("iea_may_apr_supply", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "global_oil_supply", "World", 95.1, "mb/d", "IEA total oil supply.", "total_oil", "high", may, "A further 1.8 mb/d monthly fall."),
        ("iea_may_apr_supply_loss", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "global_oil_supply_loss_vs_february", "World", 12.8, "mb/d", "February level less April global oil supply; positive is loss.", "total_oil", "high", may, "Level comparison, not a causal counterfactual."),
        ("iea_may_apr_gulf_loss", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "affected_gulf_output_loss_vs_prewar", "Affected Gulf producers", 14.4, "mb/d", "Output below pre-war levels for Gulf countries affected by the Hormuz closure.", "total_oil", "medium_high", may, "Broader than EIA crude shut-ins."),
        ("iea_may_apr_inventory", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "observed_inventory_change", "World", -117.0, "million_barrels", "Observed total oil inventory change; negative is a draw.", "crude_and_products_observed", "medium", may, "Includes oil on water."),
        ("iea_may_apr_onland", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "onshore_inventory_change", "World", -170.0, "million_barrels", "Observed on-land stock change.", "crude_and_products_observed", "medium", may, "Oil on water rose by 53 mb in the same month."),
        ("iea_may_apr_water", "2026-04", "2026-04", "2026-05-13", "IEA OMR May 2026", "preliminary_estimate", "oil_on_water_change", "World", 53.0, "million_barrels", "Observed oil-on-water change.", "crude_and_products_observed", "medium", may, "Do not add separately to the world total."),
        # June OMR May observations and early-June transit anchor.
        ("iea_jun_may_supply", "2026-05", "2026-05", "2026-06-17", "IEA OMR June 2026", "preliminary_estimate", "global_oil_supply", "World", 94.5, "mb/d", "IEA total oil supply.", "total_oil", "high", june, "Down 0.6 mb/d month on month."),
        ("iea_jun_may_supply_loss", "2026-05", "2026-05", "2026-06-17", "IEA OMR June 2026", "preliminary_estimate", "global_oil_supply_loss_vs_preconflict", "World", 13.6, "mb/d", "Pre-conflict level less May global oil supply; positive is loss.", "total_oil", "high", june, "Level comparison, not a causal counterfactual."),
        ("iea_jun_may_inventory", "2026-05", "2026-05", "2026-06-17", "IEA OMR June 2026", "preliminary_estimate", "observed_inventory_change", "World", -143.0, "million_barrels", "Observed total oil inventory change; negative is a draw.", "crude_and_products_observed", "medium", june, "Superseded by the July OMR estimate of -73 mb."),
        ("iea_jun_may_hormuz_low", "2026-05", "2026-05", "2026-06-17", "IEA OMR June 2026", "preliminary_estimate", "gulf_oil_flow", "Gulf exports", 9.6, "mb/d", "May low in total Gulf oil flows cited by IEA.", "total_oil", "medium", june, "The IEA text calls this a May low, not a monthly average."),
        ("iea_jun_earlyjun_flow", "2026-06", "early June", "2026-06-17", "IEA OMR June 2026", "point_in_time_estimate", "gulf_oil_flow", "Gulf exports", 12.0, "mb/d", "Total Gulf oil flows after early-June rise.", "total_oil", "medium", june, "Point-in-time level supported by ship-to-ship transfers; not a monthly average."),
        # June commentary period anchors.
        ("iea_commentary_marmay_hormuz", "2026-05", "2026-03-01/2026-05-31", "2026-06-22", "IEA June adjustment commentary", "period_average_estimate", "hormuz_oil_flow", "Strait of Hormuz", 2.7, "mb/d", "Average oil flow through Hormuz during March-May.", "total_oil", "medium_high", commentary, "Compare with IEA's roughly 20 mb/d pre-war level."),
        ("iea_commentary_prewar_hormuz", "2026-02", "pre-conflict", "2026-06-22", "IEA June adjustment commentary", "baseline_estimate", "hormuz_oil_flow", "Strait of Hormuz", 20.0, "mb/d", "Approximate oil flow through Hormuz before the conflict.", "total_oil", "medium_high", commentary, "Rounded baseline."),
        ("iea_commentary_marmay_stock_rate", "2026-05", "2026-03-01/2026-05-31", "2026-06-22", "IEA June adjustment commentary", "period_average_estimate", "observed_inventory_change_rate", "World", -3.8, "mb/d", "Average observed inventory change since conflict start; negative is a draw.", "crude_and_products_observed", "medium", commentary, "Later monthly revisions mean this should not replace the monthly ledger."),
        ("iea_commentary_jun_yanbu", "2026-06", "early June", "2026-06-22", "IEA June adjustment commentary", "point_in_time_estimate", "non_hormuz_export_flow", "Saudi Arabia via Yanbu", 5.0, "mb/d", "Saudi oil exports from the Red Sea port of Yanbu.", "total_oil", "medium", commentary, "IEA says more than 5 mb/d; value is a lower bound."),
        ("iea_commentary_mar_uae_exports", "2026-03", "2026-03", "2026-06-22", "IEA June adjustment commentary", "retrospective_estimate", "total_oil_exports", "United Arab Emirates", 1.9, "mb/d", "UAE total oil exports.", "total_oil", "medium", commentary, "Kpler-based IEA estimate."),
        ("iea_commentary_jun_uae_exports", "2026-06", "early June", "2026-06-22", "IEA June adjustment commentary", "point_in_time_estimate", "total_oil_exports", "United Arab Emirates", 4.3, "mb/d", "UAE total oil exports.", "total_oil", "medium", commentary, "Early-June level, about 85% of pre-war exports."),
        # July OMR incorporates the June partial reopening and May stock revision.
        ("iea_jul_may_demand", "2026-05", "2026-05", "2026-07-10", "IEA OMR July 2026", "revised_preliminary_estimate", "global_oil_demand", "World", 97.9, "mb/d", "IEA total oil demand.", "total_oil", "medium_high", july, "May nadir; 5.3 mb/d below May 2025."),
        ("iea_jul_may_inventory", "2026-05", "2026-05", "2026-07-10", "IEA OMR July 2026", "revised_preliminary_estimate", "observed_inventory_change", "World", -73.0, "million_barrels", "Observed total oil inventory change; negative is a draw.", "crude_and_products_observed", "medium_high", july, "Revises the June OMR estimate of -143 mb."),
        ("iea_jul_jun_supply", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "global_oil_supply", "World", 98.8, "mb/d", "IEA total oil supply.", "total_oil", "high", july, "June partial reopening lifted supply by 4.1 mb/d."),
        ("iea_jul_jun_supply_loss", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "global_oil_supply_loss_vs_prewar", "World", 9.4, "mb/d", "Pre-war level less June global oil supply; positive is loss.", "total_oil", "high", july, "Preserves the June relaxation rather than treating March-June as one closure regime."),
        ("iea_jul_jun_inventory", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "observed_inventory_change", "World", 21.0, "million_barrels", "Observed total oil inventory change; positive is a build.", "crude_and_products_observed", "medium_high", july, "Oil on water more than offset continued onshore draws."),
        ("iea_jul_jun_onshore", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "onshore_inventory_change", "World", -96.0, "million_barrels", "Observed onshore inventory change.", "crude_and_products_observed", "medium", july, "Oil on water rose by 117 mb."),
        ("iea_jul_jun_water", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "oil_on_water_change", "World", 117.0, "million_barrels", "Observed oil-on-water change.", "crude_and_products_observed", "medium", july, "Do not treat all oil on water as delivered end-market supply."),
        ("iea_jul_jun_gulf_exports", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "total_oil_exports", "Gulf producers", 16.1, "mb/d", "Total Gulf oil exports including bypass routes.", "total_oil", "medium_high", july, "Up 6.5 mb/d in June but below 24 mb/d pre-war average."),
        ("iea_jul_prewar_gulf_exports", "2026-02", "pre-conflict average", "2026-07-10", "IEA OMR July 2026", "baseline_estimate", "total_oil_exports", "Gulf producers", 24.0, "mb/d", "Average total Gulf oil exports before the war.", "total_oil", "medium_high", july, "Includes volumes bypassing Hormuz."),
        ("iea_jul_jun_gulf_prod_loss", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "affected_gulf_output_loss_vs_prewar", "Gulf producers", 11.4, "mb/d", "Gulf production below pre-war levels; positive is loss.", "total_oil", "medium_high", july, "Gulf production rose 3.5 mb/d in June."),
        ("iea_jul_jun_runs_change", "2026-06", "2026-06", "2026-07-10", "IEA OMR July 2026", "preliminary_estimate", "global_refinery_crude_throughput_change_mom", "World", 1.5, "mb/d", "Monthly change in global refinery crude runs.", "crude_throughput", "medium_high", july, "Runs were still 6 mb/d below June 2025."),
    ]
    rows = []
    for spec in specs:
        (
            row_id,
            observation_month,
            observation_period,
            vintage,
            source,
            status,
            metric,
            geography,
            value,
            unit,
            definition,
            taxonomy,
            confidence,
            citation,
            notes,
        ) = spec
        rows.append(
            row(
                row_id,
                observation_month,
                observation_period,
                vintage,
                source,
                "IEA_OMR_or_commentary",
                "postshock_vintage" if vintage >= "2026-02-28" else "frozen_prewar_forecast",
                status,
                metric,
                geography,
                value,
                unit,
                definition,
                taxonomy,
                confidence,
                citation,
                notes,
            )
        )
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("no rows built")
    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate row_id")
    for item in rows:
        if set(item) != set(FIELDS):
            raise ValueError(f"schema mismatch: {item['row_id']}")
        if item["observation_month"] < "2026-02" or item["observation_month"] > "2026-08":
            raise ValueError(f"observation outside requested window: {item['row_id']}")
        float(item["value"])
        if not item["citation"].startswith("https://"):
            raise ValueError(f"bad citation: {item['row_id']}")

    frozen = [
        item
        for item in rows
        if item["counterfactual_role"] == "frozen_prewar_forecast" and item["source_family"] == "EIA_STEO"
    ]
    expected_frozen = len(MONTH_COLUMNS) * 3
    if len(frozen) != expected_frozen:
        raise ValueError(f"expected {expected_frozen} frozen EIA rows, got {len(frozen)}")


def main() -> None:
    rows = build_eia_rows() + build_eia_narrative_rows() + build_iea_rows()
    rows.sort(key=lambda item: (item["publication_vintage"], item["observation_month"], item["row_id"]))
    validate(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows) on {date.today().isoformat()}")


if __name__ == "__main__":
    main()
