#!/usr/bin/env python3
"""Build the m8q.11 evidence and scenario ledger for the inventory residual.

The scenario rows are disciplined sensitivity cases, not estimates of hidden stocks.
Each scenario allocation closes to the 308.171 million barrel project residual.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/derived/hormuz_m8q_11_inventory_residual_scenarios.csv"

FIELDS = [
    "row_id",
    "record_type",
    "scenario",
    "mechanism",
    "geography",
    "stock_scope",
    "period_start",
    "period_end",
    "value_million_bbl",
    "status",
    "confidence",
    "source_publication_date",
    "source_url",
    "evidence_summary",
    "accounting_interpretation",
    "double_counting_rule",
]


def row(
    row_id: str,
    record_type: str,
    scenario: str,
    mechanism: str,
    geography: str,
    stock_scope: str,
    period_start: str,
    period_end: str,
    value: float,
    status: str,
    confidence: str,
    source_date: str,
    source_url: str,
    evidence: str,
    interpretation: str,
    double_counting: str,
) -> dict[str, str]:
    return {
        "row_id": row_id,
        "record_type": record_type,
        "scenario": scenario,
        "mechanism": mechanism,
        "geography": geography,
        "stock_scope": stock_scope,
        "period_start": period_start,
        "period_end": period_end,
        "value_million_bbl": f"{value:.6f}",
        "status": status,
        "confidence": confidence,
        "source_publication_date": source_date,
        "source_url": source_url,
        "evidence_summary": evidence,
        "accounting_interpretation": interpretation,
        "double_counting_rule": double_counting,
    }


def build_rows() -> list[dict[str, str]]:
    iea_may = "https://www.iea.org/reports/oil-market-report-may-2026"
    iea_june = "https://www.iea.org/reports/oil-market-report-june-2026"
    iea_july = "https://www.iea.org/reports/oil-market-report-july-2026"
    iea_method = "https://www.iea.org/articles/oil-market-report-glossary"
    eia_feb = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
    eia_july = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
    eia_spr = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
    eia_total = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1"
    kpler_may = "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2"
    kpler_june = "https://www.kpler.com/blog/returning-persian-gulf-barrels-risk-a-short-term-supply-glut"
    china_bloomberg = "https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/"
    china_policy = "https://www.straitstimes.com/asia/china-allows-state-oil-firms-to-tap-reserves-as-middle-east-war-drags"

    rows = [
        row(
            "anchor-eia-implied-draw-march-june", "observed_anchor", "", "supply_minus_demand_implied_inventory_draw",
            "World", "all_liquids_balance", "2026-03-01", "2026-06-30", 606.171,
            "project_calculation_from_frozen_forecast_vintages", "medium", "2026-07-07",
            f"{eia_feb} | {eia_july}",
            "July STEO supply less consumption compared with the frozen February path implies 606.171 million barrels of actual draw after separating the foregone February-forecast stock build.",
            "A balance residual, not a direct tank observation.",
            "Starting identity; do not add scenario components to it.",
        ),
        row(
            "anchor-iea-observed-composite-march-june", "observed_anchor", "", "global_observed_inventory_draw",
            "World", "primary_stocks_plus_observed_oil_on_water", "2026-03-01", "2026-06-30", 298.000,
            "project_mixed_vintage_composite", "medium_low", "2026-07-10",
            f"{iea_may} | {iea_july}",
            "Project composite: March 129, April 117, May 73, and June minus 21 million barrels on a draw-positive convention.",
            "This 298 is not a cumulative figure printed in one IEA vintage; later reports substantially revised preliminary months.",
            "Includes observed OECD government and industry stocks, visible non-OECD stocks, and oil on water.",
        ),
        row(
            "anchor-project-residual-march-june", "observed_anchor", "", "implied_less_observed_inventory_draw",
            "World", "coverage_model_statistical_residual", "2026-03-01", "2026-06-30", 308.171,
            "project_difference_between_unlike_systems", "low_for_physical_interpretation", "2026-08-04",
            f"{eia_feb} | {eia_july} | {iea_may} | {iea_july}",
            "606.171 less 298.000 equals 308.171 million barrels.",
            "Difference between a modeled global balance and a mixed-vintage observed-stock composite; not a measured hidden draw.",
            "Scenario allocations below partition this row and must never be added to it.",
        ),
        row(
            "anchor-us-commercial-draw-march-june", "observed_anchor", "", "commercial_petroleum_stock_draw",
            "United States", "primary_industry_all_petroleum_excluding_spr", "2026-03-01", "2026-06-26", 67.317,
            "weekly_observed_month_end_proxy", "high", "2026-07-29", eia_total,
            "Sum of project monthly weekly-EIA changes for March through June: -4.712, 26.411, 30.837, and 14.781 million barrels.",
            "Included in IEA observed OECD stocks; excluded from the IEA collective-action execution headline unless a specific obligated-industry action applies.",
            "Do not put this 67.317 into the 308.171 residual; it is already inside the 298 observed-stock composite.",
        ),
        row(
            "anchor-us-spr-draw-march-june", "observed_anchor", "", "government_spr_draw",
            "United States", "government_primary_stock", "2026-03-01", "2026-06-26", 89.786,
            "weekly_observed_month_end_proxy", "high", "2026-07-29", eia_spr,
            "Sum of project monthly weekly-EIA changes for March through June: 0.377, 17.140, 40.805, and 31.464 million barrels.",
            "Included both in global observed stocks and, to the extent delivered under the program, the IEA collective-action execution total.",
            "Do not add to either the 298 observed draw or the 290 collective release when using those aggregates.",
        ),
        row(
            "anchor-us-combined-draw-march-june", "memo_subtotal", "", "government_plus_commercial_stock_draw",
            "United States", "primary_government_and_industry", "2026-03-01", "2026-06-26", 157.103,
            "arithmetic_subtotal", "high", "2026-07-29", f"{eia_spr} | {eia_total}",
            "89.786 million barrels of SPR draw plus 67.317 million barrels of total commercial petroleum draw.",
            "About 52.7% of the 298 million barrel project composite, before small IEA standardization and endpoint differences.",
            "Memo subtotal; do not add to its two components or to the IEA observed aggregate.",
        ),
        row(
            "anchor-china-known-visible-net", "observed_anchor", "", "visible_crude_stock_draw",
            "China", "ownership_unresolved_visible_tanks", "2026-03-01", "2026-06-30", 1.000,
            "partial_month_observation", "medium", "2026-07-10", iea_july,
            "IEA reported a 40 million barrel March build and 41 million barrel June draw; April and May are not ownership-resolved in the public summary.",
            "Visible China changes are already inside observed non-OECD stocks; the known-month net says little about hidden underground movement.",
            "Do not add the March and June observations to global stocks; they are subcomponents.",
        ),
        row(
            "anchor-kpler-china-visible-midmay", "analyst_anchor", "", "visible_crude_stock_change",
            "China", "observable_onshore_crude", "2026-02-28", "2026-05-13", -25.000,
            "analyst_estimate_build_draw_positive", "medium", "2026-05-13", kpler_may,
            "Kpler estimated observable Chinese crude inventories near a record 1.24 billion barrels, up roughly 25 million since the conflict began.",
            "Evidence against a large visible early-war draw; does not observe underground SPR.",
            "Already within visible-stock estimates and not additive to IEA global observed stocks.",
        ),
        row(
            "anchor-energy-aspects-china-late-draw", "analyst_anchor", "", "visible_commercial_crude_stock_draw",
            "China", "satellite_observed_tanks", "2026-05-01", "2026-06-07", 25.000,
            "analyst_satellite_estimate", "medium", "2026-06-10", china_bloomberg,
            "Energy Aspects, citing Kayrros, estimated almost 25 million barrels drawn from May through 7 June; Vortexa, Kpler and Energy Aspects expected about 1 mb/d draws in coming months.",
            "Supports a late commercial draw, but it is likely substantially captured by the IEA visible China estimate.",
            "Do not treat as evidence for an additional 25 million hidden draw.",
        ),
        row(
            "anchor-china-commercial-authorization", "analyst_anchor", "", "commercial_inventory_release_authorization",
            "China", "commercial_and_operational", "2026-04-01", "2026-06-30", 91.000,
            "analyst_flow_scenario_not_delivery", "low_medium", "2026-04-10", china_policy,
            "Energy Aspects said China could allow around 1 mb/d of commercial-reserve use in April-June; FGE estimated as much as 1 mb/d in April.",
            "Authorization/analyst capacity, not an observed 91 million barrel draw. Later visible-tank evidence was much smaller and at times showed builds.",
            "Context only; excluded from scenario arithmetic and observed totals.",
        ),
        row(
            "anchor-kpler-japan-draw-midmay", "analyst_anchor", "", "crude_inventory_draw",
            "Japan", "government_and_commercial_crude", "2026-02-28", "2026-05-13", 70.000,
            "analyst_lower_bound_more_than", "medium", "2026-05-13", kpler_may,
            "Kpler estimated Japan had cut stocks by more than 70 million barrels from a 350 million barrel pre-war baseline.",
            "Material but OECD-visible; it helps explain the 298 observed draw, not the 308 residual.",
            "Do not allocate again as hidden stock.",
        ),
        row(
            "anchor-kpler-korea-draw-midmay", "analyst_anchor", "", "visible_crude_inventory_draw",
            "South Korea", "observable_crude", "2026-02-28", "2026-05-13", 7.000,
            "analyst_estimate", "medium_low", "2026-05-13", kpler_may,
            "Kpler estimated a seven million barrel wartime reduction while noting possible unreported SPR activity or refinery cuts.",
            "Visible portion belongs in OECD observed stocks; unreported activity remains a possibility, not a quantity.",
            "Do not add visible draw to the residual.",
        ),
        row(
            "anchor-kpler-india-draw-midmay", "analyst_anchor", "", "crude_inventory_draw",
            "India", "spr_commercial_refinery_crude", "2026-02-28", "2026-05-13", 16.000,
            "analyst_estimate", "medium", "2026-05-15", "https://m.economictimes.com/markets/commodities/news/indias-crude-oil-stocks-drop-15-amid-iran-conflict-raising-supply-concerns/amp_articleshow/131105689.cms",
            "Kpler estimated 107 million barrels at end-February and 91 million in mid-May, including SPR, commercial and refinery tanks.",
            "Likely within visible non-OECD stocks to the extent captured by IEA/Kpler; illustrates material refinery-stock use outside the IEA release program.",
            "Do not automatically classify as unobserved residual.",
        ),
        row(
            "anchor-kpler-exchina-asia-draw-march-may", "analyst_anchor", "", "regional_inventory_draw",
            "Asia-Pacific excluding China", "onshore_stockpiles", "2026-03-01", "2026-05-31", 78.000,
            "analyst_estimate", "medium", "2026-06-17", kpler_june,
            "Kpler estimated ex-China Asia-Pacific stockpiles drew 78 million barrels over March-May.",
            "Cross-check on Japan, Korea, India and regional draws; mostly overlaps country and IEA observed-stock estimates.",
            "Regional overlap; never add to country rows.",
        ),
        row(
            "anchor-iea-june-oil-on-water-build", "observed_anchor", "", "oil_on_water_stock_change",
            "World", "oil_on_water", "2026-06-01", "2026-06-30", -117.000,
            "preliminary_observation_build_draw_positive", "medium", "2026-07-10", iea_july,
            "IEA estimated oil on water swelled by 117 million barrels in June while onshore tanks drew about 96 million.",
            "Explains the net 21 million barrel June global build and shows why onshore-only and global-observed series diverge.",
            "Already included in IEA global observed stocks; only measurement/timing error around it can enter the residual scenario.",
        ),
        row(
            "anchor-iea-preliminary-revisions", "methodology_anchor", "", "preliminary_stock_revision",
            "World", "observed_stock_series", "2026-03-01", "2026-05-31", 0.000,
            "qualitative_revision_evidence", "high", "2026-07-10", f"{iea_may} | {iea_june} | {iea_july} | {iea_method}",
            "Published preliminary estimates moved materially: March 85 to 129; April 117 in May versus 74 in June; May 143 in June versus 73 in July.",
            "The 298 million barrel project figure mixes latest explicit monthly headlines rather than using a single internally consistent OMR vintage.",
            "Zero-valued methodology memo; scenario revision allowance is separate.",
        ),
        row(
            "anchor-iea-coverage-rule", "methodology_anchor", "", "stock_coverage_definition",
            "World", "primary_stocks", "2026-03-01", "2026-06-30", 0.000,
            "official_methodology", "high", "2022-04-04", iea_method,
            "IEA stocks are generally primary stocks at refineries, gas plants, terminals, entrepots, pipelines and incoming vessels; tertiary/end-user and power-station stocks are excluded. Non-OECD data have no formal submission system and variable lags.",
            "Provides a defensible place for genuine unobserved physical draws, especially outside OECD and downstream of primary storage.",
            "Definition memo; no quantity to add.",
        ),
        row(
            "anchor-iea-misc-to-balance-rule", "methodology_anchor", "", "miscellaneous_to_balance",
            "World", "balance_discrepancy", "2026-03-01", "2026-06-30", 0.000,
            "official_methodology", "high", "2022-04-04", iea_method,
            "IEA says its balancing item combines non-reported stocks, floating storage and oil in transit, plus errors in demand, supply and stock estimates; it does not force an exact balance.",
            "Direct official support for treating much of the 308.171 as model/coverage discrepancy rather than hidden SPR.",
            "Definition memo; no quantity to add.",
        ),
    ]

    allocations = {
        "low_hidden_physical": {
            "hidden_china_underground_or_spr": 0.000,
            "other_non_oecd_unreported_primary_stocks": 30.000,
            "excluded_secondary_and_tertiary_stocks": 10.000,
            "oil_on_water_and_cargo_timing_error": 20.000,
            "iea_preliminary_vintage_and_cutoff": 35.000,
            "eia_supply_demand_balance_error": 213.171,
        },
        "base_mixed": {
            "hidden_china_underground_or_spr": 20.000,
            "other_non_oecd_unreported_primary_stocks": 70.000,
            "excluded_secondary_and_tertiary_stocks": 25.000,
            "oil_on_water_and_cargo_timing_error": 35.000,
            "iea_preliminary_vintage_and_cutoff": 35.000,
            "eia_supply_demand_balance_error": 123.171,
        },
        "high_hidden_physical": {
            "hidden_china_underground_or_spr": 75.000,
            "other_non_oecd_unreported_primary_stocks": 110.000,
            "excluded_secondary_and_tertiary_stocks": 35.000,
            "oil_on_water_and_cargo_timing_error": 40.000,
            "iea_preliminary_vintage_and_cutoff": 35.000,
            "eia_supply_demand_balance_error": 13.171,
        },
    }
    metadata = {
        "hidden_china_underground_or_spr": (
            "China", "underground_government_or_noc_stocks", "scenario_hidden_physical_draw", "low",
            f"{china_bloomberg} | {kpler_may}",
            "Kpler found visible stocks building early and said SPR continued adding even as commercial tanks later drew; it could not rule out underground SPR transfers.",
            "Additional net draw not captured in visible China estimates. Base 20 is deliberately below the reported 25 million visible late draw; high 75 averages 0.62 mb/d over 121 days.",
        ),
        "other_non_oecd_unreported_primary_stocks": (
            "Non-OECD excluding China", "unreported_primary_commercial_government_and_producer_stocks", "scenario_hidden_physical_draw", "low",
            f"{iea_method} | {kpler_may}",
            "IEA has no formal non-OECD stock-submission system; India and other country evidence shows commercial/refinery stocks were used.",
            "Net draw outside the visible-stock perimeter after removing country movements already captured by IEA/Kpler.",
        ),
        "excluded_secondary_and_tertiary_stocks": (
            "World", "end_user_retail_power_station_and_other_nonprimary_stocks", "scenario_hidden_physical_draw", "low",
            iea_method,
            "IEA explicitly excludes tertiary/end-user and power-station stocks from its primary-stock definition.",
            "Physical oil consumed from stocks downstream of the primary reporting perimeter.",
        ),
        "oil_on_water_and_cargo_timing_error": (
            "World", "oil_on_water_and_in_transit_measurement", "scenario_measurement_timing", "low_medium",
            f"{iea_july} | {kpler_may} | {iea_method}",
            "Oil-on-water estimates swung by more than 100 million barrels and depend on cargo timing, AIS visibility and geographic classification.",
            "Measurement/timing difference only; the observed oil-on-water change itself is already inside the IEA total.",
        ),
        "iea_preliminary_vintage_and_cutoff": (
            "World", "preliminary_observed_stock_revision", "scenario_measurement_timing", "medium",
            f"{iea_may} | {iea_june} | {iea_july} | {iea_method}",
            "Large month revisions and mixed publication vintages make a tens-of-millions reconciliation allowance unavoidable.",
            "Not a physical draw; captures IEA standardization, preliminary-to-official revisions and endpoint mismatch.",
        ),
        "eia_supply_demand_balance_error": (
            "World", "supply_demand_forecast_and_taxonomy_error", "scenario_model_residual", "low",
            f"{eia_feb} | {eia_july} | {iea_method}",
            "Kpler said a deficit not visible in data could be underground draw or further refinery-run reductions, especially China; IEA methodology likewise leaves supply-demand-stock discrepancies in miscellaneous-to-balance.",
            "Demand may still be too high, supply too low, or taxonomy/timing inconsistent in the EIA vintage comparison. This is the closing model allocation.",
        ),
    }

    for scenario, parts in allocations.items():
        assert abs(sum(parts.values()) - 308.171) < 1e-9
        for mechanism, value in parts.items():
            geography, stock_scope, status, confidence, source_url, evidence, interpretation = metadata[mechanism]
            rows.append(
                row(
                    f"scenario-{scenario}-{mechanism}", "scenario_allocation", scenario, mechanism,
                    geography, stock_scope, "2026-03-01", "2026-06-30", value,
                    status, confidence, "2026-08-04", source_url, evidence, interpretation,
                    "Mutually exclusive within this scenario; scenario components sum to 308.171 million barrels.",
                )
            )
        physical = sum(
            parts[key]
            for key in (
                "hidden_china_underground_or_spr",
                "other_non_oecd_unreported_primary_stocks",
                "excluded_secondary_and_tertiary_stocks",
            )
        )
        rows.extend(
            [
                row(
                    f"scenario-{scenario}-hidden-physical-subtotal", "scenario_memo_subtotal", scenario,
                    "hidden_physical_draw_subtotal", "World", "outside_iea_observed_perimeter",
                    "2026-03-01", "2026-06-30", physical, "scenario_subtotal", "low", "2026-08-04",
                    iea_method, "Sum of the three hidden-physical scenario components.",
                    "Candidate physical stock draw not present in the 298 million barrel observed composite.",
                    "Memo subtotal; do not add to scenario components.",
                ),
                row(
                    f"scenario-{scenario}-total", "scenario_total", scenario,
                    "residual_allocation_total", "World", "coverage_model_statistical_residual",
                    "2026-03-01", "2026-06-30", sum(parts.values()), "scenario_total", "arithmetic", "2026-08-04",
                    f"{eia_feb} | {eia_july} | {iea_may} | {iea_july}",
                    "Exact sum of mutually exclusive scenario allocations.",
                    "Closes to the 308.171 million barrel project residual; not an estimate of hidden tanks.",
                    "Memo total; do not add to scenario components.",
                ),
            ]
        )

    return rows


def main() -> None:
    rows = build_rows()
    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row_id")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
