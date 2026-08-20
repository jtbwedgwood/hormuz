#!/usr/bin/env python3
"""Build public August-2026 IEA OMR evidence tables.

The full OMR tables are a subscription product.  This build therefore keeps
unpublished monthly cells null, while retaining the exact same-vintage public
aggregates needed for the accounting bridge.
"""

from __future__ import annotations

import calendar
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://www.iea.org/reports/oil-market-report-august-2026"
VINTAGE = "2026-08-12"
MONTHLY_OUT = ROOT / "data/derived/hormuz_a4d_1_august_omr_stocks.csv"
EVIDENCE_OUT = ROOT / "data/derived/hormuz_a4d_1_august_omr_evidence.csv"
RESIDUAL_OUT = ROOT / "data/derived/hormuz_a4d_1_august_omr_residuals.csv"
EIA_BALANCE_IN = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def stock_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    common = {
        "publication_vintage": VINTAGE,
        "source_url": SOURCE_URL,
        "stock_boundary": "global observed crude and products, including oil on water",
    }
    for month in ("2026-03", "2026-04", "2026-05", "2026-06"):
        rows.append(
            {
                "row_type": "month",
                "period": month,
                "total_stock_change_mb": "",
                "onshore_stock_change_mb": "",
                "oil_on_water_change_mb": "",
                "public_status": "not_disclosed_in_public_august_release",
                "derivation": (
                    "The public August highlights disclose only the March-July cumulative draw, "
                    "the July total and July onshore change; the subscription tables are required "
                    "to resolve these monthly cells."
                ),
                **common,
            }
        )
    rows.append(
        {
            "row_type": "month",
            "period": "2026-07",
            "total_stock_change_mb": -69,
            "onshore_stock_change_mb": -6,
            "oil_on_water_change_mb": -63,
            "public_status": "public_total_and_onshore;_oil_on_water_arithmetic",
            "derivation": "-63 = -69 total - (-6 onshore); negative values are draws.",
            **common,
        }
    )
    rows.extend(
        [
            {
                "row_type": "same_vintage_aggregate",
                "period": "2026-03_to_2026-06",
                "total_stock_change_mb": -341,
                "onshore_stock_change_mb": "",
                "oil_on_water_change_mb": "",
                "public_status": "publicly_identified_by_subtraction",
                "derivation": "-341 = -410 March-July cumulative - (-69 July).",
                **common,
            },
            {
                "row_type": "same_vintage_aggregate",
                "period": "2026-03_to_2026-07",
                "total_stock_change_mb": -410,
                "onshore_stock_change_mb": "",
                "oil_on_water_change_mb": "",
                "public_status": "public_headline",
                "derivation": "IEA reports a 410 mb cumulative draw from end-February to end-July.",
                **common,
            },
        ]
    )
    return rows


def evidence_rows() -> list[dict[str, object]]:
    specs = [
        ("2026-07", "global_oil_demand_change_yoy", -1.6, "mb/d", "2026 annual forecast", "World"),
        ("2026-Q2", "global_oil_demand_change_yoy", -4.9, "mb/d", "quarterly year-on-year change", "World"),
        ("2026-Q3", "global_oil_demand_change_yoy", -2.8, "mb/d", "quarterly year-on-year change", "World"),
        ("2026-Q3", "global_oil_balance", -1.8, "mb/d", "forecast supply less demand; negative is deficit", "World"),
        ("2026-H2", "global_oil_demand_revision_vs_july_omr", -0.55, "mb/d", "approximate revision", "World"),
        ("2026-07", "global_oil_supply", 101.5, "mb/d", "monthly estimate", "World"),
        ("2026-07", "global_oil_supply_change_mom", 2.4, "mb/d", "monthly change", "World"),
        ("2026-06", "global_oil_supply", 99.1, "mb/d", "arithmetic from July level and monthly change", "World"),
        ("2026-06", "global_oil_supply_revision_vs_july_omr", 0.3, "mb/d", "arithmetic comparison", "World"),
        ("2026-07", "global_refinery_crude_throughput", 80.9, "mb/d", "monthly estimate", "World"),
        ("2026-07", "gulf_oil_production", 23.9, "mb/d", "monthly estimate", "Middle East Gulf"),
        ("2026-07", "gulf_oil_production_change_mom", 2.5, "mb/d", "monthly change", "Middle East Gulf"),
        ("2026-07", "gulf_output_loss_vs_prewar", 8.3, "mb/d", "pre-war level less July output", "Middle East Gulf"),
        ("2026-07", "gulf_total_exports_including_bypass", 15.0, "mb/d", "monthly estimate", "Middle East Gulf"),
        ("2026-07", "gulf_total_exports_change_mom", -2.1, "mb/d", "monthly change", "Middle East Gulf"),
        ("2026-06", "gulf_total_exports_including_bypass", 17.1, "mb/d", "arithmetic from July level and monthly change", "Middle East Gulf"),
        ("2026-06", "gulf_total_exports_revision_vs_july_omr", 1.0, "mb/d", "arithmetic comparison", "Middle East Gulf"),
        ("2026-07", "gulf_total_exports_including_bypass_early_month_peak", 20.0, "mb/d", "point estimate", "Middle East Gulf"),
        ("2026-07", "gulf_total_exports_including_bypass_late_month", 12.0, "mb/d", "approximate point estimate", "Middle East Gulf"),
    ]
    rows = []
    for period, metric, value, unit, status, geography in specs:
        rows.append(
            {
                "period": period,
                "publication_vintage": VINTAGE,
                "metric": metric,
                "geography": geography,
                "value": value,
                "unit": unit,
                "status": status,
                "source_url": SOURCE_URL,
                "notes": (
                    "Public August OMR release; arithmetic rows use figures on that page. Gulf "
                    "export figures include bypass routes and therefore do not isolate Strait "
                    "transit or bypass flow. The June revision compares the implied 17.1 mb/d "
                    "with the July OMR's 16.1 mb/d."
                    if metric.startswith("gulf_total_exports")
                    else (
                        "Public August OMR release; 99.1 = 101.5 - 2.4 and the 0.3 revision "
                        "compares 99.1 with the July OMR's 98.8 mb/d."
                        if metric.startswith("global_oil_supply") and period == "2026-06"
                        else "Public August OMR release."
                    )
                ),
            }
        )
    return rows


def residual_rows() -> list[dict[str, object]]:
    """Join the OMR observations to a4d.2's validated August STEO panel."""
    with EIA_BALANCE_IN.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    selected = {
        row["observation_month"]: float(row["value"])
        for row in source_rows
        if row["publication_vintage"] == "2026-08-11"
        and row["source_family"] == "EIA_STEO"
        and row["metric"] == "implied_global_inventory_change"
        and row["observation_month"] in {"2026-03", "2026-04", "2026-05", "2026-06", "2026-07"}
    }
    if len(selected) != 5:
        raise ValueError("expected five March-July August-STEO implied-balance rows")
    monthly_draws = {
        month: -rate * calendar.monthrange(*map(int, month.split("-")))[1]
        for month, rate in selected.items()
    }
    old_residual = 308.171053
    specs = [
        ("2026-03_to_2026-06", ("2026-03", "2026-04", "2026-05", "2026-06"), 341.0),
        ("2026-03_to_2026-07", tuple(sorted(monthly_draws)), 410.0),
    ]
    rows = []
    for period, months, iea_draw in specs:
        implied_draw = sum(monthly_draws[month] for month in months)
        residual = implied_draw - iea_draw
        rows.append(
            {
                "period": period,
                "eia_implied_draw_mb": f"{implied_draw:.3f}",
                "eia_publication_vintage": "2026-08-11",
                "iea_observed_draw_mb": f"{iea_draw:.3f}",
                "iea_publication_vintage": VINTAGE,
                "residual_mb": f"{residual:.3f}",
                "prior_march_june_residual_mb": f"{old_residual:.3f}",
                "delta_vs_308_171_mb": f"{residual - old_residual:.3f}",
                "definition": "EIA implied inventory draw minus IEA observed inventory draw.",
                "comparison_note": (
                    "Like-for-like March-June change versus the old mixed-vintage residual; "
                    "published to 0.001 mb because upstream monthly rates carry six decimals."
                    if period.endswith("06")
                    else "Requested benchmark comparison; also extends the window through July; "
                    "published to 0.001 mb because upstream monthly rates carry six decimals."
                ),
                "eia_source": "data/derived/hormuz_m8q_1_monthly_oil_balance.csv",
                "iea_source": SOURCE_URL,
            }
        )
    return rows


def validate(
    stocks: list[dict[str, object]],
    evidence: list[dict[str, object]],
    residuals: list[dict[str, object]],
) -> None:
    by_period = {row["period"]: row for row in stocks}
    assert len([row for row in stocks if row["row_type"] == "month"]) == 5
    assert by_period["2026-03_to_2026-06"]["total_stock_change_mb"] == -341
    assert by_period["2026-03_to_2026-07"]["total_stock_change_mb"] == -410
    july = by_period["2026-07"]
    assert july["total_stock_change_mb"] == july["onshore_stock_change_mb"] + july["oil_on_water_change_mb"]
    assert any(row["metric"] == "gulf_total_exports_including_bypass" for row in evidence)
    assert len(residuals) == 2
    assert all(float(row["residual_mb"]) >= 0 for row in residuals)


def main() -> None:
    stocks = stock_rows()
    evidence = evidence_rows()
    residuals = residual_rows()
    validate(stocks, evidence, residuals)
    write_csv(MONTHLY_OUT, stocks)
    write_csv(EVIDENCE_OUT, evidence)
    write_csv(RESIDUAL_OUT, residuals)
    print(f"wrote {len(stocks)} rows to {MONTHLY_OUT.relative_to(ROOT)}")
    print(f"wrote {len(evidence)} rows to {EVIDENCE_OUT.relative_to(ROOT)}")
    print(f"wrote {len(residuals)} rows to {RESIDUAL_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
