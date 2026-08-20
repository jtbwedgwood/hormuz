#!/usr/bin/env python3
"""Build scenario allocations for non-Asian March-July 2026 oil-demand revisions."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv"
OUT = ROOT / "data/derived/hormuz_m8q_13_non_asia_demand_mechanisms.csv"

FIELDS = [
    "row_id", "record_type", "region", "geography", "period_start", "period_end",
    "scenario_case", "mechanism", "allocation_million_bbl", "regional_gap_million_bbl",
    "allocation_sign_in_global_bridge", "share_of_absolute_region_gap_pct", "unit",
    "evidence_status", "confidence", "source_date", "source_url", "method",
    "interpretation", "counterargument", "overlap_rule",
]

SCENARIO_LABELS = {
    "scarcity_dominant": "Forced scarcity and activity loss receive more weight; switching and voluntary behavior receive less.",
    "base": "Central project attribution balancing contemporaneous physical, policy, and macro evidence.",
    "behavior_switching_high": "Voluntary conservation, price response, and switching receive more weight, without changing the observed regional total.",
}

SOURCES = {
    "eia": "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx | https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx",
    "opec": "https://www.opec.org/assets/assetdb/asb-2025.pdf",
    "iea_mar": "https://www.iea.org/reports/oil-market-report-march-2026",
    "iea_may": "https://www.iea.org/reports/oil-market-report-may-2026",
    "iea_jul": "https://www.iea.org/reports/oil-market-report-july-2026",
    "world_bank_mena": "https://thedocs.worldbank.org/en/doc/2b672b3b0415d6b66c45b66579db4ef5-0050012026/related/GEP-Jun-2026-Regional-Highlights-MNA.pdf",
    "world_bank_global": "https://www.worldbank.org/en/news/press-release/2026/06/11/global-economic-prospects-june-2026-press-release",
    "imf_market": "https://www.imf.org/en/blogs/articles/2026/07/15/the-oil-market-absorbed-the-war-shock-but-buffers-are-running-low",
    "imf_policy": "https://www.imf.org/en/blogs/articles/2026/06/18/the-energy-shock-is-testing-government-budgets",
    "imf_spillovers": "https://www.imf.org/en/blogs/articles/2026/03/30/how-the-war-in-the-middle-east-is-affecting-energy-trade-and-finance",
    "eurostat_oil": "https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/43212.pdf",
    "eurostat_transport": "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251128-1",
    "eu_mar31": "https://energy.ec.europa.eu/news/commission-calls-eu-countries-coordinate-measures-ensure-oil-security-supply-amid-middle-east-energy-2026-03-31_en",
    "eu_may8": "https://transport.ec.europa.eu/news-events/news/commission-publishes-guidance-support-eu-transport-sector-affected-middle-east-crisis-2026-05-08_en",
    "eu_may13": "https://energy.ec.europa.eu/news/commission-provides-eu-countries-practical-examples-address-energy-crisis-2026-05-13_en",
    "eu_may18": "https://energy.ec.europa.eu/news/eu-continues-monitor-oil-market-situation-and-prepares-coordinated-response-address-jet-fuel-supply-2026-05-18_en",
    "kpler_africa": "https://www.kpler.com/blog/next-in-line-for-demand-losses-africa-transportation-fuels",
    "afdb": "https://www.afdb.org/en/news-and-events/press-releases/crisis-middle-east-could-cost-africa-02-percent-economic-growth-2026-92485",
    "egypt": "https://sis.gov.eg/en/media-center/news/pm-announces-fresh-energy-rationing-measures-amid-regional-crisis/",
    "egypt_followup": "https://sis.gov.eg/fr/centre-m%C3%A9diatique/actualit%C3%A9s/l%C3%A9gypte-maintient-les-mesures-de-rationalisation-de-la-consommation-%C3%A9nerg%C3%A9tique/",
    "south_africa": "https://www.gov.za/news/media-statements/mineral-and-petroleum-resources-fuel-supply-and-prices-10-mar-2026",
    "canada": "https://www.canada.ca/en/department-finance/news/2026/04/temporarily-suspending-the-federal-fuel-excise-tax.html",
}


def make_row(row_id: str, record_type: str, region: str, geography: str,
             scenario: str, mechanism: str, allocation: float | None, gap: float | None,
             sign: int | None, status: str, confidence: str, source_date: str,
             source: str, method: str, interpretation: str, counterargument: str,
             overlap: str) -> dict[str, str]:
    share = ""
    if allocation is not None and gap not in (None, 0):
        share = f"{100 * allocation / abs(gap):.6f}".rstrip("0").rstrip(".")
    values = {
        "row_id": row_id,
        "record_type": record_type,
        "region": region,
        "geography": geography,
        "period_start": "2026-03-01" if record_type != "baseline_structure" else "2024-01-01",
        "period_end": "2026-07-31" if record_type != "baseline_structure" else "2024-12-31",
        "scenario_case": scenario,
        "mechanism": mechanism,
        "allocation_million_bbl": "" if allocation is None else f"{allocation:.6f}".rstrip("0").rstrip("."),
        "regional_gap_million_bbl": "" if gap is None else f"{gap:.6f}".rstrip("0").rstrip("."),
        "allocation_sign_in_global_bridge": "" if sign is None else str(sign),
        "share_of_absolute_region_gap_pct": share,
        "unit": "million_bbl" if allocation is not None else "native_source_unit_or_qualitative",
        "evidence_status": status,
        "confidence": confidence,
        "source_date": source_date,
        "source_url": source,
        "method": method,
        "interpretation": interpretation,
        "counterargument": counterargument,
        "overlap_rule": overlap,
    }
    return {field: values[field] for field in FIELDS}


def load_regional_gaps() -> dict[str, float]:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    mapping = {
        "Middle East": "Middle East",
        "Africa": "Africa",
        "Europe": "Europe",
        "Eurasia": "Eurasia",
        "Central and South America": "Central and South America",
        "North America": "North America",
    }
    output: dict[str, float] = {}
    for region, geography in mapping.items():
        matches = [
            row for row in rows
            if row["ledger_group"] == "demand_counterfactual"
            and row["accounting_level"] == "component"
            and row["geography"] == geography
            and row["metric"] == "cumulative_consumption_below_frozen_february_forecast"
        ]
        if len(matches) != 1:
            raise ValueError(f"Expected one regional demand row for {region}, got {len(matches)}")
        output[region] = float(matches[0]["value_base"])
    return output


def mechanism_allocations() -> dict[str, dict[str, dict[str, float]]]:
    return {
        "Middle East": {
            "scarcity_dominant": {
                "forced_refinery_feedstock_and_LPG_scarcity": 70,
                "aviation_and_security_related_mobility_loss": 40,
                "trade_tourism_logistics_and_macro_activity_loss": 30,
                "explicit_policy_and_conservation": 5,
                "autonomous_price_response": 8,
                "rapid_fuel_switching_away_from_oil": 2,
                "forecast_model_and_unallocated_residual": 18.496208,
            },
            "base": {
                "forced_refinery_feedstock_and_LPG_scarcity": 65,
                "aviation_and_security_related_mobility_loss": 38,
                "trade_tourism_logistics_and_macro_activity_loss": 30,
                "explicit_policy_and_conservation": 10,
                "autonomous_price_response": 12,
                "rapid_fuel_switching_away_from_oil": 4,
                "forecast_model_and_unallocated_residual": 14.496208,
            },
            "behavior_switching_high": {
                "forced_refinery_feedstock_and_LPG_scarcity": 55,
                "aviation_and_security_related_mobility_loss": 40,
                "trade_tourism_logistics_and_macro_activity_loss": 28,
                "explicit_policy_and_conservation": 18,
                "autonomous_price_response": 15,
                "rapid_fuel_switching_away_from_oil": 7,
                "forecast_model_and_unallocated_residual": 10.496208,
            },
        },
        "Africa": {
            "scarcity_dominant": {
                "forced_transport_fuel_and_import_scarcity": 22,
                "LPG_kerosene_affordability_and_fuel_stacking": 3,
                "trade_logistics_and_macro_activity_loss": 5,
                "explicit_policy_and_conservation": 2,
                "autonomous_price_response": 2,
                "rapid_electrification_or_other_fuel_switching": 0.5,
                "forecast_model_and_unallocated_residual": 0.599597,
            },
            "base": {
                "forced_transport_fuel_and_import_scarcity": 20,
                "LPG_kerosene_affordability_and_fuel_stacking": 3.5,
                "trade_logistics_and_macro_activity_loss": 5,
                "explicit_policy_and_conservation": 2.5,
                "autonomous_price_response": 2,
                "rapid_electrification_or_other_fuel_switching": 1,
                "forecast_model_and_unallocated_residual": 1.099597,
            },
            "behavior_switching_high": {
                "forced_transport_fuel_and_import_scarcity": 17,
                "LPG_kerosene_affordability_and_fuel_stacking": 4,
                "trade_logistics_and_macro_activity_loss": 4,
                "explicit_policy_and_conservation": 4,
                "autonomous_price_response": 2.5,
                "rapid_electrification_or_other_fuel_switching": 2.5,
                "forecast_model_and_unallocated_residual": 1.099597,
            },
        },
        "Europe": {
            "scarcity_dominant": {
                "aviation_and_jet_fuel_constraint": 12,
                "road_freight_and_product_scarcity": 3,
                "macro_industrial_and_trade_activity_loss": 3,
                "explicit_policy_and_conservation": 2,
                "autonomous_price_response": 3,
                "biofuel_electrification_and_other_switching": 0.5,
                "forecast_model_and_unallocated_residual": 6.20088,
            },
            "base": {
                "aviation_and_jet_fuel_constraint": 10,
                "road_freight_and_product_scarcity": 2,
                "macro_industrial_and_trade_activity_loss": 3,
                "explicit_policy_and_conservation": 4,
                "autonomous_price_response": 4,
                "biofuel_electrification_and_other_switching": 1.5,
                "forecast_model_and_unallocated_residual": 5.20088,
            },
            "behavior_switching_high": {
                "aviation_and_jet_fuel_constraint": 8,
                "road_freight_and_product_scarcity": 1,
                "macro_industrial_and_trade_activity_loss": 2.5,
                "explicit_policy_and_conservation": 6,
                "autonomous_price_response": 5,
                "biofuel_electrification_and_other_switching": 3,
                "forecast_model_and_unallocated_residual": 4.20088,
            },
        },
        "Eurasia": {
            "scarcity_dominant": {
                "refinery_and_product_supply_constraint": 5.5,
                "aviation_and_mobility_loss": 0.5,
                "macro_trade_and_logistics_activity_loss": 1,
                "explicit_policy_and_conservation": 0.3,
                "autonomous_price_response": 0.5,
                "fuel_switching": 0.1,
                "forecast_model_and_unallocated_residual": 1.533329,
            },
            "base": {
                "refinery_and_product_supply_constraint": 4.5,
                "aviation_and_mobility_loss": 0.5,
                "macro_trade_and_logistics_activity_loss": 1.3,
                "explicit_policy_and_conservation": 0.5,
                "autonomous_price_response": 0.8,
                "fuel_switching": 0.2,
                "forecast_model_and_unallocated_residual": 1.633329,
            },
            "behavior_switching_high": {
                "refinery_and_product_supply_constraint": 3.5,
                "aviation_and_mobility_loss": 0.5,
                "macro_trade_and_logistics_activity_loss": 1.5,
                "explicit_policy_and_conservation": 0.8,
                "autonomous_price_response": 1.2,
                "fuel_switching": 0.4,
                "forecast_model_and_unallocated_residual": 1.533329,
            },
        },
        "Central and South America": {
            "scarcity_dominant": {
                "transport_and_fuel_price_response": 1,
                "macro_trade_and_logistics_activity_loss": 1,
                "explicit_policy_and_conservation": 0.5,
                "biofuel_electrification_and_other_switching": 0.3,
                "aviation_effect": 0.5,
                "localized_product_scarcity": 0.5,
                "forecast_model_and_unallocated_residual": 4.558965,
            },
            "base": {
                "transport_and_fuel_price_response": 1.5,
                "macro_trade_and_logistics_activity_loss": 1.2,
                "explicit_policy_and_conservation": 0.7,
                "biofuel_electrification_and_other_switching": 0.8,
                "aviation_effect": 0.7,
                "localized_product_scarcity": 0.5,
                "forecast_model_and_unallocated_residual": 2.958965,
            },
            "behavior_switching_high": {
                "transport_and_fuel_price_response": 2,
                "macro_trade_and_logistics_activity_loss": 1.3,
                "explicit_policy_and_conservation": 1,
                "biofuel_electrification_and_other_switching": 1.2,
                "aviation_effect": 0.8,
                "localized_product_scarcity": 0.5,
                "forecast_model_and_unallocated_residual": 1.558965,
            },
        },
        "North America": {
            "scarcity_dominant": {
                "fiscal_price_shielding_and_tax_relief": 4,
                "energy_producing_and_export_activity": 1,
                "US_product_mix_and_seasonality": 2,
                "Canada_Mexico_baseline_revision": 4,
                "forecast_model_and_unallocated_residual": 5.633495,
            },
            "base": {
                "fiscal_price_shielding_and_tax_relief": 6,
                "energy_producing_and_export_activity": 2,
                "US_product_mix_and_seasonality": 3,
                "Canada_Mexico_baseline_revision": 3,
                "forecast_model_and_unallocated_residual": 2.633495,
            },
            "behavior_switching_high": {
                "fiscal_price_shielding_and_tax_relief": 8,
                "energy_producing_and_export_activity": 2,
                "US_product_mix_and_seasonality": 3,
                "Canada_Mexico_baseline_revision": 2,
                "forecast_model_and_unallocated_residual": 1.633495,
            },
        },
    }


def allocation_evidence(region: str, mechanism: str) -> tuple[str, str, str, str, str]:
    if region == "Middle East":
        return (
            f"{SOURCES['iea_mar']} | {SOURCES['iea_may']} | {SOURCES['iea_jul']} | {SOURCES['world_bank_mena']}",
            "IEA documents flight cancellations, LPG disruption, export-refinery curtailment and slow restart; World Bank documents severe Gulf/Iraq output, trade, tourism and aviation losses.",
            "Direct mechanism evidence is strong, but no public source allocates the EIA regional forecast revision by sector or country.",
            "low_medium",
            "2026-07-10",
        )
    if region == "Africa":
        return (
            f"{SOURCES['kpler_africa']} | {SOURCES['afdb']} | {SOURCES['egypt']} | {SOURCES['south_africa']}",
            "Kpler estimates a 260 kb/d initial East/Southern Africa transport-fuel loss; AfDB/ECA identify extreme import dependence; Egypt adopted explicit rationing while South Africa initially reported no physical shortage.",
            "The Kpler estimate is modeled and national experiences differ sharply; fuel-tax relief can preserve demand even where prices rise.",
            "medium",
            "2026-05-06",
        )
    if region == "Europe":
        return (
            f"{SOURCES['eu_mar31']} | {SOURCES['eu_may8']} | {SOURCES['eu_may13']} | {SOURCES['eu_may18']}",
            "EU records voluntary fuel-saving guidance, aviation regulatory flexibility and jet-fuel concern; the May catalogue describes potential annual savings rather than measured March-July delivery.",
            "The Commission said on 18 May that the EU had no aggregate fuel shortage; much of the gap may be aviation, price response, or forecast revision rather than forced road-fuel scarcity.",
            "medium",
            "2026-05-18",
        )
    if region == "Eurasia":
        return (
            SOURCES["iea_jul"],
            "IEA reports Russian refinery throughputs curtailed by attacks and domestic fuel deliveries significantly affected.",
            "This is an overlapping Russia/Ukraine-war mechanism, not necessarily caused by Hormuz.",
            "medium_low",
            "2026-07-10",
        )
    if region == "Central and South America":
        return (
            f"{SOURCES['eia']} | {SOURCES['imf_spillovers']}",
            "EIA's regional revision is small and its Brazil suballocation exceeds the regional total, while IMF describes broader price, food, fertilizer and financial spillovers.",
            "There is little public evidence tying a specific realized Latin American oil volume to Hormuz; residual should remain large.",
            "low",
            "2026-07-07",
        )
    return (
        f"{SOURCES['canada']} | {SOURCES['imf_market']} | {SOURCES['eia']}",
        "Canada suspended federal gasoline, diesel and aviation-fuel excise from 20 April; IMF says transport demand was sticky where caps, subsidies and rebates muted price pass-through; EIA product revisions show mixed U.S. movements.",
        "Tax relief plausibly preserves consumption but does not prove the forecast revision was caused by policy; weather, seasonality and ordinary model revision remain material.",
        "medium_low",
        "2026-07-15",
    )


def evidence_rows(gaps: dict[str, float]) -> list[dict[str, str]]:
    specs = [
        ("baseline-middle-east", "baseline_structure", "Middle East", "Region", "2024 oil demand structure",
         SOURCES["opec"], "2025-07-02",
         "OPEC ASB 2025 tables 4.7-4.8: 2024 demand 8.854 mb/d; Saudi 3.386, Iran 1.859, UAE 1.017, Iraq 0.977, Kuwait 0.468 and Qatar 0.380 mb/d. Products: gasoline 1.755, kerosene 0.505, distillates 1.914, residuals 1.590 and other 3.091 mb/d.",
         "Saudi and Iran dominate the baseline; aviation is material but too small to explain the whole 173.5 mb gap. Residual and other products make refinery/feedstock and power-sector disruption plausible.",
         "OPEC product categories are broad and 2024 predates the shock."),
        ("baseline-africa", "baseline_structure", "Africa", "Region", "2024 oil demand structure",
         SOURCES["opec"], "2025-07-02",
         "OPEC ASB 2025: Africa demand 4.649 mb/d; Egypt 0.885, South Africa 0.632, Nigeria 0.483 and Algeria 0.467 mb/d. Distillates were 1.867 mb/d (40%), gasoline 1.208 (26%), kerosene 0.338, residuals 0.434 and other products 0.801.",
         "The 35.1 mb revision averages 0.229 mb/d, close to a 5% regional shock and to Kpler's modeled transport-fuel range.",
         "Continental totals conceal large differences between producers, refiners, importers and foreign-exchange constraints."),
        ("baseline-europe", "baseline_structure", "Europe", "EU and OECD Europe", "2024 oil and transport structure",
         f"{SOURCES['eurostat_oil']} | {SOURCES['eurostat_transport']} | {SOURCES['opec']}", "2026-06-01",
         "Eurostat reports 379.5 Mtoe EU final oil use in 2024; Germany held 20.1%, France 15.3%, Italy and Spain 11.1% each. In 2023 road transport was 73% of transport energy and aviation 13%; OPEC puts OECD Europe kerosene demand at 1.531 mb/d in 2024.",
         "Road fuels dominate baseline use, but the contemporaneous physical concern was jet fuel and flight disruption.",
         "Annual baseline shares do not identify the March-July marginal response."),
        ("baseline-eurasia", "baseline_structure", "Eurasia", "Russia and other Eurasia", "2024 oil demand structure",
         SOURCES["opec"], "2025-07-02",
         "OPEC ASB 2025: Russia consumed 3.982 mb/d and other Eurasia 1.258 mb/d in 2024; distillates were 1.640 mb/d combined. EIA allocates 9.065 of the 9.433 mb regional gap to Russia.",
         "Russia's dominance and refinery attacks make refinery/product constraints more plausible than clean Hormuz-driven conservation.",
         "The Russia-Ukraine war is a major overlapping cause."),
        ("baseline-latin-america", "baseline_structure", "Central and South America", "Region", "2024 oil demand structure",
         SOURCES["opec"], "2025-07-02",
         "OPEC ASB 2025: Latin America consumed 6.750 mb/d in 2024, led by Brazil at 3.451 mb/d. Gasoline and distillates were 1.970 and 2.165 mb/d.",
         "EIA's 9.577 mb Brazil gap exceeds the 8.359 mb regional total because other countries offset it by about 1.218 mb.",
         "This internal offset is evidence against an overconfident causal regional story."),
        ("baseline-north-america", "baseline_structure", "North America", "Region", "2024 oil demand structure",
         SOURCES["opec"], "2025-07-02",
         "OPEC ASB 2025: OECD America consumed 24.944 mb/d in 2024; gasoline was 10.599, jet/kerosene 2.007 and distillates 4.984 mb/d.",
         "A 16.633 mb upward revision over five months is tiny relative to baseline and can plausibly be model/seasonal noise plus policy shielding.",
         "The EIA region is North America rather than OPEC's OECD America, but the baseline order of magnitude is suitable."),
        ("policy-egypt", "policy_evidence", "Africa", "Egypt", "mandatory conservation and remote work",
         f"{SOURCES['egypt']} | {SOURCES['egypt_followup']}", "2026-04-23",
         "Egypt ordered 9pm commercial closures, curtailed advertising and street lighting, closed the Government District at 6pm, and introduced remote work; the prime minister later said one-day remote work lowered electricity load and urban traffic.",
         "This is the clearest non-Asian explicit conservation evidence and plausibly reduces commuting fuel, but the government did not publish oil barrels saved.",
         "Electricity savings must not all be counted as oil savings."),
        ("policy-eu", "policy_evidence", "Europe", "European Union", "voluntary savings and transport response",
         f"{SOURCES['eu_mar31']} | {SOURCES['eu_may8']} | {SOURCES['eu_may13']}", "2026-05-13",
         "The Commission urged voluntary transport fuel savings on 31 March, enabled aviation slot/fuel flexibility on 8 May, and published a catalogue whose full annual potential was 15-20 Mtoe of oil.",
         "Historical realized savings by July are necessarily far below an annual technical potential announced in May.",
         "Do not convert the 15-20 Mtoe annual potential into observed March-July barrels."),
        ("policy-canada", "policy_evidence", "North America", "Canada", "fuel tax suspension",
         SOURCES["canada"], "2026-04-14",
         "Canada set federal excise to zero on gasoline, diesel and aviation fuels from 20 April through 7 September: 10 cents/litre for gasoline and 4 cents/litre for diesel/aviation fuel.",
         "This muted price pass-through and is directionally consistent with Canada's 10.138 mb upward revision.",
         "The temporal association is not an elasticity estimate or proof of causation."),
        ("counterexample-south-africa", "counterargument", "Africa", "South Africa", "no immediate shortage and fiscal cushioning",
         SOURCES["south_africa"], "2026-03-10",
         "South Africa initially stated there was no immediate shortage risk; subsequent temporary fuel-levy relief cushioned pump-price pass-through.",
         "Africa's revision cannot be described as uniform physical rationing.",
         "Country price-support policies may preserve demand while worsening fiscal balances."),
        ("us-product-revision", "country_anchor", "North America", "United States", "mixed product-level forecast revision",
         SOURCES["eia"], "2026-07-07",
         "Project extraction from EIA STEO Table 4a: July-vintage minus frozen-February March-July consumption revisions were gasoline +3.342 mb, residual fuel +5.672, HGL +0.978, distillate -13.488 and jet fuel -3.908; total U.S. consumption was +5.561 mb after other products.",
         "The U.S. upward total is not a simple gasoline-driving story; offsetting distillate and jet weakness is material.",
         "Product rows are nested within total U.S. consumption."),
    ]
    rows = []
    for row_id, record_type, region, geography, mechanism, source, date, method, interpretation, counterargument in specs:
        rows.append(make_row(
            row_id, record_type, region, geography, "", mechanism, None, gaps.get(region), None,
            "observed_baseline_or_policy_evidence", "medium_high" if record_type == "baseline_structure" else "medium",
            date, source, method, interpretation, counterargument,
            "Evidence rows explain or constrain scenario allocations; they are not additional barrels."
        ))
    return rows


def build() -> list[dict[str, str]]:
    gaps = load_regional_gaps()
    allocations = mechanism_allocations()
    rows: list[dict[str, str]] = []
    for region, scenarios in allocations.items():
        gap = gaps[region]
        sign = -1 if gap < 0 else 1
        for scenario, components in scenarios.items():
            source, method, counterargument, confidence, date = allocation_evidence(region, "")
            for mechanism, value in components.items():
                rows.append(make_row(
                    f"{region.lower().replace(' ', '-').replace('&', 'and')}-{scenario}-{mechanism}",
                    "mechanism_scenario", region, region, scenario, mechanism, value, gap, sign,
                    "project_scenario_allocation_not_observation", confidence, date, source, method,
                    f"{SCENARIO_LABELS[scenario]} Positive allocation explains {'an upward consumption revision' if sign < 0 else 'lower consumption'}.",
                    counterargument,
                    "Mechanism rows are mutually exclusive within a scenario and sum exactly to the absolute regional gap; never add scenarios together."
                ))
    rows.extend(evidence_rows(gaps))

    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    for region, scenarios in allocations.items():
        for scenario, components in scenarios.items():
            total = sum(components.values())
            if abs(total - abs(gaps[region])) > 1e-6:
                raise ValueError(f"{region} {scenario} does not close: {total} vs {gaps[region]}")
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
