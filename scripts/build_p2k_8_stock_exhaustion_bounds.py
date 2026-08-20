#!/usr/bin/env python3
"""Build explicit stock-exhaustion and binding-floor bounds for p2k.8.

The output distinguishes three quantities that are often conflated:

* days to physical zero at a fixed observed draw rate;
* days to a statutory or operational binding floor; and
* release-rate capability at the current stock level.

For the IEA aggregate, ``more than 1 billion barrels`` is a lower bound on
gross government stocks.  Dividing that by a rate therefore gives a lower
bound on the hypothetical days-to-zero calculation, not a strict upper bound
on the unknown usable duration above country-specific floors.
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_8_stock_exhaustion_bounds.csv"

EIA_SPR = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
DOE_FACTS = "https://www.energy.gov/hgeo/opr/spr-quick-facts"
DOE_FAQ = "https://www.energy.gov/hgeo/opr/spr-faqs"
GAO_2026 = "https://files.gao.gov/reports/GAO-26-106918/index.html"
IEA_STOCK_TOOL = "https://www.iea.org/data-and-statistics/data-tools/oil-stocks-of-iea-countries"
IEA_STOCK_API = "https://api.iea.org/netimports/monthly?year=2026&month=04"
IEA_JULY = "https://www.iea.org/news/iea-executive-director-statement-on-oil-markets"
IEA_AUGUST = "https://www.iea.org/reports/oil-market-report-august-2026"
IEA_ADJUSTMENT = "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"

FIELDS = [
    "row_id", "record_type", "geography", "as_of_date", "period_start",
    "period_end", "stock_level_million_bbl", "stock_level_status",
    "draw_rate_mb_per_day", "draw_rate_status", "days_to_zero",
    "zero_date", "zero_bound_type", "binding_floor", "binding_floor_unit",
    "usable_headroom", "usable_headroom_unit", "days_to_binding_floor",
    "floor_bound_type", "effective_rate_capacity_mb_per_day",
    "nominal_rate_capacity_mb_per_day", "rate_capacity_status",
    "evidence_tier", "confidence", "source_url", "method",
    "interpretation", "caveat",
]


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(**values: object) -> dict[str, str]:
    unknown = set(values) - set(FIELDS)
    if unknown:
        raise ValueError(f"Unknown fields: {sorted(unknown)}")
    result = {field: "" for field in FIELDS}
    result.update({key: fmt(value) for key, value in values.items()})
    return result


def zero_bound(
    *, row_id: str, geography: str, as_of: date, level: float,
    rate: float, period_start: str, period_end: str, rate_status: str,
    level_status: str = "observed_exact", bound_type: str = "upper_bound_fixed_rate",
    source_url: str, method: str, interpretation: str, caveat: str,
    confidence: str = "high_arithmetic",
) -> dict[str, str]:
    days = level / rate
    return row(
        row_id=row_id, record_type="days_to_zero_bound", geography=geography,
        as_of_date=as_of.isoformat(), period_start=period_start,
        period_end=period_end, stock_level_million_bbl=level,
        stock_level_status=level_status, draw_rate_mb_per_day=rate,
        draw_rate_status=rate_status, days_to_zero=days,
        zero_date=(as_of + timedelta(days=days)).isoformat(),
        zero_bound_type=bound_type, binding_floor="separate_not_used_here",
        binding_floor_unit="million_bbl", usable_headroom=level,
        usable_headroom_unit="million_bbl_to_physical_zero_only",
        days_to_binding_floor="unknown_unless_separate_floor_row",
        floor_bound_type="not_a_binding_floor_estimate", evidence_tier="T1_inputs",
        confidence=confidence, source_url=source_url, method=method,
        interpretation=interpretation, caveat=caveat,
    )


def build() -> list[dict[str, str]]:
    us_level = 298.694
    us_latest_rate = 26.961 / 42
    us_mar_jun_calendar_rate = 89.786 / 122
    us_mar_jun_endpoint_rate = 89.786 / 119
    iea_average_rate = 290 / 132
    iea_may_rate = 2.5

    # IEA April 2026 net-import-cover table: aggregate net importers.
    total_cover_days = 136.0
    industry_cover_days = 78.0
    public_cover_days = 58.0
    iea_obligation_days = 90.0
    minimum_public_days = max(0.0, iea_obligation_days - industry_cover_days)
    maximum_public_headroom_days = max(0.0, public_cover_days - minimum_public_days)

    rows = [
        zero_bound(
            row_id="us-spr-zero-bound-july-rate", geography="United States",
            as_of=date(2026, 8, 7), level=us_level, rate=us_latest_rate,
            period_start="2026-06-26", period_end="2026-08-07",
            rate_status="observed_weekly_endpoint_average_26.961_mb_over_42_days",
            source_url=EIA_SPR,
            method="Divide 298.694 mb by 26.961/42 mb/d; add the quotient to 7 August.",
            interpretation="At the latest six-week draw rate, physical zero is about 465 days away (15.3 months), around 15 November 2027.",
            caveat="This is a permissive upper bound on duration, not days to an operational or policy floor; the rate can change or degrade.",
        ),
        zero_bound(
            row_id="us-spr-zero-bound-march-june-calendar-rate",
            geography="United States", as_of=date(2026, 8, 7),
            level=us_level, rate=us_mar_jun_calendar_rate,
            period_start="2026-03-01", period_end="2026-06-30",
            rate_status="calendar_accounting_rate_89.786_mb_over_122_days",
            source_url=EIA_SPR,
            method="Divide 298.694 mb by the project March-June accounting rate, 89.786/122 mb/d.",
            interpretation="At the March-June calendar-accounting rate, physical zero is about 406 days away (13.3 months), around 16 September 2027.",
            caveat="The weekly observations are 27 February and 26 June, 119 elapsed days; this 122-day denominator matches the March-June accounting window.",
        ),
        zero_bound(
            row_id="us-spr-zero-bound-march-june-endpoint-rate",
            geography="United States", as_of=date(2026, 8, 7),
            level=us_level, rate=us_mar_jun_endpoint_rate,
            period_start="2026-02-27", period_end="2026-06-26",
            rate_status="observed_weekly_endpoint_rate_89.786_mb_over_119_elapsed_days",
            source_url=EIA_SPR,
            method="Divide 298.694 mb by 89.786/119 mb/d using the literal weekly-endpoint interval.",
            interpretation="At the literal March-June endpoint rate, physical zero is about 396 days away (13.0 months), around 6 September 2027.",
            caveat="This alternative prevents the calendar-accounting convention from masquerading as an exact observation interval.",
        ),
        row(
            row_id="us-spr-iea-statutory-floor", record_type="binding_floor_bound",
            geography="United States", as_of_date="2026-04-30",
            stock_level_million_bbl=us_level,
            stock_level_status="7_August_level_shown_for_context",
            binding_floor=0, binding_floor_unit="million_bbl_under_IEA_90_day_rule",
            usable_headroom=us_level, usable_headroom_unit="million_bbl_above_IEA_statutory_floor",
            days_to_binding_floor="same_as_days_to_zero_for_IEA_rule_only",
            floor_bound_type="computed_statutory_floor_not_operational_floor",
            rate_capacity_status="operational_and_policy_constraints_still_bind_before_zero",
            evidence_tier="T1", confidence="high_for_IEA_classification",
            source_url=f"{IEA_STOCK_TOOL} | {IEA_STOCK_API}",
            method="The IEA April 2026 table classifies the United States as a net exporter; net exporters have no 90-day net-import stock obligation.",
            interpretation="The IEA rule does not create a positive U.S. SPR floor. The binding U.S. floor is operational/political, not the IEA obligation.",
            caveat="DOE's 125 days of crude-import protection is not the IEA all-petroleum net-import calculation; it must not be converted into a formal 90-day SPR floor.",
        ),
        row(
            row_id="us-spr-operational-floor", record_type="binding_floor_bound",
            geography="United States", as_of_date="2026-08-07",
            stock_level_million_bbl=us_level, stock_level_status="observed_exact",
            binding_floor="not_public", binding_floor_unit="million_bbl_operational_or_policy_floor",
            usable_headroom="between_0_and_298.694",
            usable_headroom_unit="million_bbl_above_unknown_binding_floor",
            days_to_binding_floor="between_0_and_days_to_zero_at_each_rate",
            floor_bound_type="trivial_volume_bound_with_specific_rate_upper_bounds_elsewhere",
            effective_rate_capacity_mb_per_day=2.7,
            nominal_rate_capacity_mb_per_day=4.415,
            rate_capacity_status="December_2025_effective_rate_61_percent_of_design",
            evidence_tier="T1_level_T1_GAO_audit", confidence="high_for_reported_snapshot_low_for_current_floor",
            source_url=f"{EIA_SPR} | {GAO_2026}",
            method="Retain the exact current stock and GAO's December-2025 DOE capability snapshot; do not invent a minimum safe cavern inventory.",
            interpretation="The operational floor remains unpublished, but the release-rate constraint is already observable and material.",
            caveat="GAO's 2.7 mb/d capability is a December-2025 snapshot affected by construction, aging infrastructure and low inventory; it is not an August-2026 test result.",
        ),
        row(
            row_id="us-spr-gao-accessibility-snapshot", record_type="rate_inventory_evidence",
            geography="United States", as_of_date="2025-12-31",
            stock_level_million_bbl=413.0, stock_level_status="GAO_January_2026_volume_snapshot",
            binding_floor="more_than_25_percent_temporarily_unavailable",
            binding_floor_unit="share_of_inventory_due_to_construction_and_cavern_outages",
            usable_headroom="less_than_309.75",
            usable_headroom_unit="million_bbl_available_for_draw_in_snapshot",
            days_to_binding_floor="not_propagated_to_July",
            floor_bound_type="dated_operational_availability_bound",
            effective_rate_capacity_mb_per_day=2.7, nominal_rate_capacity_mb_per_day=4.415,
            rate_capacity_status="61_percent_of_design_effective_drawdown",
            evidence_tier="T1_GAO_audit", confidence="high_for_snapshot",
            source_url=GAO_2026,
            method="Apply GAO's 'more than a quarter unavailable' statement to its 413 mb inventory snapshot: available volume was below 75%, or below 309.75 mb.",
            interpretation="Actual accessibility was already below gross inventory, and effective draw capability was far below the 4.4 mb/d nominal figure.",
            caveat="Do not subtract 103.25 mb from July inventory: outages and construction status may have changed, and withdrawals need not have been distributed proportionately.",
        ),
        row(
            row_id="us-spr-gao-low-inventory-site-evidence", record_type="rate_inventory_evidence",
            geography="Bayou Choctaw and West Hackberry", as_of_date="2025-12-31",
            stock_level_million_bbl=139.0, stock_level_status="GAO_site_snapshot_51_plus_88",
            effective_rate_capacity_mb_per_day=1.2,
            nominal_rate_capacity_mb_per_day=1.815,
            rate_capacity_status="Bayou_0.450_of_0.515_and_West_Hackberry_0.750_of_1.300_with_low_inventory_cited",
            evidence_tier="T1_GAO_audit", confidence="high_for_snapshot",
            source_url=GAO_2026,
            method="Sum GAO Table 2 values for the two sites where DOE explicitly cited low cavern inventory as a drawdown limitation.",
            interpretation="Public evidence directly links low site inventory to reduced draw capability; a single constant 4.4 mb/d rate is physically inappropriate.",
            caveat="Construction, wells, pipelines and brine systems also affect rates, so this is evidence of a relationship, not a fitted rate-versus-volume curve.",
        ),
        row(
            row_id="us-spr-doe-nominal-decline-rule", record_type="rate_inventory_evidence",
            geography="United States", as_of_date="2026-08-06",
            effective_rate_capacity_mb_per_day="not_currently_claimed_by_DOE_FAQ",
            nominal_rate_capacity_mb_per_day=4.4,
            rate_capacity_status="nominal_max_up_to_90_days_then_declines_as_caverns_empty",
            evidence_tier="T1_DOE", confidence="high_for_qualitative_rule",
            source_url=f"{DOE_FAQ} | {DOE_FACTS}",
            method="Transcribe DOE's qualitative operating rule and keep it separate from GAO's current effective capability.",
            interpretation="DOE confirms that nominal maximum withdrawal is not sustainable throughout depletion.",
            caveat="DOE does not publish a current numeric curve mapping total SPR inventory to effective draw rate.",
        ),
        row(
            row_id="us-spr-history-low-verification", record_type="historical_verification",
            geography="United States", as_of_date="2026-08-07",
            stock_level_million_bbl=us_level, stock_level_status="observed_exact",
            evidence_tier="T1_EIA_full_weekly_history", confidence="high",
            source_url=EIA_SPR,
            method="Compare 298.694 mb with every earlier weekly WCSSTUS1 observation since August 1982. The latest earlier value at or below it is 298.379 mb on 28 January 1983; 4 February was 299.484 mb.",
            interpretation="298.694 mb was the lowest U.S. SPR level since 28 January 1983—more than 43 years, not merely since the mid-1980s.",
            caveat="The EIA weekly series begins in August 1982; the claim is 'lowest since', not an all-time minimum.",
        ),
        zero_bound(
            row_id="iea-government-zero-arithmetic-average-release-rate",
            geography="IEA member government-controlled stocks",
            as_of=date(2026, 7, 21), level=1000.0, rate=iea_average_rate,
            period_start="2026-03-11", period_end="2026-07-21",
            rate_status="collective_public_plus_obligated_industry_average_290_mb_over_132_days",
            level_status="lower_bound_more_than_1000_mb",
            bound_type="illustrative_minimum_days_to_zero_not_strict_upper_bound",
            source_url=f"{IEA_JULY} | {IEA_AUGUST}",
            method="Divide the stated 1,000 mb lower-bound level by 290/132 mb/d.",
            interpretation="The mechanical calculation is at least about 455 days (15.0 months) to zero, around 19 October 2027 if the stock were exactly 1,000 mb.",
            caveat="Because the level is greater than 1,000 mb and the release includes obligated-industry stocks, 455 is not a rigorous upper bound on the aggregate zero date. The 12 August OMR says the July release pace slowed but gives no newer public cumulative quantity or holdings level.",
            confidence="high_arithmetic_low_for_duration_interpretation",
        ),
        zero_bound(
            row_id="iea-government-zero-arithmetic-may-release-rate",
            geography="IEA member government-controlled stocks",
            as_of=date(2026, 7, 21), level=1000.0, rate=iea_may_rate,
            period_start="2026-05-01", period_end="2026-05-31",
            rate_status="IEA_reported_collective_action_market_flow_in_May",
            level_status="lower_bound_more_than_1000_mb",
            bound_type="illustrative_minimum_days_to_zero_not_strict_upper_bound",
            source_url=f"{IEA_JULY} | {IEA_ADJUSTMENT} | {IEA_AUGUST}",
            method="Divide the stated 1,000 mb lower-bound level by the IEA-reported 2.5 mb/d May collective-action rate.",
            interpretation="The mechanical calculation is at least 400 days (13.1 months) to zero, around 25 August 2027 if the stock were exactly 1,000 mb.",
            caveat="The May flow includes government and obligated-industry releases; public-stock ownership of the rate is not reported, and the gross government level is only a lower bound. The August OMR provides no replacement numeric release rate.",
            confidence="high_arithmetic_low_for_duration_interpretation",
        ),
        row(
            row_id="iea-net-importer-aggregate-floor-april", record_type="binding_floor_bound",
            geography="IEA net importers", as_of_date="2026-04-30",
            stock_level_status="IEA_days_of_previous_year_net_imports",
            binding_floor=minimum_public_days,
            binding_floor_unit="days_of_aggregate_net_imports_minimum_public_contribution",
            usable_headroom=f"0_to_{maximum_public_headroom_days:.0f}",
            usable_headroom_unit="public_stock_days_above_aggregate_90_day_obligation",
            days_to_binding_floor="not_convertible_without_public_stock_release_ownership_and_country_constraints",
            floor_bound_type="computed_aggregate_obligation_bound",
            rate_capacity_status="country_product_and_logistics_specific",
            evidence_tier="T1_IEA", confidence="high_for_aggregate_days_low_for_fungibility",
            source_url=f"{IEA_STOCK_TOOL} | {IEA_STOCK_API}",
            method=f"IEA reports {total_cover_days:.0f} total days: {industry_cover_days:.0f} industry plus {public_cover_days:.0f} public. The 90-day rule requires at least max(0,90-78)={minimum_public_days:.0f} public days, leaving at most {maximum_public_headroom_days:.0f} public days above the aggregate rule.",
            interpretation="At the aggregate April snapshot, the government-stock floor implied solely by the IEA obligation was at least 12 days of net imports; freely releasable public headroom was between zero and 46 days after country constraints.",
            caveat="The IEA explicitly says country systems differ and totals may not equal components. Barrels are not fungible across countries, and April is the latest free table vintage, not a July snapshot.",
        ),
    ]

    # Guard the key acceptance-criterion arithmetic.
    keyed = {item["row_id"]: item for item in rows}
    assert 465 < float(keyed["us-spr-zero-bound-july-rate"]["days_to_zero"]) < 466
    assert 405 < float(keyed["us-spr-zero-bound-march-june-calendar-rate"]["days_to_zero"]) < 407
    assert 454 < float(keyed["iea-government-zero-arithmetic-average-release-rate"]["days_to_zero"]) < 456
    assert minimum_public_days == 12 and maximum_public_headroom_days == 46
    assert len(keyed) == len(rows)
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
