#!/usr/bin/env python3
"""Build the p2k.9 forward-surplus and no-reopening decomposition.

The July STEO workbook supplies the published world balance.  Its report text
supplies the Gulf crude shut-in assumptions.  EIA does not publish an exact
monthly 2027 Gulf shut-in path, so the no-reopening cases are transparent
sensitivities rather than a reconstruction falsely labelled as EIA data.

Positive balances are implied stock builds.  They are forecast flows, not
already-held inventory or engineering capacity.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/hormuz_p2k_5_foregone_build_capacity.csv"
OUT = ROOT / "data/derived/hormuz_p2k_9_forward_surplus_decomposition.csv"

JUL_WORKBOOK_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
FEB_WORKBOOK_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_REPORT_URL = "https://www.eia.gov/outlooks/steo/archives/jul26.pdf"

# Direct transcription from July STEO Table 1 (thousand b/d in the PDF,
# represented here as million b/d).
JUNE_SHUTINS = 8.290
Q3_SHUTINS = 5.427
Q4_SHUTINS = 1.440

# EIA says most output/trade is near pre-conflict by end-2026 and a majority
# of the remaining shut-ins returns in Q1 2027.  It does not publish a 2027
# monthly shut-in series.  Under a no-backsliding interpretation, an extremely
# conservative maximum annual residual keeps all 1.44 mb/d offline throughout
# Q1, then just under half (bounded here at 0.72) throughout Q2-Q4.
EIA_2027_RESIDUAL_LOW = 0.0
EIA_2027_RESIDUAL_HIGH = (Q4_SHUTINS * 90 + (Q4_SHUTINS / 2) * 275) / 365
EIA_2027_RESIDUAL_BASE = (EIA_2027_RESIDUAL_LOW + EIA_2027_RESIDUAL_HIGH) / 2

FIELDS = [
    "row_id", "record_type", "period", "period_start", "period_end", "days",
    "scenario", "world_supply_mb_d", "world_demand_mb_d",
    "published_balance_mb_d", "published_balance_million_bbl",
    "held_gulf_shutins_mb_d", "assumed_eia_2027_residual_shutins_mb_d",
    "removed_gulf_recovery_mb_d", "demand_adjustment_vs_july_mb_d",
    "no_reopening_balance_mb_d", "no_reopening_balance_million_bbl",
    "creditable_positive_surplus_mb_d", "source_urls", "source_locator",
    "confidence", "method", "interpretation", "caveat",
]


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def outrow(**values: object) -> dict[str, str]:
    result = {field: "" for field in FIELDS}
    for key, value in values.items():
        if key not in result:
            raise KeyError(key)
        result[key] = fmt(value)
    return result


def weighted_average(rows: list[dict[str, str]], field: str) -> float:
    days = sum(int(row["days"]) for row in rows)
    return sum(float(row[field]) * int(row["days"]) for row in rows) / days


def build() -> list[dict[str, str]]:
    with INPUT.open(newline="") as handle:
        source = list(csv.DictReader(handle))

    monthly = [
        row for row in source
        if row["record_type"] == "monthly_path"
        and row["vintage"] == "postshock_july_2026"
        and row["period"] >= "2026-07"
    ]
    if len(monthly) != 18:
        raise ValueError("Expected July 2026 through December 2027 monthly rows")

    feb_2027 = [
        row for row in source
        if row["record_type"] == "monthly_path"
        and row["vintage"] == "frozen_february_2026"
        and row["period"].startswith("2027-")
    ]
    july_2027 = [row for row in monthly if row["period"].startswith("2027-")]
    q3_2026 = [row for row in monthly if "2026-07" <= row["period"] <= "2026-09"]
    if len(feb_2027) != 12 or len(july_2027) != 12 or len(q3_2026) != 3:
        raise ValueError("Missing period rows")

    rows: list[dict[str, str]] = []
    for item in monthly:
        rows.append(outrow(
            row_id=f"published-{item['period']}", record_type="published_monthly_balance",
            period=item["period"], period_start=item["period_start"],
            period_end=item["period_end"], days=item["days"],
            scenario="july_steo_reopening_branch",
            world_supply_mb_d=float(item["supply_mb_d"]),
            world_demand_mb_d=float(item["demand_mb_d"]),
            published_balance_mb_d=float(item["implied_balance_mb_d"]),
            published_balance_million_bbl=float(item["implied_balance_million_bbl"]),
            source_urls=JUL_WORKBOOK_URL, source_locator=item["row_id"],
            confidence="high_arithmetic_medium_forecast",
            method="Carry the July STEO world petroleum and other liquids production-minus-consumption balance from p2k.5.",
            interpretation="Positive is an implied stock build; negative is an implied stock draw.",
            caveat="This is EIA's reopening branch, not a continued-disruption balance and not observed inventory.",
        ))

    crossover = next(item for item in monthly if float(item["implied_balance_mb_d"]) > 0)
    rows.append(outrow(
        row_id="published-crossover", record_type="published_crossover",
        period=crossover["period"], period_start=crossover["period_start"],
        period_end=crossover["period_end"], days=crossover["days"],
        scenario="july_steo_reopening_branch",
        world_supply_mb_d=float(crossover["supply_mb_d"]),
        world_demand_mb_d=float(crossover["demand_mb_d"]),
        published_balance_mb_d=float(crossover["implied_balance_mb_d"]),
        published_balance_million_bbl=float(crossover["implied_balance_million_bbl"]),
        source_urls=JUL_WORKBOOK_URL, source_locator=crossover["row_id"],
        confidence="high_arithmetic_medium_forecast",
        method="First positive monthly balance after July 2026 in the July STEO path.",
        interpretation="The published path crosses from deficit to surplus in October 2026 at 2.362 mb/d.",
        caveat="The crossover is conditional on EIA's rapid Gulf recovery assumption.",
    ))

    assumption_rows = [
        ("documented-june-shutins", "2026-06", JUNE_SHUTINS,
         "July STEO Table 1, estimated June crude-oil shut-ins."),
        ("documented-q3-shutins", "2026-Q3", Q3_SHUTINS,
         "July STEO Table 1, forecast aggregate Q3 crude-oil shut-ins."),
        ("documented-q4-shutins", "2026-Q4", Q4_SHUTINS,
         "July STEO Table 1, forecast aggregate Q4 crude-oil shut-ins."),
    ]
    for row_id, period, shutins, interpretation in assumption_rows:
        rows.append(outrow(
            row_id=row_id, record_type="documented_gulf_recovery_assumption",
            period=period, scenario="july_steo_reopening_branch",
            held_gulf_shutins_mb_d=shutins,
            source_urls=JUL_REPORT_URL, source_locator="pp. 4-5, Table 1",
            confidence="high_for_eia_assumption",
            method="Direct transcription; PDF values are reported in thousand b/d and converted to mb/d.",
            interpretation=interpretation,
            caveat="Crude shut-ins are not identical to total liquids, exports, or physical Strait flow.",
        ))

    rows.append(outrow(
        row_id="bounded-eia-2027-residual-shutins", record_type="bounded_missing_assumption",
        period="2027", period_start="2027-01-01", period_end="2027-12-31", days=365,
        scenario="july_steo_reopening_branch",
        assumed_eia_2027_residual_shutins_mb_d=EIA_2027_RESIDUAL_BASE,
        source_urls=JUL_REPORT_URL, source_locator="pp. 1 and 5",
        confidence="low_for_bound_high_for_disclosure_gap",
        method=(
            "EIA does not publish the monthly 2027 Gulf path. Low is zero. High assumes all 1.44 mb/d "
            "Q4 residual persists throughout Q1 and 0.72 mb/d (half) persists throughout Q2-Q4, "
            "consistent with only a bare majority returning by end-Q1 and no later backsliding."
        ),
        interpretation=(
            f"Transparent 2027 annual residual sensitivity: {EIA_2027_RESIDUAL_LOW:.3f}/"
            f"{EIA_2027_RESIDUAL_BASE:.3f}/{EIA_2027_RESIDUAL_HIGH:.3f} mb/d low/base/high."
        ),
        caveat="This is a project bound, not a hidden EIA series; the exact embedded 2027 country path cannot be recovered from the public report/workbook.",
    ))

    july_supply = weighted_average(july_2027, "supply_mb_d")
    july_demand = weighted_average(july_2027, "demand_mb_d")
    july_balance = weighted_average(july_2027, "implied_balance_mb_d")
    feb_demand = weighted_average(feb_2027, "demand_mb_d")
    feb_balance = weighted_average(feb_2027, "implied_balance_mb_d")
    q3_supply = weighted_average(q3_2026, "supply_mb_d")
    q3_demand = weighted_average(q3_2026, "demand_mb_d")
    q3_balance = weighted_average(q3_2026, "implied_balance_mb_d")

    rows.extend([
        outrow(
            row_id="annual-published-july-2027", record_type="annual_published_balance",
            period="2027", period_start="2027-01-01", period_end="2027-12-31", days=365,
            scenario="july_steo_reopening_branch", world_supply_mb_d=july_supply,
            world_demand_mb_d=july_demand, published_balance_mb_d=july_balance,
            published_balance_million_bbl=july_balance * 365,
            source_urls=JUL_WORKBOOK_URL, source_locator="p2k.5 monthly 2027 rows",
            confidence="high_arithmetic_medium_forecast",
            method="Day-weighted average of July STEO monthly world production minus consumption.",
            interpretation="EIA's published reopening branch implies a 5.031 mb/d (1,836.441 mb) 2027 build.",
            caveat="The full number is circular if used as headroom under a no-reopening scenario.",
        ),
        outrow(
            row_id="annual-frozen-february-2027", record_type="annual_counterfactual_context",
            period="2027", period_start="2027-01-01", period_end="2027-12-31", days=365,
            scenario="frozen_february_preconflict", world_demand_mb_d=feb_demand,
            published_balance_mb_d=feb_balance, published_balance_million_bbl=feb_balance * 365,
            source_urls=FEB_WORKBOOK_URL, source_locator="p2k.5 frozen-February monthly 2027 rows",
            confidence="high_arithmetic_low_counterfactual",
            method="Day-weighted average of frozen February STEO monthly world production minus consumption.",
            interpretation="The pre-conflict vintage already projected a 2.680 mb/d 2027 surplus.",
            caveat="A stale forecast is context, not a post-shock no-reopening scenario.",
        ),
        outrow(
            row_id="decomposition-q3-to-2027", record_type="noncircular_change_decomposition",
            period="2026-Q3_to_2027", scenario="july_demand_q3_disruption_held",
            world_supply_mb_d=july_supply - q3_supply,
            world_demand_mb_d=july_demand - q3_demand,
            published_balance_mb_d=july_balance - q3_balance,
            held_gulf_shutins_mb_d=Q3_SHUTINS,
            assumed_eia_2027_residual_shutins_mb_d=EIA_2027_RESIDUAL_BASE,
            removed_gulf_recovery_mb_d=Q3_SHUTINS - EIA_2027_RESIDUAL_BASE,
            source_urls=f"{JUL_WORKBOOK_URL} | {JUL_REPORT_URL}",
            source_locator="July workbook Q3 2026 and 2027; report Table 1 and pp. 1, 5",
            confidence="medium_for_arithmetic_low_for_gulf_split",
            method="From Q3 to 2027, world supply rises 8.549 mb/d and demand rises 1.294 mb/d. Remove the bounded Gulf recovery before treating the residual supply growth as non-circular.",
            interpretation="Most of the 7.255 mb/d balance improvement from the Q3 deficit is conditional on Gulf recovery; the no-reopening remainder only brings the market back to roughly balance.",
            caveat="Residual supply growth includes all non-Gulf changes and any classification/model effects; it is not a country-level causal forecast.",
        ),
    ])

    cases = [
        (
            "q3_partial_flow_hold_july_demand", Q3_SHUTINS, 0.0,
            "Hold Q3 forecast shut-ins through 2027 and retain July's depressed 2027 demand path.",
            "Primary no-reopening proxy; it is generous because the Q3 average itself follows the June opening and embeds improving traffic."
        ),
        (
            "q3_partial_flow_hold_february_demand", Q3_SHUTINS, feb_demand - july_demand,
            "Hold Q3 forecast shut-ins but let 2027 demand return to the frozen-February path.",
            "Stress test for a demand rebound without Gulf recovery; not a claim that demand would rebound under continued scarcity."
        ),
        (
            "june_disruption_hold_july_demand", JUNE_SHUTINS, 0.0,
            "Hold June estimated shut-ins through 2027 while retaining July's depressed demand path.",
            "Severe partial-flow sensitivity; June shut-ins are an upstream crude measure, not a traffic observation."
        ),
    ]
    residuals = [
        ("low_surviving_balance", EIA_2027_RESIDUAL_LOW),
        ("base_surviving_balance", EIA_2027_RESIDUAL_BASE),
        ("high_surviving_balance", EIA_2027_RESIDUAL_HIGH),
    ]
    for case, held, demand_adjustment, interpretation, caveat in cases:
        for label, eia_residual in residuals:
            removed = held - eia_residual
            balance = july_balance - removed - demand_adjustment
            rows.append(outrow(
                row_id=f"scenario-{case}-{label}", record_type="no_reopening_2027_sensitivity",
                period="2027", period_start="2027-01-01", period_end="2027-12-31", days=365,
                scenario=f"{case}_{label}", world_supply_mb_d=july_supply - removed,
                world_demand_mb_d=july_demand + demand_adjustment,
                published_balance_mb_d=july_balance,
                published_balance_million_bbl=july_balance * 365,
                held_gulf_shutins_mb_d=held,
                assumed_eia_2027_residual_shutins_mb_d=eia_residual,
                removed_gulf_recovery_mb_d=removed,
                demand_adjustment_vs_july_mb_d=demand_adjustment,
                no_reopening_balance_mb_d=balance,
                no_reopening_balance_million_bbl=balance * 365,
                creditable_positive_surplus_mb_d=max(0.0, balance),
                source_urls=f"{JUL_WORKBOOK_URL} | {JUL_REPORT_URL}" + (f" | {FEB_WORKBOOK_URL}" if demand_adjustment else ""),
                source_locator="July report Table 1 and pp. 1, 5; STEO workbook monthly paths",
                confidence="low_scenario_high_arithmetic",
                method="Published 2027 balance minus held disruption less the bounded residual disruption already embedded in EIA, then minus any demand rebound relative to July.",
                interpretation=interpretation,
                caveat=caveat,
            ))

    primary = [
        row for row in rows
        if row["record_type"] == "no_reopening_2027_sensitivity"
        and row["scenario"].startswith("q3_partial_flow_hold_july_demand")
    ]
    primary_balances = [float(row["no_reopening_balance_mb_d"]) for row in primary]
    rows.append(outrow(
        row_id="verdict-no-reopening-credit", record_type="creditability_verdict",
        period="2027", period_start="2027-01-01", period_end="2027-12-31", days=365,
        scenario="continued_q3_partial_flow",
        published_balance_mb_d=july_balance, published_balance_million_bbl=july_balance * 365,
        no_reopening_balance_mb_d=(min(primary_balances) + max(primary_balances)) / 2,
        creditable_positive_surplus_mb_d=max(0.0, max(primary_balances)),
        source_urls=f"{JUL_WORKBOOK_URL} | {JUL_REPORT_URL}",
        source_locator="Derived from primary p2k.9 sensitivity rows",
        confidence="low_scenario_high_arithmetic",
        method="Report the primary no-reopening envelope; cap creditable positive flow at the optimistic edge rather than the 5.031 mb/d published reopening balance.",
        interpretation=(
            f"Under a Q3-level partial-flow hold, only {min(primary_balances):.3f} to "
            f"{max(primary_balances):.3f} mb/d of 2027 balance survives (central "
            f"{(min(primary_balances) + max(primary_balances)) / 2:.3f}); effectively zero rather than 5.031 mb/d."
        ),
        caveat="Even the optimistic 0.502 mb/d is a conditional forecast flow, not banked inventory or assured absorption headroom.",
    ))

    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
