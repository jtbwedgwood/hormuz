#!/usr/bin/env python3
"""Build the p2k.6 audit of historical durability-parameter transferability.

This is intentionally a rejection-heavy evidence matrix.  Historical prices
and severity scores are not forward parameters, and blanks remain blanks where
the source record does not identify a transferable numerical quantity.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv"
OUT = ROOT / "data/derived/hormuz_p2k_6_historical_durability_transfer.csv"

FIELDS = [
    "row_id", "parameter_family", "candidate_parameter", "historical_cases",
    "transferability_verdict", "usable_low", "usable_base", "usable_high", "unit",
    "integration_use", "derivation", "reason", "source_urls", "confidence",
    "nontransferable_to", "price_forecast_rule",
]

IEA_SECURITY = "https://www.iea.org/about/oil-security-and-emergency-response"
IEA_2005 = "https://www.iea.org/news/conclusion-of-iea-collective-action"
IEA_2011 = "https://www.iea.org/news/iea-30-day-review-of-libya-collective-action"
IEA_2022 = "https://www.iea.org/news/an-update-on-member-countries-contributions-to-iea-collective-actions"
IEA_2022_END = "https://www.iea.org/news/iea-governing-board-concludes-2022-collective-actions"
DOE_REFILL = "https://www.energy.gov/articles/biden-harris-administration-purchases-more-4-million-barrels-strategic-petroleum-reserve"
DOE_REFILL_FIRST = "https://www.energy.gov/articles/doe-announces-6-million-barrels-strategic-petroleum-reserve-replenishment"
DOE_2026 = "https://www.energy.gov/articles/united-states-release-172-million-barrels-oil-strategic-petroleum-reserve"
DEMAND_PAPER = "https://www.nber.org/papers/w12530"
PRESIDENCY_1991 = "https://www.presidency.ucsb.edu/documents/statement-press-secretary-fitzwater-the-strategic-petroleum-reserve"


def item(
    row_id: str,
    family: str,
    parameter: str,
    cases: str,
    verdict: str,
    low: object = "",
    base: object = "",
    high: object = "",
    unit: str = "",
    integration: str = "",
    derivation: str = "",
    reason: str = "",
    sources: str = "",
    confidence: str = "",
    nontransferable_to: str = "",
) -> dict[str, str]:
    values = {
        "row_id": row_id, "parameter_family": family, "candidate_parameter": parameter,
        "historical_cases": cases, "transferability_verdict": verdict,
        "usable_low": low, "usable_base": base, "usable_high": high, "unit": unit,
        "integration_use": integration, "derivation": derivation, "reason": reason,
        "source_urls": sources, "confidence": confidence,
        "nontransferable_to": nontransferable_to,
        "price_forecast_rule": "Historical price responses are excluded from all forward-price inference.",
    }
    return {field: str(values.get(field, "")) for field in FIELDS}


ROWS = [
    item(
        "transfer-stock-action-deployment-window", "emergency_stocks",
        "coordinated release programme duration", "historical-2005-katrina-rita | historical-2011-libya | historical-2022-russia-ukraine",
        "bounded_process_precedent", 30, 120, 180, "days",
        "Use only as an institutional execution-window sensitivity; current announced and observed execution supersedes it.",
        "2005 and 2011 actions each made 60 mb available over about 30 days. The April 2022 action made 120 mb available over six months. Base is the current US 2026 planned 120-day delivery window, included only as an integration midpoint.",
        "The same IEA member institutions, stockholding laws and tender/obligation mechanisms still operate, so order of magnitude transfers better than shock-specific barrels.",
        f"{IEA_2005} | {IEA_2011} | {IEA_2022} | {DOE_2026}", "medium_high_for_process_low_for_volume",
        "remaining usable stock volume; country allocation; sustainable release rate; current release ceiling",
    ),
    item(
        "context-stock-action-market-equivalent-rate", "emergency_stocks",
        "announced collective market-equivalent rate", "historical-1990-iraq-kuwait | historical-2005-katrina-rita | historical-2011-libya | historical-2022-russia-ukraine",
        "context_only_not_a_forward_bound", 0.67, 2.0, 2.5, "mb/d",
        "Do not insert as p2k.1 burn rate; compare only with independently measured 2026 execution.",
        "1991 contingency plan: 2.5 mb/d from mixed stock draw, saving and replacement. 2005/2011: 60 mb over 30 days = 2.0 mb/d. April 2022: 120 mb over six months = about 0.67 mb/d, excluding the separate March action and US unilateral barrels.",
        "Definitions differ: the 1991 figure includes demand restraint and replacement; 2022 overlaps a larger US action; made-available is not identical to delivered.",
        f"{PRESIDENCY_1991} | {IEA_2005} | {IEA_2011} | {IEA_2022}", "medium_for_scale_low_for_comparability",
        "current government-stock burn rate; physical inventory draw; price effect",
    ),
    item(
        "transfer-stock-obligation-normalisation-window", "emergency_stocks",
        "administrative emergency-stock normalisation window", "historical-2005-katrina-rita | historical-2022-russia-ukraine",
        "bounded_process_precedent", 12, 15, 18, "months",
        "Use as a slow-recharge flag: depleted/relaxed emergency cover should not be assumed to reset within a 6-12 month closure scenario.",
        "After the December 2005 conclusion, IEA members were told to use flexibility in re-establishing stocks through 2006. For 2022, volumes were largely available by end-October and obligations were reinstated after 2024Q1, about 17 months later.",
        "Administrative restoration and obligation timing transfer at order-of-magnitude scale, but neither observation proves physical tanks returned to their exact pre-release level.",
        f"{IEA_2005} | {IEA_2022_END}", "medium",
        "physical global refill rate; current country-specific statutory floor",
    ),
    item(
        "transfer-us-direct-purchase-refill-pace", "emergency_stocks",
        "US SPR direct-purchase replenishment pace after 2022", "historical-2022-russia-ukraine",
        "country_specific_order_of_magnitude", 0.06, 0.083, 0.10, "mb/d",
        "Use only to mark US direct physical repurchase as a years-scale recharge channel; do not extrapolate to IEA members or exchanges.",
        "DOE reported 43.25 mb directly purchased for delivery through December 2024. The first 2023 repurchase was for August delivery; dividing by the roughly August 2023-December 2024 span gives about 0.083 mb/d; 0.06-0.10 is a rounded scheduling band.",
        "Same US caverns and procurement system make the order of magnitude relevant, but price conditions, appropriations, maintenance and exchange returns dominate timing.",
        f"{DOE_REFILL_FIRST} | {DOE_REFILL}", "medium_for_us_order_of_magnitude",
        "global refill pace; gross exchange returns; cancelled mandated sales; net inventory change",
    ),
    item(
        "reject-demand-response-decay-half-life", "demand_response",
        "post-shock conservation decay half-life", "historical-1973-oil-embargo | historical-1978-iranian-revolution | historical-1980-iran-iraq-war | historical-2022-russia-ukraine",
        "reject_no_identified_parameter", unit="months",
        integration="Leave durability unset; model current demand tiers from current sector mechanics and policy evidence.",
        derivation="The 4j7 panel contains no matched consumption-policy counterfactual or post-price-normalisation decay series for these cases.",
        reason="Recession, vehicle turnover, efficiency rules, fuel switching, subsidies and persistent policy changes are inseparable from temporary conservation. No defensible decay rate was identified.",
        sources=f"data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv | {DEMAND_PAPER}", confidence="high_for_rejection",
        nontransferable_to="voluntary-conservation persistence; forced-demand recovery; country demand half-lives",
    ),
    item(
        "reject-1970s-gasoline-elasticity", "demand_response",
        "1975-1980 US short-run gasoline price elasticity", "historical-1973-oil-embargo | historical-1978-iranian-revolution | historical-1980-iran-iraq-war",
        "reject_numeric_transfer", -0.34, -0.275, -0.21, "elasticity",
        "Use only as evidence that demand response is structurally unstable across eras; do not use in a 2026 demand or price calculation.",
        "Hughes, Knittel and Sperling estimate -0.21 to -0.34 in 1975-1980 versus -0.034 to -0.077 in 2001-2006 using comparable US gasoline models.",
        "The large cross-era shift is direct evidence against transferring a 1970s elasticity. The estimate is US gasoline, not global total oil, and is not a conservation-decay measure.",
        DEMAND_PAPER, "high_for_paper_result_high_for_rejection",
        "2026 global oil-demand elasticity; duration; price path",
    ),
    item(
        "reject-rationing-threshold", "demand_response",
        "gross supply-loss threshold for mandatory rationing", "historical-1973-oil-embargo | historical-1990-iraq-kuwait | historical-2005-katrina-rita | historical-2022-russia-ukraine",
        "reject_no_identified_parameter", unit="percent_of_global_supply",
        integration="Use current legal/policy triggers by jurisdiction; historical loss shares are narrative context only.",
        derivation="Historical cases span roughly 2-9% gross peak loss in 4j7, yet policy intensity did not order monotonically with that share.",
        reason="Local product shortages, price controls, distribution failures, war expectations, existing stocks and political institutions—not one global percentage—drove mandatory measures.",
        sources=f"data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv | {IEA_SECURITY}", confidence="high_for_rejection",
        nontransferable_to="a universal tier-3 trigger; country rationing date",
    ),
    item(
        "reject-preexisting-surplus-share", "market_balance",
        "foregone-build share of absorption", "all 4j7 historical oil shocks",
        "reject_no_comparable_observation", unit="percent",
        integration="Use p2k.5's 2026 vintage-specific result only; set historical transfer weight to zero.",
        derivation="The 4j7 panel does not contain frozen pre-event global supply-demand paths comparable to February 2026, and no case has a documented persistent all-month surplus of similar construction.",
        reason="Expected inventory build is vintage- and starting-balance-specific, not an intrinsic shock parameter.",
        sources="data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv | data/derived/hormuz_p2k_5_foregone_build_capacity.csv", confidence="high_for_rejection",
        nontransferable_to="remaining cushion; absorption shares; future market balance",
    ),
    item(
        "reject-route-persistence-as-bypass-decay", "rerouting",
        "multi-year route adaptation duration", "suez-1967-1975 | tanker-war-1984-1988 | red-sea-houthi-2023-ongoing",
        "qualitative_only_reject_numeric_transfer", 1682, "", 2923, "days_observed_in_closed_historical_cases",
        "Use only to say logistics adaptations can persist for years when an alternative route or continued attacked-route traffic exists.",
        "4j7 records 1,682 days for the Tanker War and 2,923 days for the 1967-75 Suez closure. Red Sea traffic substituted around the Cape.",
        "Hormuz has no Cape-equivalent seaborne detour. Its oil bypass is a few fixed pipelines and terminals, so historical route duration does not estimate bypass throughput decay or failure probability.",
        "data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv", "high_for_duration_high_for_rejection",
        "Saudi/UAE pipeline headroom; terminal outage probability; Hormuz flow rate",
    ),
    item(
        "reject-detour-days", "rerouting",
        "modern Suez/Red Sea detour time", "suez-ever-given-2021 | red-sea-houthi-2023-ongoing",
        "reject_numeric_transfer", 10, 12, 14, "days",
        "Do not use in Hormuz oil scenarios.",
        "4j7 primary-source notes report 10 days or more for Cape diversions and roughly two weeks for prolonged Suez blockage.",
        "This parameter applies only where ships can sail around Africa; Hormuz-trapped Gulf cargoes cannot make that detour.",
        "data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv", "high_for_suez_low_for_hormuz",
        "Hormuz delay; pipeline capacity; missing oil supply",
    ),
    item(
        "reject-producer-outage-recovery-time", "supply_recovery",
        "producer/facility outage duration", "historical-2019-abqaiq-khurais | historical-2011-libya | historical-2005-katrina-rita",
        "reject_numeric_transfer", 16, 63, 319, "days",
        "No p2k.1 duration parameter; use current route and facility evidence instead.",
        "Durations are taken from 4j7 event windows and deliberately show the enormous mechanism-dependent spread.",
        "Abqaiq was a repairable concentrated facility attack, Katrina a weather/refining-logistics shock and Libya a civil-war producer outage; none is a de facto closure of the sole maritime outlet for several producers.",
        "data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv", "high_for_rejection",
        "Hormuz reopening date; Gulf production recovery ramp; bypass durability",
    ),
    item(
        "reject-severity-score", "method",
        "4j7 historical severity score", "all 4j7 cases",
        "reject_not_a_physical_parameter", unit="index_points",
        integration="Do not ingest severity rankings into the buffer balance sheet or marginal-absorber timeline.",
        derivation="4j7 explicitly defines the score as a weighted rubric spanning exposure, inventories, route constraints, policy and prices.",
        reason="A composite rank has no physical unit, burn rate, stock floor, capacity ceiling or decay law.",
        sources="docs/hormuz-historical-comparison.md | data/derived/hormuz_4j7_4_case_ranking_scores.csv", confidence="high_for_rejection",
        nontransferable_to="buffer level; burn rate; exhaustion month; price",
    ),
    item(
        "reject-historical-price-path", "method",
        "historical real oil-price response", "all 4j7 oil cases",
        "reject_out_of_scope", unit="percent",
        integration="Exclude from all p2k forward arithmetic.",
        derivation="Price embeds news, expectations, macro demand, policy, market structure and risk premia in addition to physical balances.",
        reason="Historical price moves do not identify a supply-buffer durability parameter and the epic explicitly prohibits price forecasts.",
        sources="docs/hormuz-historical-comparison.md", confidence="high_for_rejection",
        nontransferable_to="future oil price; barrel shortfall; buffer exhaustion",
    ),
]


def validate_case_links(rows: list[dict[str, str]]) -> None:
    with INPUT.open(newline="") as handle:
        case_ids = {record["case_id"] for record in csv.DictReader(handle)}
    for row in rows:
        for candidate in (part.strip() for part in row["historical_cases"].split("|")):
            if not candidate or candidate.startswith("all "):
                continue
            if candidate not in case_ids:
                raise ValueError(f"Unknown 4j7 case ID {candidate} in {row['row_id']}")


def main() -> None:
    validate_case_links(ROWS)
    ids = [row["row_id"] for row in ROWS]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ROWS)
    print(f"Wrote {len(ROWS)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
