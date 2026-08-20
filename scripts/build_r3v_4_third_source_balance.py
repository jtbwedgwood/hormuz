#!/usr/bin/env python3
"""Build the r3v.4 EIA/IEA/OPEC balance triangulation and history benchmark."""

from __future__ import annotations

import calendar
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EIA_INPUT = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
OUT = ROOT / "data/derived/hormuz_r3v_4_third_source_balance.csv"

FIELDS = [
    "row_id", "record_type", "agency", "publication_vintage", "observation_period",
    "period_start", "period_end", "metric", "value", "unit", "comparison_value",
    "comparison_unit", "scope", "data_status", "source_url", "method",
    "interpretation", "comparability_warning",
]

OPEC_URL = "https://www.opec.org/assets/assetdb/momr-{month}-2026.pdf"
IEA_JULY = "https://www.iea.org/reports/oil-market-report-july-2026"
IEA_JUNE = "https://www.iea.org/reports/oil-market-report-june-2026"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEF_JULY = (
    "https://www.ief.org/_resources/files/news/comparative-analysis-of-monthly-reports-"
    "on-the-oil-market/july-2026/ief-comparative-analysis-07-2026.pdf"
)
IEF_2015 = "https://paperzz.com/doc/9204301/introductory-paper--a-comparison-of-recent-iea-and-opec-o..."
IEF_2019 = (
    "https://www.ief.org/_resources/files/events/11th-iea-ief-opec-symposium-on-energy-"
    "outlooks/ief-rff-outlooks-comparison-report-final.pdf"
)
IEF_2020 = "https://www.rff.org/documents/3297/12th_IEF_RFF_Outlooks_Comparison_Report_2022.pdf"
IEF_2021 = "https://media.rff.org/documents/ief-rff-outlooks-comparison-report.pdf"
IEF_2022_2023 = (
    "https://www.ief.org/_resources/files/events/14th-iea-ief-opec-symposium-on-energy-"
    "outlooks/key-documents/outlooks-comparison-report-2024.pdf"
)
IEA_2017 = "https://www.iea.org/reports/oil-market-report-april-2017"
IEA_2020 = "https://www.iea.org/reports/oil-market-report-november-2020"
IEA_2025 = "https://www.iea.org/reports/oil-market-report-december-2025"


def fmt(value: float | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.6f}".rstrip("0").rstrip(".")


def row(row_id: str, record_type: str, agency: str, vintage: str, period: str,
        start: str, end: str, metric: str, value: float, unit: str,
        comparison: float | None, comparison_unit: str, scope: str, status: str,
        source: str, method: str, interpretation: str, warning: str) -> dict[str, str]:
    values = [
        row_id, record_type, agency, vintage, period, start, end, metric, fmt(value), unit,
        fmt(comparison), comparison_unit, scope, status, source, method, interpretation, warning,
    ]
    return dict(zip(FIELDS, values, strict=True))


def eia_rows() -> tuple[list[dict[str, str]], float]:
    with EIA_INPUT.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    output = []
    total_draw = 0.0
    for month in (3, 4, 5, 6):
        period = f"2026-{month:02d}"
        matches = [
            x for x in source_rows
            if x["source_family"] == "EIA_STEO"
            and x["publication_vintage"] == "2026-07-07"
            and x["observation_month"] == period
            and x["metric"] in {"global_liquids_supply", "global_liquids_consumption"}
        ]
        vals = {x["metric"]: float(x["value"]) for x in matches}
        if set(vals) != {"global_liquids_supply", "global_liquids_consumption"}:
            raise ValueError(f"Missing EIA values for {period}")
        days = calendar.monthrange(2026, month)[1]
        imbalance = vals["global_liquids_consumption"] - vals["global_liquids_supply"]
        barrels = imbalance * days
        total_draw += barrels
        for metric, value in vals.items():
            output.append(row(
                f"eia-{period}-{metric}", "agency_balance_input", "EIA", "2026-07-07",
                period, f"{period}-01", f"{period}-{days:02d}", metric, value, "mb/d",
                None, "", "petroleum_and_other_liquids", "preliminary_estimate",
                "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx",
                "Direct July STEO Table 3c/3e world value extracted upstream by m8q.1.",
                "Same-vintage input to supply-minus-consumption implied stock change.",
                "EIA includes petroleum and other liquids and labels past months estimates subject to revision.",
            ))
        output.append(row(
            f"eia-{period}-implied-draw", "agency_balance_result", "EIA", "2026-07-07",
            period, f"{period}-01", f"{period}-{days:02d}", "implied_inventory_draw",
            barrels, "million_bbl", imbalance, "mb/d", "petroleum_and_other_liquids",
            "same_vintage_arithmetic", "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx",
            "Consumption less supply multiplied by calendar days.",
            "Positive is an implied draw, not an observed tank movement.",
            "Statistical discrepancy and unobserved stocks are embedded in the balance.",
        ))
    output.append(row(
        "eia-mar-jun-implied-draw", "agency_balance_summary", "EIA", "2026-07-07",
        "2026-03_to_2026-06", "2026-03-01", "2026-06-30", "implied_inventory_draw",
        total_draw, "million_bbl", total_draw / 122, "mb/d", "petroleum_and_other_liquids",
        "same_vintage_arithmetic", "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx",
        "Sum of four same-vintage monthly supply-demand gaps.",
        "EIA implies a 606.171 mb draw, or 4.97 mb/d.",
        "Do not confuse this actual/post-shock balance with the separate February-vs-July supply revision.",
    ))
    return output, total_draw


def opec_archive_rows() -> list[dict[str, str]]:
    specs = [
        # report, latest OECD month, level, change, 1Q demand, 2Q demand, 1Q call, 2Q call, 1Q production, 2Q production
        ("february", "2025-12", 2845.0, 6.5, 105.6, 105.6, 42.6, 42.2, None, None),
        ("march", "2026-01", 2824.0, -19.9, 105.6, 105.6, 42.6, 42.2, None, None),
        ("april", "2026-02", 2826.0, 6.2, 105.7, 105.1, 42.8, 41.8, 39.9, None),
        ("may", "2026-03", 2774.0, -21.6, 106.1, 104.6, 43.1, 41.4, 39.9, None),
        ("june", "2026-04", 2748.0, -48.4, 105.9, 104.2, 42.9, 41.0, 39.9, None),
        ("july", "2026-05", 2770.0, -21.8, 106.0, 103.7, 42.8, 40.7, 39.9, 34.3),
    ]
    output = []
    for month, stock_month, stock, change, q1d, q2d, q1call, q2call, q1prod, q2prod in specs:
        source = OPEC_URL.format(month=month)
        vintage = f"2026-{['january','february','march','april','may','june','july'].index(month)+1:02d}"
        for metric, value, unit in (
            ("oecd_commercial_stock_level", stock, "million_bbl"),
            ("oecd_commercial_stock_change_mom", change, "million_bbl"),
            ("world_oil_demand_1q26", q1d, "mb/d"),
            ("world_oil_demand_2q26", q2d, "mb/d"),
            ("call_on_doc_crude_1q26", q1call, "mb/d"),
            ("call_on_doc_crude_2q26", q2call, "mb/d"),
        ):
            output.append(row(
                f"opec-{month}-{metric}", "opec_momr_archive", "OPEC", vintage,
                stock_month if metric.startswith("oecd") else "2026_quarterly_balance",
                "", "", metric, value, unit, None, "", "OPEC MOMR stated scope",
                "preliminary_stock_or_quarterly_estimate", source,
                "Transcribed from MOMR Table 9-1 (stocks) or Table 10-1 (balance).",
                "Shows the evolution of OPEC's data vintage and the two-month stock publication lag.",
                "OECD commercial stocks are observed coverage, while demand and call-on-DoC are global balance estimates.",
            ))
        for quarter, production in (("1q26", q1prod), ("2q26", q2prod)):
            if production is not None:
                output.append(row(
                    f"opec-{month}-doc-production-{quarter}", "opec_momr_archive", "OPEC", vintage,
                    quarter, "", "", f"doc_crude_production_{quarter}", production, "mb/d",
                    None, "", "DoC crude", "quarterly_estimate", source,
                    "Transcribed from MOMR Table 10-1.",
                    "OPEC's production row closes its call-on-DoC balance.",
                    "This is crude from DoC participants, not total world liquids supply.",
                ))
    return output


def iea_balance_rows() -> tuple[list[dict[str, str]], float]:
    # July IEF supplies the same-vintage quarterly IEA call on DoC. The public IEA
    # summaries expose one monthly OPEC+ production observation per release, not a
    # fully revised July monthly history. r3v.7 showed that subtracting those monthly
    # crude observations from a quarterly call is not a total-oil balance. Retain the
    # arithmetic only as a deprecated cross-scope diagnostic.
    specs = [
        ("2026-03", 31, 38.0, 35.24, "https://www.iea.org/reports/oil-market-report-april-2026"),
        ("2026-04", 30, 34.2, 34.13, IEA_MAY),
        ("2026-05", 31, 34.2, 30.30, IEA_JUNE),
        ("2026-06", 30, 34.2, 32.44, IEA_JULY),
    ]
    output = []
    total = 0.0
    for period, days, call, production, production_source in specs:
        rate = call - production
        barrels = rate * days
        total += barrels
        output.append(row(
            f"iea-{period}-implied-draw", "agency_balance_result", "IEA", "2026-07_call_plus_monthly_public_chain",
            period, f"{period}-01", f"{period}-{days:02d}", "implied_inventory_draw",
            barrels, "million_bbl", rate, "mb/d", "IEA_call_on_DoC_less_IEA_OPEC_plus_crude",
            "deprecated_cross_scope_reconstruction", f"{IEF_JULY} | {production_source}",
            "July IEF/IEA call on DoC (38.0 mb/d 1Q; 34.2 mb/d 2Q) less each public IEA monthly total OPEC+ production estimate, times days.",
            "Deprecated diagnostic: this is not IEA's total-oil implied inventory draw.",
            "It mixes a quarterly call-on-DoC with successive-vintage monthly OPEC+ crude observations; use r3v.7's matched Q2 total-supply/demand decomposition instead.",
        ))
    output.append(row(
        "iea-mar-jun-implied-draw", "agency_balance_summary", "IEA", "2026-07_call_plus_monthly_public_chain",
        "2026-03_to_2026-06", "2026-03-01", "2026-06-30", "implied_inventory_draw",
        total, "million_bbl", total / 122, "mb/d", "IEA total-oil/DoC balance reconstruction",
        "deprecated_cross_scope_reconstruction_not_a_total_balance", IEF_JULY,
        "Sum of July-call/contemporaneous-production monthly reconstruction.",
        "Retired by r3v.7: 261.36 mb is not a valid IEA total-oil balance comparator.",
        "Do not use this point to claim same-agency closure or to set the residual low case; the exact public March IEA demand level is unavailable.",
    ))
    return output, total


def opec_balance_summary() -> tuple[list[dict[str, str]], float]:
    # July MOMR Table 10-1: 1Q balance -2.9, 2Q balance -6.4 mb/d.
    march = 2.9 * 31
    q2 = 6.4 * 91
    total = march + q2
    source = OPEC_URL.format(month="july")
    rows = [
        row("opec-march-proxy-implied-draw", "agency_balance_result", "OPEC", "2026-07-13",
            "2026-03", "2026-03-01", "2026-03-31", "implied_inventory_draw", march,
            "million_bbl", 2.9, "mb/d", "OPEC DoC production-demand balance", "quarter_proxy",
            source, "Apply OPEC's 1Q26 -2.9 mb/d balance to March only.",
            "March is proxied by the 1Q average because MOMR does not publish monthly world demand.",
            "January-February were pre-war; applying the quarterly average to March is low fidelity."),
        row("opec-q2-implied-draw", "agency_balance_result", "OPEC", "2026-07-13",
            "2026-04_to_2026-06", "2026-04-01", "2026-06-30", "implied_inventory_draw", q2,
            "million_bbl", 6.4, "mb/d", "OPEC DoC production-demand balance", "quarterly_estimate",
            source, "OPEC July Table 10-1 balance (-6.4 mb/d) times 91 days.",
            "Equivalent global balance plug under OPEC's liquids-demand/call-on-DoC framework.",
            "OPEC's demand is 4.6 mb/d above IEA in 2Q26; scope and modeling dominate the result."),
        row("opec-mar-jun-implied-draw", "agency_balance_summary", "OPEC", "2026-07-13",
            "2026-03_to_2026-06", "2026-03-01", "2026-06-30", "implied_inventory_draw", total,
            "million_bbl", total / 122, "mb/d", "OPEC DoC production-demand balance", "quarterly_proxy",
            source, "March at 1Q balance plus full 2Q balance.",
            "OPEC implies about 672 mb drawn, larger than EIA's 606 mb.",
            "March inherits the 1Q average and OPEC's demand path differs sharply from IEA/EIA."),
    ]
    return rows, total


def observed_stock_sensitivities() -> list[dict[str, str]]:
    specs = [
        ("updated_compatible_low", 258.6,
         "June OMR's rounded 3.8 mb/d March-May draw implies ~206.6 mb for March-April after removing its then-May 143 mb; replace May with July's revised 73 mb draw and add June's 21 mb build."),
        ("mixed_latest_base", 298.0,
         "May OMR March 129 + April 117 + July OMR May 73 - June 21; the existing project composite."),
        ("contemporaneous_high", 368.0,
         "May OMR March-April 246 + June OMR preliminary May 143 - July OMR June build 21."),
    ]
    return [row(
        f"observed-{name}", "observed_stock_sensitivity", "IEA", name,
        "2026-03_to_2026-06", "2026-03-01", "2026-06-30", "observed_inventory_draw",
        value, "million_bbl", value / 122, "mb/d", "global observed crude/products including oil on water",
        "public_summary_sensitivity", f"{IEA_MAY} | {IEA_JUNE} | {IEA_JULY}", method,
        "Public summaries do not expose a single fully revised July-vintage March-June monthly series.",
        "Low/base/high describe vintage sensitivity, not a statistical interval.",
    ) for name, value, method in specs]


def historical_rows() -> list[dict[str, str]]:
    agency_spreads = [
        (2015, 0.30, IEF_2015, "IEA versus OPEC annual total stock change and miscellaneous items."),
        (2019, 0.50, IEF_2019, "IEA versus OPEC annual total stock change and miscellaneous items."),
        (2020, 0.94, IEF_2020, "Range across IEA 2.94, OPEC 2.69 and EIA 2.00 mb/d."),
        (2021, 0.66, IEF_2021, "Range across IEA -2.33, OPEC -1.70 and EIA -1.86 mb/d."),
        (2022, 0.42, IEF_2022_2023, "Range across IEA +0.63, OPEC +0.41 and EIA +0.84 mb/d."),
        (2023, 1.30, IEF_2022_2023, "Annual range; IEF called it unusually large and reported 4Q forecast divergence of 2.6 mb/d."),
    ]
    rows = []
    current = 308.171053 / 122.0
    for year, spread, source, method in agency_spreads:
        rows.append(row(
            f"history-agency-spread-{year}", "historical_interagency_benchmark", "IEA_OPEC_EIA",
            str(year + 1), str(year), f"{year}-01-01", f"{year}-12-31",
            "range_in_net_global_stock_change_and_miscellaneous", spread, "mb/d",
            spread * 122, "four_month_equivalent_million_bbl", "annual global liquids balance",
            "published_comparison", source, method,
            "Historical scale for agency balance disagreement.",
            "Annual estimates are more mature than March-June 2026 and are not a matched-horizon probability sample.",
        ))
    within = [
        ("2017q1", 0.2, IEA_2017, "IEA observed global stocks roughly flat versus implied 0.2 mb/d draw."),
        ("2020q3", 1.3, IEA_2020, "IEA observed draw 0.8 mb/d versus implied draw 2.1 mb/d."),
        ("2025q1q3", 0.7, IEA_2025, "IEA observed 1.3 mb/d build versus near 2 mb/d implied build; periods are approximately aligned."),
        ("2026marjun", current, IEA_JULY, "Project point diagnostic: EIA implied draw less mixed-vintage IEA observed draw."),
    ]
    for tag, gap, source, method in within:
        rows.append(row(
            f"history-observed-implied-{tag}", "historical_observed_vs_implied_benchmark", "IEA_or_project",
            tag, tag, "", "", "absolute_observed_vs_implied_stock_gap", gap, "mb/d",
            gap * 122, "four_month_equivalent_million_bbl", "global observed stocks versus balance implication",
            "published_or_project_calculation", source, method,
            "The current 2.55 mb/d point gap exceeds all three published historical examples.",
            "The current row crosses agencies and mixes vintages; historical rows are same-agency narrative comparisons.",
        ))
    max_prior = max(x[1] for x in agency_spreads)
    rows.append(row(
        "history-current-percentile", "benchmark_summary", "Project", "2026-08-05",
        "historical_benchmark", "2015-01-01", "2026-06-30", "current_gap_empirical_rank",
        100.0, "percent_at_or_below", current / max_prior, "times_largest_annual_agency_spread",
        "six documented annual agency comparisons", "descriptive_not_statistical",
        f"{IEF_2015} | {IEF_2019} | {IEF_2020} | {IEF_2021} | {IEF_2022_2023}",
        "Rank 2.547 mb/d against annual interagency spreads 0.30, 0.50, 0.94, 0.66, 0.42 and 1.30 mb/d.",
        "Current point is above 6/6 observations and 1.96 times the largest annual spread: exceptional in this bounded benchmark.",
        "Small purposive sample; 2023's still-forecast 4Q divergence reached 2.6 mb/d, so exceptional does not mean unprecedented for a preliminary quarter.",
    ))
    return rows


def residual_range_rows(eia: float, iea: float, opec: float) -> list[dict[str, str]]:
    observed = {"low": 258.6, "base": 298.0, "high": 368.0}
    agency = {"EIA": eia, "IEA": iea, "OPEC": opec}
    rows = []
    residuals = []
    for name, implied in agency.items():
        for case, obs in observed.items():
            gap = abs(implied - obs)
            residuals.append(gap)
            rows.append(row(
                f"residual-{name.lower()}-{case}", "residual_sensitivity", name, "2026-07",
                "2026-03_to_2026-06", "2026-03-01", "2026-06-30",
                "absolute_balance_less_observed_stock_gap", gap, "million_bbl", gap / 122,
                "mb/d", "agency balance implication versus public IEA observed-stock sensitivity",
                ("deprecated_cross_scope_sensitivity" if name == "IEA" else "cross_system_sensitivity"),
                f"{IEF_JULY} | {IEA_MAY} | {IEA_JUNE} | {IEA_JULY}",
                f"Absolute difference between {name} implied draw {implied:.3f} mb and observed-{case} {obs:.1f} mb.",
                ("Deprecated r3v.4 diagnostic, not hidden physical inventory." if name == "IEA" else
                 "Diagnostic discrepancy, not hidden physical inventory."),
                ("The IEA leg is invalidated by r3v.7's scope audit; other agency balances share country submissions and are not statistically independent." if name == "IEA" else
                 "Agency balances share country submissions and are not statistically independent."),
            ))
    low = min(residuals)
    high = max(residuals)
    for case, value, method in (
        ("low", low, "Closest public agency balance/observed-stock pairing."),
        ("base", 308.171053, "Existing EIA 606.171 less mixed-vintage observed 298.000 point."),
        ("high", high, "Largest public agency balance/observed-stock pairing."),
    ):
        rows.append(row(
            f"recommended-residual-{case}", "recommended_range", "Project", "2026-08-05",
            "2026-03_to_2026-06", "2026-03-01", "2026-06-30", "unreconciled_balance_residual",
            value, "million_bbl", value / 122, "mb/d", "cross-agency/public-stock sensitivity envelope",
            "deprecated_pre_r3v7_range", f"{IEF_JULY} | {IEA_JULY} | {OPEC_URL.format(month='july')}",
            method, "Historical r3v.4 range only; r3v.7 invalidated the 261.36 mb IEA input that generated its low edge.",
            "Do not cite this range as current. The 308.171 mb EIA-minus-observed point remains a diagnostic, while the public IEA March demand input remains unavailable.",
        ))
    return rows


def build() -> list[dict[str, str]]:
    eia, eia_total = eia_rows()
    iea, iea_total = iea_balance_rows()
    opec, opec_total = opec_balance_summary()
    rows = (
        eia + opec_archive_rows() + iea + opec + observed_stock_sensitivities()
        + historical_rows() + residual_range_rows(eia_total, iea_total, opec_total)
    )
    ids = [x["row_id"] for x in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    assert abs(eia_total - 606.171053) < 1e-3
    assert abs(iea_total - 261.36) < 1e-9
    assert abs(opec_total - 672.3) < 1e-9
    ranges = {x["row_id"]: float(x["value"]) for x in rows if x["record_type"] == "recommended_range"}
    assert abs(ranges["recommended-residual-low"] - 2.76) < 1e-6
    assert abs(ranges["recommended-residual-base"] - 308.171053) < 1e-9
    assert abs(ranges["recommended-residual-high"] - 413.7) < 1e-6
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
