#!/usr/bin/env python3
"""Build the February-July 2026 China crude-balance reconciliation.

Positive implied stock changes are builds; negative values are draws.  The
February NBS production and processing inputs are Jan-Feb daily-average proxies;
GAC publishes a separate February trade observation.  This is explicit in output.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/derived/hormuz_g7t_1_china_crude_balance.csv"
BBL_PER_TONNE = 7.3

GAC_JAN_FEB = "https://english.customs.gov.cn/Statistics/Statistics"
GAC_MARCH = "https://www.energyconnects.com/news/oil/2026/april/china-s-oil-and-gas-imports-shrink-on-gulf-turmoil/"
GAC_APRIL = "https://www.marketscreener.com/news/china-energy-imports-drop-in-april-amid-iran-war-as-fuel-exports-hit-decade-low-ce7f5bd8d98af627"
GAC_MAY = "https://www.bairdmaritime.com/amp/story/shipping/tankers/chinas-eight-year-low-in-oil-imports-offers-relief-for-global-prices"
GAC_JUNE = "https://www.marketscreener.com/news/china-s-june-oil-imports-hit-near-10-year-low-amid-iran-war-ce7f5edcdc8bfe2d"
GAC_JULY = "https://www.brecorder.com/news/amp/40433885"
NBS_JAN_FEB = "https://www.stats.gov.cn/english/PressRelease/202603/t20260317_1962806.html"
NBS_MARCH = "https://www.stats.gov.cn/english/PressRelease/202604/t20260417_1963350.html"
NBS_APRIL = "https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html"
NBS_MAY = "https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html"
NBS_JUNE = "https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html"
NBS_JULY = "https://www.stats.gov.cn/english/PressRelease/202608/t20260819_1965079.html"
KPLER_FEB_MAY = "https://www.hydrocarbonprocessing.com/news/2026/06/chinas-crude-oil-imports-slump-but-its-economics-not-altruism/"
KPLER_MARCH = "https://archive.is/PJQz3"
VORTEXA_JUNE = GAC_JUNE
VORTEXA_JULY = GAC_JULY


ROWS = [
    {
        "month": "2026-02",
        "days": 28,
        "customs_total_imports_mt": 48.045,
        "seaborne_imports_mbd": 11.39,
        "seaborne_vendor": "Kpler",
        "domestic_crude_production_mt": 35.73 * 28 / 59,
        "crude_processing_mt": 122.63 * 28 / 59,
        "official_period_status": "GAC monthly import observation; NBS Jan-Feb production and processing totals allocated by calendar days",
        "observed_comparator_mb": "",
        "observed_comparator_period": "none",
        "sign_check_total": "no monthly observed comparator",
        "sign_check_seaborne": "no monthly observed comparator",
        "customs_source": GAC_JAN_FEB,
        "nbs_source": NBS_JAN_FEB,
        "seaborne_source": KPLER_FEB_MAY,
    },
    {
        "month": "2026-03", "days": 31,
        "customs_total_imports_mt": 49.982, "seaborne_imports_mbd": 10.10,
        "seaborne_vendor": "Kpler (press-reported rounded value)",
        "domestic_crude_production_mt": 19.07, "crude_processing_mt": 61.67,
        "official_period_status": "monthly official observations",
        "observed_comparator_mb": 40, "observed_comparator_period": "IEA March crude-tank build",
        "sign_check_total": "match: build", "sign_check_seaborne": "match: small build",
        "customs_source": GAC_MARCH, "nbs_source": NBS_MARCH, "seaborne_source": KPLER_MARCH,
    },
    {
        "month": "2026-04", "days": 30,
        "customs_total_imports_mt": 38.50, "seaborne_imports_mbd": 8.10,
        "seaborne_vendor": "Kpler", "domestic_crude_production_mt": 17.94,
        "crude_processing_mt": 54.65, "official_period_status": "monthly official observations",
        "observed_comparator_mb": "", "observed_comparator_period": "Kpler: war-onset to mid-May visible tanks built about 25 mb (cross-month)",
        "sign_check_total": "consistent: build", "sign_check_seaborne": "DISAGREES: draw versus cross-month build",
        "customs_source": GAC_APRIL, "nbs_source": NBS_APRIL, "seaborne_source": KPLER_FEB_MAY,
    },
    {
        "month": "2026-05", "days": 31,
        "customs_total_imports_mt": 33.08, "seaborne_imports_mbd": 6.36,
        "seaborne_vendor": "Kpler", "domestic_crude_production_mt": 18.57,
        "crude_processing_mt": 53.72, "official_period_status": "monthly official observations",
        "observed_comparator_mb": "", "observed_comparator_period": "Kpler: +25 mb war-onset to mid-May; Kayrros/Energy Aspects: about -25 mb May to 7 June",
        "sign_check_total": "consistent with late-May draw; exact May sign not isolated by comparators",
        "sign_check_seaborne": "consistent with late-May draw but magnitude far larger than observed cross-month draw",
        "customs_source": GAC_MAY, "nbs_source": NBS_MAY, "seaborne_source": KPLER_FEB_MAY,
    },
    {
        "month": "2026-06", "days": 30,
        "customs_total_imports_mt": 29.27, "seaborne_imports_mbd": 6.00,
        "seaborne_vendor": "Vortexa (reported as around 6.0)", "domestic_crude_production_mt": 18.12,
        "crude_processing_mt": 51.24, "official_period_status": "monthly official observations",
        "observed_comparator_mb": -41, "observed_comparator_period": "IEA June crude-stock draw",
        "sign_check_total": "match: draw", "sign_check_seaborne": "match: draw; overstates magnitude",
        "customs_source": GAC_JUNE, "nbs_source": NBS_JUNE, "seaborne_source": VORTEXA_JUNE,
    },
    {
        "month": "2026-07", "days": 31,
        "customs_total_imports_mt": 35.73, "seaborne_imports_mbd": 7.10,
        "seaborne_vendor": "Vortexa", "domestic_crude_production_mt": 18.27,
        "crude_processing_mt": 53.11, "official_period_status": "monthly official observations",
        "observed_comparator_mb": "", "observed_comparator_period": "none located by 2026-08-20 cutoff",
        "sign_check_total": "no observed comparator; implies build", "sign_check_seaborne": "no observed comparator; implies draw and opposite total-balance sign",
        "customs_source": GAC_JULY, "nbs_source": NBS_JULY, "seaborne_source": VORTEXA_JULY,
    },
]


def rounded(value: float) -> str:
    return f"{value:.3f}"


def build() -> None:
    output_rows = []
    for row in ROWS:
        days = row["days"]
        imports_mb = row["customs_total_imports_mt"] * BBL_PER_TONNE
        production_mb = row["domestic_crude_production_mt"] * BBL_PER_TONNE
        processing_mb = row["crude_processing_mt"] * BBL_PER_TONNE
        total_change = imports_mb + production_mb - processing_mb
        seaborne_change = row["seaborne_imports_mbd"] * days + production_mb - processing_mb
        total_mbd = imports_mb / days
        gap_mbd = total_mbd - row["seaborne_imports_mbd"]
        # Sensitivity requested in the issue: vary the customs conversion alone by +/-2%,
        # holding the two NBS legs at the central factor to expose import-grade uncertainty.
        total_low = imports_mb * 0.98 + production_mb - processing_mb
        total_high = imports_mb * 1.02 + production_mb - processing_mb
        output_rows.append({
            **row,
            "customs_total_imports_mt": rounded(row["customs_total_imports_mt"]),
            "domestic_crude_production_mt": rounded(row["domestic_crude_production_mt"]),
            "crude_processing_mt": rounded(row["crude_processing_mt"]),
            "barrels_per_tonne": f"{BBL_PER_TONNE:.1f}",
            "customs_total_imports_mbd": rounded(total_mbd),
            "total_minus_seaborne_gap_mbd": rounded(gap_mbd),
            "pipeline_plus_tracking_gap_mb": rounded(gap_mbd * days),
            "domestic_crude_production_mbd": rounded(production_mb / days),
            "crude_processing_mbd": rounded(processing_mb / days),
            "implied_stock_change_total_imports_mb": rounded(total_change),
            "implied_stock_change_seaborne_imports_mb": rounded(seaborne_change),
            "total_import_balance_low_2pct_import_conversion_mb": rounded(min(total_low, total_high)),
            "total_import_balance_high_2pct_import_conversion_mb": rounded(max(total_low, total_high)),
        })

    fieldnames = list(output_rows[0].keys())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


if __name__ == "__main__":
    build()
