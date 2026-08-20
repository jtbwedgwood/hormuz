#!/usr/bin/env python3
"""Build the p2k.13 rerouting and oil-on-water causal-test ledger.

The core identity is deliberately simple: incremental working voyage float equals
flow (mb/d) times incremental voyage days.  The script distinguishes structural
*longer-route* float from ordinary route refill when Hormuz sailings resumed.
Those mechanisms are often described together, but only the first is strictly
rerouting.  Public data do not identify vessel-level geography, so all causal
allocations remain ranges and no row is presented as an AIS decomposition.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_13_rerouting_causal_test.csv"

IEA_FEB = "https://www.iea.org/reports/oil-market-report-february-2026"
IEA_APR = "https://www.iea.org/reports/oil-market-report-april-2026"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEA_JUN = "https://www.iea.org/reports/oil-market-report-june-2026"
IEA_JUL = "https://www.iea.org/reports/oil-market-report-july-2026"
IEA_2022 = "https://www.iea.org/articles/2022-energy-crisis-frequently-asked-questions"
IEA_OIL_2023 = "https://www.iea.org/reports/oil-2023/executive-summary"
IEA_2020 = "https://www.iea.org/reports/oil-market-report-july-2020"
EIA_REDSEA_TIME = "https://www.eia.gov/todayinenergy/detail.php?id=61363"
EIA_REDSEA_FLOW = "https://www.eia.gov/todayinenergy/detail.php?id=62263"
EIA_PANAMA = "https://www.eia.gov/todayinenergy/detail.php?id=39272"
UNCTAD_2023 = "https://unctad.org/system/files/official-document/rmt2023_en.pdf"
WORLD_BANK_REDSEA = (
    "https://documents1.worldbank.org/curated/en/099414105062418860/"
    "pdf/IDU1a1491aa617394148a91856c1eaa57a28f15b.pdf"
)
ARAMCO_Q1 = (
    "https://www.aramco.com/-/media/publications/corporate-reports/"
    "reports-and-presentations/2026/q1/"
    "saudi-aramco-q1-2026-webcast-presentation-english.pdf"
)
CME_MAR = "https://www.cmegroup.com/openmarkets/energy/2026/WTI-Crude-Oil-Market-Volatility.html"

FIELDS = [
    "row_id", "record_type", "case_name", "period", "geography",
    "flow_mb_d", "flow_low_mb_d", "flow_high_mb_d",
    "baseline_voyage_days", "added_days_low", "added_days_base", "added_days_high",
    "added_distance_nm_low", "added_distance_nm_base", "added_distance_nm_high",
    "implied_float_mb_low", "implied_float_mb_base", "implied_float_mb_high",
    "observed_oow_change_mb", "comparison_value", "comparison_unit",
    "attribution_status", "source_urls", "source_locator", "confidence",
    "method", "interpretation", "limitations",
]


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    for key, value in values.items():
        if key not in result:
            raise KeyError(key)
        result[key] = fmt(value)
    return result


def route_row(
    row_id: str, case_name: str, period: str, geography: str,
    flow: float, flow_low: float, flow_high: float,
    base_days: float, days: tuple[float, float, float],
    sources: str, locator: str, confidence: str,
    method: str, interpretation: str, limitations: str,
) -> dict[str, str]:
    low_days, mid_days, high_days = days
    # EIA's public Red Sea voyage examples use a laden speed of 14 knots.
    nm_per_day = 14 * 24
    return row(
        row_id=row_id, record_type="route_float_calculation", case_name=case_name,
        period=period, geography=geography, flow_mb_d=flow,
        flow_low_mb_d=flow_low, flow_high_mb_d=flow_high,
        baseline_voyage_days=base_days,
        added_days_low=low_days, added_days_base=mid_days, added_days_high=high_days,
        added_distance_nm_low=low_days * nm_per_day,
        added_distance_nm_base=mid_days * nm_per_day,
        added_distance_nm_high=high_days * nm_per_day,
        implied_float_mb_low=flow_low * low_days,
        implied_float_mb_base=flow * mid_days,
        implied_float_mb_high=flow_high * high_days,
        attribution_status="bounded_mechanical_estimate", source_urls=sources,
        source_locator=locator, confidence=confidence, method=method,
        interpretation=interpretation, limitations=limitations,
    )


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    atlantic = route_row(
        "route-2026-atlantic-east", "Atlantic Basin replacement crude to East of Suez",
        "2026-03_to_2026-06", "Atlantic Basin to East of Suez", 3.5, 3.5, 3.5,
        18, (12, 20, 28), f"{IEA_MAY} | {IEA_JUN} | {EIA_REDSEA_TIME} | {EIA_PANAMA}",
        "IEA May/June highlights; EIA 14-knot voyage examples and crude-vessel Panama limit",
        "low_medium",
        "IEA reports 3.5 mb/d more Atlantic crude moving East of Suez. The 12/20/28-day envelope represents its disclosed mix of US, Brazil, Canada, Kazakhstan and Venezuela replacing a shorter Gulf-to-Asia barrel. At EIA's 14-knot convention, it is 4,032/6,720/9,408 additional nautical miles.",
        "This structural route shift ties up 42/70/98 mb at a steady 3.5 mb/d.",
        "IEA does not disclose origin-destination weights. The days are a route-mix envelope, not observed average sailing times; queuing and ballast legs are excluded.",
    )
    yanbu = route_row(
        "route-2026-yanbu-asia", "Incremental Saudi Yanbu exports to Asian buyers",
        "2026-03_to_2026-06", "Saudi Arabia Red Sea to East of Suez", 3.0, 3.0, 3.0,
        18, (5, 7, 9), f"{IEA_JUN} | {ARAMCO_Q1} | {EIA_REDSEA_TIME}",
        "IEA reports more than 5 mb/d from Yanbu versus 2 mb/d pre-war; Aramco reports 1,200 km pipeline; EIA 14-knot convention",
        "low_medium",
        "Use only the 3 mb/d observed lower-bound increment over the 2 mb/d pre-war route. The 5/7/9 extra days represent sailing from Yanbu through Bab el-Mandeb and around Arabia rather than loading in the Gulf; at 14 knots this is 1,680/2,352/3,024 nautical miles.",
        "The incremental Yanbu route adds 15/21/27 mb of structural voyage float.",
        "Destination mix is not public and some Yanbu crude travels west, for which the route may be shorter. The bound should not be generalized to all 5 mb/d.",
    )
    refill = route_row(
        "route-2026-june-hormuz-refill", "Ordinary route refill after June partial reopening",
        "2026-06", "Hormuz to importing markets", 6.2, 5.5, 6.9,
        18, (12, 18, 22), f"{IEA_JUN} | {IEA_JUL}",
        "p2k.2 inference: June Hormuz 8.2/8.9/9.6 mb/d versus 2.7 mb/d March-May average",
        "low_medium",
        "Multiply the p2k.2 low/base/high June increase in Hormuz flow by a 12/18/22-day laden destination envelope. The distance equivalents at 14 knots are 4,032/6,048/7,392 nautical miles.",
        "Ordinary maritime-pipeline refill adds 66/111.6/151.8 mb. This is voyage float, but it is not longer-route inflation and should not be called rerouting.",
        "The June rate is a monthly reconstruction and the 2.7 mb/d comparator is a March-May period average. A ramp during June means the formula is an end-state/order-of-magnitude estimate, not a day-exact change.",
    )
    rows.extend([atlantic, yanbu, refill])

    structural = tuple(float(atlantic[f"implied_float_mb_{x}"]) + float(yanbu[f"implied_float_mb_{x}"]) for x in ("low", "base", "high"))
    logistics = tuple(structural[i] + float(refill[f"implied_float_mb_{x}"]) for i, x in enumerate(("low", "base", "high")))
    rows.extend([
        row(
            row_id="synthesis-structural-rerouting", record_type="causal_attribution",
            case_name="Strict longer-route voyage float", period="end_2026-06", geography="World",
            implied_float_mb_low=structural[0], implied_float_mb_base=structural[1], implied_float_mb_high=structural[2],
            attribution_status="project_causal_range", source_urls=f"{IEA_MAY} | {IEA_JUN} | {EIA_REDSEA_TIME} | {ARAMCO_Q1}",
            source_locator="sum of route-2026-atlantic-east and route-2026-yanbu-asia",
            confidence="low_medium", method="Sum non-overlapping Atlantic replacement and incremental Yanbu structural route cases.",
            interpretation="Strict rerouting explains 57/91/125 mb of end-June oil on water relative to the pre-shock route mix.",
            limitations="This is a stock-level counterfactual, not the change in a single month; ramp timing and destination weights are not observed.",
        ),
        row(
            row_id="synthesis-all-route-logistics", record_type="conditional_snapshot_sensitivity",
            case_name="Conditional end-June conjunction: structural rerouting plus ordinary route refill", period="end_2026-06", geography="World",
            implied_float_mb_low=logistics[0], implied_float_mb_base=logistics[1], implied_float_mb_high=logistics[2],
            attribution_status="project_causal_range", source_urls=f"{IEA_MAY} | {IEA_JUN} | {IEA_JUL} | {EIA_REDSEA_TIME}",
            source_locator="sum of all three 2026 route calculations", confidence="low_medium",
            method="Conditionally add the distinct route stocks only if the 3.5 mb/d Atlantic shift and incremental Yanbu flow persisted while the ordinary Hormuz maritime pipeline refilled.",
            interpretation="Under that conjunction, route logistics require 123/202.6/276.8 mb at the end-June snapshot. This is a useful scale check, not a monthly causal sum.",
            limitations="Do not add these components by default across time: structural float may have accumulated before June and may unwind as Gulf supply returns. The total excludes discharge queues and can overlap sanctioned-oil long voyages.",
        ),
    ])

    # Latest-composite monthly accounting supplied by p2k.12. May has no public
    # global split; zero with +/-35 mb is its explicit sensitivity, not a fact.
    monthly = [
        ("2026-03", -117.0, "Global oil on water fell even though Middle East Gulf floating storage rose 100 mb."),
        ("2026-04", 53.0, "Global oil on water rebounded as Atlantic replacement routes scaled."),
        ("2026-05", 0.0, "No public global split found; base holds oil on water flat with a +/-35 mb sensitivity."),
        ("2026-06", 117.0, "Net build during the export surge; p2k.12 separates a large voyage-float build from Gulf storage drawdown."),
    ]
    for period, change, interpretation in monthly:
        rows.append(row(
            row_id=f"observed-oow-{period}", record_type="monthly_observed_anchor",
            case_name="Latest-composite global oil-on-water change", period=period,
            geography="World", observed_oow_change_mb=change,
            attribution_status="observed_or_explicit_missing_split",
            source_urls=f"{IEA_MAY} | {IEA_JUL}", source_locator="p2k.12 monthly restatement",
            confidence="medium" if period != "2026-05" else "low",
            method="Use IEA onshore-versus-total arithmetic for March/April, no-change sensitivity center for May, and IEA's direct June figure.",
            interpretation=interpretation,
            limitations="Mixed public OMR vintages; May's split is not published and March's +100 mb Gulf storage is regional, nested within the -117 mb global change.",
        ))
    rows.extend([
        row(
            row_id="observed-oow-period-net", record_type="period_denominator",
            case_name="March-June net global oil-on-water change", period="2026-03_to_2026-06", geography="World",
            implied_float_mb_low=18, implied_float_mb_base=53, implied_float_mb_high=88,
            observed_oow_change_mb=53, attribution_status="latest_composite_with_may_sensitivity",
            source_urls=f"{IEA_MAY} | {IEA_JUL}", source_locator="-117 + 53 + May(-35/0/+35) + 117",
            confidence="low_medium", method="Sum the four monthly global changes; retain p2k.12's +/-35 mb May split sensitivity.",
            interpretation="Net oil on water rose only 18-88 mb (base 53), not 270 mb. Large gross builds were offset by March's collapse in normal voyage float and later release of blocked Gulf cargoes.",
            limitations="This denominator is not the gross amount moved onto water and is highly sensitive to revisions and missing May decomposition.",
        ),
        row(
            row_id="geography-march-gulf-storage", record_type="geographic_mechanism_test",
            case_name="Blocked-export floating storage", period="2026-03", geography="Middle East Gulf",
            observed_oow_change_mb=100, comparison_value=-181, comparison_unit="million barrels in-transit change",
            attribution_status="direct_regional_plus_arithmetic_remainder", source_urls=IEA_APR,
            source_locator="April OMR: +100 mb Gulf floating; global OOW -117 mb from p2k.12",
            confidence="medium_for_gulf_low_for_remainder_composition",
            method="Use p2k.12's April-OMR bridge: in-transit -181 mb plus Middle East floating storage +100 mb plus a -36 mb other/vintage term equals revised global oil on water -117 mb.",
            interpretation="March is not a rerouting signature: cargoes were trapped near loading areas while the pre-existing global maritime pipeline drained faster elsewhere.",
            limitations="The -36 mb other/vintage term is an arithmetic remainder and can contain geography or classification revisions.",
        ),
        row(
            row_id="geography-june-storage-unwind", record_type="geographic_mechanism_test",
            case_name="Gulf armada sails and blocked storage unwinds", period="2026-06", geography="Middle East Gulf to destination lanes",
            implied_float_mb_low=66, implied_float_mb_base=111.6, implied_float_mb_high=151.8,
            observed_oow_change_mb=117, comparison_value=5.4, comparison_unit="million barrels base discretionary-or-other remainder",
            attribution_status="p2k12_route_refill_decomposition", source_urls=IEA_JUL,
            source_locator="July OMR export surge and floating/onshore draw; p2k.12 route-refill 66/111.6/151.8",
            confidence="low_medium", method="Pair the mechanical ordinary route-refill range with an arithmetic discretionary/other remainder of +51/+5.4/-34.8 mb so the two sum to June's +117 mb.",
            interpretation="The June build can be explained primarily by the moving maritime pipeline refilling; the remaining discretionary/other term ranges from a 51 mb build to a 35 mb unwind.",
            limitations="IEA does not publish the June voyage-versus-floating-storage split, so this is scenario arithmetic rather than vessel classification. Structural longer-route float likely accumulated partly before June and is not automatically additive here.",
        ),
    ])

    # Historical like-for-like mechanical controls.
    rows.extend([
        route_row(
            "analogue-2022-russia-named", "2022 Russian rerouting: named Asian destination increases",
            "2022-02_to_2022-10", "Russia to India and China", 1.19, 1.19, 1.19,
            5, (25, 30, 35), f"{IEA_2022} | {UNCTAD_2023} | {EIA_REDSEA_TIME}",
            "IEA: India +0.965 and China +0.225 mb/d; UNCTAD: crude ton-miles +8% in 2022",
            "medium_for_flow_low_medium_for_days",
            "Sum named India and China gains and apply 25/30/35 extra days versus short-haul European deliveries, using the same 14-knot convention. Turkiye is excluded because it is not a comparable long-haul Asian shift.",
            "The named Asian shift mechanically added 29.75/35.7/41.65 mb of voyage float; UNCTAD's 8% global crude ton-mile growth independently confirms the sign and large scale.",
            "Named gains are not a complete trade matrix. No comparable public global oil-on-water level is available, so this validates order of magnitude, not a barrels-per-day causal coefficient.",
        ),
        route_row(
            "analogue-2022-russia-broad", "2022 Russian rerouting: broader Europe/G7 displacement",
            "2022_to_2023", "Russia to East of Suez", 2.5, 2.5, 2.5,
            5, (25, 30, 35), f"{IEA_OIL_2023} | {UNCTAD_2023} | {EIA_REDSEA_TIME}",
            "IEA Oil 2023: most of 2.5 mb/d backed out of Europe/G7 flowed eastward",
            "medium_for_flow_low_medium_for_days",
            "Apply the same 25/30/35-day route envelope to IEA's broader 2.5 mb/d eastward displacement.",
            "The broad rerouting implies 62.5/75/87.5 mb of working float, bracketing the 2026 strict-rerouting scale without calibrating it.",
            "The IEA flow is approximate and spans 2022-23; the public source does not provide a same-vintage global oil-on-water series.",
        ),
        route_row(
            "analogue-2024-red-sea", "2024 Red Sea diversion around Cape of Good Hope",
            "2024-01_to_2024-05", "Arabian Sea/Asia-Europe routes around Cape", 2.8, 2.8, 2.8,
            19, (10, 15, 21), f"{EIA_REDSEA_FLOW} | {EIA_REDSEA_TIME} | {WORLD_BANK_REDSEA}",
            "EIA: Cape oil flow 8.7 vs 5.9 mb/d and Arabian Sea-Europe +15 days; World Bank: tanker distances up to +53%",
            "medium_high_for_flow_and_example_low_medium_for_mix",
            "Treat the +2.8 mb/d Cape flow as the observable rerouting proxy and apply 10/15/21 added days around EIA's representative +15-day voyage.",
            "The route shift implies 28/42/58.8 mb of extra working float, a clean modern precedent for a tens-of-millions routing effect.",
            "Not all incremental Cape flow was caused by Houthi avoidance and the destination mix differs. No public global oil-on-water change is supplied for a direct ratio test.",
        ),
        row(
            row_id="control-2020-contango-storage", record_type="historical_negative_control",
            case_name="COVID contango floating storage", period="2020-05_to_2020-06", geography="World",
            observed_oow_change_mb=211.3, comparison_value=-34.9, comparison_unit="million barrels June monthly change",
            attribution_status="observed_storage_control", source_urls=IEA_2020,
            source_locator="July 2020 OMR highlights", confidence="high",
            method="Recover May's all-time-high crude floating storage as June level 176.4 mb plus the reported 34.9 mb June fall.",
            interpretation="A storage-driven episode reached 211.3 mb, then unwound as contango flattened. It demonstrates that very large floating stocks can arise without route inflation when the curve pays for storage.",
            limitations="Crude floating storage is narrower than the 2026 crude-and-products global oil-on-water scope.",
        ),
        row(
            row_id="control-2026-timespread", record_type="price_structure_test",
            case_name="Profit-seeking carry-storage discriminator", period="2026-03_to_2026-06", geography="WTI and Brent",
            comparison_value=15.943, comparison_unit="USD/b WTI front-minus-Dec mean",
            attribution_status="test_rejects_contango_carry", source_urls=CME_MAR,
            source_locator="hormuz_r3v_3_time_spread_summary.csv; WTI 84/84 and Brent 82/84 backwardated observations",
            confidence="medium", method="Use r3v.3 daily public-close front-minus-deferred and fixed Sep-Oct spreads; positive means backwardation.",
            interpretation="Persistent backwardation strongly rejects profit-seeking carry as a major March-June mechanism, especially March-May.",
            limitations="Does not reject forced blocked storage, sanctioned dwell, port congestion or operational timing; Yahoo daily closes are not exchange-certified settlements.",
        ),
    ])

    sanctioned_total_4m = 248 / 12 * 4
    sanctioned_oil_4m = 248 * 0.72 / 12 * 4
    rows.extend([
        row(
            row_id="alternative-sanctioned-trend", record_type="competing_mechanism_bound",
            case_name="Continuation of 2025 oil-on-water trend", period="2026-03_to_2026-06", geography="World sanctioned/dark fleet",
            implied_float_mb_low=0, implied_float_mb_base=30, implied_float_mb_high=sanctioned_total_4m,
            comparison_value=sanctioned_oil_4m, comparison_unit="million barrels sanctioned-only four-month straight-line equivalent",
            attribution_status="hard_cap_not_additive", source_urls=IEA_FEB,
            source_locator="2025 OOW +248 mb, 72% sanctioned",
            confidence="low_for_2026_continuation_high_for_2025_anchor",
            method="Straight-line four-month hard cap is 82.67 mb total and 59.52 mb sanctioned. Use 0/30/82.67 as a stress range, not a forecast.",
            interpretation="A pre-existing sanctioned/dark-fleet trend is a real confound, but the shock-period path was not smooth: global oil on water collapsed in March and Gulf storage unwound in June.",
            limitations="Do not add this range to rerouting: sanctioned cargoes themselves take longer routes and can already be inside the Atlantic/routing arithmetic.",
        ),
        row(
            row_id="alternative-congestion", record_type="competing_mechanism_bound",
            case_name="Discharge congestion and queueing", period="2026-03_to_2026-06", geography="Asian discharge ports and transit approaches",
            implied_float_mb_low=0, implied_float_mb_base=15, implied_float_mb_high=30,
            attribution_status="unsupported_sensitivity_only", source_urls=IEA_JUL,
            source_locator="No public port-queue decomposition found",
            confidence="low", method="Publish a 0-30 mb placeholder sensitivity rather than silently assigning the unobserved remainder to rerouting.",
            interpretation="Congestion is physically plausible but not quantified in public data reviewed for this issue.",
            limitations="This is not evidence of congestion and should be replaced by vessel-level anchorage/dwell data if acquired.",
        ),
        row(
            row_id="alternative-measurement", record_type="competing_mechanism_bound",
            case_name="May split and classification error", period="2026-03_to_2026-06", geography="World",
            implied_float_mb_low=-35, implied_float_mb_base=0, implied_float_mb_high=35,
            attribution_status="explicit_measurement_sensitivity", source_urls=f"{IEA_MAY} | {IEA_JUL}",
            source_locator="p2k.12 May missing-split range",
            confidence="low", method="Carry p2k.12's +/-35 mb May oil-on-water sensitivity; no additional numeric AIS-classification correction is invented.",
            interpretation="A material part of the period net change can be revision/classification noise, but measurement cannot explain the physical April and June gross builds by itself.",
            limitations="The +/-35 mb range is a project sensitivity, not an agency error estimate.",
        ),
        row(
            row_id="accounting-boundary-warning", record_type="accounting_guardrail",
            case_name="Oil-on-water reclassification versus balance residual", period="2026-03_to_2026-06", geography="World",
            comparison_value=0, comparison_unit="million barrels valid same-bound residual closure",
            attribution_status="matched_boundary_identity", source_urls=f"{IEA_MAY} | {IEA_JUL}",
            source_locator="p2k.12 matched total-inventory-boundary test",
            confidence="high_for_identity", method="Keep oil on water inside the observed total-inventory comparator used by the balance. Reclassify only for accessible-headroom analysis, not as an additional draw.",
            interpretation="The 18/53/88 mb oil-on-water net change changes where inventory sat and how usable it was, but closes zero barrels of the balance residual on a valid matched total-inventory boundary.",
            limitations="An onshore-only restatement is useful for durability, but subtracting oil on water again from a total already containing it is double counting.",
        ),
        row(
            row_id="verdict-june-voyage", record_type="causal_verdict",
            case_name="June route refill versus storage-to-voyage reclassification", period="2026-06", geography="World",
            implied_float_mb_low=66, implied_float_mb_base=111.6, implied_float_mb_high=117,
            comparison_value=117, comparison_unit="million barrels net June oil-on-water build",
            attribution_status="bounded_partial_attribution", source_urls=f"{IEA_MAY} | {IEA_JUN} | {IEA_JUL}",
            source_locator="route-2026-june-hormuz-refill; p2k.12 June decomposition",
            confidence="low_medium", method="Cap the 66/111.6/151.8 mb ordinary-refill calculation at the observed +117 mb net build. The paired discretionary/other remainder is +51/+5.4/-34.8 mb before the cap and includes storage, congestion, other route changes and measurement.",
            interpretation="Ordinary system refill can explain 66-117 mb (56-100%; best 111.6 mb or 95%) of June's net +117 mb. The honest non-refill remainder is a 51 mb build to a 35 mb unwind, with a 5.4 mb base build.",
            limitations="Strict longer-route float is not added here because much of it likely accumulated before June. Negative remainder in the high-refill case means discretionary/other oil on water was simultaneously released.",
        ),
        row(
            row_id="verdict-period-net", record_type="causal_verdict",
            case_name="March-June net oil-on-water interpretation", period="2026-03_to_2026-06", geography="World",
            implied_float_mb_low=18, implied_float_mb_base=53, implied_float_mb_high=88,
            comparison_value=91, comparison_unit="million barrels base strict structural rerouting",
            attribution_status="offsetting_stock_flows_no_single_share", source_urls=f"{IEA_APR} | {IEA_MAY} | {IEA_JUL}",
            source_locator="p2k.12 net denominator and p2k.13 route arithmetic",
            confidence="low_medium", method="Compare the net change with gross mechanism movements; decline to divide because blocked-storage and normal-float releases offset new route float.",
            interpretation="Rerouting is sufficient to explain the small +53 mb net rise, but saying it explains more than 100% would be misleading. The correct story is large, offsetting gross movements: persistent longer-route float, ordinary June refill, March maritime-pipeline drainage and release or reclassification of blocked Gulf storage.",
            limitations="The net series cannot identify exact shares. Vessel-level location, cargo state and dwell-time data remain the principal missing evidence.",
        ),
    ])

    return rows


def validate(rows: list[dict[str, str]]) -> None:
    ids = [r["row_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    lookup = {r["row_id"]: r for r in rows}
    assert abs(float(lookup["synthesis-structural-rerouting"]["implied_float_mb_base"]) - 91) < 1e-9
    assert abs(float(lookup["synthesis-all-route-logistics"]["implied_float_mb_base"]) - 202.6) < 1e-9
    assert abs(float(lookup["observed-oow-period-net"]["observed_oow_change_mb"]) - 53) < 1e-9
    assert abs(float(lookup["analogue-2024-red-sea"]["implied_float_mb_base"]) - 42) < 1e-9


def main() -> None:
    rows = build()
    validate(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
