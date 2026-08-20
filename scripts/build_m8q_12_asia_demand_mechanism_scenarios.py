#!/usr/bin/env python3
"""Build speculative Asia/Oceania oil-demand mechanism scenarios for m8q.12.

The February-to-July STEO demand gaps are measured forecast-vintage revisions.
Everything below the geography totals is a deliberately low-fidelity allocation,
not an econometric causal estimate.  Each scenario column closes exactly.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_12_asia_demand_mechanism_scenarios.csv"

FIELDS = [
    "row_id", "accounting_view", "record_type", "geography", "parent_geography",
    "period_start", "period_end", "mechanism", "value_low_scenario",
    "value_base_scenario", "value_high_scenario", "unit", "low_scenario_definition",
    "base_scenario_definition", "high_scenario_definition", "causal_type",
    "policy_attribution", "confidence", "source_url", "evidence_and_method",
    "counterargument", "double_counting_rule",
]

EIA_VINTAGES = (
    "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx | "
    "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
)

LOW_DEF = (
    "Low incremental switching: more of the forecast-vintage gap is forced shortage, "
    "lost activity, or ordinary revision; Korea is 7.65 million barrels of the Asian residual."
)
BASE_DEF = (
    "Preferred narrative allocation: mixed feedstock shortage, price response, activity loss, "
    "and limited incremental switching; Korea is 30.60 million barrels of the Asian residual."
)
HIGH_DEF = (
    "High incremental switching/conservation: faster behavioral and technology response; "
    "Korea is 61.20 million barrels of the Asian residual."
)

TOTALS = {
    "China": (119.992047, 119.992047, 119.992047),
    "India": (41.140711, 41.140711, 41.140711),
    "Japan": (19.521871, 19.521871, 19.521871),
    "South Korea (bounded suballocation)": (7.65, 30.60, 61.20),
    "Other Asia and Oceania ex South Korea": (138.595724, 115.645724, 85.045724),
}

# Percentages are scenario allocations, not probability distributions.  Every
# geography/scenario column sums to 100%.  "Other" changes because Korea is a
# bounded suballocation of a fixed 146.245724 million-barrel residual.
MECHANISM_SHARES = {
    "China": {
        "incremental_fuel_switching_and_electrification": (8, 20, 35),
        "voluntary_conservation_and_efficiency": (12, 20, 22),
        "forced_shortage_refinery_and_feedstock_constraints": (40, 30, 20),
        "activity_loss_and_macroeconomic_feedback": (20, 15, 10),
        "structural_trend_and_forecast_revision": (15, 10, 8),
        "unresolved_residual": (5, 5, 5),
    },
    "India": {
        "incremental_fuel_switching_and_electrification": (3, 8, 15),
        "voluntary_conservation_and_efficiency": (7, 10, 15),
        "forced_shortage_refinery_and_feedstock_constraints": (22, 18, 14),
        "activity_loss_and_macroeconomic_feedback": (25, 25, 22),
        "structural_trend_and_forecast_revision": (38, 32, 29),
        "unresolved_residual": (5, 7, 5),
    },
    "Japan": {
        "incremental_fuel_switching_and_electrification": (3, 8, 18),
        "voluntary_conservation_and_efficiency": (8, 12, 18),
        "forced_shortage_refinery_and_feedstock_constraints": (55, 45, 32),
        "activity_loss_and_macroeconomic_feedback": (12, 15, 12),
        "structural_trend_and_forecast_revision": (17, 15, 15),
        "unresolved_residual": (5, 5, 5),
    },
    "South Korea (bounded suballocation)": {
        "incremental_fuel_switching_and_electrification": (2, 5, 12),
        "voluntary_conservation_and_efficiency": (5, 8, 15),
        "forced_shortage_refinery_and_feedstock_constraints": (55, 45, 35),
        "activity_loss_and_macroeconomic_feedback": (15, 18, 18),
        "structural_trend_and_forecast_revision": (18, 19, 15),
        "unresolved_residual": (5, 5, 5),
    },
    "Other Asia and Oceania ex South Korea": {
        "incremental_fuel_switching_and_electrification": (3, 8, 18),
        "voluntary_conservation_and_efficiency": (10, 17, 22),
        "forced_shortage_refinery_and_feedstock_constraints": (40, 30, 22),
        "activity_loss_and_macroeconomic_feedback": (20, 20, 18),
        "structural_trend_and_forecast_revision": (22, 20, 15),
        "unresolved_residual": (5, 5, 5),
    },
}

POLICY_SHARES = {
    "China": {
        "explicit_policy_direct_demand_restraint": (1, 5, 10),
        "decentralized_market_and_household_response": (20, 35, 50),
        "forced_supply_and_industrial_constraint": (50, 35, 25),
        "noncausal_revision_structural_trend_and_unknown": (29, 25, 15),
    },
    "India": {
        "explicit_policy_direct_demand_restraint": (1, 5, 10),
        "decentralized_market_and_household_response": (15, 25, 35),
        "forced_supply_and_industrial_constraint": (30, 25, 20),
        "noncausal_revision_structural_trend_and_unknown": (54, 45, 35),
    },
    "Japan": {
        "explicit_policy_direct_demand_restraint": (0, 2, 5),
        "decentralized_market_and_household_response": (10, 20, 30),
        "forced_supply_and_industrial_constraint": (60, 50, 40),
        "noncausal_revision_structural_trend_and_unknown": (30, 28, 25),
    },
    "South Korea (bounded suballocation)": {
        "explicit_policy_direct_demand_restraint": (0, 3, 7),
        "decentralized_market_and_household_response": (8, 15, 25),
        "forced_supply_and_industrial_constraint": (65, 55, 45),
        "noncausal_revision_structural_trend_and_unknown": (27, 27, 23),
    },
    "Other Asia and Oceania ex South Korea": {
        "explicit_policy_direct_demand_restraint": (10, 20, 30),
        "decentralized_market_and_household_response": (15, 25, 35),
        "forced_supply_and_industrial_constraint": (45, 30, 20),
        "noncausal_revision_structural_trend_and_unknown": (30, 25, 15),
    },
}

MECHANISM_META = {
    "incremental_fuel_switching_and_electrification": (
        "mixed_policy_and_decentralized", "low",
        "Includes only acceleration beyond the February forecast: extra EV/LNG-truck mileage, public transport, biofuel blending, or substitution away from oil-fired uses.",
        "Most EV, renewable, nuclear and biofuel adoption was already in the February path; power-sector renewables usually displace coal or gas, not oil.",
    ),
    "voluntary_conservation_and_efficiency": (
        "mostly_decentralized_price_response_with_some_campaigns", "low_medium",
        "Less discretionary driving/flying, carpooling, telework, slower speeds, and operational efficiency caused by prices or appeals.",
        "Price caps, subsidies and tax relief muted incentives in China, Japan, Korea and parts of Southeast Asia.",
    ),
    "forced_shortage_refinery_and_feedstock_constraints": (
        "not_voluntary", "medium",
        "Unavailable crude, naphtha, LPG or jet fuel reduces refinery, cracker and end-user deliveries; especially important in Northeast Asian petrochemicals.",
        "Lower refinery runs are not automatically lower final demand when product inventories, imports, or export cuts bridge the gap.",
    ),
    "activity_loss_and_macroeconomic_feedback": (
        "decentralized_and_indirect", "low_medium",
        "Reduced trucking, aviation, construction, manufacturing and household activity as fuel/feedstock costs propagate through the economy.",
        "Some activity weakness would have happened without Hormuz and therefore belongs in forecast revision rather than causal destruction.",
    ),
    "structural_trend_and_forecast_revision": (
        "not_incremental_crisis_policy", "low",
        "Ordinary vintage changes, weather, seasonality and structural EV/efficiency trends not cleanly identified as a post-February response.",
        "The July vintage may correctly incorporate crisis effects that cannot be separately observed; this bucket is a caution, not dismissal.",
    ),
    "unresolved_residual": (
        "unknown", "low",
        "Explicit residual retained because product balances and causal evidence cannot identify every barrel.",
        "May conceal any of the named mechanisms; it is not an independent physical process.",
    ),
}

POLICY_META = {
    "explicit_policy_direct_demand_restraint": (
        "direct_policy", "low_medium",
        "Government telework, carpool/public-transport, travel-reduction, rationing, fuel-purchase control, or emergency conservation measures.",
        "Announcements and policy counts do not reveal realized barrels; some policies began too late to explain March-April.",
    ),
    "decentralized_market_and_household_response": (
        "decentralized", "low",
        "Price-driven household and firm decisions, plus autonomous switching using equipment already installed.",
        "Consumer subsidies and price caps suppress this channel; supply constraints can be mistaken for voluntary response.",
    ),
    "forced_supply_and_industrial_constraint": (
        "not_voluntary", "medium",
        "Refinery/feedstock scarcity, rationing, curtailed aviation or industrial output, and downstream shortages.",
        "Export suppression and inventories can protect domestic end users even while refinery imports collapse.",
    ),
    "noncausal_revision_structural_trend_and_unknown": (
        "not_identified", "low",
        "Forecast error, ordinary macro/weather revision, pre-existing structural trends, and unallocated residual.",
        "Some true crisis response is inevitably swept into this bucket because public data are incomplete.",
    ),
}

SOURCES = {
    "China": (
        "https://www.eia.gov/international/content/analysis/countries_long/China/ | "
        "https://www.spglobal.com/energy/en/news-research/latest-news/shipping/052926-china-may-extend-refining-run-cuts-in-june-amid-tight-supply-low-demand | "
        "https://en.ndrc.gov.cn/news/mediarusources/202506/t20250626_1404387.html | "
        "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2"
    ),
    "India": (
        "https://www.eia.gov/international/content/analysis/countries_long/India/ | "
        "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2239794&lang=1&reg=3 | "
        "https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=289939 | "
        "https://www.marketscreener.com/news/india-s-fuel-demand-outlook-hit-by-price-hikes-slowing-industrial-activity-ce7f5ddfdb8ff52c"
    ),
    "Japan": (
        "https://www.eia.gov/international/content/analysis/countries_long/Japan/ | "
        "https://www.sahmcapital.com/news/content/update-1-japans-april-oil-imports-fall-nearly-66-yy-as-iran-war-disrupts-supply-2026-05-29 | "
        "https://www.dir.co.jp/english/research/report/analysis/20260707_025886.html | "
        "https://www.enecho.meti.go.jp/category/gekihen_lp/"
    ),
    "South Korea (bounded suballocation)": (
        "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2 | "
        "https://www.spglobal.com/energy/en/news-research/latest-news/refined-products/040826-south-korean-govt-secures-110-mil-barrels-of-crude-for-april-may-amid-hormuz-disruptions | "
        "https://apnews.com/article/south-korea-oil-tanker-iran-hormuz-03228f42ac32c0bfce3bab744a77d199 | "
        "https://www.iea.org/articles/korea-oil-security-policy"
    ),
    "Other Asia and Oceania ex South Korea": (
        "https://www.iea.org/reports/southeast-asia-energy-outlook-2026/southeast-asia-s-energy-challenges-and-emerging-opportunities | "
        "https://www.spglobal.com/energy/en/news-research/special-reports/chemicals/emerging-stronger-apic-2026/asia-petrochemicals-face-middle-east-war-challenges | "
        "https://www.iea.org/reports/oil-market-report-may-2026"
    ),
}


def fmt(value: float) -> str:
    return f"{value:.6f}"


def allocation_row(view: str, geography: str, mechanism: str,
                   values: tuple[float, float, float], meta: tuple[str, str, str, str]) -> dict[str, str]:
    causal_type, confidence, evidence, counterargument = meta
    return {
        "row_id": f"{view}-{geography}-{mechanism}".lower().replace(" ", "_").replace("(", "").replace(")", ""),
        "accounting_view": view,
        "record_type": "speculative_allocation",
        "geography": geography,
        "parent_geography": "Asia and Oceania",
        "period_start": "2026-03-01",
        "period_end": "2026-07-31",
        "mechanism": mechanism,
        "value_low_scenario": fmt(values[0]),
        "value_base_scenario": fmt(values[1]),
        "value_high_scenario": fmt(values[2]),
        "unit": "million_bbl",
        "low_scenario_definition": LOW_DEF,
        "base_scenario_definition": BASE_DEF,
        "high_scenario_definition": HIGH_DEF,
        "causal_type": causal_type,
        "policy_attribution": causal_type,
        "confidence": confidence,
        "source_url": f"{EIA_VINTAGES} | {SOURCES.get(geography, '')}".rstrip(" |"),
        "evidence_and_method": evidence,
        "counterargument": counterargument,
        "double_counting_rule": "Alternative allocations within this accounting view close to the geography total; do not add mechanism and policy-overlay views.",
    }


def build_view(view: str, shares: dict[str, dict[str, tuple[int, int, int]]],
               metadata: dict[str, tuple[str, str, str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for geography, mechanisms in shares.items():
        totals = TOTALS[geography]
        for scenario_index in range(3):
            if sum(percentages[scenario_index] for percentages in mechanisms.values()) != 100:
                raise ValueError(f"{view} shares do not close: {geography}, scenario {scenario_index}")
        mechanism_names = list(mechanisms)
        calculated: dict[str, list[float]] = {
            mechanism: [totals[i] * percentages[i] / 100 for i in range(3)]
            for mechanism, percentages in mechanisms.items()
        }
        # Make the final row an exact six-decimal remainder so the CSV itself,
        # not merely the unrounded calculation, closes to the denominator.
        final_mechanism = mechanism_names[-1]
        for scenario_index in range(3):
            rounded_others = sum(
                float(fmt(calculated[mechanism][scenario_index]))
                for mechanism in mechanism_names[:-1]
            )
            calculated[final_mechanism][scenario_index] = totals[scenario_index] - rounded_others
        for mechanism in mechanism_names:
            rows.append(allocation_row(
                view, geography, mechanism, tuple(calculated[mechanism]), metadata[mechanism]
            ))

    # Asia aggregate is generated, not independently assumed, and therefore
    # provides a direct audit of all nested rows.
    for mechanism in next(iter(shares.values())):
        child_rows = [r for r in rows if r["mechanism"] == mechanism]
        values = tuple(sum(float(r[field]) for r in child_rows) for field in (
            "value_low_scenario", "value_base_scenario", "value_high_scenario"
        ))
        aggregate = allocation_row(view, "Asia and Oceania", mechanism, values, metadata[mechanism])
        aggregate["record_type"] = "derived_region_aggregate"
        aggregate["parent_geography"] = "World"
        aggregate["source_url"] = EIA_VINTAGES
        aggregate["evidence_and_method"] = "Sum of the five mutually exclusive Asia/Oceania child geographies in this scenario column."
        rows.append(aggregate)
    return rows


def total_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    totals = {**TOTALS, "Asia and Oceania": (326.900353, 326.900353, 326.900353)}
    for geography, values in totals.items():
        rows.append({
            "row_id": f"measured-gap-{geography}".lower().replace(" ", "_").replace("(", "").replace(")", ""),
            "accounting_view": "measured_gap_denominator",
            "record_type": "denominator",
            "geography": geography,
            "parent_geography": "World" if geography == "Asia and Oceania" else "Asia and Oceania",
            "period_start": "2026-03-01", "period_end": "2026-07-31",
            "mechanism": "consumption_below_frozen_february_forecast",
            "value_low_scenario": fmt(values[0]), "value_base_scenario": fmt(values[1]),
            "value_high_scenario": fmt(values[2]), "unit": "million_bbl",
            "low_scenario_definition": LOW_DEF, "base_scenario_definition": BASE_DEF,
            "high_scenario_definition": HIGH_DEF, "causal_type": "forecast_vintage_revision",
            "policy_attribution": "not_identified", "confidence": "medium_high_arithmetic_low_causal",
            "source_url": EIA_VINTAGES,
            "evidence_and_method": "Frozen February STEO minus July STEO consumption, integrated over March-July calendar days; July is forecast.",
            "counterargument": "The revision includes crisis response, normal forecast error, weather, macro changes and structural trends.",
            "double_counting_rule": "China, India, Japan, Korea and Other Asia/Oceania are nested within the region. Korea is a bounded candidate suballocation of the fixed residual.",
        })
    return rows


def build() -> list[dict[str, str]]:
    rows = total_rows()
    rows += build_view("mechanism_allocation", MECHANISM_SHARES, MECHANISM_META)
    rows += build_view("policy_attribution_overlay", POLICY_SHARES, POLICY_META)

    # Validate exact closure (within CSV precision) for every geography/view.
    for view in ("mechanism_allocation", "policy_attribution_overlay"):
        for geography, totals in {**TOTALS, "Asia and Oceania": (326.900353,) * 3}.items():
            subset = [r for r in rows if r["accounting_view"] == view and r["geography"] == geography]
            for index, field in enumerate(("value_low_scenario", "value_base_scenario", "value_high_scenario")):
                difference = sum(float(r[field]) for r in subset) - totals[index]
                if abs(difference) > 5e-6:
                    raise ValueError(f"{view} does not close for {geography} {field}: {difference}")
    row_ids = [r["row_id"] for r in rows]
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("Duplicate row IDs")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
