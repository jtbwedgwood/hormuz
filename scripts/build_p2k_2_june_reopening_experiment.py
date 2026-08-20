#!/usr/bin/env python3
"""Build the March-June 2026 partial-reopening natural-experiment ledger.

The output deliberately separates physical flow, inventories, refinery activity,
and demand proxies.  Positive ``relaxation_mbd`` means a coping mechanism was used
less intensively in June than in May (or, for shut-ins, that lost production fell).
It is a diagnostic convention, not a causal coefficient.
"""

from __future__ import annotations

import calendar
import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTWATCH = ROOT / "data/external/portwatch/hormuz_daily_chokepoint.csv"
BALANCE = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
GULF = ROOT / "data/derived/hormuz_m8q_6_gulf_physical_oil_ledger.csv"
COUNTRY = ROOT / "data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv"
EMERGENCY = ROOT / "data/derived/hormuz_m8q_10_emergency_release_execution.csv"
OUT = ROOT / "data/derived/hormuz_p2k_2_june_reopening_experiment.csv"

MONTHS = ["2026-03", "2026-04", "2026-05", "2026-06"]
MONTH_DAYS = {month: calendar.monthrange(2026, int(month[-2:]))[1] for month in MONTHS}

FIELDS = [
    "row_id",
    "record_type",
    "period_start",
    "period_end",
    "observation_month",
    "channel_group",
    "channel",
    "geography",
    "value",
    "value_low",
    "value_high",
    "unit",
    "may_value",
    "june_minus_may",
    "relaxation_mbd",
    "relaxation_rank",
    "data_status",
    "confidence",
    "source_url",
    "source_row_ids",
    "method",
    "interpretation",
    "identification_limit",
]

IEA_JULY = "https://www.iea.org/reports/oil-market-report-july-2026"
IEA_JUNE = "https://www.iea.org/reports/oil-market-report-june-2026"
PORTWATCH_METHOD = "https://portwatch.imf.org/pages/data-and-methodology"
JAPAN_MAY = "https://www.meti.go.jp/english/press/2026/0515_003.html"
JAPAN_JUNE = "https://www.meti.go.jp/press/2026/06/20260615004/20260615004.html"
KPLER_MAY = "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def make_row(row_id: str, record_type: str, **values: object) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row.update({"row_id": row_id, "record_type": record_type})
    for key, value in values.items():
        if key not in row:
            raise KeyError(key)
        row[key] = fmt(value)
    return row


def one(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    matches = [row for row in rows if row["row_id"] == row_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {row_id}, found {len(matches)}")
    return matches[0]


def month_bounds(month: str) -> tuple[str, str]:
    return f"{month}-01", f"{month}-{MONTH_DAYS[month]:02d}"


def monthly_row(
    row_id: str,
    month: str,
    channel_group: str,
    channel: str,
    geography: str,
    value: float | None,
    unit: str,
    status: str,
    confidence: str,
    source_url: str,
    source_row_ids: str,
    method: str,
    interpretation: str,
    limit: str,
) -> dict[str, str]:
    start, end = month_bounds(month)
    return make_row(
        row_id,
        "monthly_channel",
        period_start=start,
        period_end=end,
        observation_month=month,
        channel_group=channel_group,
        channel=channel,
        geography=geography,
        value=value,
        unit=unit,
        data_status=status,
        confidence=confidence,
        source_url=source_url,
        source_row_ids=source_row_ids,
        method=method,
        interpretation=interpretation,
        identification_limit=limit,
    )


def build_portwatch_rows(portwatch: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def subset(start: str, end: str) -> list[dict[str, str]]:
        selected = [row for row in portwatch if start <= row["date"] <= end]
        expected = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
        if len(selected) != expected:
            raise ValueError(f"PortWatch gap in {start}/{end}: {len(selected)} of {expected}")
        return selected

    baseline = subset("2026-01-01", "2026-02-27")
    base_calls = sum(float(row["n_tanker"]) for row in baseline) / len(baseline)
    base_capacity = sum(float(row["capacity_tanker"]) for row in baseline) / len(baseline)

    for month in MONTHS:
        start, end = month_bounds(month)
        selected = subset(start, end)
        calls = sum(float(row["n_tanker"]) for row in selected) / len(selected)
        capacity = sum(float(row["capacity_tanker"]) for row in selected) / len(selected)
        for suffix, channel, value, baseline_value, unit in [
            ("calls", "PortWatch tanker transit calls", calls, base_calls, "tanker_calls_per_day"),
            ("capacity", "PortWatch tanker capacity proxy", capacity, base_capacity, "deadweight_tonnes_per_day"),
        ]:
            rows.append(monthly_row(
                f"portwatch-{month.replace('-', '')}-{suffix}", month, "traffic", channel,
                "Strait of Hormuz", value, unit, "observed_AIS_derived_preliminary",
                "medium_for_direction_low_for_oil_volume", PORTWATCH_METHOD,
                "data/external/portwatch/hormuz_daily_chokepoint.csv",
                f"Daily mean; January 1-February 27 baseline={baseline_value:.3f}. June tail may be revised.",
                f"Equals {100 * value / baseline_value:.1f}% of the pre-shock daily mean.",
                "Broad tanker class; no direction, loading status, cargo type, onboard volume, or AIS-dark movements. Never convert mechanically to mb/d.",
            ))

    windows = [
        ("pre-shock", "2026-01-01", "2026-02-27"),
        ("june-01-07", "2026-06-01", "2026-06-07"),
        ("june-08-14", "2026-06-08", "2026-06-14"),
        ("june-15-21", "2026-06-15", "2026-06-21"),
        ("june-22-30", "2026-06-22", "2026-06-30"),
    ]
    june_capacity_total = sum(float(row["capacity_tanker"]) for row in subset("2026-06-01", "2026-06-30"))
    for label, start, end in windows:
        selected = subset(start, end)
        calls = sum(float(row["n_tanker"]) for row in selected) / len(selected)
        capacity = sum(float(row["capacity_tanker"]) for row in selected) / len(selected)
        capacity_total = sum(float(row["capacity_tanker"]) for row in selected)
        for suffix, channel, value, unit, interpretation in [
            ("calls", "PortWatch tanker transit calls", calls, "tanker_calls_per_day", f"{100 * calls / base_calls:.1f}% of pre-shock mean."),
            ("capacity", "PortWatch tanker capacity proxy", capacity, "deadweight_tonnes_per_day", f"{100 * capacity / base_capacity:.1f}% of pre-shock mean."),
        ]:
            rows.append(make_row(
                f"timing-{label}-{suffix}", "reopening_timing",
                period_start=start, period_end=end, channel_group="traffic", channel=channel,
                geography="Strait of Hormuz", value=value, unit=unit,
                data_status="observed_AIS_derived_preliminary", confidence="medium_for_direction_low_for_oil_volume",
                source_url=PORTWATCH_METHOD, source_row_ids="data/external/portwatch/hormuz_daily_chokepoint.csv",
                method="Daily mean within the stated window.", interpretation=interpretation,
                identification_limit="The tail is revisable and cannot be mapped mechanically to loaded oil volumes.",
            ))
        if label.startswith("june"):
            rows.append(make_row(
                f"timing-{label}-june-capacity-share", "reopening_timing",
                period_start=start, period_end=end, channel_group="traffic", channel="share of June PortWatch tanker capacity proxy",
                geography="Strait of Hormuz", value=100 * capacity_total / june_capacity_total, unit="percent_of_june_total",
                data_status="observed_AIS_derived_preliminary", confidence="medium_for_timing_low_for_oil_volume",
                source_url=PORTWATCH_METHOD, source_row_ids="data/external/portwatch/hormuz_daily_chokepoint.csv",
                method="Window tanker-capacity sum divided by the June sum.",
                interpretation="Shows how strongly the observed June relaxation was concentrated late in the month.",
                identification_limit="Capacity is DWT-based and can be zero or revised; it does not observe cargo onboard.",
            ))
    return rows


def build_physical_rows(gulf: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    route_names = {
        "saudi_arabia": "Saudi East-West/Petroline to Yanbu",
        "united_arab_emirates": "UAE Habshan-Fujairah pipeline",
        "iraq": "Iraq-Türkiye pipeline to Ceyhan",
        "other_gulf_route_residual": "Other non-Hormuz route residual",
    }
    for month in MONTHS:
        suffix = month.replace("-", "")
        for slug, name in route_names.items():
            source = one(gulf, f"{slug}_{month}_bypass_flow")
            rows.append(monthly_row(
                f"physical-{suffix}-bypass-{slug}", month, "rerouting", name, source["country"],
                float(source["value_mb_per_day"]), "mb/d", source["data_status"], source["confidence"],
                source["source_url"], source["row_id"], source["method"],
                "Gross route flow, already embodied in production/exports; only its increment above baseline mitigates the shock.",
                source["double_counting_note"],
            ))
        bypass_sources = [one(gulf, f"{slug}_{month}_bypass_flow") for slug in route_names]
        bypass = sum(float(source["value_mb_per_day"]) for source in bypass_sources)
        rows.append(monthly_row(
            f"physical-{suffix}-bypass-total", month, "rerouting", "Total gross non-Hormuz route flow", "Gulf producers",
            bypass, "mb/d", "bounded_reconstruction", "low_medium",
            " | ".join(dict.fromkeys(source["source_url"] for source in bypass_sources)),
            " | ".join(source["row_id"] for source in bypass_sources), "Sum of four route reconstruction rows.",
            "The working total rises from 5.5 mb/d in March to 7.2 mb/d from April onward and does not fall in June.",
            "A flat June estimate may reflect capacity, contracts, or slow reversal; it does not by itself prove bypass is the cheapest channel.",
        ))
        hormuz = one(gulf, f"hormuz_{month}_oil_flow")
        rows.append(monthly_row(
            f"physical-{suffix}-hormuz", month, "physical_flow", "Oil flow through Hormuz", "Strait of Hormuz",
            float(hormuz["value_mb_per_day"]), "mb/d", hormuz["data_status"], hormuz["confidence"],
            hormuz["source_url"], hormuz["row_id"], hormuz["method"],
            "March-May repeats an IEA period average; June is inferred as 16.1 mb/d total Gulf exports minus 7.2 mb/d bypass.",
            "The June number is not an observed IEA Hormuz-flow series and cannot be validated by vessel counts alone.",
        ))
        shutins = [row for row in gulf if row["observation_month"] == month and row["metric"] == "closure_related_crude_production_shutin"]
        if len(shutins) != 7:
            raise ValueError(f"expected seven shut-in rows for {month}, found {len(shutins)}")
        shutin = sum(float(row["value_mb_per_day"]) for row in shutins)
        rows.append(monthly_row(
            f"physical-{suffix}-crude-shutin", month, "physical_supply", "Closure-related crude production shut-in", "Affected Gulf producers",
            shutin, "mb/d", "official_estimate", "medium_high",
            "https://www.eia.gov/outlooks/steo/archives/jul26.pdf",
            " | ".join(row["row_id"] for row in shutins), "Sum of seven EIA July STEO country estimates.",
            "Positive is production unavailable. The decline from 11.20 mb/d in May to 8.29 mb/d in June is a 2.91 mb/d production relaxation.",
            "Crude only; do not compare directly with broader IEA total-oil Gulf losses without a taxonomy adjustment.",
        ))
    return rows


def build_inventory_rows(balance: list[dict[str, str]], country: list[dict[str, str]], emergency: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    inventory_ids = {
        "2026-03": "iea_may_mar_inventory",
        "2026-04": "iea_may_apr_inventory",
        "2026-05": "iea_jul_may_inventory",
        "2026-06": "iea_jul_jun_inventory",
    }
    onshore_ids = {"2026-04": "iea_may_apr_onland", "2026-06": "iea_jul_jun_onshore"}
    water_ids = {"2026-04": "iea_may_apr_water", "2026-06": "iea_jul_jun_water"}
    for month in MONTHS:
        days = MONTH_DAYS[month]
        observed = one(balance, inventory_ids[month])
        # IEA stock change is positive build; the ledger convention below is positive draw.
        draw_rate = -float(observed["value"]) / days
        rows.append(monthly_row(
            f"inventory-{month.replace('-', '')}-global-total", month, "inventory", "Global observed total stock draw rate", "World",
            draw_rate, "mb/d", observed["status"], observed["confidence"], observed["citation"], observed["row_id"],
            "Negative of IEA monthly stock change divided by calendar days; positive means draw, negative means build.",
            "The total balance flips from a 2.35 mb/d draw in May to a 0.70 mb/d build in June.",
            "Includes oil on water. The June flip is not evidence that consumer tanks rebuilt.",
        ))
        for slug, ids, channel, interpretation in [
            ("onshore", onshore_ids, "Global onshore stock draw rate", "Positive means onshore tanks continued to supply the market."),
            ("water", water_ids, "Global oil-on-water accumulation rate", "Positive means barrels entered the in-transit/floating bucket, not end-user tanks."),
        ]:
            if month in ids:
                source = one(balance, ids[month])
                value = (-1 if slug == "onshore" else 1) * float(source["value"]) / days
                status, confidence, source_url, source_id = source["status"], source["confidence"], source["citation"], source["row_id"]
            else:
                value = None
                status, confidence, source_url, source_id = "not_publicly_reported_in_project_input", "none", IEA_JULY, ""
            rows.append(monthly_row(
                f"inventory-{month.replace('-', '')}-global-{slug}", month, "inventory_timing", channel, "World",
                value, "mb/d", status, confidence, source_url, source_id,
                "IEA monthly volume divided by calendar days; blank where no matching public component is available.",
                interpretation, "Component coverage is incomplete across months, so April-to-June comparisons are descriptive, not a continuous panel.",
            ))

        for stock_slug, metric, label, group in [
            ("spr", "public_strategic_stock_draw", "U.S. SPR draw rate", "emergency_inventory"),
            ("commercial_total", "total_commercial_petroleum_stock_draw", "U.S. total commercial petroleum stock draw rate", "commercial_inventory"),
        ]:
            source = one(country, f"us-{stock_slug}-actual-{month.replace('-', '')}")
            value = float(source["value_base"]) / days
            rows.append(monthly_row(
                f"inventory-{month.replace('-', '')}-us-{stock_slug}", month, group, label, "United States",
                value, "mb/d", source["status"], source["confidence"], source["source_url"], source["row_id"],
                "Observed project monthly draw divided by calendar days. The source endpoints are the last weekly observations, not exact month-end dates.",
                "Positive is a draw; negative is a build. Commercial total excludes SPR.",
                "U.S. is a high-frequency illustration, not the global emergency/commercial split.",
            ))

        china_rows = [row for row in country if row["geography"] == "China" and row["observation_month"] == month and row["metric"] == "crude_stock_draw"]
        china = china_rows[0] if len(china_rows) == 1 else None
        rows.append(monthly_row(
            f"inventory-{month.replace('-', '')}-china-crude", month, "commercial_or_state_inventory", "China crude tank draw rate", "China",
            float(china["value_base"]) / days if china else None, "mb/d",
            china["status"] if china else "not_publicly_reported_in_project_input",
            china["confidence"] if china else "none", china["source_url"] if china else IEA_JULY,
            china["row_id"] if china else "", "IEA tank-change estimate divided by days; positive is draw, negative is build.",
            "China built 40 mb in March and drew 41 mb in June; April-May are missing from the public project series.",
            "Ownership is unresolved among government, commercial/operational, bonded, and other stocks.",
        ))

    june_government = 44.0 / 30.0
    rows.append(monthly_row(
        "inventory-202606-oecd-government", "2026-06", "emergency_inventory", "OECD government stock release rate", "OECD",
        june_government, "mb/d", "IEA_preliminary_estimate", "medium_high", IEA_JULY, "iea_jul_jun_onshore",
        "IEA reported 44 mb of OECD government releases in June; divided by 30 days.",
        "Emergency releases continued at 1.47 mb/d even after reopening began.",
        "Government release is inside the OECD and global observed-stock totals; never add it to those totals.",
    ))

    japan_components = [
        one(emergency, "japan_national_draw_to_2026-04-30"),
        one(emergency, "japan_private_draw_to_2026-04-30"),
        one(emergency, "japan_producer_joint_draw_to_2026-04-30"),
    ]
    japan_draw = sum(float(row["observed_or_confirmed_million_bbl"]) for row in japan_components)
    rows.append(make_row(
        "inventory-japan-20260301-20260430-observed", "period_channel",
        period_start="2026-03-01", period_end="2026-04-30", channel_group="emergency_inventory",
        channel="Japan emergency and obligated-industry net stock draw", geography="Japan",
        value=japan_draw / 61, unit="mb/d", data_status="official_monthly_endpoint_net_change", confidence="medium_high",
        source_url=" | ".join(dict.fromkeys(row["source_url"] for row in japan_components)),
        source_row_ids=" | ".join(row["row_id"] for row in japan_components),
        method=f"National, private and producer-joint net draws total {japan_draw:.3f} mb from February 28 to April 30; divide by 61 days.",
        interpretation="Japan was still drawing multiple reserve categories through April; public direct-volume monthly endpoints do not yet provide a clean May-to-June reversal.",
        identification_limit="Period average, not separately observed March and April delivery; net stock change is not gross programme delivery.",
    ))
    return rows


def build_refining_demand_rows(balance: list[dict[str, str]], country: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for month in MONTHS:
        days = MONTH_DAYS[month]
        china_run = [row for row in country if row["row_id"] == f"china-refinery-run-shortfall-{month.replace('-', '')}"]
        if china_run:
            source = china_run[0]
            shortfall = float(source["value_base"]) / days
            # Recover the reported actual volume from the builder's official NBS inputs.
            actual_mt = {"2026-04": 54.65, "2026-05": 53.72, "2026-06": 51.24}[month]
            actual_mbd = actual_mt * 7.33 / days
            source_url, source_id, status, confidence = source["source_url"], source["row_id"], source["status"], source["confidence"]
        else:
            shortfall = actual_mbd = None
            source_url, source_id, status, confidence = "https://www.stats.gov.cn/english/", "", "not_available", "none"
        rows.append(monthly_row(
            f"refining-{month.replace('-', '')}-china-actual", month, "refining", "China crude processing", "China",
            actual_mbd, "mb/d_oil_equivalent", status, confidence, source_url, source_id,
            "Official NBS monthly tonnes converted at the project central 7.33 bbl/tonne factor and divided by days.",
            "Actual runs fell from 13.35 mb/d in April to 12.52 mb/d in June despite the late-June reopening.",
            "Conversion is approximate and actual runs are not the same as final domestic consumption.",
        ))
        rows.append(monthly_row(
            f"refining-{month.replace('-', '')}-china-yoy-gap", month, "refining", "China refinery throughput below prior year", "China",
            shortfall, "mb/d_oil_equivalent", status, confidence, source_url, source_id,
            "Existing official year-on-year shortfall converted to a daily rate.",
            "The gap widened sharply in June; China refining did not reveal a same-month relaxation.",
            "Year-on-year comparison includes ordinary trends, export decisions and macro effects, and is not a February-forecast counterfactual.",
        ))

        korea_runs = 2.0 if month in {"2026-04", "2026-05"} else None
        rows.append(monthly_row(
            f"refining-{month.replace('-', '')}-korea", month, "refining", "South Korea refinery crude runs", "South Korea",
            korea_runs, "mb/d", "analyst_rounded_estimate" if korea_runs is not None else "not_publicly_reported_in_project_input",
            "low_medium" if korea_runs is not None else "none", KPLER_MAY, "",
            "Kpler estimated runs at roughly 2 mb/d in April and May, nearly 1 mb/d below normal; blank where the project has no comparable month estimate.",
            "Korea's available series confirms deep refinery curtailment but cannot show whether it relaxed in June.",
            "Rounded analyst estimate, not an official monthly series; products, exports and stock use prevent equating run cuts with end demand.",
        ))

        for geography, slug in [("World", "patc_world"), ("China", "patc_ch"), ("India", "patc_in"), ("Japan", "patc_ja")]:
            source = one(country, f"demand-{slug}-{month.replace('-', '')}")
            value = float(source["value_base"]) / days
            rows.append(monthly_row(
                f"demand-{month.replace('-', '')}-{slug}", month, "demand", "Consumption below frozen February forecast", geography,
                value, "mb/d", source["status"], source["confidence"], source["source_url"], source["row_id"],
                "Existing February-minus-July STEO monthly gap divided by calendar days.",
                "Positive is lower consumption than the pre-shock forecast path.",
                "Forecast-vintage revision includes Hormuz, ordinary revisions, weather, macro changes, prices and structural trends; it is not a causal treatment effect.",
            ))

    rows.append(monthly_row(
        "refining-202606-global-mom", "2026-06", "refining", "Global refinery crude throughput change month on month", "World",
        1.5, "mb/d", "IEA_preliminary_estimate", "medium_high", IEA_JULY, "iea_jul_jun_runs_change",
        "Direct IEA July OMR headline.",
        "The clearest same-month downstream relaxation, but runs remained 6 mb/d below June 2025 and Asia stayed reduced.",
        "Global aggregate is concurrent with Russian refinery attacks, seasonality and a late-month reopening.",
    ))
    for month, share, source_url, interpretation in [
        ("2026-05", 60.0, JAPAN_MAY, "METI estimated alternative procurement at about 60% of the volume that otherwise would have crossed Hormuz."),
        ("2026-06", 80.0, JAPAN_JUNE, "METI expected procurement at about 80% of the prior-year normal-month level and extended private-stock relief."),
    ]:
        rows.append(monthly_row(
            f"procurement-{month.replace('-', '')}-japan", month, "procurement", "Japan crude procurement recovery proxy", "Japan",
            share, "percent", "official_forward_or_contemporaneous_estimate", "medium_high", source_url, "", "Direct METI statement.",
            interpretation, "May and June statements use related but not identical denominators; treat the direction as stronger than the exact change.",
        ))
    return rows


def add_comparisons_and_ordering(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    monthly = {(row["channel"], row["geography"], row["observation_month"]): row for row in rows if row["record_type"] == "monthly_channel"}
    comparisons = {
        ("Oil flow through Hormuz", "Strait of Hormuz"): ("flow relief; positive June-minus-May", None),
        ("Total gross non-Hormuz route flow", "Gulf producers"): ("flat route use", None),
        ("Closure-related crude production shut-in", "Affected Gulf producers"): ("lower shut-in is relief", "reverse"),
        ("Global observed total stock draw rate", "World"): ("lower draw is apparent relief", "reverse"),
        ("U.S. SPR draw rate", "United States"): ("lower draw is relief", "reverse"),
        ("U.S. total commercial petroleum stock draw rate", "United States"): ("lower draw is relief", "reverse"),
        ("Consumption below frozen February forecast", "World"): ("lower gap is demand recovery", "reverse"),
        ("Consumption below frozen February forecast", "China"): ("lower gap is demand recovery", "reverse"),
        ("Consumption below frozen February forecast", "India"): ("lower gap is demand recovery", "reverse"),
        ("Consumption below frozen February forecast", "Japan"): ("lower gap is demand recovery", "reverse"),
        ("China refinery throughput below prior year", "China"): ("lower gap is refining recovery", "reverse"),
    }
    for key, (_, direction) in comparisons.items():
        may = monthly.get((*key, "2026-05"))
        june = monthly.get((*key, "2026-06"))
        if not may or not june or not may["value"] or not june["value"]:
            continue
        may_value, june_value = float(may["value"]), float(june["value"])
        delta = june_value - may_value
        relaxation = -delta if direction == "reverse" else delta
        june["may_value"] = fmt(may_value)
        june["june_minus_may"] = fmt(delta)
        june["relaxation_mbd"] = fmt(relaxation if june["unit"].startswith("mb/d") else None)

    flow_low, flow_base, flow_high = 8.2, 8.9, 9.6
    for label, flow, bypass in [("low-flow", flow_low, 7.9), ("base", flow_base, 7.2), ("high-flow", flow_high, 6.5)]:
        rows.append(make_row(
            f"sensitivity-june-hormuz-{label}", "flow_inference_sensitivity",
            period_start="2026-06-01", period_end="2026-06-30", observation_month="2026-06",
            channel_group="physical_flow", channel="June inferred Hormuz oil flow", geography="Strait of Hormuz",
            value=flow, value_low=flow_low, value_high=flow_high, unit="mb/d", may_value=2.7,
            june_minus_may=flow - 2.7, relaxation_mbd=flow - 2.7,
            data_status="project_sensitivity", confidence="low_medium",
            source_url=IEA_JULY, source_row_ids="hormuz_2026-06_oil_flow",
            method=f"Hold IEA total Gulf exports at 16.1 mb/d and vary June bypass from 7.9/7.2/6.5; Hormuz={flow:.1f} mb/d.",
            interpretation=f"The inferred Hormuz-flow relief versus the 2.7 mb/d March-May period average is {flow - 2.7:.1f} mb/d ({30 * (flow - 2.7):.0f} mb in June).",
            identification_limit="The +/-0.7 mb/d bypass range is a transparent project judgment, not a statistical confidence interval.",
        ))

    # Demonstrate why capacity-proportional flow allocation is rejected.
    timing = {row["row_id"]: row for row in rows if row["record_type"] == "reopening_timing"}
    for label, days in [("june-01-07", 7), ("june-08-14", 7), ("june-15-21", 7), ("june-22-30", 9)]:
        share = float(timing[f"timing-{label}-june-capacity-share"]["value"]) / 100
        implied = 8.9 * 30 * share / days
        rows.append(make_row(
            f"rejected-capacity-map-{label}", "flow_mapping_diagnostic",
            period_start=timing[f"timing-{label}-june-capacity-share"]["period_start"],
            period_end=timing[f"timing-{label}-june-capacity-share"]["period_end"],
            channel_group="traffic", channel="Rejected capacity-proportional implied Hormuz flow", geography="Strait of Hormuz",
            value=implied, unit="mb/d", data_status="rejected_diagnostic", confidence="none_for_flow",
            source_url=f"{PORTWATCH_METHOD} | {IEA_JULY}",
            source_row_ids=f"timing-{label}-june-capacity-share | hormuz_2026-06_oil_flow",
            method="Allocate the 267 mb June base inference in proportion to PortWatch tanker-capacity proxy within June.",
            interpretation=(
                "Diagnostic only. Taken together, the mapping assigns about 22.9 mb/d to June 22-30, above the roughly 20 mb/d pre-war flow; "
                "that implausible concentration shows why mechanical within-month capacity mapping is rejected."
            ),
            identification_limit="Rejected method: vessel size, direction, loading, AIS coverage, queued exits and timing differ.",
        ))

    us_stock_relaxation = (
        float(monthly[("U.S. SPR draw rate", "United States", "2026-06")]["relaxation_mbd"])
        + float(monthly[("U.S. total commercial petroleum stock draw rate", "United States", "2026-06")]["relaxation_mbd"])
    )
    world_demand_relaxation = float(
        monthly[("Consumption below frozen February forecast", "World", "2026-06")]["relaxation_mbd"]
    )
    bypass_relaxation = float(
        monthly[("Total gross non-Hormuz route flow", "Gulf producers", "2026-06")]["relaxation_mbd"]
    )
    ordering = [
        (1, "Global refinery-run rebound", 1.5, "The clearest true downstream relaxation: global runs rose 1.5 mb/d month on month, though they remained 6 mb/d below June 2025."),
        (2, "U.S. public plus commercial stock-draw slowdown", us_stock_relaxation, "An illustrative high-frequency stock panel: SPR draw slowed about 0.27 mb/d and commercial-total draw about 0.50 mb/d."),
        (3, "Global demand-gap easing", world_demand_relaxation, "The frozen-vintage world demand gap eased only about 0.09 mb/d from May; China, India and Japan each changed by less than 0.03 mb/d."),
        (4, "Bypass-route relaxation", bypass_relaxation, "Modeled gross bypass stayed at 7.2 mb/d; no June unwind is observed in the reconstruction."),
    ]
    for rank, channel, value, interpretation in ordering:
        rows.append(make_row(
            f"ordering-{rank}", "revealed_ordering",
            period_start="2026-05-01", period_end="2026-06-30", channel_group="coping_channel",
            channel=channel, geography="Diagnostic scope", value=value, unit="mb/d", relaxation_mbd=value,
            relaxation_rank=rank, data_status="suggestive_project_diagnostic", confidence="low_medium",
            source_url=f"{IEA_JULY} | data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv",
            source_row_ids="See matching monthly-channel rows in this file.",
            method="Rank measured May-to-June reductions in coping-channel intensity; exclude the exogenous transit/production reopening and the global total-stock flip distorted by oil on water.",
            interpretation=interpretation,
            identification_limit="Not a structural cost curve: one back-loaded month, delivery lags, seasonality, heterogeneous geographies and concurrent shocks prevent causal ranking.",
        ))
    may_global_draw = float(monthly[("Global observed total stock draw rate", "World", "2026-05")]["value"])
    june_global_draw = float(monthly[("Global observed total stock draw rate", "World", "2026-06")]["value"])
    apparent_stock_relief = may_global_draw - june_global_draw
    rows.append(make_row(
        "ordering-apparent-global-stock-flip", "revealed_ordering_caveat",
        period_start="2026-05-01", period_end="2026-06-30", channel_group="inventory_timing",
        channel="Apparent global total-stock relief", geography="World", value=apparent_stock_relief, unit="mb/d", relaxation_mbd=apparent_stock_relief,
        data_status="observed_composite_but_confounding", confidence="medium_high_for_total_low_for_interpretation",
        source_url=IEA_JULY, source_row_ids="iea_jul_may_inventory | iea_jul_jun_inventory | iea_jul_jun_onshore | iea_jul_jun_water",
        method="May draw 73/31=2.355 mb/d versus June build 21/30=0.700 mb/d; apparent relief=3.055 mb/d.",
        interpretation="Do not rank this as stock-buffer relaxation: June oil on water built 3.9 mb/d while onshore tanks still drew 3.2 mb/d and OECD government reserves supplied 1.47 mb/d.",
        identification_limit="Cargo timing dominates the aggregate stock sign.",
    ))
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate row IDs")
    expected = {
        "physical-202606-hormuz": 8.9,
        "physical-202606-bypass-total": 7.2,
        "physical-202606-crude-shutin": 8.29,
        "inventory-202606-global-total": -0.7,
        "inventory-202606-oecd-government": 44 / 30,
        "refining-202606-global-mom": 1.5,
    }
    by_id = {row["row_id"]: row for row in rows}
    for row_id, target in expected.items():
        actual = float(by_id[row_id]["value"])
        if abs(actual - target) > 1e-6:
            raise ValueError(f"{row_id}: {actual} != {target}")
    rejected_late = float(by_id["rejected-capacity-map-june-22-30"]["value"])
    if rejected_late <= 20:
        raise ValueError("capacity-mapping diagnostic no longer demonstrates implausible late-month flow")


def main() -> None:
    portwatch = read_csv(PORTWATCH)
    balance = read_csv(BALANCE)
    gulf = read_csv(GULF)
    country = read_csv(COUNTRY)
    emergency = read_csv(EMERGENCY)
    rows = build_portwatch_rows(portwatch)
    rows.extend(build_physical_rows(gulf))
    rows.extend(build_inventory_rows(balance, country, emergency))
    rows.extend(build_refining_demand_rows(balance, country))
    rows = add_comparisons_and_ordering(rows)
    validate(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
