#!/usr/bin/env python3
"""Build the March-July 2026 Gulf physical-oil ledger.

The country shut-in table is a direct transcription of EIA's July 2026 STEO
Table 1. Route rows are a deliberately low-fidelity public-source
reconstruction calibrated to IEA aggregate anchors; their estimate type and
method fields prevent them from being mistaken for measured cargo data.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_6_gulf_physical_oil_ledger.csv"

FIELDS = [
    "row_id",
    "record_type",
    "observation_month",
    "period_start",
    "period_end",
    "days",
    "country",
    "route_or_scope",
    "metric",
    "value_mb_per_day",
    "period_million_barrels",
    "cumulative_million_barrels",
    "counterfactual_mb_per_day",
    "delta_vs_counterfactual_mb_per_day",
    "uncertainty_low_million_barrels",
    "uncertainty_high_million_barrels",
    "data_status",
    "estimate_type",
    "product_scope",
    "source_vintage",
    "source_url",
    "method",
    "confidence",
    "double_counting_note",
]

EIA_JULY = "https://www.eia.gov/outlooks/steo/archives/jul26.pdf"
IEA_APRIL = "https://www.iea.org/reports/oil-market-report-april-2026"
IEA_MARCH = "https://www.iea.org/reports/oil-market-report-march-2026"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEA_JULY_OMR = "https://www.iea.org/reports/oil-market-report-july-2026"
IEA_COMMENTARY = (
    "https://www.iea.org/commentaries/"
    "how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"
)
ARAMCO_Q1 = "https://www.aramco.com/en/news-media/news/2026/aramco-announces-first-quarter-2026-results"
IRAQ_CEYHAN = (
    "https://www.thenationalnews.com/business/energy/2026/03/18/"
    "iraq-to-resume-oil-exports-via-turkeys-ceyhan-port-amid-regional-tensions/"
)

MONTHS = {
    "2026-03": ("2026-03-01", "2026-03-31", 31),
    "2026-04": ("2026-04-01", "2026-04-30", 30),
    "2026-05": ("2026-05-01", "2026-05-31", 31),
    "2026-06": ("2026-06-01", "2026-06-30", 30),
    "2026-07": ("2026-07-01", "2026-07-31", 31),
}

# EIA July STEO Table 1, mb/d. February is production; March-June are
# closure-related crude-production shut-ins, not total-liquids losses.
EIA_CRUDE = {
    "Kuwait": (2.560, {"2026-03": 1.400, "2026-04": 2.000, "2026-05": 2.030, "2026-06": 1.650}),
    "United Arab Emirates": (3.600, {"2026-03": 1.450, "2026-04": 1.100, "2026-05": 1.250, "2026-06": 0.150}),
    "Iran": (3.390, {"2026-03": 0.130, "2026-04": 0.230, "2026-05": 0.780, "2026-06": 0.580}),
    "Iraq": (4.400, {"2026-03": 2.840, "2026-04": 3.080, "2026-05": 3.190, "2026-06": 2.650}),
    "Qatar": (0.557, {"2026-03": 0.450, "2026-04": 0.500, "2026-05": 0.500, "2026-06": 0.450}),
    "Bahrain": (0.193, {"2026-03": 0.120, "2026-04": 0.150, "2026-05": 0.150, "2026-06": 0.150}),
    "Saudi Arabia": (10.500, {"2026-03": 2.500, "2026-04": 3.340, "2026-05": 3.300, "2026-06": 2.660}),
}

# Public-source route reconstruction. IEA reports aggregate alternative-route
# exports at less than 4 mb/d pre-war and 7.2 mb/d in early April. Values below
# use 3.8 as an explicit working baseline, interpolate the March ramp, and hold
# the early-April demonstrated rate through June. They are not Kpler cargo data.
ROUTES = {
    "Saudi Arabia": {
        "route": "East-West/Petroline to Yanbu",
        "baseline": 2.0,
        "flows": {"2026-03": 3.5, "2026-04": 5.0, "2026-05": 5.0, "2026-06": 5.0},
        "source": f"{IEA_COMMENTARY} | {ARAMCO_Q1}",
        "method": "IEA says Yanbu exports rose from 2 mb/d pre-war to more than 5 mb/d in early June; March is an interpolated ramp and April-June use the 5 mb/d lower bound. Aramco reports the pipeline reached 7 mb/d maximum capacity in Q1.",
    },
    "United Arab Emirates": {
        "route": "Habshan-Fujairah pipeline",
        "baseline": 1.1,
        "flows": {"2026-03": 1.5, "2026-04": 1.8, "2026-05": 1.8, "2026-06": 1.8},
        "source": IEA_COMMENTARY,
        "method": "IEA gives 1.8 mb/d pipeline capability and reports UAE total exports at 1.9 mb/d in March and 4.3 mb/d in early June; the route series ramps to demonstrated pipeline capability. Dark Hormuz/STS activity is excluded from this bypass row.",
    },
    "Iraq": {
        "route": "Iraq-Turkiye pipeline to Ceyhan",
        "baseline": 0.0,
        "flows": {"2026-03": 0.113, "2026-04": 0.250, "2026-05": 0.250, "2026-06": 0.250},
        "source": f"{IEA_COMMENTARY} | {IRAQ_CEYHAN}",
        "method": "Iraq's North Oil Company reported 250 kb/d starting 18 March. March monthly average is 0.25 mb/d for 14 of 31 days; April-June hold the reported initial rate.",
    },
    "Other Gulf route residual": {
        "route": "Iran Jask, Syria and other non-Hormuz route residual",
        "baseline": 0.7,
        "flows": {"2026-03": 0.387, "2026-04": 0.150, "2026-05": 0.150, "2026-06": 0.150},
        "source": f"{IEA_APRIL} | {IEA_COMMENTARY}",
        "method": "Arithmetic remainder needed for named routes to equal the 5.5 mb/d March working estimate and IEA's 7.2 mb/d early-April aggregate. It is not a measured Iran/Jask series.",
    },
}


def fmt(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def add(rows: list[dict[str, str]], **kwargs: object) -> None:
    row = {field: "" for field in FIELDS}
    for key, value in kwargs.items():
        row[key] = fmt(value) if isinstance(value, float) else str(value)
    rows.append(row)


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    country_cumulative: dict[str, float] = {}

    for country, (baseline, shutins) in EIA_CRUDE.items():
        cumulative = 0.0
        for month, shutin in shutins.items():
            start, end, days = MONTHS[month]
            actual = baseline - shutin
            volume = shutin * days
            cumulative += volume
            add(
                rows,
                row_id=f"{country.lower().replace(' ', '_')}_{month}_crude_shutin",
                record_type="monthly_country_production",
                observation_month=month,
                period_start=start,
                period_end=end,
                days=days,
                country=country,
                route_or_scope="upstream crude production",
                metric="closure_related_crude_production_shutin",
                value_mb_per_day=shutin,
                period_million_barrels=volume,
                counterfactual_mb_per_day=baseline,
                delta_vs_counterfactual_mb_per_day=-shutin,
                data_status="estimated_actual",
                estimate_type="official_estimate",
                product_scope="crude_oil",
                source_vintage="EIA STEO 2026-07-07",
                source_url=EIA_JULY,
                method="Direct transcription of EIA July STEO Table 1; actual implied production is February production less the estimated closure-related shut-in.",
                confidence="high_for_source_medium_for_measurement",
                double_counting_note="This is the production loss itself. Do not add the corresponding implied actual production or route-preserved exports to it.",
            )
            add(
                rows,
                row_id=f"{country.lower().replace(' ', '_')}_{month}_implied_crude_production",
                record_type="monthly_country_production",
                observation_month=month,
                period_start=start,
                period_end=end,
                days=days,
                country=country,
                route_or_scope="upstream crude production",
                metric="implied_actual_crude_production",
                value_mb_per_day=actual,
                period_million_barrels=actual * days,
                counterfactual_mb_per_day=baseline,
                delta_vs_counterfactual_mb_per_day=-shutin,
                data_status="calculated_from_official_estimate",
                estimate_type="arithmetic",
                product_scope="crude_oil",
                source_vintage="EIA STEO 2026-07-07",
                source_url=EIA_JULY,
                method="February EIA production less EIA estimated shut-in.",
                confidence="medium_high",
                double_counting_note="Diagnostic production level; do not add it to the shut-in volume.",
            )
        country_cumulative[country] = cumulative
        add(
            rows,
            row_id=f"{country.lower().replace(' ', '_')}_mar_jun_cumulative_crude_shutin",
            record_type="cumulative_country_summary",
            period_start="2026-03-01",
            period_end="2026-06-30",
            days=122,
            country=country,
            route_or_scope="upstream crude production",
            metric="cumulative_closure_related_crude_production_shutin",
            cumulative_million_barrels=cumulative,
            counterfactual_mb_per_day=baseline,
            data_status="estimated_actual",
            estimate_type="official_estimate_times_calendar_days",
            product_scope="crude_oil",
            source_vintage="EIA STEO 2026-07-07",
            source_url=EIA_JULY,
            method="Sum of EIA monthly shut-in rates multiplied by calendar days, March-June.",
            confidence="medium_high",
            double_counting_note="Country rows sum exactly to the EIA total row.",
        )

    # July is not yet observed by country. Preserve the official quarterly
    # aggregate forecast without pretending it is a July actual or allocation.
    add(
        rows,
        row_id="gulf_2026_07_country_breakdown_unavailable",
        record_type="coverage_flag",
        observation_month="2026-07",
        period_start="2026-07-01",
        period_end="2026-07-31",
        days=31,
        country="Affected Gulf producers",
        route_or_scope="upstream crude production",
        metric="country_level_crude_shutin",
        data_status="not_yet_observed",
        estimate_type="coverage_flag",
        product_scope="crude_oil",
        source_vintage="as of 2026-08-04",
        source_url=EIA_JULY,
        method="EIA explicitly publishes only aggregate future disruptions. Its 3Q26 forecast is 5.427 mb/d, but this is not a July actual and predates renewed 7-8 July hostilities.",
        confidence="high",
        double_counting_note="Do not assign the 3Q aggregate to countries or treat it as observed July history.",
    )
    add(
        rows,
        row_id="gulf_2026_q3_official_crude_shutin_forecast",
        record_type="forecast_context",
        observation_month="2026-07",
        period_start="2026-07-01",
        period_end="2026-09-30",
        days=92,
        country="Affected Gulf producers",
        route_or_scope="upstream crude production",
        metric="aggregate_crude_production_shutin_forecast",
        value_mb_per_day=5.427,
        data_status="forecast_not_historical",
        estimate_type="official_forecast",
        product_scope="crude_oil",
        source_vintage="EIA STEO 2026-07-07",
        source_url=EIA_JULY,
        method="Direct EIA 3Q26 aggregate; retained only as forecast context.",
        confidence="low_after_renewed_july_hostilities",
        double_counting_note="Excluded from every March-June cumulative actual/estimate total.",
    )

    # Broader IEA total-oil anchors. These are not as consistently defined or
    # measured as EIA's country crude table, but they keep condensates, NGLs and
    # other liquids visible instead of silently calling crude 'all oil'.
    iea_total_oil = {
        "2026-03": (10.0, "point_in_time_lower_bound", IEA_MARCH, "IEA said Gulf total-oil production was curtailed by at least 10 mb/d, comprising at least 8 mb/d crude and 2 mb/d condensates/NGLs."),
        "2026-04": (14.4, "preliminary_monthly_estimate", IEA_MAY, "IEA estimated affected Gulf-country output 14.4 mb/d below pre-war levels in April."),
        "2026-05": (14.0, "point_in_time_lower_bound", IEA_MAY, "IEA said more than 14 mb/d of Gulf oil was shut in at publication; 14 is retained as a conservative floor, not an exact monthly observation."),
        "2026-06": (11.4, "preliminary_monthly_estimate", IEA_JULY_OMR, "IEA estimated Gulf production 11.4 mb/d below pre-war levels after the June partial reopening."),
    }
    integrated_total_oil = 0.0
    for month, (loss, status, url, method) in iea_total_oil.items():
        start, end, days = MONTHS[month]
        integrated_total_oil += loss * days
        add(
            rows,
            row_id=f"iea_{month}_affected_gulf_total_oil_loss",
            record_type="monthly_aggregate_crosscheck",
            observation_month=month,
            period_start=start,
            period_end=end,
            days=days,
            country="Affected Gulf producers",
            route_or_scope="upstream total-oil production",
            metric="affected_gulf_total_oil_loss_vs_prewar",
            value_mb_per_day=loss,
            period_million_barrels=loss * days,
            data_status=status,
            estimate_type="official_reported_anchor",
            product_scope="total_oil_including_crude_condensates_ngls",
            source_vintage="IEA OMR March-July 2026",
            source_url=url,
            method=method,
            confidence="medium",
            double_counting_note="Broader taxonomy than EIA country crude shut-ins. Use as a cross-check/range, not an additive component.",
        )
    add(
        rows,
        row_id="iea_mar_jun_total_oil_loss_rough_integration",
        record_type="cumulative_aggregate_crosscheck",
        period_start="2026-03-01",
        period_end="2026-06-30",
        days=122,
        country="Affected Gulf producers",
        route_or_scope="upstream total-oil production",
        metric="rough_cumulative_affected_gulf_total_oil_loss",
        cumulative_million_barrels=integrated_total_oil,
        data_status="rough_integration_of_mixed_status_anchors",
        estimate_type="calculated_crosscheck",
        product_scope="total_oil_including_crude_condensates_ngls",
        source_vintage="IEA OMR March-July 2026",
        source_url=f"{IEA_MARCH} | {IEA_MAY} | {IEA_JULY_OMR} | {IEA_COMMENTARY}",
        method="Monthly rates are multiplied by calendar days. March and May are point-in-time lower bounds, so 1.518 billion barrels is a rough floor-like integration, not an official IEA cumulative series. IEA independently reported cumulative Middle East producer losses above 1.3 billion barrels as of 22 June.",
        confidence="low_medium",
        double_counting_note="Do not add to the 1.183 billion barrels of EIA crude shut-ins; crude is a subset of this broader total-oil estimate.",
    )

    # Route reconstruction, including aggregate alternative-route totals.
    route_month_totals: dict[str, float] = {m: 0.0 for m in MONTHS if m != "2026-07"}
    route_baseline_total = sum(spec["baseline"] for spec in ROUTES.values())
    for country, spec in ROUTES.items():
        cumulative_gross = 0.0
        cumulative_incremental = 0.0
        for month, flow in spec["flows"].items():
            start, end, days = MONTHS[month]
            baseline = float(spec["baseline"])
            incremental = flow - baseline
            route_month_totals[month] += flow
            cumulative_gross += flow * days
            cumulative_incremental += incremental * days
            add(
                rows,
                row_id=f"{country.lower().replace(' ', '_')}_{month}_bypass_flow",
                record_type="monthly_route_reconstruction",
                observation_month=month,
                period_start=start,
                period_end=end,
                days=days,
                country=country,
                route_or_scope=spec["route"],
                metric="gross_non_hormuz_export_flow",
                value_mb_per_day=flow,
                period_million_barrels=flow * days,
                counterfactual_mb_per_day=baseline,
                delta_vs_counterfactual_mb_per_day=incremental,
                data_status="bounded_reconstruction",
                estimate_type="calibrated_estimate",
                product_scope="total_oil_route_flow",
                source_vintage="IEA 2026-04-14 and 2026-06-22; operator/press as cited",
                source_url=spec["source"],
                method=spec["method"],
                confidence="low_medium",
                double_counting_note="Gross route flow preserves exports already embedded in actual production. Only the increment above the pre-war route baseline is a mitigation increment; neither is new global production.",
            )
        add(
            rows,
            row_id=f"{country.lower().replace(' ', '_')}_mar_jun_bypass_summary",
            record_type="cumulative_route_summary",
            period_start="2026-03-01",
            period_end="2026-06-30",
            days=122,
            country=country,
            route_or_scope=spec["route"],
            metric="cumulative_gross_and_incremental_non_hormuz_exports",
            period_million_barrels=cumulative_gross,
            cumulative_million_barrels=cumulative_incremental,
            counterfactual_mb_per_day=float(spec["baseline"]),
            data_status="bounded_reconstruction",
            estimate_type="calibrated_estimate",
            product_scope="total_oil_route_flow",
            source_vintage="IEA 2026-04-14 and 2026-06-22; operator/press as cited",
            source_url=spec["source"],
            method="period_million_barrels is gross route flow; cumulative_million_barrels is the increment above the pre-war route baseline.",
            confidence="low_medium",
            double_counting_note="Do not sum gross and incremental columns; incremental is a subset/difference of gross.",
        )

    # Hormuz aggregate: March-May is the IEA period average replicated solely
    # for volume integration; June is total Gulf exports less the 7.2 route
    # reconstruction. The latter is an inference, not a tanker-volume measure.
    hormuz_flows = {"2026-03": 2.7, "2026-04": 2.7, "2026-05": 2.7, "2026-06": 8.9}
    gross_missing_hormuz = 0.0
    gross_hormuz = 0.0
    bypass_incremental = 0.0
    bypass_gross = 0.0
    for month, flow in hormuz_flows.items():
        start, end, days = MONTHS[month]
        alt = route_month_totals[month]
        gross_hormuz += flow * days
        gross_missing_hormuz += (20.0 - flow) * days
        bypass_gross += alt * days
        bypass_incremental += (alt - route_baseline_total) * days
        add(
            rows,
            row_id=f"hormuz_{month}_oil_flow",
            record_type="monthly_route_reconstruction",
            observation_month=month,
            period_start=start,
            period_end=end,
            days=days,
            country="Gulf producers",
            route_or_scope="Strait of Hormuz",
            metric="oil_flow_through_hormuz",
            value_mb_per_day=flow,
            period_million_barrels=flow * days,
            counterfactual_mb_per_day=20.0,
            delta_vs_counterfactual_mb_per_day=flow - 20.0,
            data_status="period_average" if month != "2026-06" else "inferred_monthly_average",
            estimate_type="IEA_period_average" if month != "2026-06" else "arithmetic_inference",
            product_scope="total_oil_route_flow",
            source_vintage="IEA 2026-06-22 and OMR 2026-07-10",
            source_url=f"{IEA_COMMENTARY} | {IEA_JULY_OMR}",
            method="March-May each display the same IEA 2.7 mb/d March-May period average for integration, not separate monthly observations. June is 16.1 mb/d total Gulf exports less 7.2 mb/d alternative-route estimate.",
            confidence="medium" if month != "2026-06" else "low_medium",
            double_counting_note="Hormuz and non-Hormuz routes sum to reconstructed total Gulf exports. Neither is additional production.",
        )

    total_crude_shutin = sum(country_cumulative.values())
    route_net_disruption = gross_missing_hormuz - bypass_incremental
    residual = route_net_disruption - total_crude_shutin
    summaries = [
        ("mar_jun_eia_crude_shutin", "EIA country crude shut-ins", total_crude_shutin, None, None, "crude_oil", "official_estimate_times_calendar_days", EIA_JULY, "Sum of seven EIA country rows; exact match to EIA monthly totals multiplied by calendar days.", "medium_high"),
        ("mar_jun_gross_hormuz_flow_loss", "Gross missing Hormuz transit", gross_missing_hormuz, None, None, "total_oil_route_flow", "period_average_integration", IEA_COMMENTARY, "Pre-war 20 mb/d less 2.7 mb/d March-May average and inferred 8.9 mb/d June flow, multiplied by calendar days.", "medium"),
        ("mar_jun_gross_bypass_exports", "Gross exports via non-Hormuz routes", bypass_gross, None, None, "total_oil_route_flow", "calibrated_estimate", f"{IEA_APRIL} | {IEA_COMMENTARY}", "Named-route reconstruction calibrated to IEA's less-than-4 pre-war and 7.2 early-April aggregate.", "low_medium"),
        ("mar_jun_incremental_bypass_exports", "Incremental non-Hormuz exports above baseline", bypass_incremental, 300.0, 430.0, "total_oil_route_flow", "calibrated_estimate", f"{IEA_APRIL} | {IEA_COMMENTARY}", "Gross reconstructed bypass less a 3.8 mb/d pre-war working baseline. Range reflects ramp timing and the published 'less than 4' baseline.", "low_medium"),
        ("mar_jun_route_implied_net_disruption", "Route-implied disruption after incremental bypass", route_net_disruption, None, None, "mixed_total_oil_route_vs_crude", "arithmetic_diagnostic", f"{IEA_APRIL} | {IEA_COMMENTARY}", "Gross missing Hormuz flow less incremental bypass. Compare, do not add, to EIA crude shut-ins.", "low_medium"),
        ("mar_jun_route_vs_crude_residual", "Non-crude and timing residual after crude shut-ins", residual, None, None, "taxonomy_timing_residual", "arithmetic_residual", f"{EIA_JULY} | {IEA_COMMENTARY}", "Route-implied total-oil disruption less EIA crude shut-ins. It captures condensates/NGL/products, domestic use and refinery-run changes, storage timing, and route-estimation error; it is not a measured product loss.", "low"),
    ]
    for row_id, label, value, low, high, scope, estimate_type, url, method, confidence in summaries:
        add(
            rows,
            row_id=row_id,
            record_type="cumulative_reconciliation_summary",
            period_start="2026-03-01",
            period_end="2026-06-30",
            days=122,
            country="Gulf producers",
            route_or_scope=label,
            metric=row_id.removeprefix("mar_jun_"),
            cumulative_million_barrels=value,
            uncertainty_low_million_barrels=low,
            uncertainty_high_million_barrels=high,
            data_status="estimated_actual" if "forecast" not in row_id else "forecast",
            estimate_type=estimate_type,
            product_scope=scope,
            source_vintage="latest public evidence through 2026-07-10",
            source_url=url,
            method=method,
            confidence=confidence,
            double_counting_note="These rows form an audit comparison, not additive pie slices. Route preservation is already embodied in observed production and exports.",
        )

    # Storage timing anchors that explain why production, transit and delivered
    # exports do not line up month by month.
    add(
        rows,
        row_id="gulf_2026_03_storage_build",
        record_type="storage_timing_anchor",
        observation_month="2026-03",
        period_start="2026-03-01",
        period_end="2026-03-31",
        days=31,
        country="Middle East Gulf",
        route_or_scope="floating plus onshore storage",
        metric="gulf_inventory_change",
        period_million_barrels=120.0,
        data_status="preliminary_estimate",
        estimate_type="official_estimate",
        product_scope="crude_and_oil_products",
        source_vintage="IEA OMR 2026-04-14",
        source_url=IEA_APRIL,
        method="IEA reported +100 mb floating crude/products and +20 mb onshore crude in March.",
        confidence="medium",
        double_counting_note="A stock build is delayed export availability, not new supply and not an additional production loss.",
    )
    add(
        rows,
        row_id="gulf_2026_06_stock_release_inferred",
        record_type="storage_timing_anchor",
        observation_month="2026-06",
        period_start="2026-06-01",
        period_end="2026-06-30",
        days=30,
        country="Gulf producers",
        route_or_scope="floating and onshore inventories",
        metric="inferred_gulf_inventory_release_to_exports",
        value_mb_per_day=2.0,
        period_million_barrels=60.0,
        data_status="inferred",
        estimate_type="arithmetic_inference",
        product_scope="total_oil",
        source_vintage="IEA OMR 2026-07-10",
        source_url=IEA_JULY_OMR,
        method="June Gulf exports rose 6.5 mb/d while production rose 3.5 mb/d; the roughly 3 mb/d gap includes stock release and timing. A conservative 2 mb/d is recorded here because IEA explicitly attributes much of the crude/condensate increase to floating/onshore draws.",
        confidence="low",
        double_counting_note="Already embodied in June exports; do not add to production or route-preservation supply.",
    )

    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
