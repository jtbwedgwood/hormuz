#!/usr/bin/env python3
"""Build August-vintage regional/country demand splits and mechanism tables.

The measured quantities are frozen-February minus August STEO consumption.
Mechanism rows are explicitly scenarios: they allocate, but do not identify, the
measured vintage gaps.  Positive demand gaps mean consumption below the frozen
path; negative gaps mean consumption above it.
"""

from __future__ import annotations

import calendar
import csv
from pathlib import Path

from build_a4d_2_august_steo_comparison import AUG_URL, FEB_URL, download, workbook_rows
from build_m8q_12_asia_demand_mechanism_scenarios import POLICY_SHARES
from build_m8q_13_non_asia_demand_mechanisms import mechanism_allocations

ROOT = Path(__file__).resolve().parents[1]
ASIA_OUT = ROOT / "data/derived/hormuz_m8q_12_asia_demand_mechanism_scenarios.csv"
NONASIA_OUT = ROOT / "data/derived/hormuz_m8q_13_non_asia_demand_mechanisms.csv"
BLOG_OUT = ROOT / "data/derived/hormuz_a4d_8_demand_splits_blog_table.csv"

MONTHS = {
    "2026-03": ("BA", 31), "2026-04": ("BB", 30), "2026-05": ("BC", 31),
    "2026-06": ("BD", 30), "2026-07": ("BE", 31),
}
FRAMES = {"march_june": list(MONTHS)[:4], "march_july": list(MONTHS)}
REGIONS = {
    "North America": "patc_r01", "Central and South America": "patc_r02",
    "Europe": "patc_r03", "Eurasia": "patc_r04", "Middle East": "patc_r05",
    "Africa": "patc_r06", "Asia and Oceania": "patc_r07",
}
COUNTRIES = {
    "United States": "patc_us", "Canada": "patc_ca", "Mexico": "patc_mx",
    "Brazil": "patc_br", "Russia": "patc_rs", "China": "patc_ch",
    "India": "patc_in", "Japan": "patc_ja",
}
WORLD = "patc_world"
EIA_SOURCES = f"{FEB_URL} | {AUG_URL}"

ASIA_FIELDS = [
    "row_id", "accounting_view", "record_type", "frame", "geography",
    "parent_geography", "period_start", "period_end", "mechanism",
    "value_low_scenario", "value_base_scenario", "value_high_scenario", "unit",
    "causal_type", "confidence", "source_url", "evidence_and_method",
    "counterargument", "double_counting_rule",
]
NONASIA_FIELDS = [
    "row_id", "record_type", "frame", "region", "geography", "period_start",
    "period_end", "scenario_case", "mechanism", "allocation_million_bbl",
    "regional_gap_million_bbl", "share_of_absolute_region_gap_pct", "unit",
    "evidence_status", "confidence", "source_url", "method", "interpretation",
    "overlap_rule",
]
BLOG_FIELDS = [
    "row_id", "record_type", "frame", "geography", "parent_geography",
    "period_start", "period_end", "days", "metric", "value", "unit",
    "frozen_february_demand_mb_d", "share_of_frozen_february_period_demand_pct",
    "prewar_2024_demand_mb_d", "share_of_prewar_2024_period_demand_pct",
    "data_status", "source_url", "method", "interpretation", "confidence", "caveat",
]

PREWAR_2024 = {"Middle East": 8.854, "India": 5.5}
OPEC_ASB = "https://www.opec.org/assets/assetdb/asb-2025.pdf"

CLASS_ORDER = [
    "explicit_government_demand_restraint",
    "decentralized_response_and_rapid_switching",
    "forced_supply_refinery_feedstock_and_activity_constraint",
    "structural_ordinary_revision_and_unknown",
]
ASIA_CLASS_MAP = {
    "explicit_policy_direct_demand_restraint": CLASS_ORDER[0],
    "decentralized_market_and_household_response": CLASS_ORDER[1],
    "forced_supply_and_industrial_constraint": CLASS_ORDER[2],
    "noncausal_revision_structural_trend_and_unknown": CLASS_ORDER[3],
}

NBS_RUNS = {
    "2026-04": (54.65, -5.8, "https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html"),
    "2026-05": (53.72, -9.1, "https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html"),
    "2026-06": (51.24, -17.7, "https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html"),
}
NBS_CALENDAR = "https://www.stats.gov.cn/english/PressRelease/ReleaseCalendar/202512/t20251226_1962154.html"
EXPORT_SOURCE = "https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d"


def f(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def bounds(frame: str) -> tuple[list[str], str, str, int]:
    months = FRAMES[frame]
    days = sum(MONTHS[m][1] for m in months)
    return months, "2026-03-01", f"{months[-1]}-{MONTHS[months[-1]][1]:02d}", days


def measured(feb: dict[str, dict[str, str]], aug: dict[str, dict[str, str]], mnemonic: str, frame: str) -> tuple[float, float]:
    months, _, _, days = bounds(frame)
    gap = sum((float(feb[mnemonic][MONTHS[m][0]]) - float(aug[mnemonic][MONTHS[m][0]])) * MONTHS[m][1] for m in months)
    denominator = sum(float(feb[mnemonic][MONTHS[m][0]]) * MONTHS[m][1] for m in months) / days
    return gap, denominator


def asia_totals(feb: dict[str, dict[str, str]], aug: dict[str, dict[str, str]], frame: str) -> dict[str, tuple[float, float, float]]:
    totals = {name: (measured(feb, aug, mnemonic, frame)[0],) * 3 for name, mnemonic in {"China": "patc_ch", "India": "patc_in", "Japan": "patc_ja"}.items()}
    _, _, _, days = bounds(frame)
    korea = (0.05 * days, 0.20 * days, 0.40 * days)
    totals["South Korea (bounded suballocation)"] = korea
    region = measured(feb, aug, REGIONS["Asia and Oceania"], frame)[0]
    named = [totals[x][0] for x in ("China", "India", "Japan")]
    totals["Other Asia and Oceania ex South Korea"] = tuple(region - sum(named) - value for value in korea)
    totals["Asia and Oceania"] = (region,) * 3
    return totals


def build_asia(feb: dict[str, dict[str, str]], aug: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for frame in FRAMES:
        _, start, end, _ = bounds(frame)
        totals = asia_totals(feb, aug, frame)
        for geography, values in totals.items():
            rows.append(dict(zip(ASIA_FIELDS, [
                f"{frame}-denominator-{geography.lower().replace(' ', '-')}", "measured_gap_denominator", "denominator", frame,
                geography, "World" if geography == "Asia and Oceania" else "Asia and Oceania", start, end,
                "consumption_below_frozen_february_forecast", *(f(x) for x in values), "million_bbl",
                "forecast_vintage_revision", "medium_high_arithmetic_low_causal", EIA_SOURCES,
                "Frozen February minus August STEO consumption integrated by calendar days. Korea alone is a bounded 0.05/0.20/0.40 mb/d suballocation; Other Asia is the exact residual.",
                "The revision includes crisis response, forecast error, weather, macro changes and structural trends.",
                "Country rows nest within Asia/Oceania; Korea is not an EIA observation.",
            ], strict=True)))
        for geography in [x for x in totals if x != "Asia and Oceania"]:
            mechanisms = POLICY_SHARES[geography]
            values = totals[geography]
            for mechanism, pcts in mechanisms.items():
                allocations = [values[i] * pcts[i] / 100 for i in range(3)]
                rows.append(dict(zip(ASIA_FIELDS, [
                    f"{frame}-{geography.lower().replace(' ', '-')}-{mechanism}", "policy_attribution_overlay", "speculative_allocation", frame,
                    geography, "Asia and Oceania", start, end, ASIA_CLASS_MAP[mechanism], *(f(x) for x in allocations), "million_bbl",
                    "scenario_not_identification", "low", EIA_SOURCES,
                    "Reuses the documented low/base/high policy-attribution percentages and applies them to the August-vintage geography denominator.",
                    "Public evidence does not identify causal barrel shares.", "Mutually exclusive within a scenario; never add low/base/high or add this overlay to another mechanism view.",
                ], strict=True)))
        for mechanism in CLASS_ORDER:
            values = tuple(sum(float(r[column]) for r in rows if r["frame"] == frame and r["record_type"] == "speculative_allocation" and r["mechanism"] == mechanism)
                           for column in ("value_low_scenario", "value_base_scenario", "value_high_scenario"))
            rows.append(dict(zip(ASIA_FIELDS, [
                f"{frame}-asia-{mechanism}", "policy_attribution_overlay", "derived_region_aggregate", frame, "Asia and Oceania", "World", start, end,
                mechanism, *(f(value) for value in values), "million_bbl", "scenario_not_identification", "low", EIA_SOURCES,
                "Sum of mutually exclusive Asia/Oceania child geographies.", "Scenario allocation, not observed causation.",
                "Low/base/high are alternative allocations of the same measured regional denominator.",
            ], strict=True)))
    return rows


def nonasia_class(mechanism: str) -> str:
    low = mechanism.lower()
    if "explicit_policy" in low:
        return CLASS_ORDER[0]
    if any(token in low for token in ("autonomous", "switching", "electrification", "transport_and_fuel_price_response")):
        return CLASS_ORDER[1]
    if "forecast_model" in low or "baseline_revision" in low or "seasonality" in low:
        return CLASS_ORDER[3]
    return CLASS_ORDER[2]


def build_nonasia(feb: dict[str, dict[str, str]], aug: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    old = mechanism_allocations()
    rows: list[dict[str, str]] = []
    for frame in FRAMES:
        _, start, end, _ = bounds(frame)
        for region, mnemonic in REGIONS.items():
            if region == "Asia and Oceania":
                continue
            gap, _ = measured(feb, aug, mnemonic, frame)
            for scenario, components in old[region].items():
                old_total = sum(components.values())
                grouped = {name: 0.0 for name in CLASS_ORDER}
                if gap > 0 and region == "North America":
                    grouped[CLASS_ORDER[3]] = gap
                else:
                    for mechanism, value in components.items():
                        grouped[nonasia_class(mechanism)] += abs(gap) * value / old_total
                for mechanism in CLASS_ORDER:
                    value = grouped[mechanism]
                    rows.append(dict(zip(NONASIA_FIELDS, [
                        f"{frame}-{region.lower().replace(' ', '-')}-{scenario}-{mechanism}", "mechanism_scenario", frame, region, region, start, end,
                        scenario, mechanism, f(value), f(gap), f(100 * value / abs(gap)) if gap else "", "million_bbl",
                        "project_scenario_allocation_not_observation", "low", EIA_SOURCES,
                        "Old documented scenario proportions rescaled to the August-vintage absolute regional gap; positive/negative sign remains in regional_gap_million_bbl.",
                        "Explains lower consumption." if gap >= 0 else "Counterexample: consumption is above the frozen February path.",
                        "Classes close to the absolute regional gap within each scenario; upward-revision regions are offsets, not gross demand reduction.",
                    ], strict=True)))
    return rows


def build_blog(feb: dict[str, dict[str, str]], aug: dict[str, dict[str, str]], asia: list[dict[str, str]], nonasia: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    specs = {"World": WORLD, **REGIONS, **COUNTRIES}
    for frame in FRAMES:
        _, start, end, days = bounds(frame)
        for geography, mnemonic in specs.items():
            gap, denominator = measured(feb, aug, mnemonic, frame)
            parent = "World" if geography in {"World", *REGIONS} else next((r for r, m in [("North America", ["United States", "Canada", "Mexico"]), ("Central and South America", ["Brazil"]), ("Eurasia", ["Russia"]), ("Asia and Oceania", ["China", "India", "Japan"])] if geography in m), "World")
            rows.append(dict(zip(BLOG_FIELDS, [
                f"{frame}-demand-{geography.lower().replace(' ', '-')}", "demand_revision", frame, geography, parent, start, end, str(days),
                "consumption_below_frozen_february_forecast", f(gap), "million_bbl", f(denominator), f(100 * gap / (denominator * days)),
                f(PREWAR_2024[geography]) if geography in PREWAR_2024 else "",
                f(100 * gap / (PREWAR_2024[geography] * days)) if geography in PREWAR_2024 else "",
                "preliminary_estimates", f"{EIA_SOURCES} | {OPEC_ASB}" if geography in PREWAR_2024 else EIA_SOURCES,
                "Frozen-February minus August STEO monthly consumption times calendar days; the separate 2024 prewar anchor is from OPEC ASB 2025.",
                "Positive means lower consumption; negative means consumption above the frozen path.", "medium_high_arithmetic_low_causal",
                "Forecast-vintage revision, not a causal estimate; international values remain revisable.",
            ], strict=True)))
        totals = asia_totals(feb, aug, frame)
        for geography in ("South Korea (bounded suballocation)", "Other Asia and Oceania ex South Korea"):
            value = totals[geography][1]
            rows.append(dict(zip(BLOG_FIELDS, [
                f"{frame}-demand-{geography.lower().replace(' ', '-')}", "country_suballocation", frame, geography, "Asia and Oceania", start, end, str(days),
                "consumption_below_frozen_february_forecast", f(value), "million_bbl", "", "", "", "",
                "bounded_scenario" if "Korea" in geography else "calculated_residual", EIA_SOURCES,
                "Korea base is 0.20 mb/d times frame days; Other Asia is the exact region-minus-China-minus-India-minus-Japan-minus-Korea residual.",
                "Nested suballocation, not an EIA country observation.", "low" if "Korea" in geography else "medium_high_arithmetic_low_causal", "Do not add to the Asia/Oceania row.",
            ], strict=True)))
        downward = {region: measured(feb, aug, mnemonic, frame)[0] for region, mnemonic in REGIONS.items()}
        gross = sum(x for x in downward.values() if x > 0)
        offsets = sum(x for x in downward.values() if x < 0)
        classes = {name: 0.0 for name in CLASS_ORDER}
        for row in asia:
            if row["frame"] == frame and row["record_type"] == "derived_region_aggregate" and row["value_base_scenario"]:
                classes[row["mechanism"]] += float(row["value_base_scenario"])
        for row in nonasia:
            if row["frame"] == frame and row["scenario_case"] == "base" and float(row["regional_gap_million_bbl"]) > 0:
                classes[row["mechanism"]] += float(row["allocation_million_bbl"])
        if abs(sum(classes.values()) - gross) > 1e-5:
            raise ValueError(f"Mechanism classes do not close for {frame}: {sum(classes.values())} vs {gross}")
        for mechanism, value in classes.items():
            rows.append(dict(zip(BLOG_FIELDS, [
                f"{frame}-mechanism-{mechanism}", "mechanism_class", frame, "Gross regions with lower consumption", "World", start, end, str(days), mechanism,
                f(value), "million_bbl", "", f(100 * value / gross), "", "", "scenario_not_observation", EIA_SOURCES,
                "Cross-walk of Asia policy overlays and non-Asia base mechanism scenarios; exact gross-gap closure.",
                "Disciplined explanatory scenario, not causal identification.", "low", "Shares change with regional composition and August revisions.",
            ], strict=True)))
        for metric, value in (("gross_regions_with_lower_consumption", gross), ("regions_with_higher_consumption_offset", offsets), ("world_net_demand_gap", gross + offsets)):
            rows.append(dict(zip(BLOG_FIELDS, [
                f"{frame}-{metric}", "accounting_summary", frame, "World", "", start, end, str(days), metric, f(value), "million_bbl", "", "",
                "", "",
                "calculated", EIA_SOURCES, "Sum of the seven mutually exclusive EIA regional revisions.", "Negative offsets reduce the gross downward revision.", "high_for_arithmetic", "World row independently verifies the net.",
            ], strict=True)))
    for month, (runs, yoy, url) in NBS_RUNS.items():
        prior = runs / (1 + yoy / 100)
        shortfall = (prior - runs) * 7.33
        rows.append(dict(zip(BLOG_FIELDS, [
            f"china-nbs-runs-{month}", "china_mechanism_evidence", "monthly", "China", "Asia and Oceania", f"{month}-01", f"{month}-{calendar.monthrange(2026, int(month[-2:]))[1]:02d}",
            str(calendar.monthrange(2026, int(month[-2:]))[1]), "crude_processing_shortfall_vs_prior_year", f(shortfall), "million_bbl_equivalent", "", "",
            "", "",
            "official_observation_calculated_comparison", url, "NBS current tonnes divided by (1+y/y rate) to infer comparable prior-year tonnes; difference converted at 7.33 bbl/tonne.",
            "Observed refinery-throughput constraint, not a one-for-one measure of final oil demand.", "medium_high", "Approximate density conversion; runs, stocks, exports and final use are different balance terms.",
        ], strict=True)))
    rows.append(dict(zip(BLOG_FIELDS, [
        "china-product-export-controls-march-june", "china_mechanism_evidence", "march_june", "China", "Asia and Oceania", "2026-03-01", "2026-06-30", "122",
        "broad_refined_product_exports_retained_vs_2025_base_estimate", "35.226", "million_bbl_equivalent", "", "", "", "",
        "customs_data_reported_by_reuters_derived_sources", EXPORT_SOURCE,
        "Existing p2k.4 customs reconstruction: March-May reported declines plus June H1/Jan-May reconstruction.",
        "Export curbs preserved domestic product availability and shifted scarcity abroad; they are not new supply or an SPR release.", "medium", "Non-official secondary reporting; nested in China's product balance.",
    ], strict=True)))
    rows.append(dict(zip(BLOG_FIELDS, [
        "china-nbs-july-release-availability", "china_mechanism_evidence", "monthly", "China", "Asia and Oceania", "2026-07-01", "2026-07-31", "31",
        "july_crude_processing_release", "", "not_available", "", "", "", "", "not_located_at_2026_08_18_cutoff", NBS_CALENDAR,
        "The NBS calendar scheduled July national-economy data for 17 August; no official English or Chinese July energy-production release was located by the 18 August research cutoff.",
        "Do not impute July refinery runs from the August STEO demand estimate.", "high_for_availability_check", "Refresh when the official NBS release becomes accessible.",
    ], strict=True)))
    return rows


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def validate(asia: list[dict[str, str]], nonasia: list[dict[str, str]], blog: list[dict[str, str]]) -> None:
    for name, rows in (("asia", asia), ("nonasia", nonasia), ("blog", blog)):
        ids = [row["row_id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate {name} row IDs")
    world = {r["frame"]: float(r["value"]) for r in blog if r["metric"] == "consumption_below_frozen_february_forecast" and r["geography"] == "World"}
    net = {r["frame"]: float(r["value"]) for r in blog if r["metric"] == "world_net_demand_gap"}
    if any(abs(world[k] - net[k]) > 1e-5 for k in world):
        raise ValueError("Regional bridge does not match world")


def main() -> None:
    feb, aug = (workbook_rows(download(url), 9) for url in (FEB_URL, AUG_URL))
    asia = build_asia(feb, aug)
    nonasia = build_nonasia(feb, aug)
    blog = build_blog(feb, aug, asia, nonasia)
    validate(asia, nonasia, blog)
    write(ASIA_OUT, ASIA_FIELDS, asia)
    write(NONASIA_OUT, NONASIA_FIELDS, nonasia)
    write(BLOG_OUT, BLOG_FIELDS, blog)
    print(f"Wrote {len(asia)} Asia rows, {len(nonasia)} non-Asia rows, and {len(blog)} blog rows")


if __name__ == "__main__":
    main()
