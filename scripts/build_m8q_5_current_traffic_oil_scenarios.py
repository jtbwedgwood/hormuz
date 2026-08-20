#!/usr/bin/env python3
"""Build provisional constant-current-traffic oil-supply scenarios for m8q.5.

The model deliberately does not turn tanker calls into barrels. PortWatch selects
the post-8 July traffic regime; IEA/EIA oil-flow and balance anchors set the
barrel ranges. Historical supply is compared with the frozen February 2026 EIA
STEO month-by-month counterfactual. Future cases hold the inferred Hormuz flow
range constant while allowing bypass, non-Gulf supply, stocks, and demand to
follow explicit durability rules.
"""

from __future__ import annotations

import calendar
import csv
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BALANCE = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
TRAFFIC = ROOT / "data/derived/hormuz_m8q_2_current_traffic_scenario.csv"
EVIDENCE = ROOT / "data/derived/hormuz_m8q_3_global_adjustment_evidence.csv"
OUT = ROOT / "data/derived/hormuz_m8q_5_current_traffic_oil_scenarios.csv"

FIELDS = [
    "row_id",
    "record_type",
    "scenario_case",
    "case_definition",
    "period_start",
    "period_end",
    "days",
    "horizon_date",
    "period_role",
    "data_status",
    "accounting_frame",
    "metric",
    "value_mb_per_day",
    "period_million_bbl",
    "cumulative_million_bbl",
    "unit",
    "source_vintage",
    "oil_data_cutoff",
    "traffic_data_cutoff",
    "source_url",
    "assumption",
    "durability_rule",
    "confidence",
    "double_counting_note",
]

EIA_FEB = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
EIA_JUL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
IEA_JUL = "https://www.iea.org/reports/oil-market-report-july-2026"
IEA_ADJUSTMENT = (
    "https://www.iea.org/commentaries/"
    "how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"
)
IEA_JUL21 = "https://www.iea.org/news/iea-executive-director-statement-on-oil-markets"
PORTWATCH = "https://portwatch.imf.org/pages/data-and-methodology"

OIL_CUTOFF = "2026-06-30"
TRAFFIC_CUTOFF = "2026-07-23"

# Frozen February STEO implied builds after the sibling source panel's July end.
# These values are supply less consumption from the same archived workbook.
FUTURE_PLANNED_BUILD = {
    "2026-08": 2.813778,
    "2026-09": 2.534034,
    "2026-10": 4.004066,
    "2026-11": 3.437439,
    "2026-12": 2.112715,
    "2027-01": 4.647934,
    "2027-02": 2.348762,
    "2027-03": 3.572021,
}

# Positive values are inventory draws that help clear the market; June is a
# negative contribution because IEA observed a net global build. July is an EIA
# 3Q-rate proxy, not an observation, and is kept visibly forecast-labelled.
OBSERVED_STOCK_CONTRIBUTION_MB = {
    "2026-03": 129.0,
    "2026-04": 117.0,
    "2026-05": 73.0,
    "2026-06": -21.0,
    "2026-07": 68.2,
}

CASES = {
    "low_supply": {
        "definition": "Stress case: lower inferred Strait flow, weaker bypass durability, and conservative stock-release capacity.",
        "hormuz_flow": 3.0,
        "bypass": {"near": 3.0, "q4": 2.7, "q1": 2.4},
        "non_gulf": {"near": 0.4, "q4": 0.5, "q1": 0.6},
        "demand": {"near": 5.0, "q4": 5.5, "q1": 6.0},
        "government": {"near": 1.0, "q4": 0.3, "q1": 0.1},
        "commercial": {"near": 2.5, "q4": 1.5, "q1": 0.8},
        "july_emergency_release": 290.0,
    },
    "base": {
        "definition": "Central case: inferred Strait flow modestly above the March-May oil-flow average, demonstrated bypass use, and tapering stock draws.",
        "hormuz_flow": 4.0,
        "bypass": {"near": 3.3, "q4": 3.1, "q1": 2.9},
        "non_gulf": {"near": 0.6, "q4": 0.8, "q1": 1.0},
        "demand": {"near": 4.5, "q4": 4.8, "q1": 5.2},
        "government": {"near": 1.4, "q4": 0.6, "q1": 0.3},
        "commercial": {"near": 3.1, "q4": 2.0, "q1": 1.2},
        "july_emergency_release": 315.0,
    },
    "high_supply": {
        "definition": "Resilient case: more AIS-dark/cargo flow, stronger bypass performance, and stronger durable supply and stock response.",
        "hormuz_flow": 5.5,
        "bypass": {"near": 3.8, "q4": 3.7, "q1": 3.6},
        "non_gulf": {"near": 0.9, "q4": 1.1, "q1": 1.3},
        "demand": {"near": 3.6, "q4": 3.6, "q1": 4.0},
        "government": {"near": 1.2, "q4": 0.8, "q1": 0.4},
        "commercial": {"near": 1.0, "q4": 0.8, "q1": 0.5},
        "july_emergency_release": 330.0,
    },
}

HORIZONS = ["2026-09-30", "2026-12-31", "2027-03-31"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def month_bounds(month: str) -> tuple[str, str, int]:
    year, number = map(int, month.split("-"))
    days = calendar.monthrange(year, number)[1]
    return f"{month}-01", f"{month}-{days:02d}", days


def number(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def make_row(**kwargs: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    for key, value in kwargs.items():
        if key not in result:
            raise KeyError(key)
        if isinstance(value, float):
            result[key] = number(value)
        else:
            result[key] = str(value)
    result["oil_data_cutoff"] = result["oil_data_cutoff"] or OIL_CUTOFF
    result["traffic_data_cutoff"] = result["traffic_data_cutoff"] or TRAFFIC_CUTOFF
    result["unit"] = result["unit"] or "mb/d and million_bbl"
    return result


def eia_value(
    rows: list[dict[str, str]], vintage: str, month: str, metric: str
) -> tuple[float, str]:
    matches = [
        row
        for row in rows
        if row["publication_vintage"] == vintage
        and row["observation_month"] == month
        and row["metric"] == metric
        and row["source_family"] == "EIA_STEO"
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one EIA row for {vintage} {month} {metric}, got {len(matches)}")
    return float(matches[0]["value"]), matches[0]["status"]


def validate_inputs(
    balance: list[dict[str, str]], traffic: list[dict[str, str]], evidence: list[dict[str, str]]
) -> None:
    if not balance or not traffic or not evidence:
        raise ValueError("one or more required m8q inputs are empty")
    tanker = [
        row
        for row in traffic
        if row["metric"] == "n_tanker_calls_per_day"
        and row["scenario_horizon"] == "2026-09-30"
    ]
    if len(tanker) != 1 or abs(float(tanker[0]["current_mean_calls_per_day"]) - 3.5) > 1e-9:
        raise ValueError("unexpected PortWatch current-regime anchor")
    needed = {"adj-004", "adj-008", "adj-010", "adj-018", "adj-019", "adj-039", "adj-040"}
    present = {row["evidence_id"] for row in evidence}
    if not needed.issubset(present):
        raise ValueError(f"missing adjustment evidence: {sorted(needed - present)}")


def add_component(
    rows: list[dict[str, str]],
    *,
    case: str,
    start: str,
    end: str,
    period_role: str,
    status: str,
    frame: str,
    metric: str,
    rate: float,
    source_vintage: str,
    source_url: str,
    assumption: str,
    durability: str,
    confidence: str,
    double_counting: str,
) -> None:
    days = (iso_date(end) - iso_date(start)).days + 1
    rows.append(
        make_row(
            row_id=f"{case}_{start}_{end}_{metric}",
            record_type="period_component",
            scenario_case=case,
            case_definition=CASES[case]["definition"],
            period_start=start,
            period_end=end,
            days=days,
            period_role=period_role,
            data_status=status,
            accounting_frame=frame,
            metric=metric,
            value_mb_per_day=rate,
            period_million_bbl=rate * days,
            source_vintage=source_vintage,
            source_url=source_url,
            assumption=assumption,
            durability_rule=durability,
            confidence=confidence,
            double_counting_note=double_counting,
        )
    )


def add_market_period(
    rows: list[dict[str, str]],
    *,
    case: str,
    start: str,
    end: str,
    role: str,
    status: str,
    net_loss: float,
    planned_build: float,
    demand: float,
    stock_metric: str,
    stock_rate: float,
    source_vintage: str,
    source_url: str,
    assumption: str,
) -> None:
    common_dc = "Market-clearing components sum to net_global_supply_loss; do not add them to that headline."
    add_component(
        rows,
        case=case,
        start=start,
        end=end,
        period_role=role,
        status=status,
        frame="market_clearing_bridge",
        metric="foregone_counterfactual_stock_build",
        rate=planned_build,
        source_vintage=source_vintage,
        source_url=source_url,
        assumption="Frozen February EIA supply less consumption; this is an avoided planned build, not oil newly delivered.",
        durability="Finite counterfactual cushion; retained only while using the frozen pre-war balance as the benchmark.",
        confidence="medium_high" if role == "historical" else "medium",
        double_counting=common_dc,
    )
    add_component(
        rows,
        case=case,
        start=start,
        end=end,
        period_role=role,
        status=status,
        frame="market_clearing_bridge",
        metric="demand_reduction",
        rate=demand,
        source_vintage=source_vintage,
        source_url=source_url,
        assumption=assumption,
        durability="Temporary shortage and conservation can persist under closure; rates rise modestly in longer cases but are not labeled structural fuel switching.",
        confidence="medium" if role != "historical" else "medium_high",
        double_counting=common_dc + " Refinery-run cuts and unquantified fuel switching remain inside this channel.",
    )
    add_component(
        rows,
        case=case,
        start=start,
        end=end,
        period_role=role,
        status=status,
        frame="market_clearing_bridge",
        metric=stock_metric,
        rate=stock_rate,
        source_vintage=source_vintage,
        source_url=source_url,
        assumption=assumption,
        durability="Observed/proxy total stocks are used historically; future government and commercial rates are separated and taper by horizon.",
        confidence="medium" if status != "preliminary_estimate" else "medium_high",
        double_counting=common_dc + " Historical total stock flow is split by ownership only in horizon summaries.",
    )
    residual = net_loss - planned_build - demand - stock_rate
    add_component(
        rows,
        case=case,
        start=start,
        end=end,
        period_role=role,
        status=status,
        frame="market_clearing_bridge",
        metric="residual_unallocated_adjustment",
        rate=residual,
        source_vintage=source_vintage,
        source_url=source_url,
        assumption="Arithmetic residual after the named non-overlapping bridge components.",
        durability="Carried explicitly and allowed to widen rather than forced into a preferred channel.",
        confidence="low",
        double_counting=common_dc + " It includes statistical discrepancy, timing, unobserved stocks, and scenario misspecification.",
    )


def build_rows(balance: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    # March-June history: the July EIA vintage supplies preliminary monthly
    # levels; the February EIA vintage supplies a seasonally varying frozen
    # counterfactual. IEA level-loss anchors are noted as cross-checks.
    iea_crosscheck = {"2026-03": 10.1, "2026-04": 12.8, "2026-05": 13.6, "2026-06": 9.4}
    for case in CASES:
        for month in ["2026-03", "2026-04", "2026-05", "2026-06"]:
            start, end, days = month_bounds(month)
            cf_supply, _ = eia_value(balance, "2026-02-10", month, "global_liquids_supply")
            cf_demand, _ = eia_value(balance, "2026-02-10", month, "global_liquids_consumption")
            actual_supply, supply_status = eia_value(balance, "2026-07-07", month, "global_liquids_supply")
            actual_demand, _ = eia_value(balance, "2026-07-07", month, "global_liquids_consumption")
            loss = cf_supply - actual_supply
            demand = cf_demand - actual_demand
            planned = cf_supply - cf_demand
            stock_rate = OBSERVED_STOCK_CONTRIBUTION_MB[month] / days
            add_component(
                rows,
                case=case,
                start=start,
                end=end,
                period_role="historical",
                status=supply_status,
                frame="physical_supply_bridge",
                metric="net_global_supply_loss",
                rate=loss,
                source_vintage="EIA STEO 2026-02-10 counterfactual; EIA STEO 2026-07-07 preliminary",
                source_url=f"{EIA_FEB} | {EIA_JUL} | {IEA_JUL}",
                assumption=f"Frozen February monthly EIA supply less July-vintage preliminary supply; IEA level/change cross-check is {iea_crosscheck[month]:.1f} mb/d.",
                durability="Historical value; no extrapolation.",
                confidence="medium_high",
                double_counting="Net loss is the physical headline. Market-clearing rows explain how it was absorbed and must not be added to it.",
            )
            add_market_period(
                rows,
                case=case,
                start=start,
                end=end,
                role="historical",
                status="preliminary_estimate",
                net_loss=loss,
                planned_build=planned,
                demand=demand,
                stock_metric="observed_total_stock_draw",
                stock_rate=stock_rate,
                source_vintage="EIA STEO 2026-02-10/2026-07-07; latest public IEA OMR stock observation",
                source_url=f"{EIA_FEB} | {EIA_JUL} | {IEA_JUL}",
                assumption="Demand is frozen-February EIA consumption less July-vintage consumption. Stock flow uses latest public IEA observed totals, so the residual preserves the EIA/IEA measurement difference.",
            )

    # July 1-7 retains the pre-escalation EIA forecast. July 8-31 uses the
    # current-traffic oil-volume range. The PortWatch source observes calls only
    # through July 23; July 24-31 is a nowcast at the July 8-23 rate.
    jul_cf_supply, _ = eia_value(balance, "2026-02-10", "2026-07", "global_liquids_supply")
    jul_cf_demand, _ = eia_value(balance, "2026-02-10", "2026-07", "global_liquids_consumption")
    jul_latest_supply, _ = eia_value(balance, "2026-07-07", "2026-07", "global_liquids_supply")
    jul_latest_demand, _ = eia_value(balance, "2026-07-07", "2026-07", "global_liquids_consumption")
    jul_loss = jul_cf_supply - jul_latest_supply
    jul_demand = jul_cf_demand - jul_latest_demand
    jul_planned = jul_cf_supply - jul_cf_demand
    jul_stock_rate = OBSERVED_STOCK_CONTRIBUTION_MB["2026-07"] / 31

    for case, spec in CASES.items():
        add_component(
            rows,
            case=case,
            start="2026-07-01",
            end="2026-07-07",
            period_role="july_pre_escalation_forecast",
            status="forecast",
            frame="physical_supply_bridge",
            metric="net_global_supply_loss",
            rate=jul_loss,
            source_vintage="EIA STEO 2026-07-07, forecast completed 2026-07-01",
            source_url=EIA_JUL,
            assumption="Retains the July STEO forecast for the seven days before the 7-8 July renewed escalation.",
            durability="Superseded for July 8 onward by the observed low-traffic regime.",
            confidence="medium",
            double_counting="Net loss is the physical headline; market-clearing components sum to it.",
        )
        add_market_period(
            rows,
            case=case,
            start="2026-07-01",
            end="2026-07-07",
            role="july_pre_escalation_forecast",
            status="forecast",
            net_loss=jul_loss,
            planned_build=jul_planned,
            demand=jul_demand,
            stock_metric="forecast_total_stock_draw",
            stock_rate=jul_stock_rate,
            source_vintage="EIA STEO 2026-02-10/2026-07-07; project July stock proxy",
            source_url=f"{EIA_FEB} | {EIA_JUL}",
            assumption="July demand follows the July STEO; stock draw applies the 2.2 mb/d 3Q EIA proxy uniformly. Neither is observed July data.",
        )

        # The physical mapping is an independently bounded oil-flow judgment,
        # never 3.5 PortWatch tanker calls/day multiplied by a cargo factor.
        hormuz = float(spec["hormuz_flow"])
        bypass = float(spec["bypass"]["near"])
        non_gulf = float(spec["non_gulf"]["near"])
        current_loss = 20.0 - hormuz - bypass - non_gulf
        physical_specs = [
            (
                "gross_missing_hormuz_flow",
                20.0 - hormuz,
                "IEA pre-war Hormuz flow of about 20 mb/d less the independently bounded current oil flow.",
                "Held at the July 8-23 traffic regime through every horizon; political and security conditions can invalidate it abruptly.",
            ),
            (
                "incremental_gulf_bypass_offset",
                bypass,
                "Increment above the pre-war non-Hormuz route base; bounded by IEA's 7.2 mb/d early-April alternative-route total versus less than 4 mb/d pre-war.",
                "Demonstrated infrastructure continues, but the rate tapers for maintenance, terminal, security, and Bab el-Mandeb risk.",
            ),
            (
                "incremental_non_gulf_supply_offset",
                non_gulf,
                "Increment versus the frozen outlook, not Atlantic Basin export redirection; central near-term rate uses IEA's 0.6 mb/d upward Americas-growth revision.",
                "Ramps slowly with projects and wells; port, quality, decline, maintenance, and sanctions limit the response.",
            ),
            (
                "net_global_supply_loss",
                current_loss,
                "Gross missing Hormuz flow less incremental Gulf bypass and incremental non-Gulf supply.",
                "Held near the current physical state; bypass taper is partly offset by non-Gulf ramp in the base case.",
            ),
        ]
        for metric, rate, assumption, durability in physical_specs:
            add_component(
                rows,
                case=case,
                start="2026-07-08",
                end="2026-07-31",
                period_role="current_traffic_july_nowcast",
                status="analyst_nowcast",
                frame="physical_supply_bridge",
                metric=metric,
                rate=rate,
                source_vintage="PortWatch through 2026-07-23; IEA through 2026-07-21",
                source_url=f"{PORTWATCH} | {IEA_ADJUSTMENT} | {IEA_JUL} | {IEA_JUL21}",
                assumption=assumption,
                durability=durability,
                confidence="low" if metric != "net_global_supply_loss" else "low_medium",
                double_counting="Gross missing route flow minus the two physical offsets equals net global supply loss. Calls are not converted mechanically to barrels; AIS-dark, direction, loading, cargo mix, and tank draw remain uncertain.",
            )
        add_market_period(
            rows,
            case=case,
            start="2026-07-08",
            end="2026-07-31",
            role="current_traffic_july_nowcast",
            status="analyst_nowcast",
            net_loss=current_loss,
            planned_build=jul_planned,
            demand=jul_demand,
            stock_metric="forecast_total_stock_draw",
            stock_rate=jul_stock_rate,
            source_vintage="EIA STEO 2026-02-10/2026-07-07; PortWatch through 2026-07-23",
            source_url=f"{EIA_FEB} | {EIA_JUL} | {PORTWATCH}",
            assumption="Holds EIA's July demand and stock proxy fixed; the extra loss implied by the post-8 July traffic regime remains in the residual because no later July balance observation exists.",
        )

    # Full-month future periods. Traffic remains at the current regime; only
    # bypass, non-Gulf supply, and market-response durability change by phase.
    for month in FUTURE_PLANNED_BUILD:
        start, end, _ = month_bounds(month)
        phase = "near" if month <= "2026-09" else "q4" if month <= "2026-12" else "q1"
        for case, spec in CASES.items():
            hormuz = float(spec["hormuz_flow"])
            bypass = float(spec["bypass"][phase])
            non_gulf = float(spec["non_gulf"][phase])
            loss = 20.0 - hormuz - bypass - non_gulf
            physical = {
                "gross_missing_hormuz_flow": 20.0 - hormuz,
                "incremental_gulf_bypass_offset": bypass,
                "incremental_non_gulf_supply_offset": non_gulf,
                "net_global_supply_loss": loss,
            }
            for metric, rate in physical.items():
                add_component(
                    rows,
                    case=case,
                    start=start,
                    end=end,
                    period_role="future_current_traffic_scenario",
                    status="modeled_scenario",
                    frame="physical_supply_bridge",
                    metric=metric,
                    rate=rate,
                    source_vintage="scenario built 2026-08-03 from IEA/EIA/PortWatch anchors",
                    source_url=f"{PORTWATCH} | {IEA_ADJUSTMENT} | {IEA_JUL21}",
                    assumption="Traffic stays at the July 8-23 regime. Hormuz oil flow is bounded independently; bypass and non-Gulf rates follow the case's durability phase.",
                    durability=(
                        "Hormuz current flow is constant; bypass tapers with route/security/maintenance constraints; "
                        "non-Gulf incremental production ramps slowly."
                    ),
                    confidence="low",
                    double_counting="Gross missing route flow minus bypass and non-Gulf offsets equals net global supply loss; these physical rows are one bridge, not additive to market-clearing rows.",
                )

            planned = FUTURE_PLANNED_BUILD[month]
            demand = float(spec["demand"][phase])
            government = float(spec["government"][phase])
            commercial = float(spec["commercial"][phase])
            common_dc = "Components sum with residual to net global supply loss; do not add this market bridge to the physical bridge."
            for metric, rate, durability in [
                (
                    "foregone_counterfactual_stock_build",
                    planned,
                    "Frozen February EIA planned build; an avoided build rather than a deliverable stock-flow resource.",
                ),
                (
                    "demand_reduction",
                    demand,
                    "Rises modestly with duration; includes involuntary shortage and conservation, while unmeasured fuel switching stays embedded.",
                ),
                (
                    "government_and_obligated_emergency_release",
                    government,
                    "Tapers after the original 400 mb action; remains well below the IEA's >1 bn gross government-stock level, which is not all usable.",
                ),
                (
                    "commercial_and_other_stock_draw",
                    commercial,
                    "Tapers as working inventories approach operational minima; China ownership and oil-on-water remain uncertain.",
                ),
            ]:
                add_component(
                    rows,
                    case=case,
                    start=start,
                    end=end,
                    period_role="future_current_traffic_scenario",
                    status="modeled_scenario",
                    frame="market_clearing_bridge",
                    metric=metric,
                    rate=rate,
                    source_vintage="scenario built 2026-08-03 from frozen February STEO and July IEA evidence",
                    source_url=f"{EIA_FEB} | {IEA_JUL21}",
                    assumption="Case-specific low-fidelity durability path; no price forecast.",
                    durability=durability,
                    confidence="low",
                    double_counting=common_dc,
                )
            residual = loss - planned - demand - government - commercial
            if residual < -1e-9:
                raise ValueError(f"over-cleared market bridge for {case} {month}: {residual}")
            add_component(
                rows,
                case=case,
                start=start,
                end=end,
                period_role="future_current_traffic_scenario",
                status="modeled_scenario",
                frame="market_clearing_bridge",
                metric="residual_unallocated_adjustment",
                rate=residual,
                source_vintage="scenario arithmetic",
                source_url="issues/in-progress/hormuz-m8q.5-model-current-traffic-oil-supply-scenarios.md",
                assumption="Unallocated balance after named durable channels; not a price forecast.",
                durability="Widens as stock rates taper and the horizon extends; may resolve as additional demand loss, unobserved stocks, or changed physical supply.",
                confidence="low",
                double_counting=common_dc,
            )

    add_horizon_summaries(rows)
    return rows


def add_horizon_summaries(rows: list[dict[str, str]]) -> None:
    period_rows = [row for row in rows if row["record_type"] == "period_component"]
    for case, spec in CASES.items():
        for horizon in HORIZONS:
            cutoff = iso_date(horizon)
            selected = [
                row
                for row in period_rows
                if row["scenario_case"] == case and iso_date(row["period_end"]) <= cutoff
            ]
            net_loss = sum(
                float(row["period_million_bbl"])
                for row in selected
                if row["accounting_frame"] == "physical_supply_bridge"
                and row["metric"] == "net_global_supply_loss"
            )
            market = {
                metric: sum(
                    float(row["period_million_bbl"])
                    for row in selected
                    if row["accounting_frame"] == "market_clearing_bridge" and row["metric"] == metric
                )
                for metric in [
                    "foregone_counterfactual_stock_build",
                    "demand_reduction",
                    "observed_total_stock_draw",
                    "forecast_total_stock_draw",
                    "government_and_obligated_emergency_release",
                    "commercial_and_other_stock_draw",
                    "residual_unallocated_adjustment",
                ]
            }

            # Replace the historical aggregate stock rows through July with an
            # ownership split anchored to the IEA July-end program range.
            historical_total_stock = market.pop("observed_total_stock_draw") + market.pop("forecast_total_stock_draw")
            july_program = float(spec["july_emergency_release"])
            if july_program > historical_total_stock:
                raise ValueError(f"emergency release exceeds total stock contribution for {case}")
            government = july_program + market.pop("government_and_obligated_emergency_release")
            commercial = historical_total_stock - july_program + market.pop("commercial_and_other_stock_draw")
            summary = {
                "net_global_supply_loss": net_loss,
                "foregone_counterfactual_stock_build": market["foregone_counterfactual_stock_build"],
                "government_and_obligated_emergency_release": government,
                "commercial_and_other_stock_draw": commercial,
                "demand_reduction": market["demand_reduction"],
                "residual_unallocated_adjustment": market["residual_unallocated_adjustment"],
            }
            bridge = sum(value for metric, value in summary.items() if metric != "net_global_supply_loss")
            if abs(net_loss - bridge) > 1e-3:
                raise ValueError(f"horizon bridge does not close for {case} {horizon}: {net_loss} vs {bridge}")

            for metric, value in summary.items():
                frame = "physical_supply_headline" if metric == "net_global_supply_loss" else "market_clearing_summary"
                rows.append(
                    make_row(
                        row_id=f"{case}_{horizon}_{metric}_cumulative",
                        record_type="horizon_summary",
                        scenario_case=case,
                        case_definition=spec["definition"],
                        period_start="2026-03-01",
                        period_end=horizon,
                        days=(cutoff - date(2026, 3, 1)).days + 1,
                        horizon_date=horizon,
                        period_role="cumulative_historical_plus_scenario",
                        data_status="mixed_preliminary_forecast_scenario",
                        accounting_frame=frame,
                        metric=metric,
                        period_million_bbl=value,
                        cumulative_million_bbl=value,
                        source_vintage="February-July 2026 official vintages plus 2026-08-03 project scenario",
                        source_url=f"{EIA_FEB} | {EIA_JUL} | {IEA_JUL} | {IEA_JUL21} | {PORTWATCH}",
                        assumption="Cumulative from 1 March. History is preliminary through June; July is forecast/nowcast; later months hold the current traffic regime with case-specific durability.",
                        durability_rule="See period_component rows for phase-specific rules and rates.",
                        confidence="low_medium" if horizon == "2026-09-30" else "low",
                        double_counting_note=(
                            "Market-clearing summary components sum to the net-global-supply-loss headline. "
                            "Historical aggregate stock flow is split using the 290/315/330 mb July-end emergency-release range; do not add the headline to its components."
                        ),
                    )
                )


def validate_output(rows: list[dict[str, str]]) -> None:
    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate output row_id")
    if any(set(row) != set(FIELDS) for row in rows):
        raise ValueError("output schema mismatch")
    summaries = [row for row in rows if row["record_type"] == "horizon_summary"]
    if len(summaries) != len(CASES) * len(HORIZONS) * 6:
        raise ValueError(f"unexpected horizon summary count: {len(summaries)}")
    if any(row["value_mb_per_day"] for row in summaries):
        raise ValueError("horizon summaries should be cumulative volumes only")
    for row in rows:
        if row["source_url"].startswith("http"):
            continue
        if row["source_url"].startswith("issues/"):
            continue
        raise ValueError(f"bad source on {row['row_id']}")


def main() -> None:
    balance = read_csv(BALANCE)
    traffic = read_csv(TRAFFIC)
    evidence = read_csv(EVIDENCE)
    validate_inputs(balance, traffic, evidence)
    rows = build_rows(balance)
    validate_output(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows) on {date.today().isoformat()}")


if __name__ == "__main__":
    main()
