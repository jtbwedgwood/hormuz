#!/usr/bin/env python3
"""Build the independent two-stage audit of the March-July 2026 oil bridge."""

from __future__ import annotations

import calendar
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BALANCE = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
GULF = ROOT / "data/derived/hormuz_m8q_6_gulf_physical_oil_ledger.csv"
NONGULF = ROOT / "data/derived/hormuz_m8q_7_nongulf_supply_ledger.csv"
STOCK_DEMAND = ROOT / "data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv"
EMERGENCY_EXECUTION = ROOT / "data/derived/hormuz_m8q_10_emergency_release_execution.csv"
OUT = ROOT / "data/derived/hormuz_m8q_9_historical_bridge_audit.csv"

FIELDS = [
    "row_id", "accounting_frame", "stage", "period_start", "period_end",
    "data_cutoff", "component_group", "component", "geography", "arithmetic_role",
    "value_low_case", "value_base_case", "value_high_case", "unit", "data_status",
    "estimate_type", "product_scope", "confidence", "source_url", "method",
    "causal_warning", "double_counting_rule",
]

FEB_VINTAGE = "2026-02-10"
JUL_VINTAGE = "2026-07-07"
EIA_URLS = (
    "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx | "
    "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
)
IEA_OMR_URLS = (
    "https://www.iea.org/reports/oil-market-report-march-2026 | "
    "https://www.iea.org/reports/oil-market-report-april-2026 | "
    "https://www.iea.org/reports/oil-market-report-may-2026 | "
    "https://www.iea.org/reports/oil-market-report-july-2026"
)


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fmt(value: float | str | None) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.6f}".rstrip("0").rstrip(".")


def row(row_id: str, frame: str, stage: str, start: str, end: str, cutoff: str,
        group: str, component: str, geography: str, role: str,
        low: float | str | None, base: float | str | None, high: float | str | None,
        status: str, estimate_type: str, scope: str, confidence: str, source: str,
        method: str, causal: str, overlap: str) -> dict[str, str]:
    values = [
        row_id, frame, stage, start, end, cutoff, group, component, geography, role,
        fmt(low), fmt(base), fmt(high), "million_bbl", status, estimate_type, scope,
        confidence, source, method, causal, overlap,
    ]
    return dict(zip(FIELDS, values, strict=True))


def balance_totals(balance: list[dict[str, str]], months: list[str]) -> dict[str, float]:
    def value(vintage: str, month: str, metric: str) -> float:
        matches = [
            x for x in balance
            if x["source_family"] == "EIA_STEO"
            and x["publication_vintage"] == vintage
            and x["observation_month"] == month
            and x["metric"] == metric
        ]
        if len(matches) != 1:
            raise ValueError(f"Expected one {vintage=} {month=} {metric=}, got {len(matches)}")
        return float(matches[0]["value"])

    totals = {"supply": 0.0, "demand": 0.0, "foregone_build": 0.0, "draw": 0.0}
    for month in months:
        days = calendar.monthrange(2026, int(month[-2:]))[1]
        feb_supply = value(FEB_VINTAGE, month, "global_liquids_supply")
        jul_supply = value(JUL_VINTAGE, month, "global_liquids_supply")
        feb_demand = value(FEB_VINTAGE, month, "global_liquids_consumption")
        jul_demand = value(JUL_VINTAGE, month, "global_liquids_consumption")
        totals["supply"] += (feb_supply - jul_supply) * days
        totals["demand"] += (feb_demand - jul_demand) * days
        totals["foregone_build"] += (feb_supply - feb_demand) * days
        totals["draw"] += (jul_demand - jul_supply) * days
    if abs(totals["supply"] - totals["demand"] - totals["foregone_build"] - totals["draw"]) > 1e-6:
        raise ValueError("EIA global market-clearing identity failed")
    return totals


def build() -> list[dict[str, str]]:
    balance = load(BALANCE)
    gulf = load(GULF)
    nongulf = load(NONGULF)
    stock_demand = load(STOCK_DEMAND)
    emergency_execution = load(EMERGENCY_EXECUTION)
    rows: list[dict[str, str]] = []

    mar_jun = balance_totals(balance, ["2026-03", "2026-04", "2026-05", "2026-06"])
    mar_jul = balance_totals(balance, ["2026-03", "2026-04", "2026-05", "2026-06", "2026-07"])

    def gulf_value(metric: str, field: str = "cumulative_million_barrels") -> float:
        matches = [x for x in gulf if x["metric"] == metric and x["record_type"] == "cumulative_reconciliation_summary"]
        if len(matches) != 1:
            raise ValueError(f"Expected one Gulf reconciliation row for {metric}")
        return float(matches[0][field])

    gross_missing = gulf_value("gross_hormuz_flow_loss")
    bypass_base = gulf_value("incremental_bypass_exports")
    bypass_row = next(x for x in gulf if x["metric"] == "incremental_bypass_exports")
    bypass_low = float(bypass_row["uncertainty_low_million_barrels"])
    bypass_high = float(bypass_row["uncertainty_high_million_barrels"])

    # Recomputed from the frozen-February and July EIA Table 3b regional rows for
    # March-June. The completed m8q.7 ledger publishes the equivalent March-July
    # total; this matched-cutoff audit deliberately excludes its July forecast.
    non_middle_east_mar_jun = 54.3815548481
    oman_mar_jun = sum(
        float(x["revision_million_bbl"]) for x in nongulf
        if x["record_type"] == "country_month" and x["country"] == "Oman" and x["period"] <= "2026-06"
    )
    route_residual = [
        gross_missing - bypass - non_middle_east_mar_jun - oman_mar_jun - mar_jun["supply"]
        for bypass in (bypass_low, bypass_base, bypass_high)
    ]

    route_common = dict(
        frame="A_physical_route_diagnostic", stage="gross_route_exposure_to_global_supply",
        start="2026-03-01", end="2026-06-30", cutoff="2026-06-30",
        status="estimated_actual_march_june", scope="mixed_total_oil_and_petroleum_liquids",
    )
    rows.extend([
        row("physical-gross-missing-hormuz", group="route_exposure", component="gross_missing_hormuz_flow",
            geography="Strait of Hormuz", role="starting_denominator", low=gross_missing, base=gross_missing,
            high=gross_missing, estimate_type="period_average_integration", confidence="medium",
            source=next(x["source_url"] for x in gulf if x["metric"] == "gross_hormuz_flow_loss"),
            method="20 mb/d pre-war flow less 2.7 mb/d March-May and inferred 8.9 mb/d June flow, integrated over calendar days.",
            causal="Missing transit is exposure, not automatically lost production or consumption.",
            overlap="Do not add this denominator to any downstream component.", **route_common),
        row("physical-incremental-bypass", group="route_preservation", component="incremental_non_hormuz_exports",
            geography="Gulf producers", role="subtract_from_gross_route_exposure", low=bypass_low, base=bypass_base,
            high=bypass_high, estimate_type="calibrated_range", confidence="low_medium",
            source=bypass_row["source_url"],
            method="Gross reconstructed bypass less a 3.8 mb/d pre-war working baseline; cases vary ramp timing and baseline.",
            causal="Incremental bypass preserved Gulf exports, but it is already embodied in actual Gulf/global supply.",
            overlap="Use only in Frame A; never add as a market-clearing offset in Frame B.", **route_common),
        row("physical-net-non-middle-east-supply", group="production_response", component="net_non_middle_east_supply_revision",
            geography="World excluding EIA Middle East", role="subtract_from_gross_route_exposure", low=non_middle_east_mar_jun,
            base=non_middle_east_mar_jun, high=non_middle_east_mar_jun, estimate_type="forecast_vintage_revision",
            confidence="medium_high_arithmetic_low_causal", source=EIA_URLS,
            method="Sum of complete EIA North America, Central/South America, Europe, Eurasia, Africa, and Asia/Oceania Table 3b revisions, March-June.",
            causal="A reproducible forecast revision, not proof that all additional output was induced by Hormuz.",
            overlap="Contains the country rows below; do not add country supply revisions to this subtotal.", **route_common),
        row("physical-oman-supply", group="production_response", component="oman_supply_revision",
            geography="Oman", role="subtract_from_gross_route_exposure", low=oman_mar_jun, base=oman_mar_jun,
            high=oman_mar_jun, estimate_type="forecast_vintage_revision", confidence="medium_high_arithmetic_low_causal",
            source=EIA_URLS, method="Sum of Oman March-June country-month revisions in m8q.7.",
            causal="Oman's export terminals are outside Hormuz, but the vintage difference is not a controlled causal estimate.",
            overlap="Oman is excluded from the non-Middle-East subtotal above; do not add its July forecast here.", **route_common),
        row("physical-global-supply-shortfall", group="outcome", component="net_global_supply_shortfall",
            geography="World", role="accounted_outcome", low=mar_jun["supply"], base=mar_jun["supply"],
            high=mar_jun["supply"], estimate_type="forecast_vintage_revision", confidence="medium_high_arithmetic_low_causal",
            source=EIA_URLS, method="Frozen February STEO supply less July-vintage preliminary supply, times calendar days.",
            causal="This is petroleum-and-other-liquids supply revision, not a causal Hormuz estimate.",
            overlap="This is the denominator for Frame B; do not add Frame A route components again.", **route_common),
        row("physical-route-supply-residual", group="residual", component="route_taxonomy_timing_residual",
            geography="Unallocated", role="closing_residual", low=route_residual[0], base=route_residual[1],
            high=route_residual[2], estimate_type="arithmetic_residual", confidence="low",
            source=f"{EIA_URLS} | {IEA_OMR_URLS}",
            method="Gross missing route flow minus incremental bypass, net non-Middle-East supply, Oman supply, and global supply shortfall. Cases correspond to low/base/high bypass.",
            causal="Absorbs export-versus-production boundaries, Gulf storage/domestic use, NGL/taxonomy differences, timing, and source revisions.",
            overlap="Do not back-allocate this residual to named countries without new evidence.", **route_common),
    ])

    # Route and crude country detail are memo rows. They make the story specific
    # without pretending these mixed-boundary quantities are additive slices.
    for item in gulf:
        if item["record_type"] == "cumulative_route_summary":
            rows.append(row(
                f"memo-route-{item['row_id']}", "A_physical_route_diagnostic", "country_route_memo",
                "2026-03-01", "2026-06-30", "2026-06-30", "route_preservation_detail",
                item["route_or_scope"], item["country"], "memo_suballocation_not_additive",
                float(item["cumulative_million_barrels"]), float(item["cumulative_million_barrels"]),
                float(item["cumulative_million_barrels"]), "estimated_actual_march_june", item["estimate_type"],
                item["product_scope"], item["confidence"], item["source_url"], item["method"],
                "Named-route values are calibrated estimates, not complete monthly cargo observations.",
                "Components explain the base bypass subtotal only after retaining the negative other-route calibration residual."
            ))
        if item["record_type"] == "cumulative_country_summary":
            value = float(item["cumulative_million_barrels"])
            rows.append(row(
                f"memo-shutin-{item['row_id']}", "A_physical_route_diagnostic", "country_crude_shutin_memo",
                "2026-03-01", "2026-06-30", "2026-06-30", "crude_shutin_detail",
                "closure_related_crude_production_shutin", item["country"], "parallel_crosscheck_not_additive",
                value, value, value, "estimated_actual_march_june", item["estimate_type"], item["product_scope"],
                item["confidence"], item["source_url"], item["method"],
                "Crude shut-ins omit condensates/NGLs and are not the same boundary as missing route flow.",
                "Country crude rows sum to 1,183.49 mb; compare with, never add to, the route bridge."
            ))

    # Material named supplier revisions through June, nested within the complete
    # geographical subtotal above.
    supply_country: dict[str, float] = {}
    supply_source: dict[str, str] = {}
    for item in nongulf:
        if item["record_type"] == "country_month" and item["period"] <= "2026-06":
            supply_country[item["country"]] = supply_country.get(item["country"], 0.0) + float(item["revision_million_bbl"])
            supply_source[item["country"]] = item["source_url"]
    for country, value in sorted(supply_country.items(), key=lambda pair: abs(pair[1]), reverse=True):
        if abs(value) < 1:
            continue
        rows.append(row(
            f"memo-supply-{country.lower().replace(' ', '-')}", "A_physical_route_diagnostic", "country_supply_memo",
            "2026-03-01", "2026-06-30", "2026-06-30", "production_response_detail",
            "petroleum_liquids_supply_revision", country, "memo_suballocation_not_additive",
            value, value, value, "preliminary_forecast_vintage_revision", "forecast_vintage_revision",
            "petroleum_and_other_liquid_fuels", "medium_high_arithmetic_low_causal", supply_source[country],
            "Sum of March-June July-vintage minus frozen-February country production revisions.",
            "Positive output cushioned the global revision; negative output worsened it. Causation is not identified.",
            "Nested within geographical totals; exports, policy commitments, and stock releases are not additional production."
        ))

    def add_market_frame(label: str, totals: dict[str, float], end: str, status: str) -> None:
        common = dict(
            frame=f"B_global_market_clearing_{label}", stage="net_supply_shortfall_absorption",
            start="2026-03-01", end=end, cutoff=end, status=status,
            estimate_type="EIA_forecast_vintage_identity", scope="petroleum_and_other_liquid_fuels",
        )
        components = [
            ("market-supply", "denominator", "net_global_supply_shortfall", "World", "starting_denominator", totals["supply"]),
            ("market-demand", "demand", "consumption_below_frozen_forecast", "World", "additive_absorption", totals["demand"]),
            ("market-foregone-build", "stocks", "expected_inventory_build_that_did_not_occur", "World", "additive_absorption", totals["foregone_build"]),
            ("market-implied-draw", "stocks", "implied_actual_inventory_draw", "World", "additive_absorption", totals["draw"]),
        ]
        for suffix, group, component, geography, role, value in components:
            rows.append(row(
                f"{suffix}-{label}", group=group, component=component, geography=geography, role=role,
                low=value, base=value, high=value, confidence="high_arithmetic_medium_measurement", source=EIA_URLS,
                method="Frozen February and July EIA STEO supply-demand identity, integrated over calendar days.",
                causal="A revision accounting identity, not proof that every demand or stock difference was caused by Hormuz.",
                overlap="Demand + foregone build + implied draw equals the supply-shortfall denominator; these are the only additive top-level slices.",
                **common
            ))

    add_market_frame("through_june", mar_jun, "2026-06-30", "march_june_preliminary")
    add_market_frame("through_july", mar_jul, "2026-07-31", "march_june_preliminary_july_forecast")

    # Observed-stock coverage diagnostic through June.
    observed_iea_draw = 298.0
    observed_gap = mar_jun["draw"] - observed_iea_draw
    for suffix, component, value, role, confidence in [
        ("iea-observed", "IEA_observed_inventory_draw", observed_iea_draw, "observed_subset", "medium"),
        ("eia-implied", "EIA_implied_inventory_draw", mar_jun["draw"], "comparison_total", "medium"),
        ("coverage-gap", "stock_coverage_and_model_residual", observed_gap, "closing_residual", "low"),
    ]:
        rows.append(row(
            f"stock-coverage-{suffix}", "C_stock_coverage_diagnostic", "observed_vs_implied_stocks",
            "2026-03-01", "2026-06-30", "2026-06-30", "inventory_coverage", component, "World", role,
            value, value, value, "preliminary_estimate", "cross_source_comparison",
            "crude_and_products_mixed_coverage", confidence, f"{EIA_URLS} | {IEA_OMR_URLS}",
            "IEA monthly observed changes (-129, -117, -73, +21 mb) compared with EIA supply-minus-demand implied draw.",
            "The difference reflects coverage, revisions, balancing items, and definitions; it is not evidence of hidden SPR alone.",
            "IEA observed draw + residual = EIA implied draw. Do not add either diagnostic to the top-level market bridge."
        ))

    # Emergency stocks are a suballocation of implied inventory draw, never a new
    # top-level category alongside that draw.
    emergency = next(x for x in stock_demand if x["row_id"] == "iea-jul31-nowcast")
    emergency_values = [float(emergency[x]) for x in ("value_low", "value_base", "value_high")]
    other_values = [mar_jul["draw"] - x for x in emergency_values]
    rows.extend([
        row("stock-suballocation-emergency", "D_july_stock_suballocation", "implied_draw_ownership",
            "2026-03-01", "2026-07-31", "2026-07-21", "inventory_draw", "IEA_emergency_oil_delivered_or_nowcast",
            "IEA members", "suballocation_of_implied_draw", *emergency_values, "observed_through_july21_plus_nowcast_to_july31",
            "observed_low_project_nowcast_base_high", "government_and_obligated_industry_emergency_oil", "medium_low",
            emergency["source_url"], emergency["method"],
            "Only 290 mb is officially reported through 21 July; 315/330 mb are July-end project nowcasts.",
            "Contained in global inventory movements and EIA implied draw; never add to the top-level draw slice."),
        row("stock-suballocation-other", "D_july_stock_suballocation", "implied_draw_ownership",
            "2026-03-01", "2026-07-31", "2026-07-31", "inventory_draw", "non_emergency_unobserved_and_balancing_draw",
            "World residual", "closing_suballocation_residual", *other_values, "arithmetic_residual",
            "residual_to_EIA_implied_draw", "mixed_commercial_nonIEA_unobserved_and_balancing", "low", EIA_URLS,
            "EIA implied draw less the alternative 290/315/330 mb emergency-release cases.",
            "Not a measured commercial-stock total; includes unobserved stocks and model/statistical balance.",
            "Emergency plus this residual equals implied draw in each case. The residual is inversely ordered across cases."),
    ])

    # Directly observed U.S. stock facts and the known aggregate/country imputation.
    for source_id, component, role in [
        ("us-spr-actual-cumulative", "US_SPR_actual_draw", "memo_observed_subcomponent"),
        ("us-spr-forecast-cumulative", "US_SPR_frozen_forecast_draw", "memo_counterfactual"),
        ("us-spr-change-swing", "US_SPR_draw_plus_foregone_build", "memo_cross_bucket_swing"),
        ("us-commercial_total-actual-cumulative", "US_total_commercial_petroleum_actual_draw", "memo_observed_subcomponent"),
        ("us-commercial_total-forecast-cumulative", "US_total_commercial_petroleum_frozen_forecast_draw", "memo_counterfactual"),
        ("us-commercial_total-change-swing", "US_total_commercial_draw_plus_foregone_build", "memo_cross_bucket_swing"),
    ]:
        item = next(x for x in stock_demand if x["row_id"] == source_id)
        value = float(item["value_base"])
        rows.append(row(
            f"memo-{source_id}", "D_july_stock_suballocation", "country_stock_memo", item["period_start"],
            item["period_end"], item["data_cutoff"], "US_stock_detail", component, "United States", role,
            value, value, value, item["status"], "weekly_observed_or_frozen_forecast", "source_series_definition",
            item["confidence"], item["source_url"], item["method"], item["causal_assessment"], item["double_counting_rule"]
        ))

    for item in emergency_execution:
        if item["record_type"] != "iea_290_reconciliation":
            continue
        rows.append(row(
            f"memo-{item['row_id']}", "D_july_stock_suballocation", "country_emergency_delivery_imputation",
            item["period_start"], item["period_end"], item["as_of_date"], "emergency_release_detail",
            "estimated_actual_emergency_oil_delivered", item["geography"], "memo_suballocation_not_additive",
            float(item["estimate_low_million_bbl"]), float(item["estimate_base_million_bbl"]),
            float(item["estimate_high_million_bbl"]), item["evidence_status"],
            "country_execution_audit_constrained_to_aggregate", "government_and_obligated_industry_emergency_oil",
            item["confidence"], item["source_url"], item["method"],
            "Only the aggregate 290 mb and selected national observations are directly evidenced; top-down rows remain inferences.",
            item["double_counting_rule"]
        ))

    # Exact regional demand decomposition and selected country suballocations.
    for item in stock_demand:
        if item["ledger_group"] != "demand_counterfactual" or item["observation_month"]:
            continue
        if item["accounting_level"] not in {"component", "suballocation", "residual_suballocation"}:
            continue
        value = float(item["value_base"])
        role = "additive_region_component" if item["accounting_level"] == "component" else "memo_suballocation_not_additive"
        rows.append(row(
            f"memo-{item['row_id']}", "E_demand_decomposition", "regional_and_country_demand",
            item["period_start"], item["period_end"], item["data_cutoff"], "demand_detail",
            "consumption_below_frozen_february_forecast", item["geography"], role,
            value, value, value, item["status"], "forecast_vintage_revision", "petroleum_and_other_liquid_fuels",
            item["confidence"], item["source_url"], item["method"], item["causal_assessment"], item["double_counting_rule"]
        ))
    korea = next(x for x in stock_demand if x["row_id"] == "korea-demand-inference-cumulative")
    rows.append(row(
        "memo-korea-demand-inference", "E_demand_decomposition", "country_demand_inference",
        korea["period_start"], korea["period_end"], korea["data_cutoff"], "demand_detail",
        "inferred_consumption_reduction", "South Korea", "candidate_suballocation_not_additive",
        float(korea["value_low"]), float(korea["value_base"]), float(korea["value_high"]), korea["status"],
        "project_inference", "petroleum_and_other_liquid_fuels", korea["confidence"], korea["source_url"],
        korea["method"], korea["causal_assessment"], korea["double_counting_rule"]
    ))

    ids = [x["row_id"] for x in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate audit row IDs")

    # Core identity tests.
    for case, bypass, residual in zip(("low", "base", "high"),
                                      (bypass_low, bypass_base, bypass_high), route_residual):
        closed = bypass + non_middle_east_mar_jun + oman_mar_jun + mar_jun["supply"] + residual
        if abs(closed - gross_missing) > 1e-6:
            raise ValueError(f"Physical bridge does not close in {case} case")
    for emergency_value, other_value in zip(emergency_values, other_values):
        if abs(emergency_value + other_value - mar_jul["draw"]) > 1e-6:
            raise ValueError("Inventory suballocation does not close")
    regional_demand = sum(
        float(x["value_base_case"]) for x in rows
        if x["accounting_frame"] == "E_demand_decomposition" and x["arithmetic_role"] == "additive_region_component"
    )
    if abs(regional_demand - mar_jul["demand"]) > 1e-4:
        raise ValueError("Regional demand bridge does not close")
    country_execution_base = sum(
        float(x["value_base_case"]) for x in rows
        if x["stage"] == "country_emergency_delivery_imputation"
    )
    if abs(country_execution_base - 290.0) > 1e-4:
        raise ValueError("Country emergency-release base estimates do not close to 290 mb")
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
