#!/usr/bin/env python3
"""Build the r3v.6 missing-barrels precedent and commentary ledger.

This is a source/evidence ledger rather than a statistical model.  Numeric rows are
limited to quantities that a source states or that can be reproduced from stated
rates and calendar days.  Search-audit and mechanism-ranking rows preserve negative
findings and qualitative judgments without manufacturing barrel allocations.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/derived/hormuz_r3v_6_missing_barrels_evidence.csv"

GAO = "https://www.gao.gov/assets/rced-99-142.pdf"
IEEJ = "https://eneken.ieej.or.jp/data/en/data/pdf/147.pdf"
OPEC_2004 = (
    "https://www.opec.org/opec_web/static_files_project/media/downloads/"
    "publications/MOMR_092004.pdf"
)
OGJ_2001 = (
    "https://www.ogj.com/general-interest/companies/article/17220608/"
    "ogj-newsletter"
)
ENERGY_INTELLIGENCE_2004 = (
    "https://www.energyintel.com/0000017b-a7a3-de4c-a17b-e7e3fd500000"
)
MEES_2016 = (
    "https://www.mees.com/2016/9/23/op-ed-documents/"
    "oil-data-is-it-becoming-more-reliable/e5ec96b0-4932-11e7-ae2a-937ac3c1f2e9"
)
KARBUZ_2004 = "https://doi.org/10.1016/S0301-4215(02)00249-5"
KPLER_MAY13 = (
    "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-"
    "the-hormuz-shock-2"
)
KPLER_REBALANCE = (
    "https://www.kpler.com/blog/why-a-20-mbd-supply-shock-is-no-longer-moving-oil-prices"
)
ARGUS_APRIL = (
    "https://www.argusmedia.com/-/media/project/argusmedia/mainsite/english/"
    "documents-and-files/sample-reports/argus-oil-fundamentals-outlook.pdf"
)
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
EIA_JULY = "https://www.eia.gov/todayinenergy/detail.php?id=67865"
EIA_STEO = "https://www.eia.gov/outlooks/steo/report/global_oil.php"
IEF_JULY = (
    "https://www.ief.org/_resources/files/news/comparative-analysis-of-monthly-"
    "reports-on-the-oil-market/july-2026/ief-comparative-analysis-07-2026.pdf"
)
OPEC_JULY = "https://www.opec.org/assets/assetdb/momr-july-2026.pdf"
RYSTAD = (
    "https://www.rystadenergy.com/insights/Oil%20Market%20Balances%20May%20Report%202026"
)
RYSTAD_BUFFERS = (
    "https://www.rystadenergy.com/insights/oil-market-did-not-underreact-it-just-had-buffers"
)
ENERGY_ASPECTS = (
    "https://www.energyaspects.com/resources/insights/"
    "high-frequency-data-show-limited-consumer-demand-response-to-higher-oil-prices"
)
VORTEXA = (
    "https://marketinfo.vortexa.com/rs/837-MZE-578/images/"
    "Vortexa-Situation-Report-6March.pdf"
)
SPGLOBAL = (
    "https://www.spglobal.com/ratings/en/regulatory/article/"
    "oil-price-assumptions-raised-as-hormuz-disruption-deepens-and-inventory-"
    "buffers-erode-near-term-henry-hub-price-assumptions-lowered-s101689190"
)

FIELDS = [
    "row_id",
    "record_type",
    "organization",
    "publication_date",
    "observation_period",
    "direction",
    "magnitude_mb_per_day",
    "cumulative_million_bbl",
    "market_share_pct",
    "comparison_or_rank",
    "mechanism_or_claim",
    "evidence_status",
    "source_url",
    "source_type",
    "interpretation",
    "limitations",
]


def fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}".rstrip("0").rstrip(".")


def row(
    row_id: str,
    record_type: str,
    organization: str,
    publication_date: str,
    observation_period: str,
    direction: str,
    magnitude: float | None,
    cumulative: float | None,
    market_share: float | None,
    comparison_or_rank: str,
    mechanism_or_claim: str,
    evidence_status: str,
    source_url: str,
    source_type: str,
    interpretation: str,
    limitations: str,
) -> dict[str, str]:
    return {
        "row_id": row_id,
        "record_type": record_type,
        "organization": organization,
        "publication_date": publication_date,
        "observation_period": observation_period,
        "direction": direction,
        "magnitude_mb_per_day": fmt(magnitude),
        "cumulative_million_bbl": fmt(cumulative),
        "market_share_pct": fmt(market_share),
        "comparison_or_rank": comparison_or_rank,
        "mechanism_or_claim": mechanism_or_claim,
        "evidence_status": evidence_status,
        "source_url": source_url,
        "source_type": source_type,
        "interpretation": interpretation,
        "limitations": limitations,
    }


def build_rows() -> list[dict[str, str]]:
    # Calendar arithmetic.  1998 was not a leap year; March-June 2026 is 122 days.
    q1_days, q2_days, current_days = 90, 91, 122
    h1_rate = (1.9 * q1_days + 1.7 * q2_days) / (q1_days + q2_days)
    h1_total = 1.9 * q1_days + 1.7 * q2_days
    current_rate = 308.171053 / current_days
    current_market = 101.0  # round scale denominator, not a new balance estimate

    rows = [
        row(
            "history-1998-q1", "historical_precedent", "IEA via GAO", "1999-05-14",
            "1998-Q1", "positive_missing_implied_build_not_observed", 1.9,
            1.9 * q1_days, None, "opposite sign to 2026",
            "Supply exceeded demand without corresponding reported stock build.",
            "reported", GAO, "government_audit_of_IEA_data",
            "The largest quarter in the famous 1998 episode was 1.9 mb/d.",
            "Preliminary all-oil balance; stock coverage excluded non-OECD and some independent storage.",
        ),
        row(
            "history-1998-q2", "historical_precedent", "IEA via GAO", "1999-05-14",
            "1998-Q2", "positive_missing_implied_build_not_observed", 1.7,
            1.7 * q2_days, None, "opposite sign to 2026",
            "Supply exceeded demand without corresponding reported stock build.",
            "reported", GAO, "government_audit_of_IEA_data",
            "The discrepancy persisted for a second quarter but eased slightly.",
            "Same scope warning as Q1; quarterly values are rounded to 0.1 mb/d.",
        ),
        row(
            "history-1998-h1", "historical_comparison", "Project from GAO table", "2026-08-06",
            "1998-H1", "positive_missing_implied_build_not_observed", h1_rate,
            h1_total, None, "current rate / H1 rate = 1.404",
            "Calendar-weighted combination of GAO's 1998 Q1 and Q2 rates.",
            "project_arithmetic", GAO, "calculation_from_primary_table",
            "About 326 mb accumulated over six months: slightly more barrels than the current 308 mb, but at a 40% slower daily rate.",
            "Cumulative comparison is duration-sensitive and directions are opposite.",
        ),
        row(
            "history-1998-year", "historical_precedent", "IEA via GAO", "1999-05-14",
            "1998", "positive_missing_implied_build_not_observed", 1.2, 438.0, 1.6,
            "current total is 70.4% of annual 1998 total",
            "Annual supply 75.3 less demand 73.7 less reported OECD stock build 0.4.",
            "reported", GAO, "government_audit_of_IEA_data",
            "The canonical annual figure was 438 mb, or 1.6% of the roughly 75 mb/d market.",
            "Annual averaging hides the 1.9/1.7 mb/d first-half peak.",
        ),
        row(
            "current-2026-mar-jun", "current_diagnostic", "Project", "2026-08-06",
            "2026-03-01_to_2026-06-30", "negative_missing_implied_draw_not_observed",
            current_rate, 308.171053, current_rate / current_market * 100,
            "1.404x 1998-H1 rate; 1.329x 1998 peak quarter",
            "EIA implied draw less mixed-vintage public IEA observed-stock draw.",
            "cross_system_diagnostic", IEF_JULY + " | " + IEA_MAY,
            "project_cross_system_calculation",
            "Large and historically legible, but not a measured pile of 308 mb hidden in tanks.",
            "Crosses agencies, scopes and vintages; the market-share denominator is a rounded 101 mb/d scale.",
        ),
        row(
            "history-2003-mar-jun", "historical_precedent", "Energy Intelligence", "2004-04-19",
            "2003-03_to_2003-06", "negative_missing_observed_build_exceeded_implied_build",
            1.6, None, None, "same sign as 2026; current is 1.579x rate",
            "Observed stocks grew 2.5 mb/d versus a 0.9 mb/d implied build.",
            "reported_trade_analysis", ENERGY_INTELLIGENCE_2004, "trade_press_analysis",
            "A same-sign discrepancy of about 1.6 mb/d occurred during Iraq-war dislocation.",
            "The article's March-to-June wording does not support an exact day-count total.",
        ),
        row(
            "history-2003-q3", "historical_precedent", "Energy Intelligence", "2004-04-19",
            "2003-Q3", "negative_missing_observed_build_despite_implied_draw", 1.7,
            None, None, "same sign as 2026; current is 1.486x rate",
            "Demand exceeded supply by 0.6 mb/d while estimated inventories built 1.2 mb/d.",
            "reported_trade_analysis", ENERGY_INTELLIGENCE_2004, "trade_press_analysis",
            "The closest sourced same-sign quarterly precedent found is still materially below 2.526 mb/d.",
            "Non-OECD and independent-stock estimates were incomplete.",
        ),
        row(
            "method-gao-cause", "historical_resolution", "GAO with IEA and industry", "1999-05-14",
            "1998", "mixed", None, None, None, "no quantified split",
            "Both preliminary supply/demand/statistical limitations and actual unreported stocks.",
            "corroborated", GAO, "government_audit_interviews_and_data_review",
            "The authoritative contemporary review rejected a one-cause resolution and could not quantify the split.",
            "Interviewees were anonymized; subsequent revisions changed the historical balance.",
        ),
        row(
            "method-2001-demand-revision", "historical_resolution", "IEA via Oil & Gas Journal", "2001-08-20",
            "1999-2000", "revision_reduced_positive_missing", 0.383, None, None,
            "2000 miscellaneous reduced from 0.8 to 0.5 mb/d",
            "Upward non-OECD demand revisions for FSU, Indonesia, Brazil, Algeria, Philippines, Iraq and Singapore.",
            "reported_revision", OGJ_2001, "trade_press_reporting_of_IEA_revision",
            "Later demand data removed a material part of the discrepancy, including undercounted feedstocks, unrecognized refineries and direct burn.",
            "The numeric revision applies to 1999 demand and is not a direct decomposition of 1998.",
        ),
        row(
            "method-2004-five-year-resolution", "historical_resolution", "Energy Intelligence", "2004-04-19",
            "1998_revised_through_2004", "revision_reduced_positive_missing", None, None, None,
            "some but not all removed",
            "Five years of upward demand and smaller downward supply revisions removed some of 1998's missing barrels.",
            "reported_trade_analysis", ENERGY_INTELLIGENCE_2004, "trade_press_analysis",
            "The 1998 debate faded through revisions plus possible inventories; it did not end with discovery of one hidden stockpile.",
            "The surviving page does not give a revised final 1998 barrel total.",
        ),
        row(
            "method-ieej-1999-unwind", "historical_resolution", "IEEJ", "2002-07-01",
            "1999", "negative_missing_after_positive_missing", None, None, None,
            "interpretive, not a measured ownership bridge",
            "Backwardation and short supply were cited as prompting drawdown of portions of prior missing barrels.",
            "analyst_interpretation", IEEJ, "research_institute_report",
            "Some physical inventory likely existed and later unwound, but the report also lists statistical and coverage failures.",
            "Does not quantify how much of the 1998 residual physically returned.",
        ),
        row(
            "method-opec-uncertainty", "methodology_evidence", "OPEC", "2004-09-01",
            "methodological", "mixed", None, None, None, "supply uncertainty 0.3; demand 0.5 mb/d",
            "Balance is a small difference between two large uncertain numbers; non-OECD stocks and oil on water are weakly measured.",
            "primary_agency_methodology", OPEC_2004, "official_monthly_report",
            "Agency scatter and missing stocks are both expected products of the measurement architecture.",
            "Uncertainty estimates are from 2004 and should not be transplanted numerically to 2026.",
        ),
        row(
            "method-mees-revisions", "methodology_evidence", "MEES", "2016-09-23",
            "1990-2015 audit", "mixed", None, None, None, "revisions continue years later",
            "No clear long-term improvement in supply revisions; small demand/supply errors can create exaggerated stock changes.",
            "documented_archive_audit", MEES_2016, "trade_methodology_analysis",
            "Preliminary quarterly balance gaps should be expected to shrink, grow or reverse as base data mature.",
            "Trade analysis, not a peer-reviewed uncertainty distribution.",
        ),
        row(
            "method-academic-conversion-scope", "methodology_evidence", "Sohbet Karbuz / Energy Policy", "2004-01-01",
            "general world-oil statistics", "mixed", None, None, None,
            "peer-reviewed methodological corroboration",
            "Even country data submitted by one administration diverge across organizations; definitions and mass-volume conversion compound in world balances.",
            "peer_reviewed", KARBUZ_2004, "academic_journal_article",
            "Corroborates the agency-scatter mechanism: shared source data do not force identical published balances.",
            "Focuses on conversion factors and aggregation, not a numeric decomposition of the 1998 or 2026 residual.",
        ),
        row(
            "commentary-kpler-april-gap", "contemporary_direct_commentary", "Kpler", "2026-05-13",
            "2026-04", "negative_missing_implied_draw_not_observed", 0.659, 0.659 * 30,
            None, "direct residual commentary",
            "Balance deficit 1.34 mb/d versus observed inventory plus oil-on-water decline 0.682 mb/d.",
            "direct_quantified_analyst_claim", KPLER_MAY13, "tanker_and_inventory_analytics",
            "Kpler explicitly identifies a smaller version of the project's residual.",
            "Crude and condensate scope, not the project's all-liquids March-June construction.",
        ),
        row(
            "commentary-kpler-april-mechanisms", "contemporary_direct_commentary", "Kpler", "2026-05-13",
            "2026-04", "mixed", None, None, None, "named alternatives",
            "Underground or pipeline-system withdrawals not monitored, or downward refinery-run revisions, especially China.",
            "analyst_hypotheses", KPLER_MAY13, "tanker_and_inventory_analytics",
            "The only public named-analyst source found that directly frames both physical and model-error alternatives for the gap.",
            "No allocation between mechanisms; April and May estimates were preliminary.",
        ),
        row(
            "commentary-kpler-may-gap", "contemporary_direct_commentary", "Kpler", "2026-05-13",
            "2026-05_to_date", "negative_missing_implied_draw_not_observed", 1.69, None,
            None, "direct but incomplete-month estimate",
            "Gap between crude balance and combined inventory/oil-on-water data widened to 1.69 mb/d.",
            "preliminary_analyst_claim", KPLER_MAY13, "tanker_and_inventory_analytics",
            "Confirms that specialists saw the reconciliation problem in real time.",
            "Incomplete month and explicitly expected to be revised.",
        ),
        row(
            "commentary-kpler-china-later", "contemporary_direct_commentary", "Kpler", "2026-06",
            "2026-05", "mixed", None, None, None, "government-SPR claim not supported",
            "China refinery-site inventories drew about 15 mb in May while estimated SPR built about 8 mb.",
            "analyst_estimate", KPLER_REBALANCE, "tanker_and_inventory_analytics",
            "Supports commercial/operational draws while cutting against a large China government-SPR explanation.",
            "Tank classification and legal ownership remain modelled rather than officially reported.",
        ),
        row(
            "commentary-argus-forecast", "contemporary_balance_context", "Argus", "2026-04-01",
            "2026-03_to_2026-06_forecast", "forecast_draw", 4.6, None, None,
            "2.0 SPR plus 2.6 commercial mb/d assumed",
            "Forecast stock draws were used to close Argus's disruption scenario.",
            "forecast_not_observation", ARGUS_APRIL, "consultancy_outlook",
            "Shows that large draws were analytically plausible before observations matured, but does not locate the project's residual.",
            "Scenario assumptions are not ex-post stock measurements.",
        ),
        row(
            "commentary-iea-search", "search_audit", "IEA", "2026-08-06",
            "public March-July 2026 reports", "not_applicable", None, None, None,
            "no direct 308 mb reconciliation found",
            "Reports observed stocks, refinery/end-user demand cuts, supply gains and rerouting.",
            "relevant_context_no_direct_residual", IEA_MAY, "official_agency_reporting",
            "Strong component evidence, but no public explanation of the EIA-versus-IEA project plug.",
            "Public OMR summaries omit subscriber tables and revisions needed for a same-system reconciliation.",
        ),
        row(
            "commentary-eia-search", "search_audit", "EIA", "2026-08-06",
            "public March-July 2026 releases", "not_applicable", None, None, None,
            "no direct cross-agency reconciliation found",
            "July estimated 2Q crude inventory declines at 5.1 mb/d and warns timely Asian demand/HGL data are limited.",
            "relevant_context_no_direct_residual", EIA_JULY + " | " + EIA_STEO,
            "official_agency_reporting",
            "EIA itself flags the demand-estimation channel that can enlarge an implied draw.",
            "EIA's global inventory change is primarily a supply-minus-demand implication, not a tank census.",
        ),
        row(
            "commentary-opec-search", "search_audit", "OPEC", "2026-08-06",
            "public March-July 2026 MOMRs", "not_applicable", None, None, None,
            "no direct Hormuz residual discussion found",
            "Publishes a materially different balance and lagged OECD commercial stocks.",
            "agency_balance_context_no_direct_residual", OPEC_JULY, "official_agency_reporting",
            "OPEC's 672.3 mb project-implied draw helps demonstrate model scatter, not a fourth observed stock series.",
            "Balance scope and call-on-DoC construction differ from EIA and IEA.",
        ),
        row(
            "commentary-ief-search", "search_audit", "IEF", "2026-08-06",
            "July 2026 comparison", "not_applicable", None, None, None,
            "documents scatter; does not reconcile observations",
            "Compares IEA, EIA and OPEC demand, supply and call estimates.",
            "agency_comparison_no_direct_residual", IEF_JULY, "intergovernmental_comparison",
            "Best public evidence that agency balance levels diverge materially.",
            "Agencies share underlying data; comparison is not statistically independent.",
        ),
        row(
            "commentary-rystad-search", "search_audit", "Rystad Energy", "2026-08-06",
            "public March-June 2026 commentary", "not_applicable", None, None, None,
            "no direct residual quantification found",
            "Attributes rebalancing to buffers and later large refinery-run-led demand revisions; says China showed no government-SPR draw.",
            "relevant_context_no_direct_residual", RYSTAD + " | " + RYSTAD_BUFFERS,
            "consultancy_public_commentary",
            "Corroborates demand/run revision and non-China-SPR interpretation.",
            "Condensed public material lacks its detailed balance tables.",
        ),
        row(
            "commentary-energy-aspects-search", "search_audit", "Energy Aspects", "2026-08-06",
            "public March-July 2026 commentary", "not_applicable", None, None, None,
            "no direct residual quantification found",
            "High-frequency trucking, gasoline and jet indicators showed limited early end-user demand response; inventory monitoring showed draws.",
            "relevant_context_no_direct_residual", ENERGY_ASPECTS, "consultancy_high_frequency_analysis",
            "Cuts against assigning every downward demand revision to visible consumer conservation.",
            "Public commentary does not expose a global supply-demand-stock identity.",
        ),
        row(
            "commentary-vortexa-search", "search_audit", "Vortexa", "2026-08-06",
            "public March 2026 situation report", "not_applicable", None, None, None,
            "no direct residual quantification found",
            "Documents pre-positioned Iranian oil on water and prospective inventory draw/refill timing.",
            "flow_context_no_direct_residual", VORTEXA, "tanker_analytics_scenario_report",
            "Supports oil-on-water and delivery-lag mechanisms at the start of the shock.",
            "Prospective scenario published March 6, not an ex-post March-June balance.",
        ),
        row(
            "commentary-spglobal-search", "search_audit", "S&P Global", "2026-08-06",
            "public 2026 commentary", "not_applicable", 3.0, None, None,
            "full-year forecast, no direct residual",
            "Expected roughly 3 mb/d average 2026 inventory draw from 103.6 demand versus 100.7 supply.",
            "forecast_context_no_direct_residual", SPGLOBAL, "ratings_assumption",
            "Another organization found a multi-mb/d balance draw plausible, but did not verify it in observed tanks.",
            "Rounded full-year forecast and different vintage/scope.",
        ),
        row(
            "inference-agency-scatter", "inference_test", "Project", "2026-08-06",
            "2026-03_to_2026-06", "mixed", None, 411.0, None,
            "corroborates model/vintage error; does not exclude hidden stocks",
            "EIA, IEA and OPEC implied draws span about 411 mb before comparison with one observed-stock family.",
            "project_inference_supported_with_qualification", IEF_JULY + " | " + GAO,
            "project_synthesis",
            "Scatter proves the 308 mb point is model-dependent and cannot all be treated as a common physical stock movement.",
            "A shared blind spot can coexist with different agency errors; scatter alone cannot estimate the physical share.",
        ),
        row(
            "rank-1-measurement-model", "mechanism_ranking", "Project", "2026-08-06",
            "2026-03_to_2026-06", "mixed", None, None, None, "rank 1",
            "Cross-system definitions/vintages plus preliminary supply, demand and refinery-run estimation error.",
            "high_support", GAO + " | " + IEF_JULY + " | " + KPLER_MAY13,
            "project_evidence_ranking",
            "Necessarily explains a material share because balance agencies disagree by more than the base residual.",
            "Cannot split supply error from demand error with public data.",
        ),
        row(
            "rank-2-understated-demand", "mechanism_ranking", "Project", "2026-08-06",
            "2026-03_to_2026-06", "negative_missing", None, None, None, "rank 2 within model error",
            "Understated demand reduction and refinery-run cuts, especially non-OECD Asia and petrochemical feedstocks.",
            "medium_high_support", EIA_STEO + " | " + KPLER_MAY13 + " | " + OGJ_2001,
            "project_evidence_ranking",
            "Leading directional economic explanation: lower actual use reduces the implied draw without requiring hidden barrels.",
            "Partly overlaps rank 1 and cannot be barrel-allocated from current public observations.",
        ),
        row(
            "rank-3-unobserved-stocks", "mechanism_ranking", "Project", "2026-08-06",
            "2026-03_to_2026-06", "negative_missing", None, None, None, "rank 3",
            "Producer, non-OECD commercial, independent, refinery, underground and pipeline-system stock draws.",
            "medium_support", GAO + " | " + KPLER_MAY13 + " | " + OPEC_2004,
            "project_evidence_ranking",
            "Almost certainly nonzero as a category, but no evidence supports assigning the full 308 mb to it.",
            "Ownership, location and overlap with observed onshore estimates are unresolved.",
        ),
        row(
            "rank-4-oil-on-water", "mechanism_ranking", "Project", "2026-08-06",
            "2026-03_to_2026-06", "mixed", None, None, None, "rank 4",
            "Oil-on-water, arrival timing, floating storage and revisions to voyage classification.",
            "medium_support", KPLER_MAY13 + " | " + VORTEXA + " | " + OPEC_2004,
            "project_evidence_ranking",
            "Can dominate individual months and explains why shipment and tank clocks differ.",
            "Less persuasive as the sole explanation for a four-month cumulative residual because the project stock comparator includes oil on water.",
        ),
        row(
            "rank-5-china-government-spr", "mechanism_ranking", "Project", "2026-08-06",
            "2026-03_to_2026-06", "negative_missing", None, None, None, "rank 5 / not supported",
            "Large China government-SPR draw.",
            "low_support", KPLER_REBALANCE + " | " + RYSTAD_BUFFERS,
            "project_evidence_ranking",
            "Do not use as a base explanation; public analyst estimates show commercial/refinery flexibility and continued or flat strategic stocks.",
            "A small opaque contribution cannot be excluded because China does not publish a clean ownership series.",
        ),
        row(
            "verdict-characterization", "recommended_characterization", "Project", "2026-08-06",
            "2026-03_to_2026-06", "negative_missing_implied_draw_not_observed",
            current_rate, 308.171053, None, "large, not normal, historically legible",
            "Preliminary cross-system balance discrepancy with an epistemic 0-415 mb range.",
            "recommended_blog_language", GAO + " | " + ENERGY_INTELLIGENCE_2004 + " | " + IEF_JULY,
            "project_synthesis",
            "Use: 'about 310 mb in the base accounting, but not 310 measured hidden barrels; the rate exceeds the best documented historical episodes, while comparable cumulative gaps have occurred over longer windows.'",
            "Retain low/base/high and revise as agency demand, supply and stock vintages mature.",
        ),
    ]
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    assert rows and len({r["row_id"] for r in rows}) == len(rows)
    assert all(set(r) == set(FIELDS) for r in rows)
    lookup = {r["row_id"]: r for r in rows}
    assert abs(float(lookup["history-1998-h1"]["cumulative_million_bbl"]) - 325.7) < 1e-6
    assert abs(float(lookup["current-2026-mar-jun"]["magnitude_mb_per_day"]) - 2.525992) < 1e-6
    assert lookup["verdict-characterization"]["comparison_or_rank"] == "large, not normal, historically legible"
    assert lookup["rank-5-china-government-spr"]["evidence_status"] == "low_support"


def main() -> None:
    rows = build_rows()
    validate(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
