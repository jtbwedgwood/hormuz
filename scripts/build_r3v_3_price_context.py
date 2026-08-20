#!/usr/bin/env python3
"""Build a deliberately modest realized-price context for r3v.3.

This is not a shortage estimator. It downloads public EIA/FRED spot benchmarks,
computes descriptive period summaries, and preserves the causal caveat that price
also reflects news, expectations, risk premia, policy, macro conditions and trading.
"""

from __future__ import annotations

import csv
import io
import json
import statistics
import urllib.request
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_OUT = ROOT / "data/external/prices/hormuz_r3v_3_daily_price_context.csv"
SUMMARY_OUT = ROOT / "data/derived/hormuz_r3v_3_price_context_summary.csv"
TIME_SPREAD_DAILY_OUT = ROOT / "data/external/prices/hormuz_r3v_3_daily_time_spreads.csv"
TIME_SPREAD_SUMMARY_OUT = ROOT / "data/derived/hormuz_r3v_3_time_spread_summary.csv"
PRODUCT_DAILY_OUT = ROOT / "data/external/prices/hormuz_a4d_9_product_retail_prices.csv"
PRODUCT_SUMMARY_OUT = ROOT / "data/derived/hormuz_a4d_9_product_retail_price_summary.csv"
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU,DCOILWTICO"
PRODUCT_SPOT_FRED_URL = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv?"
    "id=DGASUSGULF,DDFUELUSGULF,DJFUELUSGULF"
)
RETAIL_FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GASREGW,GASDESW"
EIA_PRODUCT_SPOT_URL = "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
EIA_RETAIL_URL = "https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm"
YAHOO_CHART_ROOT = "https://query1.finance.yahoo.com/v8/finance/chart/"
START = date(2026, 1, 1)
END = date(2026, 8, 18)
LATEST_COMPLETED_FUTURES_SESSION = date(2026, 8, 17)


def download_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def number(value: str | None) -> float | None:
    if value is None or value.strip() in {"", "."}:
        return None
    return float(value)


def period_label(day: date) -> str:
    if day <= date(2026, 2, 27):
        return "pre_shock_2026"
    if day <= date(2026, 6, 30):
        return "march_june_historical_frame"
    if day <= date(2026, 7, 31):
        return "july_reclosure_context"
    return "august_publication_context"


def load_daily() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for raw in csv.DictReader(io.StringIO(download_text(FRED_URL))):
        day = datetime.strptime(raw["observation_date"], "%Y-%m-%d").date()
        if day < START or day > END:
            continue
        brent = number(raw.get("DCOILBRENTEU"))
        wti = number(raw.get("DCOILWTICO"))
        if brent is None and wti is None:
            continue
        rows.append(
            {
                "date": day.isoformat(),
                "brent_spot_usd_per_bbl": brent,
                "wti_spot_usd_per_bbl": wti,
                "brent_minus_wti_usd_per_bbl": (
                    round(brent - wti, 6) if brent is not None and wti is not None else None
                ),
                "period_label": period_label(day),
                "data_status": "observed_daily_public_benchmark",
                "source_url": FRED_URL,
                "causal_caveat": (
                    "Context only: spot prices reflect news, reopening expectations, geopolitical risk, "
                    "emergency policy, macro demand, positioning and physical balances; they do not identify "
                    "the size of the physical shortage or inventory residual."
                ),
            }
        )
    if not rows:
        raise RuntimeError("No 2026 FRED price observations returned")
    return rows


PERIODS = {
    "pre_shock_jan1_feb27": (date(2026, 1, 1), date(2026, 2, 27)),
    "march": (date(2026, 3, 1), date(2026, 3, 31)),
    "april": (date(2026, 4, 1), date(2026, 4, 30)),
    "may": (date(2026, 5, 1), date(2026, 5, 31)),
    "june": (date(2026, 6, 1), date(2026, 6, 30)),
    "march_june": (date(2026, 3, 1), date(2026, 6, 30)),
    "july": (date(2026, 7, 1), date(2026, 7, 31)),
    "august_to_publication": (date(2026, 8, 1), END),
    "july_reclosure_event_july7_21": (date(2026, 7, 7), date(2026, 7, 21)),
    "post_reclosure_july8_publication": (date(2026, 7, 8), END),
}


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    series = {
        "brent_spot": "brent_spot_usd_per_bbl",
        "wti_spot": "wti_spot_usd_per_bbl",
        "brent_minus_wti": "brent_minus_wti_usd_per_bbl",
    }
    baseline: dict[str, float] = {}
    for series_name, field in series.items():
        vals = [
            float(r[field])
            for r in rows
            if date(2026, 1, 1) <= date.fromisoformat(str(r["date"])) <= date(2026, 2, 27)
            and r[field] is not None
        ]
        baseline[series_name] = statistics.fmean(vals)
    for period_name, (start, end) in PERIODS.items():
        for series_name, field in series.items():
            selected = [
                r
                for r in rows
                if start <= date.fromisoformat(str(r["date"])) <= end and r[field] is not None
            ]
            if not selected:
                continue
            values = [float(r[field]) for r in selected]
            mean_value = statistics.fmean(values)
            peak = max(selected, key=lambda r: float(r[field]))
            trough = min(selected, key=lambda r: float(r[field]))
            last = selected[-1]
            output.append(
                {
                    "row_id": f"{period_name}-{series_name}",
                    "period": period_name,
                    "period_start": start.isoformat(),
                    "period_end": min(end, date.fromisoformat(str(selected[-1]["date"]))).isoformat(),
                    "series": series_name,
                    "observations": len(selected),
                    "mean_value": round(mean_value, 6),
                    "minimum_value": round(float(trough[field]), 6),
                    "minimum_date": trough["date"],
                    "maximum_value": round(float(peak[field]), 6),
                    "maximum_date": peak["date"],
                    "last_value": round(float(last[field]), 6),
                    "last_date": last["date"],
                    "change_from_pre_shock_mean": round(mean_value - baseline[series_name], 6),
                    "percent_change_from_pre_shock_mean": (
                        round((mean_value / baseline[series_name] - 1) * 100, 6)
                        if baseline[series_name] != 0
                        else None
                    ),
                    "unit": "usd_per_bbl",
                    "interpretation": (
                        "Descriptive market context only; do not translate this price move into barrels "
                        "or use it to validate/reject the volume balance mechanically."
                    ),
                    "source_url": FRED_URL,
                }
            )
    return output


FUTURES_SYMBOLS = {
    "wti_front": "CL=F",
    "wti_sep26": "CLU26.NYM",
    "wti_oct26": "CLV26.NYM",
    "wti_dec26": "CLZ26.NYM",
    "brent_front": "BZ=F",
    "brent_sep26": "BZU26.NYM",
    "brent_oct26": "BZV26.NYM",
    "brent_dec26": "BZZ26.NYM",
}


def yahoo_url(symbol: str) -> str:
    start_epoch = int(datetime.combine(START, time.min, tzinfo=UTC).timestamp())
    end_epoch = int(datetime.combine(END + timedelta(days=1), time.min, tzinfo=UTC).timestamp())
    return (
        f"{YAHOO_CHART_ROOT}{symbol}?period1={start_epoch}&period2={end_epoch}"
        "&interval=1d&events=history"
    )


def load_futures_close(symbol: str) -> dict[date, float]:
    payload = json.loads(download_text(yahoo_url(symbol)))
    result = payload.get("chart", {}).get("result")
    if not result:
        raise RuntimeError(f"No Yahoo Finance chart result returned for {symbol}")
    chart = result[0]
    timestamps = chart.get("timestamp", [])
    closes = chart.get("indicators", {}).get("quote", [{}])[0].get("close", [])
    if len(timestamps) != len(closes):
        raise RuntimeError(f"Timestamp/close length mismatch for {symbol}")
    observations: dict[date, float] = {}
    for epoch, close in zip(timestamps, closes, strict=True):
        day = datetime.fromtimestamp(epoch, UTC).date()
        if START <= day <= LATEST_COMPLETED_FUTURES_SESSION and close is not None:
            observations[day] = float(close)
    if not observations:
        raise RuntimeError(f"No futures closes returned for {symbol}")
    return observations


def build_time_spreads() -> list[dict[str, object]]:
    prices: dict[str, dict[date, float]] = {}
    prior_rows = (
        read_existing_time_spreads() if TIME_SPREAD_DAILY_OUT.exists() else []
    )
    for name, symbol in FUTURES_SYMBOLS.items():
        try:
            prices[name] = load_futures_close(symbol)
        except Exception:
            # Yahoo sometimes removes an expired fixed-contract chart while the
            # continuous and later fixed contracts remain available. Preserve the
            # previously captured closes rather than deleting valid history.
            if name != "brent_sep26":
                raise
            field = f"{name}_close_usd_per_bbl"
            preserved = {
                date.fromisoformat(row["date"]): float(row[field])
                for row in prior_rows if row.get(field) not in {None, ""}
            }
            if not preserved:
                raise
            prices[name] = preserved
    days = sorted(set().union(*(series.keys() for series in prices.values())))
    output: list[dict[str, object]] = []
    for day in days:
        row: dict[str, object] = {"date": day.isoformat()}
        for name in FUTURES_SYMBOLS:
            row[f"{name}_close_usd_per_bbl"] = prices[name].get(day)
        pairs = {
            "wti_front_minus_dec26_usd_per_bbl": ("wti_front", "wti_dec26"),
            "wti_sep26_minus_oct26_usd_per_bbl": ("wti_sep26", "wti_oct26"),
            "brent_front_minus_dec26_usd_per_bbl": ("brent_front", "brent_dec26"),
            "brent_sep26_minus_oct26_usd_per_bbl": ("brent_sep26", "brent_oct26"),
        }
        for field, (near_name, far_name) in pairs.items():
            near_value = prices[near_name].get(day)
            far_value = prices[far_name].get(day)
            row[field] = (
                round(near_value - far_value, 6)
                if near_value is not None and far_value is not None
                else None
            )
        row.update(
            {
                "spread_sign_convention": (
                    "near_minus_deferred: positive=backwardation; negative=contango"
                ),
                "data_status": (
                    "public daily closes transported by Yahoo Finance; not exchange-certified settlements"
                ),
                "source_url": YAHOO_CHART_ROOT,
                "method_caveat": (
                    "Continuous front symbols roll contracts; fixed Sep-Oct spreads avoid roll ambiguity but "
                    "were deferred contracts in early 2026. The curve is a storage discriminator only, not a "
                    "shortage-volume estimator or price forecast."
                ),
            }
        )
        output.append(row)
    return output


def read_existing_time_spreads() -> list[dict[str, str]]:
    with TIME_SPREAD_DAILY_OUT.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


TIME_SPREAD_FIELDS = {
    "wti_front_minus_dec26": "wti_front_minus_dec26_usd_per_bbl",
    "wti_sep26_minus_oct26": "wti_sep26_minus_oct26_usd_per_bbl",
    "brent_front_minus_dec26": "brent_front_minus_dec26_usd_per_bbl",
    "brent_sep26_minus_oct26": "brent_sep26_minus_oct26_usd_per_bbl",
}


def summarize_time_spreads(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for period_name, (start, end) in PERIODS.items():
        for series_name, field in TIME_SPREAD_FIELDS.items():
            selected = [
                row
                for row in rows
                if start <= date.fromisoformat(str(row["date"])) <= end and row[field] is not None
            ]
            if not selected:
                continue
            values = [float(row[field]) for row in selected]
            positive = sum(value > 0 for value in values)
            negative = sum(value < 0 for value in values)
            zero = len(values) - positive - negative
            output.append(
                {
                    "row_id": f"{period_name}-{series_name}",
                    "period": period_name,
                    "period_start": start.isoformat(),
                    "period_end": selected[-1]["date"],
                    "series": series_name,
                    "observations": len(values),
                    "mean_near_minus_deferred_usd_per_bbl": round(statistics.fmean(values), 6),
                    "minimum_near_minus_deferred_usd_per_bbl": round(min(values), 6),
                    "maximum_near_minus_deferred_usd_per_bbl": round(max(values), 6),
                    "backwardation_days": positive,
                    "contango_days": negative,
                    "flat_days": zero,
                    "backwardation_share_percent": round(100 * positive / len(values), 6),
                    "period_regime": (
                        "all_observed_days_backwardated"
                        if positive == len(values)
                        else "predominantly_backwardated"
                        if positive / len(values) >= 0.8
                        else "mixed_or_contango"
                    ),
                    "storage_discriminator": (
                        "Positive spreads make prompt-to-deferred carry unattractive before freight, "
                        "insurance and financing, weakening discretionary storage arbitrage as an explanation. "
                        "They do not exclude involuntary blocked cargoes, congestion, sanctioned-fleet dwell or "
                        "mechanically longer voyage float."
                    ),
                    "evidentiary_weight": (
                        "medium: public closes, cross-checked against CME commentary and latest bulletin; "
                        "not exchange-certified historical settlements"
                    ),
                    "source_url": YAHOO_CHART_ROOT,
                }
            )
    return output


PRODUCT_FIELDS = {
    "usgc_regular_gasoline_spot_usd_per_gal": "DGASUSGULF",
    "usgc_ultra_low_sulfur_diesel_spot_usd_per_gal": "DDFUELUSGULF",
    "usgc_jet_fuel_spot_usd_per_gal": "DJFUELUSGULF",
    "us_regular_gasoline_retail_usd_per_gal": "GASREGW",
    "us_onhighway_diesel_retail_usd_per_gal": "GASDESW",
}


def load_product_retail_prices(crude_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Load official EIA product spot and weekly retail prices via FRED transport."""
    by_day: dict[date, dict[str, object]] = {}
    brent = {
        date.fromisoformat(str(row["date"])): float(row["brent_spot_usd_per_bbl"])
        for row in crude_rows if row["brent_spot_usd_per_bbl"] is not None
    }

    for raw in csv.DictReader(io.StringIO(download_text(PRODUCT_SPOT_FRED_URL))):
        day = datetime.strptime(raw["observation_date"], "%Y-%m-%d").date()
        if not START <= day <= END:
            continue
        row = by_day.setdefault(day, {"date": day.isoformat()})
        for output_field, fred_id in list(PRODUCT_FIELDS.items())[:3]:
            row[output_field] = number(raw.get(fred_id))

    for raw in csv.DictReader(io.StringIO(download_text(RETAIL_FRED_URL))):
        day = datetime.strptime(raw["observation_date"], "%Y-%m-%d").date()
        if not START <= day <= END:
            continue
        row = by_day.setdefault(day, {"date": day.isoformat()})
        for output_field, fred_id in list(PRODUCT_FIELDS.items())[3:]:
            row[output_field] = number(raw.get(fred_id))

    rows: list[dict[str, object]] = []
    for day in sorted(by_day):
        row = by_day[day]
        for field in PRODUCT_FIELDS:
            row.setdefault(field, None)
        brent_value = brent.get(day)
        for product in ("gasoline", "diesel", "jet_fuel"):
            spot_field = next(field for field in PRODUCT_FIELDS if product in field and "spot" in field)
            spot = row[spot_field]
            row[f"{product}_minus_brent42_gross_crack_proxy_usd_per_gal"] = (
                round(float(spot) - brent_value / 42.0, 6)
                if spot is not None and brent_value is not None else None
            )
        row.update({
            "period_label": period_label(day),
            "data_status": (
                "EIA daily spot and weekly retail observations transported by FRED; "
                "blank fields reflect frequency or reporting lags"
            ),
            "source_url": f"{EIA_PRODUCT_SPOT_URL} | {EIA_RETAIL_URL}",
            "method_caveat": (
                "Gross crack proxies subtract Brent/42 from a US Gulf Coast product spot price. "
                "They exclude refinery yields, fuel use, losses, transport, compliance, financing, "
                "taxes and regional basis, so they are descriptive product-strength indicators, "
                "not realized refinery margins. Retail prices include taxes and lag wholesale markets."
            ),
        })
        rows.append(row)
    if not rows:
        raise RuntimeError("No EIA product or retail observations returned")
    return rows


def summarize_product_retail(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    series = [*PRODUCT_FIELDS, *[
        "gasoline_minus_brent42_gross_crack_proxy_usd_per_gal",
        "diesel_minus_brent42_gross_crack_proxy_usd_per_gal",
        "jet_fuel_minus_brent42_gross_crack_proxy_usd_per_gal",
    ]]
    baseline: dict[str, float] = {}
    for field in series:
        values = [
            float(row[field]) for row in rows
            if row[field] is not None
            and date(2026, 1, 1) <= date.fromisoformat(str(row["date"])) <= date(2026, 2, 27)
        ]
        if values:
            baseline[field] = statistics.fmean(values)
    output: list[dict[str, object]] = []
    for period_name, (start, end) in PERIODS.items():
        for field in series:
            selected = [
                row for row in rows if row[field] is not None
                and start <= date.fromisoformat(str(row["date"])) <= end
            ]
            if not selected:
                continue
            values = [float(row[field]) for row in selected]
            output.append({
                "row_id": f"{period_name}-{field.removesuffix('_usd_per_gal')}",
                "period": period_name, "period_start": start.isoformat(),
                "period_end": selected[-1]["date"], "series": field,
                "observations": len(values), "mean_usd_per_gal": round(statistics.fmean(values), 6),
                "minimum_usd_per_gal": round(min(values), 6), "maximum_usd_per_gal": round(max(values), 6),
                "last_usd_per_gal": round(values[-1], 6), "last_date": selected[-1]["date"],
                "change_from_pre_shock_mean_usd_per_gal": (
                    round(statistics.fmean(values) - baseline[field], 6) if field in baseline else None
                ),
                "interpretation": (
                    "Realized product or retail price context only. Do not infer demand reduction, "
                    "shortage volumes or causal Hormuz attribution from this series alone."
                ),
                "source_url": f"{EIA_PRODUCT_SPOT_URL} | {EIA_RETAIL_URL}",
            })
    return output


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate(daily: list[dict[str, object]], summary: list[dict[str, object]],
             spreads: list[dict[str, object]], spread_summary: list[dict[str, object]],
             products: list[dict[str, object]], product_summary: list[dict[str, object]]) -> None:
    for rows, label in ((daily, "spot"), (spreads, "spreads"), (products, "products")):
        dates = [str(row["date"]) for row in rows]
        if dates != sorted(dates) or len(dates) != len(set(dates)):
            raise ValueError(f"{label} dates are not sorted and unique")
    if daily[-1]["date"] != "2026-08-11":
        raise ValueError("EIA/FRED crude spot endpoint changed; audit reporting lag")
    if spreads[-1]["date"] != "2026-08-17":
        raise ValueError("futures curves do not reach the latest completed pre-publication session")
    retail = [row for row in products if row["us_regular_gasoline_retail_usd_per_gal"] is not None]
    if not retail or retail[-1]["date"] != "2026-08-17":
        raise ValueError("weekly retail series does not reach latest publication-week observation")
    for row in spreads:
        for prefix in ("wti", "brent"):
            front, dec = row[f"{prefix}_front_close_usd_per_bbl"], row[f"{prefix}_dec26_close_usd_per_bbl"]
            spread = row[f"{prefix}_front_minus_dec26_usd_per_bbl"]
            if front is not None and dec is not None and abs(float(front) - float(dec) - float(spread)) > 1e-5:
                raise ValueError(f"spread identity failed for {prefix} {row['date']}")
    checks = {(row["period"], row["series"]): row for row in spread_summary}
    if checks[("march_june", "wti_front_minus_dec26")]["backwardation_days"] != 84:
        raise ValueError("March-June WTI regime changed")
    if checks[("march_june", "brent_front_minus_dec26")]["backwardation_days"] != 82:
        raise ValueError("March-June Brent regime changed")
    for series in ("wti_front_minus_dec26", "brent_front_minus_dec26"):
        row = checks[("post_reclosure_july8_publication", series)]
        if row["backwardation_days"] != row["observations"]:
            raise ValueError(f"post-reclosure {series} not fully backwardated")
    if not summary or not product_summary:
        raise ValueError("empty summary output")


def main() -> None:
    daily = load_daily()
    summary = summarize(daily)
    time_spread_daily = build_time_spreads()
    time_spread_summary = summarize_time_spreads(time_spread_daily)
    product_daily = load_product_retail_prices(daily)
    product_summary = summarize_product_retail(product_daily)
    validate(daily, summary, time_spread_daily, time_spread_summary, product_daily, product_summary)
    write_csv(DAILY_OUT, daily)
    write_csv(SUMMARY_OUT, summary)
    write_csv(TIME_SPREAD_DAILY_OUT, time_spread_daily)
    write_csv(TIME_SPREAD_SUMMARY_OUT, time_spread_summary)
    write_csv(PRODUCT_DAILY_OUT, product_daily)
    write_csv(PRODUCT_SUMMARY_OUT, product_summary)
    print(f"Wrote {len(daily)} daily rows to {DAILY_OUT.relative_to(ROOT)}")
    print(f"Wrote {len(summary)} summary rows to {SUMMARY_OUT.relative_to(ROOT)}")
    print(
        f"Wrote {len(time_spread_daily)} daily time-spread rows to "
        f"{TIME_SPREAD_DAILY_OUT.relative_to(ROOT)}"
    )
    print(
        f"Wrote {len(time_spread_summary)} time-spread summaries to "
        f"{TIME_SPREAD_SUMMARY_OUT.relative_to(ROOT)}"
    )
    print(f"Wrote {len(product_daily)} product/retail rows to {PRODUCT_DAILY_OUT.relative_to(ROOT)}")
    print(f"Wrote {len(product_summary)} product/retail summaries to {PRODUCT_SUMMARY_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
