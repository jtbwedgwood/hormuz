#!/usr/bin/env python3
"""Build the canonical k4w scenarios and Gulf producer direct-GDP proxy."""

from __future__ import annotations

import csv
from calendar import monthrange
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_a4d_2_august_steo_comparison.csv"
SCENARIOS = ROOT / "data/derived/hormuz_k4w_scenarios.csv"
OUTPUT = ROOT / "data/derived/hormuz_k4w_1_producer_gdp_floor.csv"

EIA_URL = "https://www.eia.gov/outlooks/steo/archives/aug26.pdf"

# Latest usable real national-accounts weights. These are extraction/hydrocarbon
# aggregates, not export-value shares. Qatar/UAE include gas; their crude-only
# application therefore remains a mechanical proxy rather than a clean floor.
COUNTRY_META = {
    "Saudi Arabia": {
        "feb_output": 10.500,
        "share": 0.273,
        "source": "Saudi GASTAT Annual National Accounts Publication 2024",
        "url": "https://www.stats.gov.sa/documents/20117/2435267/Annual_National_Accounts_Publication_2024_EN.pdf_fixed_8631783/770f9e7b-444a-5d5e-5b75-f6825f2668d0",
        "method": "Approximate 2023 real oil-activity weight implied by -1.2 pp contribution divided by -4.4% real oil-activity growth; oil activities include extraction and refining.",
        "confidence": "medium",
    },
    "Iraq": {
        "feb_output": 4.400,
        "share": 0.527,
        "source": "Central Bank of Iraq Annual Economic Report 2024 (CSO national accounts)",
        "url": "https://cbi.iq/static/uploads/up/file-177269103623349.pdf",
        "method": "Oil-sector share of 2024 GDP at constant prices reported as 52.7%.",
        "confidence": "medium_high",
    },
    "Kuwait": {
        "feb_output": 2.560,
        "share": 0.479,
        "source": "Kuwait Central Statistical Bureau annual GDP at constant prices, 2024",
        "url": "https://www.csb.gov.kw/Pages/Statistics_en?ID=80&ParentCatID=3",
        "method": "Real oil value added KD19.3bn divided by real GDP KD40.3bn; rounded source-table extraction.",
        "confidence": "medium",
    },
    "United Arab Emirates": {
        "feb_output": 3.600,
        "share": 0.245,
        "source": "UAE Federal Competitiveness and Statistics Centre, UAE Unified Numbers",
        "url": "https://fcsc.gov.ae/wp-content/uploads/2025/12/UAE-Unified-Numbers-En.pdf",
        "method": "Oil and natural gas share of 2024 GDP at constant prices reported as 24.5%.",
        "confidence": "high_for_share_low_for_crude_application",
    },
    "Qatar": {
        "feb_output": 0.557,
        "share": 0.355,
        "source": "Qatar National Planning Council annual GDP by economic activity, 2024",
        "url": "https://www.npc.qa/en/statistics/Statistical%20Releases/Economic/National%20Accounts/GDP/Qatar%20Annual%20Gross%20Domestic%20Product%20by%20Economic%20Activity%20En%20V5.pdf",
        "method": "Mining and quarrying QAR256.737bn divided by GDP QAR723.553bn at constant 2018 prices.",
        "confidence": "high_for_share_low_for_crude_application",
    },
    "Bahrain": {
        "feb_output": 0.193,
        "share": 0.14704,
        "source": "Bahrain Open Data Portal, annual general economic indicators at constant prices",
        "url": "https://www.data.gov.bh/explore/dataset/02-annually-general-economic-indicators-by-constant-prices/table/",
        "method": "Oil GDP BHD2,232.321m divided by GDP BHD15,181.274m at constant prices in 2024.",
        "confidence": "high",
    },
    "Iran": {
        "feb_output": 3.390,
        "share": 0.126,
        "source": "IMF Middle East and Central Asia Regional Economic Outlook statistical appendix, May 2025",
        "url": "https://www.imf.org/-/media/Files/Publications/REO/MCD-CCA/2025/May/English/regional-economic-outlook-middle-east-central-asia-may-2025-statistical-appendix.ashx",
        "method": "Approximate prior-year real oil weight implied by 5.0% total, 14.7% oil, and 3.6% non-oil real growth; rounded.",
        "confidence": "low",
    },
}

MONTHS = ((8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December"))
SCENARIO_FACTORS = {
    "A_1_month": (1.0, 1.0, 0.5, 0.0, 0.0),
    "A_3_month_base": (1.0, 1.0, 5 / 6, 1 / 2, 1 / 6),
    "A_6_month": (1.0, 1.0, 11 / 12, 3 / 4, 7 / 12),
    "B_no_2026_reopening": (1.0, 1.0, 1.0, 1.0, 1.0),
}


def read_eia() -> tuple[dict[str, dict[str, float]], float, float]:
    shutins: dict[str, dict[str, float]] = {country: {} for country in COUNTRY_META}
    published_total = discrepancy = None
    with INPUT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["record_type"] == "gulf_country_crude_shutin" and row["geography"] in shutins:
                shutins[row["geography"]][row["frame"]] = float(row["august_value"])
            elif row["row_id"] == "gulf-total-march-july-cumulative":
                published_total = float(row["august_value"])
            elif row["row_id"] == "gulf-country-vs-total-discrepancy":
                discrepancy = float(row["august_value"])
    assert published_total is not None and discrepancy is not None
    assert all(set(v) == {"march_may", "june", "july"} for v in shutins.values())
    return shutins, published_total, discrepancy


def write_scenarios() -> None:
    fields = [
        "scenario_id", "scenario_label", "reopening_date", "recovery_ramp", "month",
        "month_start", "days", "july_shutin_factor", "status", "assumption", "source_url",
    ]
    rows = []
    for scenario, factors in SCENARIO_FACTORS.items():
        for (month_num, month_name), factor in zip(MONTHS, factors):
            rows.append({
                "scenario_id": scenario,
                "scenario_label": "Full reopening 30 September 2026" if scenario.startswith("A_") else "No reopening during 2026; managed partial closure persists",
                "reopening_date": "2026-09-30" if scenario.startswith("A_") else "",
                "recovery_ramp": scenario.removeprefix("A_").replace("_base", "") if scenario.startswith("A_") else "hold July country rate",
                "month": month_name,
                "month_start": f"2026-{month_num:02d}-01",
                "days": monthrange(2026, month_num)[1],
                "july_shutin_factor": f"{factor:.6f}",
                "status": "scenario_assumption",
                "assumption": "August-September hold each country's July crude shut-in; after 30 September, linearly converge to zero over the named ramp." if scenario.startswith("A_") else "August-December hold each country's July crude shut-in rate.",
                "source_url": EIA_URL,
            })
    with SCENARIOS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_output() -> None:
    shutins, published_total, discrepancy = read_eia()
    fields = [
        "country", "scenario_id", "february_crude_output_mbd", "march_may_shutin_mbd",
        "june_shutin_mbd", "july_shutin_mbd", "march_july_shutin_million_bbl",
        "projected_august_december_shutin_million_bbl", "full_year_shutin_million_bbl",
        "annual_average_crude_output_loss_pct", "hydrocarbon_real_gva_share_pct",
        "direct_real_gdp_level_decline_pp", "measure_label", "national_accounts_source",
        "national_accounts_source_url", "share_method", "confidence", "lng_treatment",
        "excluded_channels", "eia_published_gulf_total_march_july_million_bbl",
        "displayed_country_rows_gap_million_bbl", "eia_source_url",
    ]
    rows = []
    excluded = "tourism and aviation; trade and logistics; domestic energy-infrastructure outages; war-risk insurance and freight; construction and FDI; fiscal multiplier and sovereign-wealth spending offsets"
    for country, meta in COUNTRY_META.items():
        obs = shutins[country]
        observed_mb = obs["march_may"] * 92 + obs["june"] * 30 + obs["july"] * 31
        for scenario, factors in SCENARIO_FACTORS.items():
            future_mb = obs["july"] * sum(monthrange(2026, month)[1] * factor for (month, _), factor in zip(MONTHS, factors))
            full_mb = observed_mb + future_mb
            annual_loss = full_mb / (meta["feb_output"] * 365)
            gdp_decline = annual_loss * meta["share"]
            rows.append({
                "country": country,
                "scenario_id": scenario,
                "february_crude_output_mbd": f"{meta['feb_output']:.3f}",
                "march_may_shutin_mbd": f"{obs['march_may']:.3f}",
                "june_shutin_mbd": f"{obs['june']:.3f}",
                "july_shutin_mbd": f"{obs['july']:.3f}",
                "march_july_shutin_million_bbl": f"{observed_mb:.3f}",
                "projected_august_december_shutin_million_bbl": f"{future_mb:.3f}",
                "full_year_shutin_million_bbl": f"{full_mb:.3f}",
                "annual_average_crude_output_loss_pct": f"{100 * annual_loss:.3f}",
                "hydrocarbon_real_gva_share_pct": f"{100 * meta['share']:.3f}",
                "direct_real_gdp_level_decline_pp": f"{-100 * gdp_decline:.3f}",
                "measure_label": "real GDP level decline vs no-shut-in 2026 counterfactual; not a growth revision",
                "national_accounts_source": meta["source"],
                "national_accounts_source_url": meta["url"],
                "share_method": meta["method"],
                "confidence": meta["confidence"],
                "lng_treatment": "Oil-only; no monthly realized LNG shut-in series. Hydrocarbon share includes gas, so the result is a mechanical proxy, not a clean lower bound." if country in {"Qatar", "United Arab Emirates"} else "Crude-only direct channel; condensate, NGL and LNG losses excluded.",
                "excluded_channels": excluded,
                "eia_published_gulf_total_march_july_million_bbl": f"{published_total:.3f}",
                "displayed_country_rows_gap_million_bbl": f"{discrepancy:.3f}",
                "eia_source_url": EIA_URL,
            })
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    write_scenarios()
    write_output()
    print(f"wrote {SCENARIOS.relative_to(ROOT)}")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
