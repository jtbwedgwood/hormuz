#!/usr/bin/env python3
"""Build the p2k.1 oil-shock absorption buffer balance sheet.

The output deliberately keeps three different objects separate:

* upstream physical offsets (bypass and non-Gulf supply),
* downstream market-clearing absorbers (stocks, foregone builds and demand), and
* memo/uncertainty rows that must not be added to either bridge.

For inventories, the script publishes fixed-rate days-to-zero as a permissive
upper bound while preserving a separate days-to-binding-floor estimate.  It does
not substitute one for the other.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv"
R3V1 = ROOT / "data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv"
P2K4 = ROOT / "data/derived/hormuz_p2k_4_china_demand_reclassification.csv"
P2K5 = ROOT / "data/derived/hormuz_p2k_5_foregone_build_capacity.csv"
P2K7 = ROOT / "data/derived/hormuz_p2k_7_bypass_headroom_vulnerability.csv"
P2K6 = ROOT / "data/derived/hormuz_p2k_6_historical_durability_transfer.csv"
P2K3 = ROOT / "data/derived/hormuz_p2k_3_demand_cost_tier_matrix.csv"
P2K8 = ROOT / "data/derived/hormuz_p2k_8_stock_exhaustion_bounds.csv"
P2K12 = ROOT / "data/derived/hormuz_p2k_12_oil_on_water_split.csv"

FIELDS = [
    "row_id", "record_type", "accounting_frame", "additivity", "channel_group",
    "channel", "geography", "as_of_date", "horizon_months", "horizon_date",
    "historical_million_bbl", "historical_low_million_bbl",
    "historical_high_million_bbl", "current_level", "level_unit",
    "floor_or_ceiling", "floor_or_ceiling_unit", "usable_headroom",
    "headroom_unit", "current_flow_mb_per_day", "burn_or_growth_rate_mb_per_day",
    "headroom_days_at_current_rate", "volume_headroom_status",
    "rate_capacity_status", "failure_or_exhaustion_shape", "marginal_absorber",
    "economic_cost_tier", "evidence_tier", "confidence", "source_url",
    "source_row_ids", "method", "interpretation", "caveat",
]

IEA_SECURITY = "https://www.iea.org/topics/oil-security"
IEA_JULY = "https://www.iea.org/news/iea-executive-director-statement-on-oil-markets"
DOE_FACTS = "https://www.energy.gov/ceser/spr-quick-facts"
EIA_SPR = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
EIA_COMM = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1"


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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def by_id(path: Path) -> dict[str, dict[str, str]]:
    return {item["row_id"]: item for item in read_rows(path)}


def number(item: dict[str, str], field: str) -> float:
    return float(item[field])


def china_reclassification() -> tuple[float, float, float, str]:
    """Return low/base/high China inventory reclassification, if p2k.4 exists.

    The dedicated audit is allowed to conclude zero.  Matching is semantic so
    p2k.1 does not depend on an undocumented row order.
    """
    if not P2K4.exists():
        return 0.0, 0.0, 0.0, "p2k.4_not_yet_available"
    candidates = [
        item for item in read_rows(P2K4)
        if "reclassification" in item.get("row_id", "")
        and "march-june" in item.get("row_id", "")
        and "cumulative" in item.get("row_id", "")
    ]
    if len(candidates) != 1:
        raise ValueError(f"Expected one March-June reclassification row; found {len(candidates)}")
    item = candidates[0]
    value_fields = [
        ("value_low_million_bbl", "value_base_million_bbl", "value_high_million_bbl"),
        ("low_million_bbl", "base_million_bbl", "high_million_bbl"),
        ("estimate_low_million_bbl", "estimate_base_million_bbl", "estimate_high_million_bbl"),
        ("reclass_low", "reclass_base", "reclass_high"),
    ]
    for low_field, base_field, high_field in value_fields:
        if all(item.get(field, "") != "" for field in (low_field, base_field, high_field)):
            return (
                float(item[low_field]), float(item[base_field]), float(item[high_field]),
                item["row_id"],
            )
    raise ValueError("p2k.4 reclassification row lacks a recognized low/base/high field set")


def build() -> list[dict[str, str]]:
    r3v = by_id(R3V1)
    bypass = by_id(P2K7)["system-bypass-summary"]
    foregone = by_id(P2K5)["verdict-durable-buffer-credit"]
    demand_cost = by_id(P2K3)
    reclass_low, reclass_base, reclass_high, reclass_row = china_reclassification()

    net_loss = sum(
        number(r3v[row_id], "value_base_million_bbl")
        for row_id in ("b-demand", "b-foregone-build", "b-observed-draw", "b-unreconciled")
    )
    demand = number(r3v["b-demand"], "value_base_million_bbl")
    observed_draw = number(r3v["b-observed-draw"], "value_base_million_bbl")
    t4 = r3v["tier-total-t4"]
    non_gulf = r3v["a-non-gulf-supply"]
    route_residual = r3v["a-route-residual"]
    historical_days = 122
    p2k12 = by_id(P2K12)
    onshore = p2k12["period-onshore-accessible-draw-matched-total"]

    rows = [
        row(
            row_id="headline-net-global-supply-loss", record_type="accounting_headline",
            accounting_frame="downstream_market_clearing", additivity="headline_not_additive_to_components",
            channel_group="shock", channel="Net global oil supply loss", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=net_loss,
            current_flow_mb_per_day=net_loss / historical_days, evidence_tier="mixed_T1_T4",
            confidence="medium_high_arithmetic_low_medium_attribution",
            source_url=str(R3V1.relative_to(ROOT)),
            source_row_ids="b-demand | b-foregone-build | b-observed-draw | b-unreconciled",
            method="Sum the four mutually exclusive top-level downstream absorption slices for March-June.",
            interpretation="The named downstream components close exactly to this headline.",
            caveat="This is petroleum and other liquids, not crude only; the accounting is vintage-based and preliminary.",
        ),
        row(
            row_id="upstream-bypass", record_type="buffer_balance",
            accounting_frame="upstream_physical_avoidance", additivity="additive_within_upstream_only",
            channel_group="rerouting", channel="Incremental Gulf bypass routes", geography="Saudi Arabia / UAE / Iraq",
            as_of_date="2026-06-30", historical_million_bbl=number(r3v["a-incremental-bypass"], "value_base_million_bbl"),
            floor_or_ceiling=3.6, floor_or_ceiling_unit="mb/d demonstrated plus sensitivity ceiling",
            usable_headroom=0.2, headroom_unit="mb/d low-confidence sensitivity",
            current_flow_mb_per_day=number(bypass, "june_incremental_export_mb_per_day"),
            volume_headroom_status="not_exhaustible", rate_capacity_status="near_ceiling",
            failure_or_exhaustion_shape="No depletion curve; persists at steady operation, but route or terminal failure removes capacity discontinuously.",
            economic_cost_tier="low_operating_cost_capped", evidence_tier="T3", confidence=bypass["confidence"],
            source_url=bypass["source_url"], source_row_ids="system-bypass-summary",
            method="Use the p2k.7 system reconstruction; count only demonstrated flow plus 0.2 mb/d low-confidence Iraq sensitivity.",
            interpretation="About 3.4 mb/d can continue, but virtually no additional named route capacity is demonstrated.",
            caveat="Do not subtract Yanbu exports from Petroline throughput; that would create spurious Saudi headroom.",
        ),
        row(
            row_id="upstream-non-gulf-production", record_type="buffer_balance",
            accounting_frame="upstream_physical_avoidance", additivity="additive_within_upstream_only",
            channel_group="replacement_supply", channel="Net non-Gulf production revision", geography="Non-Gulf producers",
            as_of_date="2026-06-30", historical_million_bbl=number(non_gulf, "value_base_million_bbl"),
            current_flow_mb_per_day=number(non_gulf, "value_base_million_bbl") / historical_days,
            burn_or_growth_rate_mb_per_day=1.0, volume_headroom_status="not_a_stock",
            rate_capacity_status="slow_ramp_scenario_not_engineering_ceiling",
            failure_or_exhaustion_shape="Improves on project and drilling lags; no mechanical exhaustion date.",
            economic_cost_tier="durable_supply_response", evidence_tier=non_gulf["evidence_tier"],
            confidence="medium_for_history_low_for_forward_ramp", source_url=non_gulf["source_url"],
            source_row_ids="a-non-gulf-supply | base 2027-03 incremental_non_gulf_supply_offset",
            method="Historical March-June revision divided by 122 days; 1.0 mb/d is the existing central March-2027 scenario rate, not a current observation.",
            interpretation="This channel grows rather than depletes, but public evidence supports only a slow, modest ramp.",
            caveat="Production revisions are not fully causal and announced projects can slip.",
        ),
        row(
            row_id="downstream-observed-inventory", record_type="buffer_balance",
            accounting_frame="downstream_market_clearing", additivity="additive_top_level",
            channel_group="inventory", channel="Observed global inventory draw", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=observed_draw,
            historical_low_million_bbl=observed_draw,
            historical_high_million_bbl=observed_draw,
            current_level="unknown", level_unit="million_bbl", floor_or_ceiling="unknown",
            floor_or_ceiling_unit="statutory operational and working-stock floors",
            usable_headroom="unknown", headroom_unit="million_bbl above binding floors",
            current_flow_mb_per_day=observed_draw / historical_days,
            headroom_days_at_current_rate="unknown", volume_headroom_status="genuinely_exhaustible_but_unmeasured",
            rate_capacity_status="aggregate_drawability_unknown",
            failure_or_exhaustion_shape="Country-specific statutory, operational, product and logistics constraints bind before global stocks reach zero.",
            economic_cost_tier="cheap_fast_then_increasingly_policy_constrained", evidence_tier="T3",
            confidence="medium_low", source_url=str(R3V1.relative_to(ROOT)),
            source_row_ids="b-observed-draw",
            method="Carry the mixed-vintage observed-stock composite without adding unobserved China product stocks.",
            interpretation="Historical draw is measurable only in a mixed-vintage composite; usable forward headroom is not.",
            caveat="A historical average draw rate is not a sustainable forward release rate.",
        ),
        row(
            row_id="memo-onshore-accessible-inventory-draw", record_type="accessibility_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_inside_inventory_not_additive",
            channel_group="inventory_accessibility", channel="Onshore-accessible inventory draw", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=number(onshore, "value_base_million_bbl"),
            historical_low_million_bbl=number(onshore, "value_low_million_bbl"),
            historical_high_million_bbl=number(onshore, "value_high_million_bbl"),
            current_level="unknown", level_unit="million_bbl onshore",
            floor_or_ceiling="unknown", floor_or_ceiling_unit="physical policy and working-stock floors",
            usable_headroom="unknown", headroom_unit="million_bbl above binding onshore floors",
            current_flow_mb_per_day=number(onshore, "value_base_million_bbl") / historical_days,
            volume_headroom_status="more_accessible_inventory_consumed_than_total_headline_shows",
            rate_capacity_status="not_a_forward_release_capacity_measure",
            failure_or_exhaustion_shape="Onshore working minima bind before headline total inventory is exhausted; voyage float cannot sustainably replace tank stocks.",
            economic_cost_tier="already_consumed_accessible_buffer", evidence_tier="T3", confidence=onshore["confidence"],
            source_url=str(P2K12.relative_to(ROOT)), source_row_ids="period-onshore-accessible-draw-matched-total | period-voyage-float-usable-headroom",
            method="Carry p2k.12's latest-total onshore restatement: 298 mb total draw plus 18/53/88 mb cumulative oil-on-water build.",
            interpretation="Accessible onshore tanks drew 316-386 mb, base 351 mb; the extra 53 mb in the base is not usable future headroom.",
            caveat="Memo inside the 298 mb total-stock slice for durability only. It cannot replace total observed stocks in the global accounting identity.",
        ),
        row(
            row_id="memo-voyage-float-zero-headroom", record_type="accessibility_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_inside_inventory_not_additive",
            channel_group="inventory_accessibility", channel="Voyage float", geography="Global maritime oil system",
            as_of_date="2026-06-30", historical_million_bbl="not_additive_stock_reclassification",
            current_level="unknown", level_unit="million_bbl committed cargo",
            floor_or_ceiling="required_pipeline_fill", floor_or_ceiling_unit="route and flow dependent",
            usable_headroom=0, headroom_unit="million_bbl credited",
            current_flow_mb_per_day="not_applicable", burn_or_growth_rate_mb_per_day="not_applicable",
            headroom_days_at_current_rate=0, volume_headroom_status="committed_not_discretionary",
            rate_capacity_status="rises_with_flow_and_voyage_days",
            failure_or_exhaustion_shape="Drawing below required voyage fill briefly delivers cargo but breaks the steady delivery pipeline; June refill ties barrels up before arrival.",
            economic_cost_tier="logistics_requirement_not_buffer", evidence_tier="T2_classification_T3_quantity", confidence="medium_for_classification_low_for_quantity_split",
            source_url=str(P2K12.relative_to(ROOT)), source_row_ids="period-voyage-float-usable-headroom | 2026-06-voyage-scenario",
            method="Credit no ordinary voyage-pipeline fill as usable inventory headroom.",
            interpretation="The same barrels remain assets in global accounting but are unavailable as a durable discretionary buffer.",
            caveat="Cargo diversion and speed changes offer limited operational flexibility; they do not make voyage fill consumable on a sustained basis.",
        ),
        row(
            row_id="downstream-china-opaque-inventory-sensitivity", record_type="buffer_balance",
            accounting_frame="downstream_market_clearing", additivity="additive_top_level",
            channel_group="inventory", channel="Possible China product destocking reclassified from apparent demand", geography="China",
            as_of_date="2026-06-30", historical_million_bbl=reclass_base,
            historical_low_million_bbl=reclass_low, historical_high_million_bbl=reclass_high,
            current_level="unknown", level_unit="million_bbl product stocks", floor_or_ceiling="unknown",
            floor_or_ceiling_unit="commercial and operational working-stock floor", usable_headroom="unknown",
            headroom_unit="million_bbl", current_flow_mb_per_day=reclass_base / historical_days,
            headroom_days_at_current_rate="unknown", volume_headroom_status="scenario_only_exhaustible_if_real",
            rate_capacity_status="unknown", failure_or_exhaustion_shape="If real, it is exhaustible at an unknown working-stock floor; if not real, the barrels remain final-demand reduction.",
            economic_cost_tier="opaque_inventory_sensitivity", evidence_tier="T4", confidence="low",
            source_url=str(P2K4.relative_to(ROOT)), source_row_ids=reclass_row,
            method="Use p2k.4's 0/14.972/29.943 mb low/base/high sensitivity. This is not added to observed global inventories.",
            interpretation="A small part of the China apparent-demand gap may belong to an exhaustible opaque-inventory channel.",
            caveat="No public Chinese product-stock series establishes that the base value was actually drawn.",
        ),
        row(
            row_id="memo-iea-government-gross-remaining", record_type="stock_detail_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_inside_inventory_not_additive",
            channel_group="inventory", channel="Government-controlled oil stocks remaining", geography="IEA members",
            as_of_date="2026-07-21", current_level=1000, level_unit="million_bbl lower_bound",
            floor_or_ceiling="12_to_58", floor_or_ceiling_unit="public-stock days of prior-year aggregate net imports; April snapshot",
            usable_headroom="0_to_46", headroom_unit="public-stock days above aggregate 90-day obligation; April snapshot",
            current_flow_mb_per_day=290 / 132, burn_or_growth_rate_mb_per_day=290 / 132,
            headroom_days_at_current_rate="400_at_2.5_mb/d_or_455_at_2.197_mb/d_using_1bn; illustrative_zero_arithmetic_not_floor_duration",
            volume_headroom_status="gross_lower_bound_known_April_statutory_headroom_bounded_current_country_headroom_unknown",
            rate_capacity_status="country_product_and_logistics_specific",
            failure_or_exhaustion_shape="Legal, political and deliverability constraints bind country by country before gross stock reaches zero.",
            economic_cost_tier="cheap_fast_but_policy_gated", evidence_tier="T1_gross_T4_usable",
            confidence="high_for_lower_bound_and_April_floor_arithmetic_low_for_current_usable_headroom", source_url=f"{IEA_JULY} | {IEA_SECURITY} | {P2K8.relative_to(ROOT)}",
            source_row_ids="m8q.3 adj-019 | iea-government-zero-arithmetic-average-release-rate | iea-government-zero-arithmetic-may-release-rate | iea-net-importer-aggregate-floor-april",
            method="Publish p2k.8's 400/455-day mechanical divisions and April 12-to-58-day public-floor / 0-to-46-day public-headroom bound separately.",
            interpretation="Large gross stocks remain; the zero arithmetic is explicit, while country-specific usable days-to-floor remain unidentified.",
            caveat="Because the level is greater than 1 billion barrels and collective flow mixes public and obligated-industry stocks, 400/455 are lower bounds on hypothetical zero calculations, not strict upper bounds on aggregate usable duration.",
        ),
        row(
            row_id="memo-us-spr-current", record_type="stock_detail_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_inside_inventory_not_additive",
            channel_group="inventory", channel="U.S. Strategic Petroleum Reserve", geography="United States",
            as_of_date="2026-07-31", current_level=304.809, level_unit="million_bbl",
            floor_or_ceiling="0_IEA_statutory; operational_and_policy_floor_not_public",
            floor_or_ceiling_unit="million_bbl; IEA rule versus separate operational floor",
            usable_headroom="0_to_304.809", headroom_unit="million_bbl above unknown operational/policy floor",
            current_flow_mb_per_day=20.846 / 35, burn_or_growth_rate_mb_per_day=20.846 / 35,
            headroom_days_at_current_rate="0_to_511.767965; upper endpoint is fixed-rate physical zero",
            volume_headroom_status="exhaustible_512_day_zero_upper_bound_operational_floor_unknown",
            rate_capacity_status="2.7_mb/d_effective_Dec2025_GAO_vs_4.415_design; low_inventory_and_outages_bind",
            failure_or_exhaustion_shape="Draw rate can degrade with cavern pressure/integrity and logistics before volume reaches zero.",
            economic_cost_tier="cheap_fast_policy_gated", evidence_tier="T1_level_T4_floor",
            confidence="high_for_level_zero_bound_and_GAO_snapshot_low_for_current_operational_floor", source_url=f"{EIA_SPR} | {DOE_FACTS} | {P2K8.relative_to(ROOT)}",
            source_row_ids="WCSSTUS1 2026-06-26 and 2026-07-31 | us-spr-zero-bound-july-rate | us-spr-operational-floor | us-spr-history-low-verification",
            method="Carry p2k.8's exact 304.809/(20.846/35)=511.768-day zero bound; retain the operational floor as a separate 0-to-512-day interval.",
            interpretation="The U.S. SPR cannot sustain the latest draw beyond roughly 17 months even if every last barrel were usable; real limits shorten that window.",
            caveat="304.809 mb is the lowest level since February 1983. GAO's 2.7 mb/d effective capability is a December-2025 snapshot, not a current tested rate-versus-inventory curve.",
        ),
        row(
            row_id="memo-us-commercial-current", record_type="stock_detail_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_inside_inventory_not_additive",
            channel_group="inventory", channel="U.S. commercial petroleum excluding SPR", geography="United States",
            as_of_date="2026-07-31", current_level=1220.730, level_unit="million_bbl",
            floor_or_ceiling="not_public", floor_or_ceiling_unit="working-stock floor",
            usable_headroom="unknown", headroom_unit="million_bbl above working minimum",
            current_flow_mb_per_day=-0.547, burn_or_growth_rate_mb_per_day=-0.547,
            headroom_days_at_current_rate="not_applicable_currently_building",
            volume_headroom_status="exhaustible_in_principle_currently_rebuilding",
            rate_capacity_status="market_and_logistics_determined",
            failure_or_exhaustion_shape="Refinery and terminal working minima bind; July build shows commercial draws need not continue with the same sign.",
            economic_cost_tier="market_buffer", evidence_tier="T1_level_T4_floor", confidence="high_for_level_low_for_floor",
            source_url=EIA_COMM, source_row_ids="WTESTUS1 2026-06-26 and 2026-07-31",
            method="1,220.730 mb is the 31 July weekly level; negative draw is the 19.160 mb build from 26 June over 35 days.",
            interpretation="Commercial stocks rebuilt at about 0.55 mb/d over the latest weekly-endpoint window.",
            caveat="U.S. movement is informative but not a proxy for the unobserved global inventory residual.",
        ),
        row(
            row_id="downstream-foregone-build", record_type="buffer_balance",
            accounting_frame="downstream_market_clearing", additivity="additive_top_level",
            channel_group="counterfactual_balance", channel="Expected stock build that did not occur", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=number(r3v["b-foregone-build"], "value_base_million_bbl"),
            current_level=0, level_unit="million_bbl banked reserve", floor_or_ceiling=0,
            floor_or_ceiling_unit="million_bbl remaining durable credit", usable_headroom=0,
            headroom_unit="million_bbl", current_flow_mb_per_day=0, burn_or_growth_rate_mb_per_day=0,
            headroom_days_at_current_rate=0, volume_headroom_status="fully_spent",
            rate_capacity_status="not_a_release_channel",
            failure_or_exhaustion_shape="One-time counterfactual cushion; after the planned build is forgone it cannot be forgone again.",
            economic_cost_tier="historically_costless_now_unavailable", evidence_tier="T2", confidence=foregone["confidence"],
            source_url=foregone["source_urls"], source_row_ids="verdict-durable-buffer-credit",
            method="Carry p2k.5's zero durable forward credit.",
            interpretation="The historical 396.078 mb contribution is exhausted by construction.",
            caveat="Forecast Q4/2027 surpluses are conditional future balances, not already-held buffer capacity.",
        ),
        row(
            row_id="downstream-demand", record_type="buffer_balance",
            accounting_frame="downstream_market_clearing", additivity="additive_top_level",
            channel_group="demand", channel="Consumption below frozen February forecast, China-adjusted", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=demand - reclass_base,
            historical_low_million_bbl=demand - reclass_high,
            historical_high_million_bbl=demand - reclass_low,
            current_level="not_applicable", level_unit="flow adjustment", floor_or_ceiling="unknown",
            floor_or_ceiling_unit="country and sector specific feasible demand reduction",
            usable_headroom="unknown", headroom_unit="mb/d", current_flow_mb_per_day=(demand - reclass_base) / historical_days,
            headroom_days_at_current_rate="not_defined", volume_headroom_status="not_a_stock",
            rate_capacity_status="heterogeneous_by_mechanism",
            failure_or_exhaustion_shape="No common duration: efficiency and substitution can persist; deferred activity can rebound; forced scarcity compounds welfare loss.",
            marginal_absorber="increases_as_inventory_and_easy_conservation_tighten",
            economic_cost_tier="mixed_low_to_severe_see_p2k.3", evidence_tier="T3_with_T4_causal_allowance",
            confidence="high_arithmetic_low_causal", source_url=f"{R3V1.relative_to(ROOT)} | {P2K4.relative_to(ROOT)}",
            source_row_ids=f"b-demand | b-demand-structural | {reclass_row}",
            method="Subtract the p2k.4 opaque-inventory sensitivity from demand; preserve the total market-clearing bridge.",
            interpretation="Demand is the scalable residual absorber, but its durability and cost depend on which country/sector mechanism dominates.",
            caveat="The frozen-forecast gap includes ordinary forecast revision and is not a pure causal Hormuz estimate.",
        ),
        row(
            row_id="downstream-unreconciled", record_type="buffer_balance",
            accounting_frame="downstream_market_clearing", additivity="additive_top_level",
            channel_group="unknown", channel="Unreconciled implied-versus-observed stock adjustment", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=number(r3v["b-unreconciled"], "value_base_million_bbl"),
            historical_low_million_bbl=number(r3v["b-unreconciled"], "value_low_million_bbl"),
            historical_high_million_bbl=number(r3v["b-unreconciled"], "value_high_million_bbl"),
            current_level="unknown", level_unit="unknown buffer", floor_or_ceiling="unknown",
            floor_or_ceiling_unit="unknown", usable_headroom="unknown", headroom_unit="unknown",
            current_flow_mb_per_day=number(r3v["b-unreconciled"], "value_base_million_bbl") / historical_days,
            headroom_days_at_current_rate="unknown", volume_headroom_status="unknown_buffer_unknown_remaining_capacity",
            rate_capacity_status="unknown", failure_or_exhaustion_shape="Cannot be asserted: row mixes unobserved inventories, timing and model/data error.",
            marginal_absorber="cannot_be_projected", economic_cost_tier="unknown", evidence_tier="T4",
            confidence="low_for_physical_interpretation", source_url=r3v["b-unreconciled"]["source_url"],
            source_row_ids="b-unreconciled",
            method="Carry the full low/base/high r3v.1 balance plug without assigning it to a preferred channel.",
            interpretation="A 308.171 mb base residual is material, but its durability cannot be inferred from its arithmetic size.",
            caveat="Do not treat the base residual as either proven hidden stocks or normal statistical noise.",
        ),
        row(
            row_id="memo-all-t4", record_type="uncertainty_memo",
            accounting_frame="downstream_market_clearing", additivity="memo_spans_demand_and_unreconciled_not_additive",
            channel_group="unknown", channel="All T4 historical absorption", geography="Global",
            as_of_date="2026-06-30", historical_million_bbl=number(t4, "value_base_million_bbl"),
            historical_low_million_bbl=number(t4, "value_low_million_bbl"),
            historical_high_million_bbl=number(t4, "value_high_million_bbl"),
            current_level="unknown", level_unit="unknown buffer", floor_or_ceiling="unknown",
            usable_headroom="unknown", headroom_unit="unknown", headroom_days_at_current_rate="unknown",
            volume_headroom_status="unknown_buffer_unknown_remaining_capacity", rate_capacity_status="unknown",
            failure_or_exhaustion_shape="No defensible forward duration because the historical mechanism is unidentified.",
            marginal_absorber="cannot_be_projected", economic_cost_tier="unknown", evidence_tier="T4",
            confidence="low", source_url=t4["source_url"], source_row_ids="tier-total-t4",
            method="Memo total of the T4 portions nested across the market-clearing ledger.",
            interpretation="About 29% of historical absorption is too weakly identified to receive a durability assumption.",
            caveat="Includes the ordinary-demand-revision allowance nested in demand plus the unreconciled stock plug; do not add to those rows.",
        ),
        row(
            row_id="memo-upstream-route-residual", record_type="uncertainty_memo",
            accounting_frame="upstream_physical_avoidance", additivity="additive_within_upstream_only",
            channel_group="unknown", channel="Route, taxonomy and timing residual", geography="Global / Gulf routes",
            as_of_date="2026-06-30", historical_million_bbl=number(route_residual, "value_base_million_bbl"),
            current_level="unknown", level_unit="unknown", floor_or_ceiling="unknown", usable_headroom="unknown",
            headroom_unit="unknown", current_flow_mb_per_day=number(route_residual, "value_base_million_bbl") / historical_days,
            headroom_days_at_current_rate="unknown", volume_headroom_status="unidentified_not_projectable",
            rate_capacity_status="unknown", failure_or_exhaustion_shape="Unknown.", evidence_tier="T4", confidence="low",
            source_url=route_residual["source_url"], source_row_ids="a-route-residual",
            method="Carry the upstream route/taxonomy residual; never use it to close the downstream balance.",
            interpretation="Possible hidden routing or timing cannot be assumed to persist.",
            caveat="This is a different residual from the downstream implied-versus-observed stock plug.",
        ),
        row(
            row_id="memo-historical-stock-normalisation", record_type="historical_process_memo",
            accounting_frame="conditional_continued_current_traffic", additivity="memo_not_additive",
            channel_group="inventory_recharge", channel="Administrative emergency-stock normalization window", geography="IEA members",
            as_of_date="2026-08-05", current_level=15, level_unit="months process midpoint",
            floor_or_ceiling="12_to_18", floor_or_ceiling_unit="months historical process range",
            usable_headroom="not_a_headroom_measure", headroom_unit="process timing only",
            headroom_days_at_current_rate="not_applicable", volume_headroom_status="slow_recharge_flag",
            rate_capacity_status="not_a_current_release_or_refill_rate",
            failure_or_exhaustion_shape="Administrative restoration historically takes about a year or more; it does not prove exact physical tank refill.",
            marginal_absorber="stocks_should_not_be_assumed_reset_within_6_to_12_months",
            economic_cost_tier="policy_and_replenishment_constraint", evidence_tier="process_precedent",
            confidence="medium", source_url=str(P2K6.relative_to(ROOT)),
            source_row_ids="transfer-stock-obligation-normalisation-window",
            method="Carry only the transferable institutional timing range from p2k.6.",
            interpretation="Depleted or relaxed emergency cover is a slow-recharging buffer.",
            caveat="This is neither remaining usable stock nor a physical refill duration for the current episode.",
        ),
        row(
            row_id="memo-historical-us-refill-pace", record_type="historical_process_memo",
            accounting_frame="conditional_continued_current_traffic", additivity="memo_not_additive",
            channel_group="inventory_recharge", channel="U.S. SPR direct-purchase refill pace after 2022", geography="United States",
            as_of_date="2026-08-05", current_level="not_current_observation", level_unit="not_applicable",
            current_flow_mb_per_day=0.083, burn_or_growth_rate_mb_per_day=-0.083,
            usable_headroom="0.06_to_0.10", headroom_unit="mb/d historical refill-pace range",
            headroom_days_at_current_rate="not_applicable", volume_headroom_status="years_scale_recharge_context",
            rate_capacity_status="appropriation_price_maintenance_and_exchange_return_dependent",
            failure_or_exhaustion_shape="Refill is slow and policy-gated; it cannot offset a multi-mb/d current draw on the same timescale.",
            marginal_absorber="not_a_short_run_absorber", economic_cost_tier="replenishment_not_absorption",
            evidence_tier="country_specific_process_precedent", confidence="medium_for_us_order_of_magnitude",
            source_url=str(P2K6.relative_to(ROOT)), source_row_ids="transfer-us-direct-purchase-refill-pace",
            method="Carry p2k.6's 0.06/0.083/0.10 mb/d historical direct-purchase scheduling band.",
            interpretation="U.S. direct-purchase recharge operates on a years-scale, not at crisis-release speed.",
            caveat="Do not generalize to global refill, exchange returns or future appropriations.",
        ),
        row(
            row_id="memo-historical-transfer-rejections", record_type="historical_process_memo",
            accounting_frame="conditional_continued_current_traffic", additivity="memo_not_additive",
            channel_group="model_limits", channel="Historical durability parameters rejected", geography="Global",
            as_of_date="2026-08-05", current_level="not_applicable", level_unit="qualitative rejection",
            usable_headroom="not_applicable", headroom_unit="not_applicable", headroom_days_at_current_rate="not_applicable",
            volume_headroom_status="no_transferable_numeric_parameter", rate_capacity_status="no_transferable_numeric_parameter",
            failure_or_exhaustion_shape="No defensible historical half-life, rationing threshold, bypass decay, recovery time or severity-score mapping.",
            marginal_absorber="must_be_inferred_from_current_mechanisms", economic_cost_tier="not_parameterized",
            evidence_tier="negative_finding", confidence="high_for_rejection", source_url=str(P2K6.relative_to(ROOT)),
            source_row_ids="reject-demand-response-decay-half-life | reject-rationing-threshold | reject-route-persistence-as-bypass-decay | reject-producer-outage-recovery-time | reject-severity-score",
            method="Carry p2k.6's explicit non-transferability verdicts.",
            interpretation="Historical cases inform narrative stress tests, not the 6/12/18-month arithmetic.",
            caveat="Price parameters are also rejected and remain outside this epic.",
        ),
    ]

    timelines = [
        (6, date(2027, 2, 5),
         "Demand plus remaining policy-gated inventory; bypass holds near its ceiling and non-Gulf supply ramps slowly. "
         + demand_cost["horizon-6-months"]["observable_evidence"],
         "easy conservation then increasingly costly sectoral curtailment",
         "Foregone build contributes zero. Gross stocks remain large but usable headroom is unknown, so no stock-exhaustion date is claimed."),
        (12, date(2027, 8, 5),
         "Demand carries more of the marginal barrel, partly offset by durable non-Gulf supply; inventories are a discretionary supplement, not an assured base. "
         + demand_cost["horizon-12-months"]["observable_evidence"],
         "sustained substitution efficiency and forced demand destruction",
         "Any EIA surplus path is conditional on recovery/reopening and is not credited under continued current-level Strait traffic."),
        (18, date(2028, 2, 5),
         "Structural demand adaptation and new supply capacity; present stock-draw rates and unidentified T4 absorption are not extrapolated. "
         + demand_cost["horizon-18-months"]["observable_evidence"],
         "capital-intensive substitution and high-welfare-cost residual curtailment",
         "This horizon extends beyond the August-2026 public STEO month path ending December 2027; composition is directional, not volumetric."),
    ]
    for months, horizon, absorber, cost, caveat in timelines:
        rows.append(row(
            row_id=f"timeline-{months}-months", record_type="marginal_absorber_timeline",
            accounting_frame="conditional_continued_current_traffic", additivity="scenario_memo_not_additive",
            channel_group="timeline", channel="Marginal absorber under continued current-level Strait traffic",
            geography="Global", as_of_date="2026-08-05", horizon_months=months, horizon_date=horizon.isoformat(),
            current_level="not_applicable", level_unit="composition", usable_headroom="not_quantified",
            headroom_unit="conditional composition", headroom_days_at_current_rate="not_applicable",
            volume_headroom_status="scenario_dependent", rate_capacity_status="scenario_dependent",
            failure_or_exhaustion_shape="Composition shifts continuously as cheap/capped channels stop expanding; no price breakpoint is modelled.",
            marginal_absorber=absorber, economic_cost_tier=cost, evidence_tier="scenario",
            confidence="low_directional", source_url=f"{P2K3.relative_to(ROOT)} | {P2K5.relative_to(ROOT)} | {P2K7.relative_to(ROOT)} | {R3V1.relative_to(ROOT)}",
            source_row_ids=f"horizon-{months}-months | verdict-durable-buffer-credit | system-bypass-summary | tier-total-t4",
            method="Conditional durability synthesis, holding the current Strait-traffic regime rather than predicting price or political decisions.",
            interpretation=absorber, caveat=caveat,
        ))

    additive = [item for item in rows if item["accounting_frame"] == "downstream_market_clearing" and item["additivity"] == "additive_top_level"]
    closed = sum(float(item["historical_million_bbl"]) for item in additive)
    if abs(closed - net_loss) > 1e-5:
        raise ValueError(f"Downstream bridge does not close: {closed} versus {net_loss}")
    if abs((demand - reclass_base) + observed_draw + reclass_base - demand - observed_draw) > 1e-9:
        raise ValueError("China reclassification changed total market absorption")
    if len({item["row_id"] for item in rows}) != len(rows):
        raise ValueError("Duplicate row_id")
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
