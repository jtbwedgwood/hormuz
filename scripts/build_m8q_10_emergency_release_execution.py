#!/usr/bin/env python3
"""Build the March-July 2026 emergency-oil release execution audit."""

from __future__ import annotations

import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_10_emergency_release_execution.csv"

IEA_PLAN_URL = "https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions"
IEA_ACTUAL_URL = "https://www.iea.org/news/iea-executive-director-statement-on-oil-markets"
EIA_API_URL = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"
EIA_SERIES_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
EIA_FEB_STEO = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
EUROSTAT_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_stk_oilm"
JAPAN_FEB_URL = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260415oil.pdf"
JAPAN_APR_URL = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260615oil.pdf"
JAPAN_RELEASE_URL = "https://www.enecho.meti.go.jp/category/others/energysecurity/"

# Reproducible snapshots of the official API observations extracted on 2026-08-04.
# The live endpoints are still queried first; these values make regeneration robust
# to transient EIA throttling or Eurostat outages.
EIA_SPR_SNAPSHOT = {
    "2026-02-27": 415.441,
    "2026-07-17": 311.447,
    "2026-07-24": 307.650,
}
EUROSTAT_SNAPSHOT = {
    ("DE", "2026-02"): 20537.794,
    ("DE", "2026-05"): 20170.054,
    ("FR", "2026-02"): 16802.000,
    ("FR", "2026-05"): 16820.000,
    ("IT", "2026-02"): 11258.579,
    ("IT", "2026-05"): 9609.626,
    ("ES", "2026-02"): 14354.696,
    ("ES", "2026-05"): 15222.471,
}

FIELDS = [
    "row_id",
    "record_type",
    "geography",
    "period_start",
    "period_end",
    "as_of_date",
    "channel",
    "ownership",
    "measure",
    "native_value",
    "native_unit",
    "program_plan_million_bbl",
    "observed_or_confirmed_million_bbl",
    "estimate_low_million_bbl",
    "estimate_base_million_bbl",
    "estimate_high_million_bbl",
    "unit",
    "evidence_status",
    "method",
    "confidence",
    "source_publication_date",
    "source_url",
    "notes",
    "double_counting_rule",
]


PLAN = [
    # country, total, public, obligated, production, crude, products
    ("Australia", 4.8, 0.0, 4.8, 0.0, 0.0, 4.8),
    ("Austria", 2.4, 2.4, 0.0, 0.0, 2.4, 0.0),
    ("Belgium", 0.3, None, None, 0.0, None, None),
    ("Canada", 23.6, 0.0, 0.0, 23.6, 23.6, 0.0),
    ("Czechia", 2.2, 2.2, 0.0, 0.0, 2.2, 0.0),
    ("Denmark", 1.2, 1.2, 0.0, 0.0, 0.0, 1.2),
    ("Estonia", 0.3, 0.3, 0.0, 0.0, 0.0, 0.3),
    ("Finland", 1.8, None, None, 0.0, None, None),
    ("France", 14.6, None, None, 0.0, None, None),
    ("Germany", 19.5, 19.5, 0.0, 0.0, None, None),
    ("Greece", 2.0, None, None, 0.0, None, None),
    ("Hungary", 6.1, 6.1, 0.0, 0.0, 0.0, 6.1),
    ("Ireland", 1.7, 1.7, 0.0, 0.0, 0.2, 1.5),
    ("Italy", 10.0, 0.0, 10.0, 0.0, 0.0, 10.0),
    ("Japan", 79.8, 54.0, 25.8, 0.0, 54.0, 25.8),
    ("South Korea", 22.5, None, None, 0.0, None, None),
    ("Latvia", 0.3, None, None, 0.0, None, None),
    ("Lithuania", 0.6, 0.0, 0.6, 0.0, 0.0, 0.6),
    ("Luxembourg", 0.1, 0.0, 0.1, 0.0, 0.1, 0.0),
    ("Mexico", 3.9, 0.0, 0.0, 3.9, 3.9, 0.0),
    ("Netherlands", 5.4, None, None, 0.0, None, None),
    ("New Zealand", 1.6, 1.6, 0.0, 0.0, 1.3, 0.3),
    ("Norway", 0.4, 0.0, 0.4, 0.0, 0.0, 0.4),
    ("Poland", 7.5, 0.0, 7.5, 0.0, 6.0, 1.5),
    ("Portugal", 2.0, 0.0, 2.0, 0.0, 0.0, 2.0),
    ("Spain", 11.6, 0.0, 11.6, 0.0, 0.0, 11.6),
    ("Sweden", 2.1, 0.0, 2.1, 0.0, 0.0, 2.1),
    ("Türkiye", 11.7, 0.0, 11.7, 0.0, 3.6, 8.1),
    ("United Kingdom", 14.0, 0.0, 14.0, 0.0, 4.3, 9.7),
    ("United States", 172.2, 172.2, 0.0, 0.0, 172.2, 0.0),
]


def fmt(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def make_row(row_id: str, record_type: str, geography: str, **kwargs: object) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row.update({"row_id": row_id, "record_type": record_type, "geography": geography})
    for key, value in kwargs.items():
        row[key] = fmt(value) if isinstance(value, float) else str(value)
    return row


def fetch_json(url: str, params: list[tuple[str, str]]) -> dict:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{url}?{query}", headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def fetch_us_spr() -> dict[str, float]:
    try:
        payload = fetch_json(
            EIA_API_URL,
            [
                ("api_key", "DEMO_KEY"),
                ("frequency", "weekly"),
                ("data[0]", "value"),
                ("facets[series][]", "WCSSTUS1"),
                ("start", "2026-02-27"),
                ("end", "2026-07-24"),
                ("sort[0][column]", "period"),
                ("sort[0][direction]", "asc"),
                ("offset", "0"),
                ("length", "5000"),
            ],
        )
        stock = {item["period"]: float(item["value"]) / 1000 for item in payload["response"]["data"]}
        if not EIA_SPR_SNAPSHOT.keys() <= stock.keys():
            raise ValueError("live EIA response omitted a required endpoint")
        return stock
    except (urllib.error.URLError, TimeoutError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"warning: live EIA request failed ({exc}); using the 2026-08-04 official-data snapshot")
        return dict(EIA_SPR_SNAPSHOT)


def eurostat_value(geo: str, month: str) -> float:
    try:
        payload = fetch_json(
            EUROSTAT_URL,
            [
                ("lang", "en"),
                ("geo", geo),
                ("stk_flow", "STKCL_EUE"),
                ("siec", "O4000"),
                ("time", month),
            ],
        )
        value = payload.get("value", {}).get("0")
        if value is None:
            raise ValueError(f"Eurostat missing {geo} {month}")
        return float(value)
    except (urllib.error.URLError, TimeoutError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        key = (geo, month)
        if key not in EUROSTAT_SNAPSHOT:
            raise
        print(f"warning: live Eurostat request failed for {geo} {month} ({exc}); using the 2026-08-04 official-data snapshot")
        return EUROSTAT_SNAPSHOT[key]


def plan_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for country, total, public, obligated, production, crude, products in PLAN:
        if production:
            ownership = "production_increase_not_stock"
        elif public is None:
            ownership = "stock_ownership_not_final_on_2026-03-19"
        elif public and obligated:
            ownership = "public_and_obligated_industry"
        elif public:
            ownership = "public_stock"
        else:
            ownership = "obligated_industry_stock"
        rows.append(
            make_row(
                f"plan_{country.lower().replace(' ', '_').replace('ü', 'u')}",
                "provisional_program_plan",
                country,
                period_start="2026-03-11",
                period_end="2026-03-19",
                as_of_date="2026-03-19",
                channel="production_increase" if production else "emergency_stock_release",
                ownership=ownership,
                measure="provisional_total_contribution",
                program_plan_million_bbl=total,
                unit="million_bbl",
                evidence_status="provisional_plan_not_delivery",
                method=f"IEA table transcription; public={fmt(public)}, obligated={fmt(obligated)}, production={fmt(production)}, crude={fmt(crude)}, products={fmt(products)} million bbl.",
                confidence="high_for_plan_none_for_execution",
                source_publication_date="2026-03-19",
                source_url=IEA_PLAN_URL,
                notes="IEA states that the ownership and crude/product splits were not final.",
                double_counting_rule="Do not add a plan row to actual stock decline, delivery, or the 290 million barrel collective total.",
            )
        )
    for slug, ownership, amount in [
        ("public", "public_stock", 280.0),
        ("obligated_industry", "obligated_industry_stock", 119.0),
        ("production", "production_increase_not_stock", 28.0),
        ("headline_total", "all_channels", 426.0),
    ]:
        rows.append(
            make_row(
                f"plan_summary_{slug}",
                "provisional_program_summary",
                "IEA members",
                period_start="2026-03-11",
                period_end="2026-03-19",
                as_of_date="2026-03-19",
                channel="production_increase" if slug == "production" else "collective_action",
                ownership=ownership,
                measure="published_rounded_channel_total",
                program_plan_million_bbl=amount,
                unit="million_bbl_rounded",
                evidence_status="provisional_plan_not_delivery",
                method="IEA published rounded channel or headline total.",
                confidence="high_for_plan_none_for_execution",
                source_publication_date="2026-03-19",
                source_url=IEA_PLAN_URL,
                notes="Rounded components sum to 427 million barrels while the headline is 426; rounded country entries sum to 426.2. This is source rounding, not an accounting discrepancy.",
                double_counting_rule="Summary row; never add to country plan rows, actual stock declines, or the 290 million barrel actual total.",
            )
        )
    return rows


def us_rows(stock: dict[str, float]) -> tuple[list[dict[str, str]], dict[str, float]]:
    required = ["2026-02-27", "2026-07-17", "2026-07-24"]
    missing = [date for date in required if date not in stock]
    if missing:
        raise ValueError(f"EIA SPR observations missing: {missing}")
    feb = stock["2026-02-27"]
    jul17 = stock["2026-07-17"]
    jul24 = stock["2026-07-24"]
    draw_to_jul17 = feb - jul17
    draw_to_jul24 = feb - jul24
    jul21_level = jul17 + (jul24 - jul17) * 4 / 7
    draw_to_jul21 = feb - jul21_level
    latest_week_draw = jul17 - jul24
    july_end_base = draw_to_jul24 + latest_week_draw
    july_end_stock_base = feb - july_end_base
    feb_steo_july = 423.861
    rows = [
        make_row("us_spr_2026-02-27", "stock_observation", "United States", period_start="2026-02-27", period_end="2026-02-27", as_of_date="2026-02-27", channel="public_stock", ownership="federal_SPR", measure="ending_stock", observed_or_confirmed_million_bbl=feb, unit="million_bbl", evidence_status="weekly_observation", method="EIA weekly SPR stock level.", confidence="high", source_publication_date="weekly", source_url=EIA_SERIES_URL, notes="Last weekly observation before the 28 February conflict start.", double_counting_rule="Stock level, not supply; only the change between non-overlapping endpoints is additive."),
        make_row("us_spr_2026-07-17", "stock_observation", "United States", period_start="2026-07-17", period_end="2026-07-17", as_of_date="2026-07-17", channel="public_stock", ownership="federal_SPR", measure="ending_stock", observed_or_confirmed_million_bbl=jul17, unit="million_bbl", evidence_status="weekly_observation", method="EIA weekly SPR stock level.", confidence="high", source_publication_date="weekly", source_url=EIA_SERIES_URL, notes="Last weekly endpoint fully preceding the IEA's 21 July statement.", double_counting_rule="Stock level, not supply."),
        make_row("us_spr_2026-07-24", "stock_observation", "United States", period_start="2026-07-24", period_end="2026-07-24", as_of_date="2026-07-24", channel="public_stock", ownership="federal_SPR", measure="ending_stock", observed_or_confirmed_million_bbl=jul24, unit="million_bbl", evidence_status="weekly_observation", method="EIA weekly SPR stock level.", confidence="high", source_publication_date="weekly", source_url=EIA_SERIES_URL, notes="Latest weekly observation used in this audit.", double_counting_rule="Stock level, not supply."),
        make_row("us_spr_draw_2026-02-27_2026-07-24", "physical_stock_change", "United States", period_start="2026-02-27", period_end="2026-07-24", as_of_date="2026-07-24", channel="public_stock", ownership="federal_SPR", measure="net_tank_draw", program_plan_million_bbl=172.2, observed_or_confirmed_million_bbl=draw_to_jul24, estimate_low_million_bbl=draw_to_jul24, estimate_base_million_bbl=draw_to_jul24, estimate_high_million_bbl=draw_to_jul24, unit="million_bbl", evidence_status="observed_physical_stock_change", method="415.441 minus 307.650 million barrels from EIA weekly endpoints.", confidence="high_for_stock_change_medium_high_for_program_attribution", source_publication_date="weekly through 2026-07-24", source_url=EIA_SERIES_URL, notes="A tank draw is stronger evidence than contracts awarded, but may include timing adjustments or other authorized movements; the 2026 emergency exchange requires later return barrels with a premium.", double_counting_rule="Use this physical draw instead of DOE contract awards or delivery checkpoints, never in addition to them."),
        make_row("us_spr_draw_2026-02-27_2026-07-21", "execution_estimate", "United States", period_start="2026-02-27", period_end="2026-07-21", as_of_date="2026-07-21", channel="public_stock", ownership="federal_SPR", measure="net_tank_draw_aligned_to_iea_asof", program_plan_million_bbl=172.2, observed_or_confirmed_million_bbl=draw_to_jul17, estimate_low_million_bbl=draw_to_jul17, estimate_base_million_bbl=draw_to_jul21, estimate_high_million_bbl=draw_to_jul24, unit="million_bbl", evidence_status="bounded_interpolation", method="Low is the 17 July observed draw; base linearly interpolates four of seven days from the 17-24 July weekly change; high is the 24 July observed draw.", confidence="medium_high", source_publication_date="weekly through 2026-07-24", source_url=EIA_SERIES_URL, notes="The base estimate is only an as-of-date alignment; EIA does not publish a daily SPR series.", double_counting_rule="This is the U.S. component used in the 290 million barrel top-down reconciliation."),
        make_row("us_feb_steo_july_spr", "counterfactual_forecast", "United States", period_start="2026-07-01", period_end="2026-07-31", as_of_date="2026-02-10", channel="public_stock", ownership="federal_SPR", measure="forecast_july_end_stock", observed_or_confirmed_million_bbl=feb_steo_july, unit="million_bbl", evidence_status="frozen_prewar_forecast", method="EIA February 2026 STEO monthly forecast.", confidence="high_for_forecast_vintage", source_publication_date="2026-02-10", source_url=EIA_FEB_STEO, notes="The prewar STEO expected the SPR to rise 8.420 million barrels from the 27 February weekly level by end-July.", double_counting_rule="Counterfactual level, not delivered oil."),
        make_row("us_july_end_nowcast", "nowcast", "United States", period_start="2026-07-25", period_end="2026-07-31", as_of_date="2026-07-31", channel="public_stock", ownership="federal_SPR", measure="july_end_net_draw_from_2026-02-27", observed_or_confirmed_million_bbl=draw_to_jul24, estimate_low_million_bbl=draw_to_jul24, estimate_base_million_bbl=july_end_base, estimate_high_million_bbl=july_end_base + latest_week_draw, unit="million_bbl", evidence_status="nowcast_after_latest_weekly_observation", method="Low freezes the 24 July draw; base repeats the 17-24 July weekly draw once; high repeats it twice as an explicit acceleration sensitivity.", confidence="low_medium", source_publication_date="2026-07-24 observation", source_url=EIA_SERIES_URL, notes=f"Base implies a {fmt(july_end_stock_base)} million barrel July-end SPR, {fmt(feb_steo_july - july_end_stock_base)} million barrels below the frozen February forecast.", double_counting_rule="Use only when the accounting cutoff is 31 July; replace with the next observed weekly value when available."),
    ]
    return rows, {"draw_jul17": draw_to_jul17, "draw_jul21": draw_to_jul21, "draw_jul24": draw_to_jul24}


def implementation_event_rows() -> list[dict[str, str]]:
    specs = [
        ("us_award_2026-03-20", "United States", "2026-03-20", "exchange_contract_award", 45.2, "public_stock_exchange", "First shipments began; 55 million barrels are contractually due back later.", "https://www.energy.gov/hgeo/articles/energy-department-begins-delivering-spr-barrels-record-speeds"),
        ("us_award_2026-04-10", "United States", "2026-04-10", "exchange_contract_award", 8.5, "public_stock_exchange", "Deliveries could begin immediately.", "https://www.energy.gov/hgeo/opr/articles/energy-department-awards-contracts-85-million-barrels-spr-second-phase-emergency"),
        ("us_award_2026-04-17", "United States", "2026-04-17", "exchange_contract_award", 26.0, "public_stock_exchange", "DOE separately said more than 10 million barrels had been delivered by this date.", "https://www.energy.gov/hgeo/opr/articles/energy-department-awards-new-contracts-strategic-petroleum-reserve-advancing"),
        ("us_award_2026-05-11", "United States", "2026-05-11", "exchange_contract_award", 53.3, "public_stock_exchange", "DOE said about 35 million barrels had been delivered by this date; cumulative awards were about 133 million barrels.", "https://www.energy.gov/hgeo/opr/articles/energy-department-awards-contracts-strategic-petroleum-reserve-advancing"),
        ("us_delivery_checkpoint_2026-05-11", "United States", "2026-05-11", "reported_delivered_to_market", 35.0, "public_stock_exchange", "DOE reported approximately 35 million barrels delivered to date.", "https://www.energy.gov/hgeo/opr/articles/energy-department-awards-contracts-strategic-petroleum-reserve-advancing"),
        ("japan_private_relief_2026-03-16", "Japan", "2026-03-16", "obligation_relief_days", 15.0, "obligated_industry_stock", "Private obligation cut from 70 to 55 days; this authorizes use but is not proof that every relieved barrel left tanks.", "https://www.meti.go.jp/english/press/2026/0316_003.html"),
        ("japan_first_release_2026-03-26", "Japan", "2026-03-26", "scheduled_site_release", 8.5 * 6.28981, "public_national_crude", "8.5 million kilolitres scheduled sequentially from 26 March; METI later posted site start timestamps.", "https://www.meti.go.jp/english/press/2026/0324_001.html"),
        ("japan_second_release_2026-05-01", "Japan", "2026-05-01", "scheduled_site_release", 5.8 * 6.28981, "public_national_crude", "5.8 million kilolitres scheduled from 1 May; site schedule reached into mid-May.", "https://www.meti.go.jp/english/press/2026/0424_004.html"),
    ]
    rows = []
    for row_id, geography, event_date, measure, value, ownership, notes, url in specs:
        is_days = measure == "obligation_relief_days"
        rows.append(make_row(row_id, "implementation_event", geography, period_start=event_date, period_end=event_date, as_of_date=event_date, channel="emergency_stock_release", ownership=ownership, measure=measure, native_value=value if is_days else None, native_unit="days" if is_days else "", observed_or_confirmed_million_bbl=None if is_days else value, unit="days" if is_days else "million_bbl", evidence_status="official_notice_or_checkpoint", method="Direct official notice transcription; a contract, schedule, obligation reduction, and delivered checkpoint are deliberately separate record types.", confidence="high_for_notice_varies_for_physical_delivery", source_publication_date=event_date, source_url=url, notes=notes, double_counting_rule="Implementation-event rows are milestones, not additive to tank-level stock changes or the IEA 290 million barrel total."))
    return rows


def japan_rows() -> tuple[list[dict[str, str]], dict[str, float]]:
    kl_to_bbl = 6.28981
    categories = [
        ("national", "public_national_stock", 41.11, 35.42),
        ("private", "obligated_industry_stock", 25.73, 23.68),
        ("producer_joint", "producer_country_joint_stock", 1.79, 0.19),
    ]
    rows: list[dict[str, str]] = []
    total_draw = 0.0
    for slug, ownership, feb_million_kl, apr_million_kl in categories:
        feb = feb_million_kl * kl_to_bbl
        apr = apr_million_kl * kl_to_bbl
        draw = feb - apr
        total_draw += draw
        rows.extend([
            make_row(f"japan_{slug}_2026-02-28", "stock_observation", "Japan", period_start="2026-02-28", period_end="2026-02-28", as_of_date="2026-02-28", channel="emergency_stock", ownership=ownership, measure="ending_stock_product_equivalent", native_value=feb_million_kl, native_unit="million_kl", observed_or_confirmed_million_bbl=feb, unit="million_bbl", evidence_status="official_monthly_observation", method=f"METI product-equivalent holding {feb_million_kl} million kl times 6.28981 bbl/kl.", confidence="high", source_publication_date="2026-04-15", source_url=JAPAN_FEB_URL, notes="Last official month-end before release implementation.", double_counting_rule="Stock level, not supply."),
            make_row(f"japan_{slug}_2026-04-30", "stock_observation", "Japan", period_start="2026-04-30", period_end="2026-04-30", as_of_date="2026-04-30", channel="emergency_stock", ownership=ownership, measure="ending_stock_product_equivalent", native_value=apr_million_kl, native_unit="million_kl", observed_or_confirmed_million_bbl=apr, unit="million_bbl", evidence_status="official_monthly_observation", method=f"METI product-equivalent holding {apr_million_kl} million kl times 6.28981 bbl/kl.", confidence="high", source_publication_date="2026-06-15", source_url=JAPAN_APR_URL, notes="METI records national/joint stock release only after refiner receipt is confirmed.", double_counting_rule="Stock level, not supply."),
            make_row(f"japan_{slug}_draw_to_2026-04-30", "physical_stock_change", "Japan", period_start="2026-02-28", period_end="2026-04-30", as_of_date="2026-04-30", channel="emergency_stock_release", ownership=ownership, measure="net_tank_draw", observed_or_confirmed_million_bbl=draw, estimate_low_million_bbl=draw, estimate_base_million_bbl=draw, estimate_high_million_bbl=draw, unit="million_bbl", evidence_status="receiver_confirmed_net_stock_change", method="Official February month-end holding minus official April month-end holding.", confidence="high_for_net_change_medium_high_for_release_attribution", source_publication_date="2026-06-15", source_url=f"{JAPAN_FEB_URL} | {JAPAN_APR_URL}", notes="Net change can understate gross delivery if stocks were replenished during the interval.", double_counting_rule="Components sum to the Japan observed floor; do not add the total floor or release schedules to these rows."),
        ])
    rows.append(make_row("japan_execution_to_2026-07-21", "execution_estimate", "Japan", period_start="2026-02-28", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="public_obligated_and_joint", measure="cumulative_oil_released", program_plan_million_bbl=79.8, observed_or_confirmed_million_bbl=total_draw, estimate_low_million_bbl=total_draw, estimate_base_million_bbl=79.8, estimate_high_million_bbl=14.3 * kl_to_bbl, unit="million_bbl", evidence_status="bounded_from_stock_floor_and_dated_schedules", method="Low is the receiver-confirmed February-April net decline across national, private, and joint stocks; base caps execution at the IEA provisional country allocation; high is the two official national-crude site schedules alone (8.5+5.8 million kl), showing that later domestic action exceeded the initial IEA public allocation.", confidence="medium", source_publication_date="latest official inputs 2026-06-15", source_url=f"{IEA_PLAN_URL} | {JAPAN_RELEASE_URL} | {JAPAN_FEB_URL} | {JAPAN_APR_URL}", notes="The high is not a simultaneous IEA-action estimate and excludes private stock; it is a national implementation ceiling/sensitivity.", double_counting_rule="Use only the base in the IEA 290 million barrel reconciliation; components and schedules are supporting evidence."))
    return rows, {"observed_floor": total_draw, "base": 79.8, "high": 14.3 * kl_to_bbl}


def europe_rows() -> tuple[list[dict[str, str]], dict[str, float]]:
    targets = {"Germany": ("DE", 19.5), "France": ("FR", 14.6), "Italy": ("IT", 10.0), "Spain": ("ES", 11.6)}
    rows: list[dict[str, str]] = []
    floors: dict[str, float] = {}
    for country, (geo, plan) in targets.items():
        feb_kt = eurostat_value(geo, "2026-02")
        may_kt = eurostat_value(geo, "2026-05")
        net_draw = (feb_kt - may_kt) * 7.33 / 1000
        floor = max(0.0, net_draw)
        floors[country] = floor
        rows.extend([
            make_row(f"{geo.lower()}_emergency_stock_2026-02", "stock_observation", country, period_start="2026-02-28", period_end="2026-02-28", as_of_date="2026-02-28", channel="emergency_stock", ownership="EU_emergency_stock_all_holders", measure="ending_emergency_stock", native_value=feb_kt, native_unit="thousand_tonnes", observed_or_confirmed_million_bbl=feb_kt * 7.33 / 1000, unit="million_bbl_approx", evidence_status="official_monthly_stock_observation_converted", method=f"Eurostat {feb_kt} thousand tonnes times 7.33 bbl/tonne; generic conversion because product mix varies.", confidence="medium_high", source_publication_date="latest API extract 2026-08-04", source_url=EUROSTAT_URL, notes="Dataset nrg_stk_oilm, closing EU emergency stock, all oil and petroleum products.", double_counting_rule="Stock level, not supply."),
            make_row(f"{geo.lower()}_emergency_stock_2026-05", "stock_observation", country, period_start="2026-05-31", period_end="2026-05-31", as_of_date="2026-05-31", channel="emergency_stock", ownership="EU_emergency_stock_all_holders", measure="ending_emergency_stock", native_value=may_kt, native_unit="thousand_tonnes", observed_or_confirmed_million_bbl=may_kt * 7.33 / 1000, unit="million_bbl_approx", evidence_status="official_monthly_stock_observation_converted", method=f"Eurostat {may_kt} thousand tonnes times 7.33 bbl/tonne; generic conversion because product mix varies.", confidence="medium_high", source_publication_date="latest API extract 2026-08-04", source_url=EUROSTAT_URL, notes="Latest commonly available month for the four target EU countries in this audit.", double_counting_rule="Stock level, not supply."),
            make_row(f"{geo.lower()}_net_emergency_draw_to_2026-05", "physical_stock_change", country, period_start="2026-02-28", period_end="2026-05-31", as_of_date="2026-05-31", channel="emergency_stock_release", ownership="EU_emergency_stock_all_holders", measure="net_emergency_stock_draw", program_plan_million_bbl=plan, observed_or_confirmed_million_bbl=net_draw, estimate_low_million_bbl=floor, unit="million_bbl_approx", evidence_status="net_stock_change_not_gross_execution", method="February minus May Eurostat emergency-stock levels, converted at 7.33 bbl/tonne.", confidence="medium", source_publication_date="latest API extract 2026-08-04", source_url=EUROSTAT_URL, notes="A negative draw means emergency stocks rose. Gross releases can coexist with replenishment, reclassification, or product transfers; therefore France and Spain have a zero observed floor, not proof of zero release.", double_counting_rule="Use as a floor/cross-check only; it cannot replace the IEA top-down gross-release total."),
        ])
    return rows, floors


def reconciliation_rows(us: dict[str, float], japan: dict[str, float], eu_floors: dict[str, float]) -> list[dict[str, str]]:
    selected_plan = {
        "South Korea": 22.5,
        "Germany": 19.5,
        "France": 14.6,
        "United Kingdom": 14.0,
        "Spain": 11.6,
        "Türkiye": 11.7,
    }
    total_stock_plan = sum(total - production for _, total, _, _, production, _, _ in PLAN)
    other_plan = total_stock_plan - 172.2 - 79.8 - 10.0 - sum(selected_plan.values())
    fixed = us["draw_jul21"] + japan["base"] + 10.0
    remaining_actual = 290.0 - fixed
    pro_rata_denominator = sum(selected_plan.values()) + other_plan
    factor = remaining_actual / pro_rata_denominator
    floors = {
        "South Korea": 0.0,
        "Germany": eu_floors["Germany"],
        "France": eu_floors["France"],
        "United Kingdom": 0.0,
        "Spain": eu_floors["Spain"],
        "Türkiye": 0.0,
    }
    rows = [
        make_row("recon_us", "iea_290_reconciliation", "United States", period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="public_stock", measure="estimated_actual_component", program_plan_million_bbl=172.2, observed_or_confirmed_million_bbl=us["draw_jul17"], estimate_low_million_bbl=us["draw_jul17"], estimate_base_million_bbl=us["draw_jul21"], estimate_high_million_bbl=us["draw_jul24"], unit="million_bbl", evidence_status="bounded_interpolation_of_observed_stock", method="Same U.S. as-of-21-July interpolation documented in the execution row.", confidence="medium_high", source_publication_date="weekly through 2026-07-24", source_url=EIA_SERIES_URL, notes="Physical stock change; program attribution is slightly less certain than the tank balance.", double_counting_rule="Country base rows sum to 290 million barrels; do not add supporting rows."),
        make_row("recon_japan", "iea_290_reconciliation", "Japan", period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="public_and_obligated_industry_stock", measure="estimated_actual_component", program_plan_million_bbl=79.8, observed_or_confirmed_million_bbl=japan["observed_floor"], estimate_low_million_bbl=japan["observed_floor"], estimate_base_million_bbl=japan["base"], estimate_high_million_bbl=japan["high"], unit="million_bbl", evidence_status="bounded_national_execution", method="Observed receiver-confirmed floor; base capped at the IEA plan; high from later official national schedules.", confidence="medium", source_publication_date="latest official inputs 2026-06-15", source_url=f"{IEA_PLAN_URL} | {JAPAN_RELEASE_URL}", notes="High is a sensitivity and not constrained to the initial IEA allocation.", double_counting_rule="Country base rows sum to 290 million barrels; do not add supporting rows."),
        make_row("recon_italy", "iea_290_reconciliation", "Italy", period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="obligated_industry_stock", measure="estimated_actual_component", program_plan_million_bbl=10.0, observed_or_confirmed_million_bbl=eu_floors["Italy"], estimate_low_million_bbl=10.0, estimate_base_million_bbl=10.0, estimate_high_million_bbl=eu_floors["Italy"], unit="million_bbl", evidence_status="allocation_capped_by_observed_net_stock_decline", method="Eurostat February-May net emergency-stock decline exceeds the 10 million barrel IEA allocation, so the collective-action estimate is capped at 10.", confidence="medium_high", source_publication_date="latest API extract 2026-08-04", source_url=f"{IEA_PLAN_URL} | {EUROSTAT_URL}", notes="The excess net draw may be commercial/other emergency use and is not assigned to the IEA action.", double_counting_rule="Country base rows sum to 290 million barrels; do not add supporting rows."),
    ]
    for country, plan in selected_plan.items():
        base = plan * factor
        high = plan
        rows.append(make_row(f"recon_{country.lower().replace(' ', '_').replace('ü', 'u')}", "iea_290_reconciliation", country, period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="mixed_or_country_specific", measure="topdown_pro_rata_estimated_actual_component", program_plan_million_bbl=plan, observed_or_confirmed_million_bbl=floors[country], estimate_low_million_bbl=floors[country], estimate_base_million_bbl=base, estimate_high_million_bbl=high, unit="million_bbl", evidence_status="topdown_inference_not_country_observation", method=f"After fixing U.S., Japan, and Italy, allocate the remaining {fmt(remaining_actual)} million barrels pro rata to remaining provisional stock contributions; common execution factor={fmt(factor)}.", confidence="low_medium", source_publication_date="2026-07-21", source_url=f"{IEA_PLAN_URL} | {IEA_ACTUAL_URL}", notes="For EU countries, the observed field is only the non-negative February-May net emergency-stock draw. For South Korea, UK, and Türkiye no comparable current public execution series was found.", double_counting_rule="Country base rows sum to 290 million barrels; low/high ranges are marginal country bounds and must not be summed as a simultaneous global range."))
    rows.append(make_row("recon_other_iea_members", "iea_290_reconciliation", "Other IEA stock contributors", period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="mixed_public_and_obligated_industry", measure="topdown_pro_rata_estimated_actual_component", program_plan_million_bbl=other_plan, observed_or_confirmed_million_bbl=0.0, estimate_low_million_bbl=0.0, estimate_base_million_bbl=other_plan * factor, estimate_high_million_bbl=other_plan, unit="million_bbl", evidence_status="topdown_inference_not_country_observation", method=f"Residual group uses the same {fmt(factor)} pro-rata factor after fixing U.S., Japan, and Italy.", confidence="low_medium", source_publication_date="2026-07-21", source_url=f"{IEA_PLAN_URL} | {IEA_ACTUAL_URL}", notes="Includes the smaller stock contributors and countries whose ownership detail was provisional. Canada and Mexico production increases are excluded.", double_counting_rule="Country base rows sum to 290 million barrels; this group is mutually exclusive with all named reconciliation rows."))
    base_sum = sum(float(row["estimate_base_million_bbl"]) for row in rows)
    if abs(base_sum - 290.0) > 1e-6:
        raise ValueError(f"reconciliation does not close: {base_sum}")
    rows.append(make_row("recon_total_iea_actual", "reconciliation_total", "IEA members", period_start="2026-03-11", period_end="2026-07-21", as_of_date="2026-07-21", channel="emergency_stock_release", ownership="public_and_obligated_industry_stock", measure="cumulative_oil_released", program_plan_million_bbl=total_stock_plan, observed_or_confirmed_million_bbl=290.0, estimate_low_million_bbl=290.0, estimate_base_million_bbl=290.0, estimate_high_million_bbl=290.0, unit="million_bbl_rounded", evidence_status="iea_observed_estimate", method="IEA said around 290 million barrels had been released; named country base estimates are constrained to this rounded headline.", confidence="high_for_aggregate_medium_for_exact_rounding", source_publication_date="2026-07-21", source_url=IEA_ACTUAL_URL, notes=f"The exact country-plan stock envelope is {fmt(total_stock_plan)} million barrels from the rounded table entries; IEA's published ownership totals round to 280 public plus 119 obligated-industry. The 27.5 million barrel Canada/Mexico production plan is separate.", double_counting_rule="Headline total; never add the country rows to this row. Use either the total or its decomposition."))
    return rows


def main() -> None:
    rows = plan_rows()
    us_stock = fetch_us_spr()
    us_detail, us_values = us_rows(us_stock)
    rows.extend(us_detail)
    rows.extend(implementation_event_rows())
    japan_detail, japan_values = japan_rows()
    rows.extend(japan_detail)
    europe_detail, europe_floors = europe_rows()
    rows.extend(europe_detail)
    rows.extend(reconciliation_rows(us_values, japan_values, europe_floors))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
