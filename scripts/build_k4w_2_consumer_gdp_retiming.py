#!/usr/bin/env python3
"""Audit ADB July 2026 Asia forecasts and re-time them to k4w scenarios."""

from __future__ import annotations

import csv
from calendar import monthrange
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_INPUT = ROOT / "data/derived/hormuz_k4w_scenarios.csv"
PRICE_INPUT = ROOT / "data/derived/hormuz_r3v_3_price_context_summary.csv"
DEMAND_INPUT = ROOT / "data/derived/hormuz_a4d_8_demand_splits_blog_table.csv"
PRICE_OUTPUT = ROOT / "data/derived/hormuz_k4w_2_price_paths.csv"
OUTPUT = ROOT / "data/derived/hormuz_k4w_2_consumer_gdp_retiming.csv"

ADB_JULY = "https://www.adb.org/sites/default/files/publication/1155601/asian-development-outlook-july-2026.pdf"
ADB_APRIL = "https://www.adb.org/sites/default/files/publication/1135881/ado-april-2026.pdf"
ADB_BRIEF = "https://www.adb.org/sites/default/files/publication/1142926/adb-brief-388-middle-east-conflict-updated-analysis.pdf"

FORECASTS = {
    # forecast, April forecast, grouping, calendar/fiscal, physical-bias note
    "China": (4.6, 4.6, "developing_east_asia", "calendar", "High: refinery/petrochemical throughput and feedstock cuts plus price caps/export controls obscure the scarcity signal."),
    "India": (6.6, 6.9, "south_asia", "fiscal_year_2026", "Very high: LPG scarcity and allocation, naphtha/bitumen/fertilizer constraints, subsidies and tax cuts are not a benchmark-price shock."),
    "Indonesia": (5.2, 5.2, "developing_southeast_asia", "calendar", "Medium: subsidies suppress pass-through; transit, work-pattern and biofuel responses preserve some activity but carry fiscal/opportunity costs."),
    "Thailand": (1.8, 1.8, "developing_southeast_asia", "calendar", "High: work-from-home and curtailed official travel miss tourism, aviation and service-network losses."),
    "Vietnam": (7.2, 7.2, "developing_southeast_asia", "calendar", "Unknown-to-medium: no country-resolved realized demand response was found; absence of evidence is not evidence of no rationing."),
    "Philippines": (3.8, 4.4, "developing_southeast_asia", "calendar", "High in exposed sectors: compressed workweeks and fewer fishing trips include direct service, income and food-supply losses."),
    "Malaysia": (4.6, 4.6, "developing_southeast_asia", "calendar", "Medium: fuel subsidies, telework and reduced travel shift part of the shock into fiscal cost and service activity."),
    "Singapore": (3.2, 3.0, "advanced_asia_pacific", "calendar", "Lower but nonzero: dense public transport cushions mobility, while refining/trade exposure is not captured by household fuel prices."),
    "Japan": (0.7, 0.7, "advanced_asia_pacific", "calendar", "High: refinery and naphtha/petrochemical curtailment plus stock releases and fuel subsidies weaken benchmark-price transmission."),
    "South Korea": (2.6, 1.9, "advanced_asia_pacific", "calendar", "High: roughly 1 mb/d refinery-run weakness and cracker curtailment hit an export complex even when retail prices are shielded."),
}

# Current, published ADB regional scenario endpoints. The resulting slopes are
# reduced-form sensitivities, not structural oil-only elasticities: ADB changes
# oil, gas, fertilizer, supply-chain and financial conditions together.
ADB_SCENARIO_GROWTH = {
    "developing_east_asia": (4.6, 4.4),
    "south_asia": (6.3, 5.7),
    "developing_southeast_asia": (4.7, 4.2),
    "advanced_asia_pacific": (2.2, 1.5),
}
ADB_EARLY_BRENT = 72.0
ADB_REFERENCE_BRENT = 96.0
ADB_JULY_BRENT = 87.0

NET_STATUS = {
    "China": ("net crude/petroleum importer", "https://www.eia.gov/todayinenergy/detail.php?id=64544"),
    "India": ("net crude/petroleum importer", ADB_APRIL),
    "Indonesia": ("net oil importer; LNG and coal exporter, so broader energy terms of trade are mixed", "https://www.eia.gov/international/content/analysis/countries_long/Indonesia/"),
    "Thailand": ("net crude/petroleum importer", ADB_APRIL),
    "Vietnam": ("net petroleum importer overall, with domestic crude production and trade", ADB_JULY),
    "Philippines": ("net crude/petroleum importer", ADB_APRIL),
    "Malaysia": ("net oil user on production-consumption balance and major LNG exporter; broader energy terms of trade are mixed", "https://www.eia.gov/international/content/analysis/countries_long/malaysia/"),
    "Singapore": ("net crude importer and major refining/product-export hub; not an upstream windfall case", "https://www.eia.gov/international/analysis/country/SGP"),
    "Japan": ("net crude/petroleum importer", ADB_APRIL),
    "South Korea": ("net crude/petroleum importer", ADB_APRIL),
}


def realized_prices() -> dict[int, float]:
    periods = {
        "pre_shock_jan1_feb27": (1, 2),
        "march": (3,), "april": (4,), "may": (5,), "june": (6,), "july": (7,),
        "august_to_publication": (8,),
    }
    found: dict[str, float] = {}
    with PRICE_INPUT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["series"] == "brent_spot" and row["period"] in periods:
                found[row["period"]] = float(row["mean_value"])
    assert set(found) == set(periods)
    return {month: found[period] for period, months in periods.items() for month in months}


def scenario_factors() -> dict[str, dict[int, float]]:
    result: dict[str, dict[int, float]] = {}
    with SCENARIO_INPUT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            month = int(row["month_start"][5:7])
            result.setdefault(row["scenario_id"], {})[month] = float(row["july_shutin_factor"])
    assert all(set(v) == set(range(8, 13)) for v in result.values())
    return result


def demand_revisions() -> dict[str, tuple[str, str]]:
    # The exact blog-bearing values are stable outputs of a4d.8. Read them by
    # country where available; Korea remains explicitly a bounded suballocation.
    result = {}
    with DEMAND_INPUT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            country = row["geography"]
            if country in {"China", "India", "Japan"} and row["frame"] == "march_july":
                result[country] = (row["value"], "country estimate, March-July")
            elif country == "South Korea (bounded suballocation)" and row["frame"] == "march_july":
                result["South Korea"] = (f"{float(row['value']):.6f}", "bounded suballocation, March-July")
    assert set(result) == {"China", "India", "Japan", "South Korea"}
    return result


def build_price_paths() -> dict[str, float]:
    observed = realized_prices()
    factors = scenario_factors()
    pre_shock = observed[1]
    august = observed[8]
    fields = ["scenario_id", "month", "days", "brent_usd_per_bbl", "price_status", "method", "source_url"]
    rows = []
    averages = {}
    for scenario, monthly_factors in factors.items():
        values = observed.copy()
        for month in range(9, 13):
            values[month] = pre_shock + monthly_factors[month] * (august - pre_shock)
        averages[scenario] = sum(values[m] * monthrange(2026, m)[1] for m in range(1, 13)) / 365
        for month in range(1, 13):
            rows.append({
                "scenario_id": scenario,
                "month": f"2026-{month:02d}",
                "days": monthrange(2026, month)[1],
                "brent_usd_per_bbl": f"{values[month]:.6f}",
                "price_status": "observed_monthly_mean" if month <= 7 else ("partial_month_mean_held_for_month" if month == 8 else "scenario_assumption"),
                "method": "Observed through July; August 1-11 mean held for August; September-December premium over the Jan-Feb mean scales with the canonical crude shut-in factor. This is a transparent bridge, not an econometric price forecast.",
                "source_url": "data/derived/hormuz_r3v_3_price_context_summary.csv | data/derived/hormuz_k4w_scenarios.csv",
            })
    with PRICE_OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return averages


def build_retiming() -> None:
    averages = build_price_paths()
    fields = [
        "country", "scenario_id", "published_2026_real_gdp_growth_pct", "published_april_2026_forecast_pct",
        "published_growth_revision_pp", "forecast_measure", "forecast_vintage", "information_cutoff",
        "forecast_assumption", "net_petroleum_status", "net_status_source_url", "scenario_2026_brent_usd_per_bbl",
        "forecast_brent_usd_per_bbl", "scenario_price_delta_pct", "regional_sensitivity_pp_per_10pct_price",
        "sensitivity_type", "retimed_growth_delta_pp", "retimed_2026_real_gdp_growth_pct",
        "measured_march_july_oil_demand_revision_million_bbl", "demand_measure_status",
        "physical_rationing_bias", "forecast_source_url", "sensitivity_source_url", "caveat",
    ]
    rows = []
    demand_map = demand_revisions()
    for country, (forecast, april, group, period) in {k: (v[0], v[1], v[2], v[3]) for k, v in FORECASTS.items()}.items():
        early_growth, reference_growth = ADB_SCENARIO_GROWTH[group]
        price_change_pct = 100 * (ADB_REFERENCE_BRENT / ADB_EARLY_BRENT - 1)
        sensitivity = (reference_growth - early_growth) / (price_change_pct / 10)
        bias = FORECASTS[country][4]
        demand_value, demand_status = demand_map.get(country, ("", "No country-resolved value; included within Other Asia/Oceania ex-Korea 92.166 mb."))
        for scenario, price in averages.items():
            delta_pct = 100 * (price / ADB_JULY_BRENT - 1)
            retime_delta = sensitivity * delta_pct / 10
            rows.append({
                "country": country,
                "scenario_id": scenario,
                "published_2026_real_gdp_growth_pct": f"{forecast:.3f}",
                "published_april_2026_forecast_pct": f"{april:.3f}",
                "published_growth_revision_pp": f"{forecast - april:.3f}",
                "forecast_measure": f"real GDP growth; growth rate/revision, not GDP level decline; {period}",
                "forecast_vintage": "ADB Asian Development Outlook, 8 July 2026",
                "information_cutoff": "Varies by economy; global assumptions cite market data through 23 June 2026.",
                "forecast_assumption": "Hormuz shock incorporated; only partial normalization, gradual recovery in 2H26, and 2026 average Brent $87/bbl. Also includes gas, fertilizer, freight, policy and supply-chain judgment.",
                "net_petroleum_status": NET_STATUS[country][0],
                "net_status_source_url": NET_STATUS[country][1],
                "scenario_2026_brent_usd_per_bbl": f"{price:.3f}",
                "forecast_brent_usd_per_bbl": f"{ADB_JULY_BRENT:.3f}",
                "scenario_price_delta_pct": f"{delta_pct:.3f}",
                "regional_sensitivity_pp_per_10pct_price": f"{sensitivity:.3f}",
                "sensitivity_type": "ADB current Asia regional bundled scenario slope, derived from published $72/$96 and growth endpoints; not a structural or oil-only elasticity",
                "retimed_growth_delta_pp": f"{retime_delta:.3f}",
                "retimed_2026_real_gdp_growth_pct": f"{forecast + retime_delta:.3f}",
                "measured_march_july_oil_demand_revision_million_bbl": demand_value,
                "demand_measure_status": demand_status,
                "physical_rationing_bias": bias,
                "forecast_source_url": ADB_JULY,
                "sensitivity_source_url": f"{ADB_APRIL} | {ADB_BRIEF}",
                "caveat": "The retiming is a small price-path sensitivity around ADB's forecast, not a new macro forecast. ADB's own model says physical scarcity can make effects materially larger; country-specific coefficients were not published, so regional slopes are used without false precision.",
            })
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    build_retiming()
    print(f"wrote {PRICE_OUTPUT.relative_to(ROOT)}")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
