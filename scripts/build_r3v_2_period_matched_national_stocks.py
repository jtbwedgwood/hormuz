#!/usr/bin/env python3
"""Build the March-June 2026 national-stock endpoint audit.

The output is deliberately a *net stock-change* ledger, not an emergency-release
execution ledger.  Gross programme delivery can coexist with replenishment, transfers,
or reclassification, so no national net change is interpreted as gross IEA delivery.

Positive ``net_draw_million_bbl`` means stocks fell; negative means they rose.  The
Eurostat snapshot is frozen to the API response extracted on 2026-08-18 so the build is
reproducible even when preliminary national observations are revised later.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_r3v_2_period_matched_national_stocks.csv"

EUROSTAT_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
    "nrg_stk_oilm"
)
IEA_PLAN_URL = (
    "https://www.iea.org/news/iea-confirms-member-country-contributions-to-"
    "collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions"
)
EIA_SPR_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
EIA_COMM_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1"
JAPAN_FEB_URL = (
    "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/"
    "260415oil.pdf"
)
JAPAN_MAY_URL = (
    "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/"
    "260715oil.pdf"
)
JAPAN_JUNE_URL = (
    "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/"
    "260817oil.pdf"
)
JAPAN_JUNE_ESTAT_URL = (
    "https://www.e-stat.go.jp/stat-search/file-download?"
    "statInfId=000040491305&fileKind=2"
)
JAPAN_MONTHLY_MIRROR_URL = "https://opengov.jp/economy/energy/petroleum-reserves/"
JAPAN_JUNE_DAILY_MIRROR_URL = (
    "https://www.mie-sekiyu.or.jp/wp-content/uploads/2026/07/123.pdf"
)
JAPAN_PORTAL_URL = (
    "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/"
)
KOREA_NO_RELEASE_URL = "https://en.yna.co.kr/view/AEN20260526010800320"
KOREA_SWAP_URL = "https://en.yna.co.kr/view/AEN20260602006300320"
KOREA_SWAP_END_URL = "https://en.yna.co.kr/view/AEN20260630004352320"

BBL_PER_KL = 6.28981
BBL_PER_TONNE_GENERIC = 7.33

# IEA 19 March provisional stock-release contribution. Canada and Mexico are omitted
# here because their IEA contributions were production, not stocks.
PLAN = {
    "Australia": 4.8,
    "Austria": 2.4,
    "Belgium": 0.3,
    "Czechia": 2.2,
    "Denmark": 1.2,
    "Estonia": 0.3,
    "Finland": 1.8,
    "France": 14.6,
    "Germany": 19.5,
    "Greece": 2.0,
    "Hungary": 6.1,
    "Ireland": 1.7,
    "Italy": 10.0,
    "Japan": 79.8,
    "South Korea": 22.5,
    "Latvia": 0.3,
    "Lithuania": 0.6,
    "Luxembourg": 0.1,
    "Netherlands": 5.4,
    "New Zealand": 1.6,
    "Norway": 0.4,
    "Poland": 7.5,
    "Portugal": 2.0,
    "Slovak Republic": 0.0,
    "Spain": 11.6,
    "Sweden": 2.1,
    "Türkiye": 11.7,
    "United Kingdom": 14.0,
    "United States": 172.2,
}

# Official Eurostat nrg_stk_oilm snapshot extracted 2026-08-18 (API update timestamp
# 2026-08-13T23:00:00+0200).  Filter:
# stk_flow=STKCL_EUE, siec=O4000.  Unit reported by the API is thousand tonnes.
# ``None`` is a genuine missing observation in that API response, not a zero.
EUROSTAT = {
    "Austria": ("AT", {"2026-02": 2493.454, "2026-03": 2484.069, "2026-04": 2442.321, "2026-05": 2437.988, "2026-06": 2424.202}),
    "Belgium": ("BE", {"2026-02": 4274.0, "2026-03": 4341.1, "2026-04": 4469.9, "2026-05": 4467.0, "2026-06": 4463.4}),
    "Czechia": ("CZ", {"2026-02": 2158.0, "2026-03": 2161.0, "2026-04": 2065.0, "2026-05": 2067.0, "2026-06": 424.0}),
    "Denmark": ("DK", {"2026-02": 1225.564, "2026-03": 1237.307, "2026-04": 1200.0, "2026-05": 1193.916, "2026-06": None}),
    "Estonia": ("EE", {"2026-02": 267.0, "2026-03": 264.0, "2026-04": 247.0, "2026-05": 244.0, "2026-06": None}),
    "Finland": ("FI", {"2026-02": 3244.0, "2026-03": 3242.0, "2026-04": 3240.0, "2026-05": 3241.0, "2026-06": 3241.0}),
    "France": ("FR", {"2026-02": 16802.0, "2026-03": 16643.0, "2026-04": 16698.0, "2026-05": 16820.0, "2026-06": None}),
    "Germany": ("DE", {"2026-02": 20537.794, "2026-03": 20785.653, "2026-04": 20405.05, "2026-05": 20170.054, "2026-06": None}),
    "Greece": ("EL", {"2026-02": 3702.644, "2026-03": 3855.879, "2026-04": 3687.041, "2026-05": None, "2026-06": None}),
    "Hungary": ("HU", {"2026-02": 1344.1, "2026-03": 697.8, "2026-04": 1045.3, "2026-05": 942.0, "2026-06": None}),
    "Ireland": ("IE", {"2026-02": 1639.53, "2026-03": 1638.854, "2026-04": 1527.301, "2026-05": 1531.994, "2026-06": None}),
    "Italy": ("IT", {"2026-02": 11258.579, "2026-03": 11255.475, "2026-04": 9632.117, "2026-05": 9609.626, "2026-06": None}),
    "Latvia": ("LV", {"2026-02": 378.26, "2026-03": 381.411, "2026-04": 381.411, "2026-05": 381.411, "2026-06": None}),
    "Lithuania": ("LT", {"2026-02": 647.9, "2026-03": 570.6, "2026-04": 550.3, "2026-05": 569.7, "2026-06": None}),
    "Luxembourg": ("LU", {"2026-02": 668.629, "2026-03": 660.244, "2026-04": 661.836, "2026-05": 661.836, "2026-06": None}),
    "Netherlands": ("NL", {"2026-02": 4487.0, "2026-03": 4455.0, "2026-04": 4491.0, "2026-05": None, "2026-06": None}),
    "Norway": ("NO", {"2026-02": 0.0, "2026-03": 0.0, "2026-04": 0.0, "2026-05": 0.0, "2026-06": None}),
    "Poland": ("PL", {"2026-02": 8033.883, "2026-03": 8026.953, "2026-04": 8025.56, "2026-05": 8027.692, "2026-06": None}),
    "Portugal": ("PT", {"2026-02": 2604.635, "2026-03": 2595.69, "2026-04": 2584.278, "2026-05": None, "2026-06": None}),
    "Slovak Republic": ("SK", {"2026-02": 842.662, "2026-03": 802.662, "2026-04": 842.662, "2026-05": 842.662, "2026-06": None}),
    "Spain": ("ES", {"2026-02": 14354.696, "2026-03": 14021.168, "2026-04": 14492.98, "2026-05": 15222.471, "2026-06": None}),
    "Sweden": ("SE", {"2026-02": 2160.761, "2026-03": 2328.438, "2026-04": 2136.637, "2026-05": 2122.421, "2026-06": None}),
    "Türkiye": ("TR", {"2026-02": None, "2026-03": 0.0, "2026-04": 0.0, "2026-05": 0.0, "2026-06": None}),
}

MONTH_END = {
    "2026-02": "2026-02-28",
    "2026-03": "2026-03-31",
    "2026-04": "2026-04-30",
    "2026-05": "2026-05-31",
    "2026-06": "2026-06-30",
}

FIELDS = [
    "row_id",
    "record_type",
    "geography",
    "iso2",
    "stock_scope",
    "ownership",
    "program_plan_million_bbl",
    "period_start",
    "period_end",
    "period_match_status",
    "start_native",
    "end_native",
    "native_unit",
    "net_draw_million_bbl",
    "gross_release_observed_million_bbl",
    "conversion_or_method",
    "source_status",
    "confidence",
    "include_in_r3v1_t1",
    "exclusion_reason",
    "source_publication_date",
    "source_url",
    "notes",
    "double_counting_rule",
]


def fmt(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(row_id: str, record_type: str, geography: str, **values: object) -> dict[str, str]:
    out = {field: "" for field in FIELDS}
    out.update({"row_id": row_id, "record_type": record_type, "geography": geography})
    for key, value in values.items():
        out[key] = fmt(value)
    return out


def japan_rows() -> list[dict[str, str]]:
    # Official monthly product-equivalent quantities are in million kl.  METI's August
    # release reports the exact June month-end endpoint, superseding the earlier estimate
    # derived from June 26 days of cover.
    categories = {
        "public_national_stock": (41.11, 29.67),
        "obligated_private_industry_stock": (25.73, 26.81),
        "producer_country_joint_stock": (1.79, 0.76),
    }
    result: list[dict[str, str]] = []
    for ownership, (feb_kl, june_kl) in categories.items():
        draw = (feb_kl - june_kl) * BBL_PER_KL
        slug = ownership.replace("_stock", "").replace("_", "-")
        result.append(
            row(
                f"japan-{slug}-feb-to-jun26",
                "period_matched_stock_change",
                "Japan",
                iso2="JP",
                stock_scope="oil_reserves_product_equivalent",
                ownership=ownership,
                program_plan_million_bbl=PLAN["Japan"],
                period_start="2026-02-28",
                period_end="2026-06-30",
                period_match_status="exact_month_end",
                start_native=feb_kl,
                end_native=june_kl,
                native_unit="million_kl_product_equivalent",
                net_draw_million_bbl=draw,
                conversion_or_method=(
                    f"February minus June official month-end product-equivalent volume; "
                    f"{BBL_PER_KL} bbl/kl"
                ),
                source_status="official_monthly_product_equivalent_volume",
                confidence="high_native_volume_medium_barrel_conversion",
                include_in_r3v1_t1="yes",
                exclusion_reason="",
                source_publication_date="2026-08-17",
                source_url=(
                    f"{JAPAN_FEB_URL} | {JAPAN_JUNE_URL} | {JAPAN_JUNE_ESTAT_URL} | "
                    f"{JAPAN_PORTAL_URL}"
                ),
                notes=(
                    "METI reflects national and producer-country joint releases when "
                    "refiner receipt is confirmed. Product-equivalent volume is used "
                    "because it is comparable across the three ownership categories."
                ),
                double_counting_rule=(
                    "Net stock change only. Nested inside the IEA observed-stock composite; "
                    "do not add to the IEA collective-release aggregate or Japan schedules."
                ),
            )
        )
    return result


def eurostat_rows() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for country, (iso2, observations) in EUROSTAT.items():
        start = observations["2026-02"]
        available = [(month, value) for month, value in observations.items() if value is not None]
        end_month, end = available[-1]
        exact = start is not None and observations["2026-06"] is not None
        net_draw = None if start is None or end is None else (start - end) * BBL_PER_TONNE_GENERIC / 1000
        plan = PLAN.get(country, 0.0)

        # Czechia's published June observation is a discontinuity: an 80% one-month fall
        # and a converted draw nearly six times its IEA allocation.  Preserve it in the
        # ledger, but do not promote it to T1 until a national source confirms the break.
        continuity_hold = (
            country == "Czechia"
            and observations["2026-05"] is not None
            and observations["2026-06"] is not None
            and observations["2026-06"] < observations["2026-05"] * 0.5
        )
        if exact and not continuity_hold:
            include = "yes"
            exclusion = ""
        elif continuity_hold:
            include = "no_data_quality_hold"
            exclusion = (
                "June level fell 79.5% month on month; implied 12.71 mb draw is 5.8x the "
                "2.2 mb programme plan and lacks national corroboration."
            )
        else:
            include = "no_period_mismatch"
            exclusion = f"Latest public observation is {end_month}, not June."

        result.append(
            row(
                f"eurostat-{iso2.lower()}-feb-to-{end_month}",
                "period_matched_stock_change" if exact else "partial_stock_change",
                country,
                iso2=iso2,
                stock_scope="closing_EU_emergency_stock_all_oil_and_petroleum_products",
                ownership="all_holders_mixed_not_separable_in_selected_series",
                program_plan_million_bbl=plan,
                period_start="2026-02-28" if start is not None else "",
                period_end=MONTH_END[end_month],
                period_match_status="exact_month_end" if exact else "partial_latest_public_month",
                start_native=start,
                end_native=end,
                native_unit="thousand_tonnes",
                net_draw_million_bbl=net_draw,
                conversion_or_method=(
                    f"February minus latest available closing stock; generic "
                    f"{BBL_PER_TONNE_GENERIC} bbl/tonne because product mix varies."
                ),
                source_status="official_eurostat_api_snapshot_extracted_2026-08-18",
                confidence="medium_high_net_tonnes_medium_converted_barrels",
                include_in_r3v1_t1=include,
                exclusion_reason=exclusion,
                source_publication_date="API updated 2026-08-13T23:00:00+0200",
                source_url=EUROSTAT_URL,
                notes=(
                    "Negative net draw means an observed stock build, not zero delivery. "
                    "The selected aggregate does not separate government and obligated holders."
                ),
                double_counting_rule=(
                    "Net national stock movement inside the IEA observed-stock composite. "
                    "Do not add to gross collective-action delivery."
                ),
            )
        )
    return result


def build_rows() -> list[dict[str, str]]:
    rows = [
        row(
            "us-spr-feb27-to-jun26",
            "already_observed_reference",
            "United States",
            iso2="US",
            stock_scope="strategic_petroleum_reserve_crude",
            ownership="public_government_stock",
            program_plan_million_bbl=PLAN["United States"],
            period_start="2026-02-27",
            period_end="2026-06-26",
            period_match_status="near_match_weekly_month_end_proxy",
            start_native=415.441,
            end_native=325.655,
            native_unit="million_bbl",
            net_draw_million_bbl=89.786,
            conversion_or_method="Direct weekly EIA stock level difference.",
            source_status="official_weekly_observation",
            confidence="high",
            include_in_r3v1_t1="already_present",
            source_publication_date="2026-07-01",
            source_url=EIA_SPR_URL,
            notes="Existing r3v.1 T1 component; repeated here only to make coverage explicit.",
            double_counting_rule="Already in r3v.1 and the IEA observed-stock composite.",
        ),
        row(
            "us-commercial-total-feb27-to-jun26",
            "already_observed_reference",
            "United States",
            iso2="US",
            stock_scope="total_commercial_petroleum_excluding_SPR",
            ownership="ordinary_commercial_stock",
            period_start="2026-02-27",
            period_end="2026-06-26",
            period_match_status="near_match_weekly_month_end_proxy",
            net_draw_million_bbl=67.317,
            conversion_or_method="Sum of weekly month-end-proxy changes for March-June.",
            source_status="official_weekly_observation",
            confidence="high",
            include_in_r3v1_t1="already_present",
            source_publication_date="2026-07-01",
            source_url=EIA_COMM_URL,
            notes="Ordinary commercial stock movement, not emergency-program delivery.",
            double_counting_rule="Already in r3v.1 and the IEA observed-stock composite.",
        ),
    ]
    rows.extend(japan_rows())
    rows.extend(eurostat_rows())
    rows.extend(
        [
            row(
                "korea-government-crude-swap-through-jun2",
                "official_gross_execution_statement_not_stock_series",
                "South Korea",
                iso2="KR",
                stock_scope="government_strategic_reserve_crude",
                ownership="public_government_stock",
                program_plan_million_bbl=PLAN["South Korea"],
                period_start="2026-04-01",
                period_end="2026-06-02",
                period_match_status="gross_swap_execution_inside_window_not_net_tank_change",
                gross_release_observed_million_bbl=21.0,
                conversion_or_method=(
                    "Industry ministry said 21 million barrels had been lent from government "
                    "reserves to refiners through the crude-swap system; refiners must restore "
                    "the barrels later."
                ),
                source_status="attributed_official_statement_reported_by_yonhap",
                confidence="medium_high_for_gross_swap_none_for_net_stock_change",
                include_in_r3v1_t1="no_gross_execution_not_net_stock_endpoint",
                exclusion_reason=(
                    "Gross reserve lending is not a comparable February-June net tank change, "
                    "and the public statement does not identify it as delivery against the IEA pledge."
                ),
                source_publication_date="2026-06-02; wind-down confirmed 2026-06-30",
                source_url=f"{KOREA_SWAP_URL} | {KOREA_SWAP_END_URL}",
                notes=(
                    "This upgrades Korea from an execution unknown: 21 mb of gross strategic "
                    "reserve swaps were executed. It does not establish the June closing stock "
                    "or how much the IEA counted toward Korea's 22.5 mb provisional contribution."
                ),
                double_counting_rule=(
                    "Gross programme evidence only. Do not add to net national stock changes or "
                    "to the IEA collective-release aggregate without an explicit reconciliation."
                ),
            ),
            row(
                "korea-government-release-status-may26",
                "official_execution_statement_not_stock_series",
                "South Korea",
                iso2="KR",
                stock_scope="government_strategic_reserves",
                ownership="public_government_stock",
                program_plan_million_bbl=PLAN["South Korea"],
                period_start="2026-03-11",
                period_end="2026-05-26",
                period_match_status="statement_only_not_june_endpoint",
                gross_release_observed_million_bbl=0.0,
                conversion_or_method=(
                    "Deputy minister said the government was still determining timing and "
                    "viewed the release as a final card."
                ),
                source_status="attributed_official_statement_reported_by_yonhap",
                confidence="medium_high_through_statement_date_none_for_june_stock_level",
                include_in_r3v1_t1="no_not_stock_change_and_not_june",
                exclusion_reason="No comparable public June tank-level series was found.",
                source_publication_date="2026-05-26",
                source_url=KOREA_NO_RELEASE_URL,
                notes=(
                    "This contradicts imputing the 22.46 mb plan as a Korean draw by May. "
                    "It does not prove no action occurred after May 26."
                ),
                double_counting_rule="Context only; do not add zero or the plan to stock totals.",
            ),
        ]
    )

    for country in ["Australia", "New Zealand", "United Kingdom"]:
        rows.append(
            row(
                f"{country.lower().replace(' ', '-')}-public-series-gap",
                "availability_gap",
                country,
                stock_scope="IEA_contribution_stock_channel",
                ownership="country_specific_not_observed_here",
                program_plan_million_bbl=PLAN[country],
                period_start="2026-02-28",
                period_end="2026-06-30",
                period_match_status="no_comparable_public_endpoint_located",
                source_status="coverage_audit_gap",
                confidence="none_for_stock_change",
                include_in_r3v1_t1="no_no_public_series",
                exclusion_reason="No comparable public March-June tank-level series located in this audit.",
                source_publication_date="audit cutoff 2026-08-05",
                source_url=IEA_PLAN_URL,
                notes="Country remains inside the residual of the IEA observed-stock composite.",
                double_counting_rule="Do not substitute programme allocation for observed stock change.",
            )
        )
    return rows


def main() -> None:
    rows = build_rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    promoted = [r for r in rows if r["include_in_r3v1_t1"] == "yes"]
    promoted_total = sum(float(r["net_draw_million_bbl"]) for r in promoted)
    exact_eu = [
        r for r in rows
        if r["record_type"] == "period_matched_stock_change"
        and r["geography"] != "Japan"
    ]
    czech = next(r for r in rows if r["geography"] == "Czechia")

    assert len(rows) == len({r["row_id"] for r in rows})
    assert len(exact_eu) == 4
    assert czech["include_in_r3v1_t1"] == "no_data_quality_hold"
    assert abs(promoted_total - 70.782240) < 1e-6, promoted_total
    assert any(float(r["net_draw_million_bbl"]) < 0 for r in promoted)

    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"new signed national observations promoted to r3v.1 T1: {promoted_total:.6f} mb")
    print("Exact June endpoints: Japan; Eurostat Austria, Belgium, Czechia, Finland")
    print("Czechia retained in ledger but held out of T1 pending continuity confirmation")


if __name__ == "__main__":
    main()
