#!/usr/bin/env python3
"""Build no-price demand-scaling scenarios for continued Hormuz disruption.

The output deliberately separates three things that are easy to conflate:

* absorber flows already present in the historical accounting;
* genuinely incremental, but conditional, non-demand flow headroom; and
* illustrative demand-pressure landing if the March-June demand adjustment
  has to scale to 1.25x, 1.5x, or 2x.

The country figures are a transparent continuity benchmark, not a forecast.
They allocate each scenario increment in proportion to the *positive* current
country/region gap resolved in p2k.10.  The qualitative marginal-pressure
assessment comes from p2k.3 and explicitly overrides a naive claim that this
pro-rata benchmark predicts the next barrel.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P2K3 = ROOT / "data/derived/hormuz_p2k_3_demand_cost_tier_matrix.csv"
P2K7 = ROOT / "data/derived/hormuz_p2k_7_bypass_headroom_vulnerability.csv"
P2K8 = ROOT / "data/derived/hormuz_p2k_8_stock_exhaustion_bounds.csv"
P2K9 = ROOT / "data/derived/hormuz_p2k_9_forward_surplus_decomposition.csv"
P2K10 = ROOT / "data/derived/hormuz_p2k_10_country_demand_resolution.csv"
OUT = ROOT / "data/derived/hormuz_p2k_11_demand_scaling_scenarios.csv"

HISTORICAL_DAYS = 122
SCENARIO_MULTIPLIERS = (1.25, 1.50, 2.00)

FIELDS = [
    "row_id", "record_type", "scenario", "multiplier", "parent_row_id",
    "period_start", "period_end", "current_demand_reduction_mb_d",
    "scenario_demand_reduction_mb_d", "incremental_demand_reduction_mb_d",
    "incremental_non_demand_low_mb_d", "incremental_non_demand_base_mb_d",
    "incremental_non_demand_high_mb_d", "residual_increment_low_mb_d",
    "residual_increment_base_mb_d", "residual_increment_high_mb_d",
    "ongoing_absorber_flow_mb_d", "channel", "geography",
    "sector_or_mechanism", "historical_gap_million_bbl",
    "historical_positive_gap_share_pct", "continuity_benchmark_increment_mb_d",
    "current_cost_tier", "pressure_order", "headroom_status",
    "exhaustion_or_bound_date", "bound_type", "evidence_status", "confidence",
    "source_row_ids", "source_urls", "method", "interpretation", "consequences",
    "caveat", "non_additivity_rule",
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def outrow(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    unknown = set(values) - set(FIELDS)
    if unknown:
        raise KeyError(sorted(unknown))
    result.update({key: fmt(value) for key, value in values.items()})
    return result


def by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    index = {row["row_id"]: row for row in rows}
    if len(index) != len(rows):
        raise ValueError("Duplicate source row_id")
    return index


def number(index: dict[str, dict[str, str]], row_id: str, field: str) -> float:
    return float(index[row_id][field])


def source_urls(index: dict[str, dict[str, str]], row_ids: list[str]) -> str:
    urls: list[str] = []
    for row_id in row_ids:
        for url in index[row_id]["source_url"].split(" | "):
            if url and url not in urls:
                urls.append(url)
    return " | ".join(urls)


def build() -> list[dict[str, str]]:
    p2k3_rows = read(P2K3)
    p2k7_rows = read(P2K7)
    p2k8_rows = read(P2K8)
    p2k9_rows = read(P2K9)
    p2k10_rows = read(P2K10)
    t3 = by_id(p2k3_rows)
    t7 = by_id(p2k7_rows)
    t8 = by_id(p2k8_rows)
    t9 = by_id(p2k9_rows)
    t10 = by_id(p2k10_rows)

    current_volume = number(t10, "exact-world", "value_base_million_bbl")
    current_rate = current_volume / HISTORICAL_DAYS

    # No-reopening flow is a conditional forecast, not inventory.  A negative
    # balance is not positive headroom and is therefore floored at zero here.
    forward_low = max(0.0, number(
        t9, "scenario-q3_partial_flow_hold_july_demand-low_surviving_balance",
        "no_reopening_balance_mb_d",
    ))
    forward_base = max(0.0, number(
        t9, "scenario-q3_partial_flow_hold_july_demand-base_surviving_balance",
        "no_reopening_balance_mb_d",
    ))
    forward_high = max(0.0, number(
        t9, "scenario-q3_partial_flow_hold_july_demand-high_surviving_balance",
        "no_reopening_balance_mb_d",
    ))
    bypass_possible = number(t7, "iraq-ceyhan-operational", "remaining_headroom_mb_per_day")

    # The base case does not credit the undemonstrated Iraq increment.  The high
    # case does.  Global stock draw-rate expansion is unknown, so it is absent.
    headroom_low = forward_low
    headroom_base = forward_base
    headroom_high = forward_high + bypass_possible

    iea_release_rate = number(
        t8, "iea-government-zero-arithmetic-average-release-rate", "draw_rate_mb_per_day"
    )
    bypass_flow = number(t7, "system-bypass-summary", "june_incremental_export_mb_per_day")

    rows: list[dict[str, str]] = []
    rows.append(outrow(
        row_id="historical-demand-baseline", record_type="historical_baseline",
        scenario="march_june_2026_vintage_gap", period_start="2026-03-01",
        period_end="2026-06-30", current_demand_reduction_mb_d=current_rate,
        scenario_demand_reduction_mb_d=current_rate,
        incremental_demand_reduction_mb_d=0.0, channel="demand adjustment",
        geography="World", sector_or_mechanism="all oil end uses",
        historical_gap_million_bbl=current_volume,
        evidence_status="EIA February-minus-July demand-vintage difference",
        confidence="high_arithmetic_low_causal",
        source_row_ids="p2k.10 exact-world", source_urls=t10["exact-world"]["source_url"],
        method="Divide the 439.228 mb March-June vintage gap by 122 calendar days.",
        interpretation=f"The scenario baseline is {current_rate:.3f} mb/d, not a causal estimate of Hormuz-only conservation.",
        caveat="The vintage gap includes ordinary forecast revision and contemporaneous shocks.",
        non_additivity_rule="Headline denominator; country rows below are nested continuity benchmarks.",
    ))

    rows.extend([
        outrow(
            row_id="ongoing-bypass-flow", record_type="ongoing_absorber_flow",
            scenario="continued_q3_partial_flow", ongoing_absorber_flow_mb_d=bypass_flow,
            channel="Gulf bypass rerouting", geography="Saudi Arabia / UAE / Iraq",
            sector_or_mechanism="existing non-Hormuz routes",
            headroom_status="ongoing_3.4_mb_d_but_only_0.2_mb_d_possible_increment",
            bound_type="non_exhaustible_rate_ceiling_with_step_failure_risk",
            evidence_status="route reconstruction plus reported capacity",
            confidence="medium_low", source_row_ids="p2k.7 system-bypass-summary",
            source_urls=t7["system-bypass-summary"]["source_url"],
            method="Carry the p2k.7 current flow separately from incremental rate headroom.",
            interpretation="Roughly 3.4 mb/d can persist but is already in the current accounting; it cannot be used again against a larger demand scenario.",
            caveat="Upstream disruption avoidance and downstream market clearing are different accounting frames and are not additive.",
            non_additivity_rule="Do not add this current flow to incremental headroom or emergency-stock releases.",
        ),
        outrow(
            row_id="incremental-bypass-headroom", record_type="incremental_headroom_component",
            scenario="continued_q3_partial_flow", incremental_non_demand_low_mb_d=0.0,
            incremental_non_demand_base_mb_d=0.0,
            incremental_non_demand_high_mb_d=bypass_possible,
            channel="Gulf bypass rerouting", geography="Iraq",
            sector_or_mechanism="possible additional Ceyhan flow",
            headroom_status="possible_not_demonstrated", bound_type="flow_not_stock_no_exhaustion_date",
            evidence_status="government-indicated operational sensitivity",
            confidence="medium_low", source_row_ids="p2k.7 iraq-ceyhan-operational",
            source_urls=t7["iraq-ceyhan-operational"]["source_url"],
            method="Credit zero in low/base and the 0.2 mb/d indicated increment only in high.",
            interpretation="This is the only specifically identified new bypass rate; Saudi and UAE are at demonstrated ceilings.",
            caveat="Political, gathering-system and terminal constraints can prevent delivery.",
            non_additivity_rule="Included in the high headroom envelope; do not add again.",
        ),
        outrow(
            row_id="incremental-forward-balance", record_type="incremental_headroom_component",
            scenario="continued_q3_partial_flow_2027", incremental_non_demand_low_mb_d=forward_low,
            incremental_non_demand_base_mb_d=forward_base,
            incremental_non_demand_high_mb_d=forward_high,
            channel="non-Gulf supply and balance effects", geography="World",
            sector_or_mechanism="surviving 2027 balance with Q3 shut-ins held",
            headroom_status="conditional_forecast_flow_not_assured_capacity",
            bound_type="flow_not_stock_no_exhaustion_date", evidence_status="p2k.9 sensitivity",
            confidence="low_scenario_high_arithmetic",
            source_row_ids=("p2k.9 scenario-q3_partial_flow_hold_july_demand-low/base/high_"
                            "surviving_balance"),
            source_urls=t9["verdict-no-reopening-credit"]["source_urls"],
            method="Floor the -0.396 mb/d low balance at zero positive headroom; retain 0.053 base and 0.502 high.",
            interpretation="Only 0/0.053/0.502 mb/d of positive flow is creditable, not the reopening branch's 5.031 mb/d.",
            caveat="Even 0.502 mb/d is a conditional forecast and the Q3 traffic proxy embeds June improvement.",
            non_additivity_rule="Included once in the low/base/high incremental headroom envelope.",
        ),
        outrow(
            row_id="incremental-headroom-envelope", record_type="incremental_headroom_summary",
            scenario="continued_q3_partial_flow", incremental_non_demand_low_mb_d=headroom_low,
            incremental_non_demand_base_mb_d=headroom_base,
            incremental_non_demand_high_mb_d=headroom_high,
            channel="new non-demand flow", geography="World",
            sector_or_mechanism="forward balance plus possible Iraq bypass increment",
            headroom_status="0_to_0.702_mb_d_identified_base_0.053",
            bound_type="conditional_flow_envelope_no_exhaustion_date",
            evidence_status="synthesis of p2k.7 and p2k.9", confidence="low_medium",
            source_row_ids="p2k.7 iraq-ceyhan-operational | p2k.9 verdict-no-reopening-credit",
            source_urls=(t7["iraq-ceyhan-operational"]["source_url"] + " | " +
                         t9["verdict-no-reopening-credit"]["source_urls"]),
            method="Sum only positive p2k.9 flow with the possible 0.2 mb/d Iraq increment in the high case.",
            interpretation=f"New identified non-demand flow is {headroom_low:.3f}/{headroom_base:.3f}/{headroom_high:.3f} mb/d low/base/high.",
            caveat="This is not assured capacity and excludes unknown global stock draw-rate expansion.",
            non_additivity_rule="Summary of the preceding two incremental components.",
        ),
        outrow(
            row_id="ongoing-iea-stock-release", record_type="ongoing_absorber_flow",
            scenario="historical_average_not_committed_future_path",
            ongoing_absorber_flow_mb_d=iea_release_rate, channel="government oil stocks",
            geography="IEA members", sector_or_mechanism="collective release",
            headroom_status="historical_average_flow_usable_increment_unknown",
            exhaustion_or_bound_date="2027-10-19", bound_type="gross_zero_no_earlier_than_if_rate_constant",
            evidence_status="greater-than stock level plus historical average release",
            confidence="high_arithmetic_low_for_usable_duration",
            source_row_ids="p2k.8 iea-government-zero-arithmetic-average-release-rate",
            source_urls=t8["iea-government-zero-arithmetic-average-release-rate"]["source_url"],
            method="Carry 290/132=2.197 mb/d as an already-observed average, not as a promised forward rate.",
            interpretation="Because gross stocks were greater than 1 bn barrels, physical zero at this rate cannot occur before 19 October 2027.",
            caveat="Country legal, operational, product and policy floors can bind earlier; >1 bn is not a measured stock and physical zero is not an operating floor.",
            non_additivity_rule="Do not subtract this ongoing historical flow from the scenario increment; no additional global release-rate headroom is measured.",
        ),
        outrow(
            row_id="us-spr-operating-bound", record_type="stock_date_bound",
            scenario="constant_july_draw_rate", ongoing_absorber_flow_mb_d=number(
                t8, "us-spr-zero-bound-july-rate", "draw_rate_mb_per_day"
            ), channel="U.S. Strategic Petroleum Reserve", geography="United States",
            sector_or_mechanism="gross inventory draw",
            headroom_status="0_to_304.809_mb_above_unknown_operational_floor",
            exhaustion_or_bound_date="2027-12-24", bound_type="latest_possible_physical_zero_at_fixed_rate",
            evidence_status="observed gross level and endpoint draw rate",
            confidence="high_arithmetic_low_for_operating_horizon",
            source_row_ids="p2k.8 us-spr-zero-bound-july-rate | us-spr-operational-floor",
            source_urls=t8["us-spr-zero-bound-july-rate"]["source_url"],
            method="Divide 304.809 mb by 0.5956 mb/d; keep the unpublished operating floor separate.",
            interpretation="Fixed-rate physical zero is about 24 December 2027, but usable operating duration is anywhere from zero to that upper bound.",
            caveat="The U.S. row is nested inside the IEA system; GAO found capability and accessibility constraints before July.",
            non_additivity_rule="Memo inside collective stocks; never add its rate or volume to the IEA total.",
        ),
        outrow(
            row_id="stock-exhaustion-verdict", record_type="exhaustion_verdict",
            scenario="continued_q3_partial_flow", channel="government oil stocks",
            geography="IEA members", sector_or_mechanism="usable draw capacity",
            headroom_status="no_honest_single_usable_exhaustion_date",
            exhaustion_or_bound_date="unknown; gross-zero guardrails 2027-10-19 and 2027-12-24",
            bound_type="operating_floors_can_bind_earlier",
            evidence_status="known gross bounds; unknown country usable floors",
            confidence="high_for_nonidentification",
            source_row_ids=("p2k.8 iea-government-zero-arithmetic-average-release-rate | "
                            "us-spr-operational-floor | iea-net-importer-aggregate-floor-april"),
            source_urls=t8["iea-net-importer-aggregate-floor-april"]["source_url"],
            method="Refuse to convert gross physical-zero arithmetic into a usable system exhaustion forecast.",
            interpretation="The requirement for a dated exhaustion result can only be met with bounds: no guaranteed stock horizon is identified.",
            caveat="April aggregate statutory headroom of 0-46 import days cannot be converted to a release duration without country ownership and rates.",
            non_additivity_rule="Qualitative verdict, not a flow or volume row.",
        ),
    ])

    # Positive current adjustment clusters.  Exact countries and neutral-share
    # allocations are intentionally kept distinct in source rows; both are
    # used here only for a pro-rata continuity benchmark.
    clusters = [
        {
            "id": "northeast-asia-industrial", "geography": "China / Japan / South Korea",
            "rows": ["exact-country-china", "exact-country-japan", "allocation-asia-and-oceania-south-korea"],
            "mechanism": "refinery, naphtha/petrochemical, aviation and mobility cuts",
            "tier": "2_to_3", "order": "1_large_existing_absorber_but_cheap_switching_capped",
            "evidence": ["china-refinery-petrochemical", "japan-naphtha-refining", "korea-petrochemical-refining"],
        },
        {
            "id": "gulf-fragile", "geography": "Iran / Iraq / Kuwait / Qatar / other Middle East",
            "rows": ["allocation-middle-east-iran", "allocation-middle-east-iraq", "allocation-middle-east-kuwait", "allocation-middle-east-qatar", "allocation-middle-east-other-middle-east"],
            "mechanism": "hydrocarbon activity, trade, aviation, logistics and services",
            "tier": "2_to_3_and_3", "order": "1_conflict_damage_and_service_disruption",
            "evidence": ["mena-iraq-kuwait-qatar", "mena-iran", "mena-aviation-tourism"],
        },
        {
            "id": "gulf-diversified", "geography": "Saudi Arabia / United Arab Emirates",
            "rows": ["allocation-middle-east-saudi-arabia", "allocation-middle-east-united-arab-emirates"],
            "mechanism": "refinery/output, aviation and service activity",
            "tier": "2_to_3", "order": "2_bypass_cushion_but_activity_drag",
            "evidence": ["mena-saudi-uae", "mena-aviation-tourism"],
        },
        {
            "id": "india-mixed", "geography": "India", "rows": ["exact-country-india"],
            "mechanism": "cooking LPG, industrial feedstocks and discretionary mobility",
            "tier": "1_to_3_mixed", "order": "1_lpg_and_feedstock_constraints",
            "evidence": ["india-installed-switching", "india-lpg-cooking", "india-industrial-feedstock"],
        },
        {
            "id": "southeast-asia", "geography": "Indonesia / Thailand / Malaysia / Singapore / Viet Nam / Philippines",
            "rows": ["allocation-asia-and-oceania-indonesia", "allocation-asia-and-oceania-thailand", "allocation-asia-and-oceania-malaysia", "allocation-asia-and-oceania-singapore", "allocation-asia-and-oceania-vietnam", "allocation-asia-and-oceania-philippines"],
            "mechanism": "biofuel/transit switching, telework, travel cuts and fishing fuel",
            "tier": "1_to_3_mixed", "order": "2_installed_options_then_fragile_livelihoods",
            "evidence": ["sea-indonesia-biofuel", "sea-thailand-public-sector-travel", "sea-malaysia-telework-travel", "sea-singapore-public-transit", "sea-vietnam-realized-demand", "sea-philippines-fishing"],
        },
        {
            "id": "other-asia-oceania", "geography": "Taiwan / Australia / other Asia and Oceania",
            "rows": ["allocation-asia-and-oceania-taiwan", "allocation-asia-and-oceania-australia", "allocation-asia-and-oceania-other-asia-and-oceania"],
            "mechanism": "unresolved transport and industrial oil uses",
            "tier": "unknown", "order": "3_data_gap_not_low_cost_evidence",
            "evidence": [],
        },
        {
            "id": "africa-import-pressure", "geography": "Egypt / Kenya / Nigeria / South Africa / Algeria / other Africa",
            "rows": ["allocation-africa-egypt", "allocation-africa-kenya", "allocation-africa-nigeria", "allocation-africa-south-africa", "allocation-africa-algeria", "allocation-africa-other-africa"],
            "mechanism": "freight and food distribution, mobility, retail activity and cooking LPG",
            "tier": "2_to_3_and_3", "order": "1_small_barrels_high_essential_service_cost",
            "evidence": ["africa-egypt-conservation", "africa-transport-food", "africa-kenya-lpg"],
        },
        {
            "id": "other-positive-regions", "geography": "Europe / Eurasia / Central and South America",
            "rows": ["exact-region-europe", "exact-region-eurasia", "exact-region-central-and-south-america"],
            "mechanism": "aviation, refining, transport and heterogeneous regional adjustment",
            "tier": "1_to_3_mixed", "order": "3_more_diversified_but_aviation_and_refining_exposed",
            "evidence": ["europe-installed-switching", "europe-aviation", "eurasia-russia-refining"],
        },
    ]
    positive_total = sum(
        sum(number(t10, row_id, "value_base_million_bbl") for row_id in cluster["rows"])
        for cluster in clusters
    )
    expected_positive = current_volume - number(
        t10, "exact-region-north-america", "value_base_million_bbl"
    )
    if abs(positive_total - expected_positive) > 1e-5:
        raise ValueError(f"Positive cluster closure failed: {positive_total} != {expected_positive}")

    scenario_consequences = {
        1.25: (
            "The extra 0.9 mb/d is still of tier-2 scale, but installed switching is already bounded. "
            "The marginal burden is therefore more refinery/petrochemical throughput, aviation and discretionary mobility loss, with tier-3 LPG and livelihood pockets widening."
        ),
        1.50: (
            "The extra 1.8 mb/d is too large to describe as efficiency alone. Industrial and service cuts deepen in Northeast Asia and the Gulf while rationing, cooking-fuel substitution and freight/food stress spread in import-dependent economies."
        ),
        2.00: (
            "The extra 3.6 mb/d equals the entire March-June adjustment again. It plausibly requires broad transport and industrial contraction plus materially more tier-3 essential-service failure, not merely additional voluntary conservation."
        ),
    }

    for multiplier in SCENARIO_MULTIPLIERS:
        scenario = f"demand_{multiplier:.2f}x"
        scenario_rate = current_rate * multiplier
        increment = scenario_rate - current_rate
        headline_id = f"scenario-{multiplier:.2f}x"
        rows.append(outrow(
            row_id=headline_id, record_type="scenario_headline", scenario=scenario,
            multiplier=multiplier, parent_row_id="historical-demand-baseline",
            current_demand_reduction_mb_d=current_rate,
            scenario_demand_reduction_mb_d=scenario_rate,
            incremental_demand_reduction_mb_d=increment,
            incremental_non_demand_low_mb_d=headroom_low,
            incremental_non_demand_base_mb_d=headroom_base,
            incremental_non_demand_high_mb_d=headroom_high,
            residual_increment_low_mb_d=max(0.0, increment - headroom_low),
            residual_increment_base_mb_d=max(0.0, increment - headroom_base),
            residual_increment_high_mb_d=max(0.0, increment - headroom_high),
            channel="demand adjustment", geography="World", sector_or_mechanism="scenario total",
            headroom_status="stock_rate_expansion_unknown_not_credited",
            exhaustion_or_bound_date="no single usable-stock exhaustion date",
            bound_type="illustrative_demand_scaling_not_forecast",
            evidence_status="scenario arithmetic anchored to p2k.10",
            confidence="high_arithmetic_low_scenario",
            source_row_ids="p2k.10 exact-world | p2k.7/p2k.9 incremental-headroom inputs",
            source_urls=t10["exact-world"]["source_url"],
            method="Scale 439.228/122 mb/d; subtract only the 0/0.053/0.702 mb/d identified incremental non-demand flow envelope.",
            interpretation=(f"Demand reduction rises from {current_rate:.3f} to {scenario_rate:.3f} mb/d, "
                            f"an increment of {increment:.3f} mb/d."),
            consequences=scenario_consequences[multiplier],
            caveat="Unknown additional stock draw-rate capability could reduce the increment, but no defensible global rate headroom is published.",
            non_additivity_rule="Landing rows are nested continuity benchmarks and sum to this increment; headroom component rows are separate.",
        ))
        rows.append(outrow(
            row_id=f"{headline_id}-stock-stop-sensitivity",
            record_type="stock_flow_stop_sensitivity", scenario=f"{scenario}_plus_stock_flow_loss",
            multiplier=multiplier, parent_row_id=headline_id,
            current_demand_reduction_mb_d=current_rate,
            scenario_demand_reduction_mb_d=scenario_rate + iea_release_rate,
            incremental_demand_reduction_mb_d=increment + iea_release_rate,
            ongoing_absorber_flow_mb_d=iea_release_rate,
            channel="demand adjustment replacing stock flow", geography="World",
            sector_or_mechanism="mechanical loss of a collective-release flow equal to the historical average",
            headroom_status="sensitivity_only_no_committed_forward_stock_rate",
            exhaustion_or_bound_date="unknown; no usable-stock exhaustion date identified",
            bound_type="mechanical_flow_substitution_not_forecast",
            evidence_status="scenario calculation using p2k.8 historical average rate",
            confidence="high_arithmetic_low_scenario",
            source_row_ids="p2k.8 iea-government-zero-arithmetic-average-release-rate",
            source_urls=t8["iea-government-zero-arithmetic-average-release-rate"]["source_url"],
            method="Add 2.197 mb/d to required demand adjustment if a same-sized future stock flow is present and then disappears, all else equal.",
            interpretation=(f"Loss of a {iea_release_rate:.3f} mb/d stock flow would raise this "
                            f"scenario's demand requirement to {scenario_rate + iea_release_rate:.3f} mb/d."),
            consequences="This is why stock durability is different from bypass durability: cessation creates a new flow hole even if the original demand cuts persist.",
            caveat="The 2.197 mb/d is 290/132 historical average execution, not evidence that the same rate is continuing or committed.",
            non_additivity_rule="Sensitivity branching from the headline; do not add to the scenario or landing rows.",
        ))

        allocated = 0.0
        for cluster in clusters:
            volume = sum(number(t10, row_id, "value_base_million_bbl") for row_id in cluster["rows"])
            share = volume / positive_total
            benchmark = increment * share
            allocated += benchmark
            evidence_ids = cluster["evidence"]
            urls = source_urls(t3, evidence_ids) if evidence_ids else ""
            rows.append(outrow(
                row_id=f"{headline_id}-{cluster['id']}", record_type="country_sector_landing",
                scenario=scenario, multiplier=multiplier, parent_row_id=headline_id,
                current_demand_reduction_mb_d=current_rate,
                scenario_demand_reduction_mb_d=scenario_rate,
                incremental_demand_reduction_mb_d=increment,
                channel="demand adjustment", geography=cluster["geography"],
                sector_or_mechanism=cluster["mechanism"], historical_gap_million_bbl=volume,
                historical_positive_gap_share_pct=share * 100,
                continuity_benchmark_increment_mb_d=benchmark,
                current_cost_tier=cluster["tier"], pressure_order=cluster["order"],
                evidence_status="p2k.10 gap allocation plus p2k.3 mechanism evidence",
                confidence="low_for_landing_medium_for_direction",
                source_row_ids=("p2k.10 " + " | ".join(cluster["rows"]) +
                                (("; p2k.3 " + " | ".join(evidence_ids)) if evidence_ids else "")),
                source_urls=urls,
                method="Allocate the global increment pro rata to positive current-gap clusters as a continuity benchmark only.",
                interpretation=(f"Mechanical continuity benchmark: {benchmark:.3f} mb/d of the "
                                f"{increment:.3f} mb/d increment; marginal pressure is classified separately."),
                consequences=scenario_consequences[multiplier],
                caveat="This number is not a country forecast; p2k.10 includes low-fidelity neutral-share allocations and the true marginal distribution will tilt toward constrained tier-2/3 uses.",
                non_additivity_rule="Nested in the scenario headline; cluster rows sum to the scenario increment.",
            ))
        if abs(allocated - increment) > 1e-9:
            raise ValueError(f"Scenario allocation closure failed for {multiplier}")

    candidate_rows = [
        ("india", "India", "cooking LPG and industrial feedstocks", "india-lpg-cooking | india-industrial-feedstock", "Already tier 3 for LPG because import dependence is high and household cooking has limited fast substitutes."),
        ("kenya", "Kenya and LPG-dependent African households", "cooking LPG, charcoal/firewood reversion", "africa-kenya-lpg", "Observed scarcity and fuel reversion make essential household energy, health and environmental costs the failure margin."),
        ("myanmar", "Myanmar", "fuel rationing and even-odd licence plates", "sea-myanmar-rationing", "Rationing is direct evidence that voluntary efficiency has given way to administrative scarcity."),
        ("laos", "Lao PDR", "school and work schedules", "sea-laos-school-shifts", "A three-day school week and rotating shifts show fuel scarcity spilling into essential public services."),
        ("philippines", "Philippines", "small-scale fishing livelihoods", "sea-philippines-fishing", "Shorter and fewer fishing trips show a direct food-supply and income margin even when national barrel totals are small."),
        ("fragile-gulf", "Iran / Iraq / Kuwait / Qatar", "hydrocarbon, aviation, trade and service disruption", "mena-iraq-kuwait-qatar | mena-iran | mena-aviation-tourism", "Conflict and infrastructure exposure put output and services at tier 3 before an economy-wide statistical demand series can identify the barrels."),
        ("northeast-asia", "China / Japan / South Korea", "refining and naphtha-fed petrochemicals", "china-refinery-petrochemical | japan-naphtha-refining | korea-petrochemical-refining", "Current tier-2 cuts are already deep; further sustained throughput loss is the clearest large-volume transition toward tier 3."),
    ]
    for slug, geography, mechanism, ids_text, interpretation in candidate_rows:
        ids = ids_text.split(" | ")
        rows.append(outrow(
            row_id=f"tier3-candidate-{slug}", record_type="tier3_transition_candidate",
            scenario="continued_disruption_marginal_pressure", channel="demand adjustment",
            geography=geography, sector_or_mechanism=mechanism, current_cost_tier="3_or_transition_to_3",
            pressure_order="priority_watch", evidence_status="realized policy or activity evidence",
            confidence="medium_for_direction_not_barrels", source_row_ids="p2k.3 " + ids_text,
            source_urls=source_urls(t3, ids),
            method="Name candidates only where p2k.3 contains a realized scarcity, service, livelihood or deep industrial-cut signal.",
            interpretation=interpretation,
            caveat="Candidate status does not quantify a future country barrel contribution.",
            non_additivity_rule="Qualitative watchlist; not part of the scenario arithmetic.",
        ))

    if len({row["row_id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate output row_id")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
