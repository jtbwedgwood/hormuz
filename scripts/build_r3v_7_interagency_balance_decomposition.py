#!/usr/bin/env python3
"""Build the r3v.7 public EIA/IEA/OPEC balance decomposition.

The public IEA record exposes monthly supply but only quarterly demand for the
matched July vintage.  The output therefore gives an exact Q2 decomposition and
an explicitly bounded March sensitivity rather than manufacturing monthly IEA
demand or repeating the cross-scope call-on-DoC reconstruction from r3v.4.
"""

from __future__ import annotations

import calendar
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EIA_INPUT = ROOT / "data/derived/hormuz_m8q_1_monthly_oil_balance.csv"
OUT = ROOT / "data/derived/hormuz_r3v_7_interagency_balance_decomposition.csv"

EIA_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
IEF_URL = (
    "https://www.ief.org/_resources/files/news/comparative-analysis-of-monthly-reports-"
    "on-the-oil-market/july-2026/ief-comparative-analysis-07-2026.pdf"
)
IEA_APRIL = "https://www.iea.org/reports/oil-market-report-april-2026"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEA_JUNE = "https://www.iea.org/reports/oil-market-report-june-2026"
IEA_JULY = "https://www.iea.org/reports/oil-market-report-july-2026"
OPEC_JULY = "https://www.opec.org/assets/assetdb/momr-july-2026.pdf"

FIELDS = [
    "row_id", "record_type", "agency", "comparator_agency", "period", "metric",
    "value_low", "value_base", "value_high", "unit", "share_of_net_gap_pct",
    "data_status", "evidence_status", "confidence", "source_urls", "source_locator",
    "method", "interpretation", "caveat", "accounting_rule",
]


def fmt(value: object) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def row(**values: object) -> dict[str, str]:
    unknown = set(values) - set(FIELDS)
    if unknown:
        raise ValueError(f"Unknown fields: {sorted(unknown)}")
    result = {field: "" for field in FIELDS}
    result.update({key: fmt(value) for key, value in values.items()})
    return result


def eia_monthly() -> dict[str, dict[str, float]]:
    with EIA_INPUT.open(newline="", encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    output: dict[str, dict[str, float]] = {}
    for month in range(3, 7):
        period = f"2026-{month:02d}"
        matches = [
            item for item in source
            if item["source_family"] == "EIA_STEO"
            and item["publication_vintage"] == "2026-07-07"
            and item["observation_month"] == period
            and item["metric"] in {"global_liquids_supply", "global_liquids_consumption"}
        ]
        values = {item["metric"]: float(item["value"]) for item in matches}
        if set(values) != {"global_liquids_supply", "global_liquids_consumption"}:
            raise ValueError(f"Missing July EIA values for {period}")
        output[period] = {
            "supply": values["global_liquids_supply"],
            "demand": values["global_liquids_consumption"],
        }
    return output


def weighted_average(values: dict[str, float]) -> float:
    total_days = sum(calendar.monthrange(2026, int(period[-2:]))[1] for period in values)
    return sum(
        value * calendar.monthrange(2026, int(period[-2:]))[1]
        for period, value in values.items()
    ) / total_days


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    eia = eia_monthly()
    iea_supply = {"2026-03": 97.0, "2026-04": 95.1, "2026-05": 94.5, "2026-06": 98.8}
    iea_supply_sources = {
        "2026-03": IEA_APRIL,
        "2026-04": IEA_MAY,
        "2026-05": IEA_JUNE,
        "2026-06": IEA_JULY,
    }

    for period in eia:
        days = calendar.monthrange(2026, int(period[-2:]))[1]
        gap = eia[period]["demand"] - eia[period]["supply"]
        for metric, value in (
            ("global_liquids_supply", eia[period]["supply"]),
            ("global_liquids_demand", eia[period]["demand"]),
            ("implied_inventory_draw_rate", gap),
        ):
            rows.append(row(
                row_id=f"eia-{period}-{metric}", record_type="agency_input_or_balance",
                agency="EIA", period=period, metric=metric,
                value_low=value, value_base=value, value_high=value, unit="mb/d",
                data_status="same_vintage_monthly", evidence_status="published_STEO_estimate",
                confidence="high_arithmetic_medium_preliminary", source_urls=EIA_URL,
                source_locator="July STEO world supply and consumption tables",
                method="Direct July-vintage monthly level." if metric != "implied_inventory_draw_rate" else
                       "Demand minus supply; positive is an implied draw.",
                interpretation=(f"Equivalent monthly volume is {gap * days:.3f} mb." if metric == "implied_inventory_draw_rate" else
                                "Same-vintage EIA balance input."),
                caveat="Preliminary estimate subject to revision.",
                accounting_rule="Supply and demand are additive only through their signed difference.",
            ))
        rows.append(row(
            row_id=f"iea-{period}-global-supply", record_type="agency_supply_input",
            agency="IEA", comparator_agency="EIA", period=period, metric="global_oil_supply",
            value_low=iea_supply[period], value_base=iea_supply[period], value_high=iea_supply[period],
            unit="mb/d", data_status="successive_public_OMR_monthly_estimate",
            evidence_status="published_OMR_headline", confidence="medium_high",
            source_urls=iea_supply_sources[period], source_locator="OMR public highlights",
            method="Direct public IEA monthly world-supply headline.",
            interpretation=f"IEA minus EIA supply is {iea_supply[period] - eia[period]['supply']:+.3f} mb/d.",
            caveat="Successive OMR vintages, not a fully revised July monthly history.",
            accounting_rule="Comparable as a level diagnostic; do not sum monthly rates without calendar weights.",
        ))

    # The July IEF table publishes IEA quarterly demand.  Q2 is matched to the
    # three public monthly IEA supply headlines; March demand remains private.
    rows.extend([
        row(
            row_id="iea-2026q1-demand", record_type="agency_demand_input", agency="IEA",
            period="2026Q1", metric="global_oil_demand", value_low=104.2, value_base=104.2,
            value_high=104.2, unit="mb/d", data_status="same_July_vintage_quarterly",
            evidence_status="published_IEF_transcription_of_IEA_OMR", confidence="high_for_quarter",
            source_urls=IEF_URL, source_locator="July IEF Table, Global Demand, IEA, 1Q26",
            method="Direct quarterly average.",
            interpretation="Cannot be substituted for March: January and February were pre-war.",
            caveat="The public July record does not expose March's revised monthly level.",
            accounting_rule="Context only for March; no March balance is computed from this average.",
        ),
        row(
            row_id="iea-2026q2-demand-input", record_type="agency_demand_input", agency="IEA",
            period="2026Q2", metric="global_oil_demand", value_low=99.1, value_base=99.1,
            value_high=99.1, unit="mb/d", data_status="same_July_vintage_quarterly",
            evidence_status="published_IEF_transcription_of_IEA_OMR", confidence="high_for_quarter",
            source_urls=IEF_URL, source_locator="July IEF Table, Global Demand, IEA, 2Q26",
            method="Direct quarterly average.",
            interpretation="Matched public demand input for the exact Q2 balance decomposition.",
            caveat="Monthly April and June demand levels remain subscriber-only; May is separately public at 97.9 mb/d.",
            accounting_rule="Use for Q2 only.",
        ),
        row(
            row_id="iea-2026-05-demand", record_type="agency_demand_input", agency="IEA",
            period="2026-05", metric="global_oil_demand", value_low=97.9, value_base=97.9,
            value_high=97.9, unit="mb/d", data_status="July_public_monthly_headline",
            evidence_status="published_OMR_headline", confidence="medium_high",
            source_urls=IEA_JULY, source_locator="July OMR overview, May demand nadir",
            method="Direct public monthly level.",
            interpretation="Only exact monthly demand level in the July public overview.",
            caveat="Does not identify April or June separately.", accounting_rule="Nested inside Q2 average.",
        ),
    ])

    eia_q2_supply = weighted_average({p: eia[p]["supply"] for p in ("2026-04", "2026-05", "2026-06")})
    eia_q2_demand = weighted_average({p: eia[p]["demand"] for p in ("2026-04", "2026-05", "2026-06")})
    iea_q2_supply = weighted_average({p: iea_supply[p] for p in ("2026-04", "2026-05", "2026-06")})
    iea_q2_demand = 99.1
    eia_q2_gap = eia_q2_demand - eia_q2_supply
    iea_q2_gap = iea_q2_demand - iea_q2_supply
    net_gap = eia_q2_gap - iea_q2_gap
    demand_effect = eia_q2_demand - iea_q2_demand
    supply_effect = iea_q2_supply - eia_q2_supply
    if abs(demand_effect + supply_effect - net_gap) > 1e-9:
        raise ValueError("Q2 agency-gap decomposition does not close")

    for agency, supply, demand, gap, source in (
        ("EIA", eia_q2_supply, eia_q2_demand, eia_q2_gap, EIA_URL),
        ("IEA", iea_q2_supply, iea_q2_demand, iea_q2_gap, f"{IEF_URL} | {IEA_MAY} | {IEA_JUNE} | {IEA_JULY}"),
    ):
        for metric, value in (("supply", supply), ("demand", demand), ("implied_draw_rate", gap)):
            rows.append(row(
                row_id=f"{agency.lower()}-2026q2-{metric}", record_type="matched_Q2_summary",
                agency=agency, period="2026Q2", metric=metric, value_low=value,
                value_base=value, value_high=value, unit="mb/d",
                data_status="same_period_public_reconstruction", evidence_status="published_or_calendar_weighted",
                confidence="medium_high", source_urls=source,
                source_locator="July-vintage demand and public monthly supply inputs",
                method="Calendar-weighted April-June level; implied draw is demand minus supply.",
                interpretation=f"{agency} Q2 {metric}.",
                caveat="IEA supply is a chain of successive public monthly estimates, not a revised July table.",
                accounting_rule="Q2 agency decomposition only.",
            ))

    for row_id, metric, value, share, interpretation in (
        ("q2-gap-demand-component", "lower_IEA_demand_reduces_draw", demand_effect,
         100 * demand_effect / net_gap,
         "IEA's lower demand explains this share of the EIA-minus-IEA Q2 balance gap."),
        ("q2-gap-supply-component", "higher_IEA_supply_reduces_draw", supply_effect,
         100 * supply_effect / net_gap,
         "IEA's higher supply explains this share of the EIA-minus-IEA Q2 balance gap."),
        ("q2-gap-total", "EIA_minus_IEA_implied_draw_rate", net_gap, 100.0,
         "The exact public Q2 decomposition closes demand plus supply to the net balance difference."),
    ):
        rows.append(row(
            row_id=row_id, record_type="interagency_gap_decomposition", agency="EIA",
            comparator_agency="IEA", period="2026Q2", metric=metric, value_low=value,
            value_base=value, value_high=value, unit="mb/d", share_of_net_gap_pct=share,
            data_status="matched_Q2_public_decomposition", evidence_status="derived_from_published_inputs",
            confidence="medium_high", source_urls=f"{EIA_URL} | {IEF_URL} | {IEA_MAY} | {IEA_JUNE} | {IEA_JULY}",
            source_locator="EIA monthly tables; IEF July Q2 demand; IEA monthly supply headlines",
            method="(EIA demand - IEA demand) + (IEA supply - EIA supply).",
            interpretation=interpretation,
            caveat="Does not solve March because revised monthly IEA March demand is not public.",
            accounting_rule="The two component rows sum exactly to q2-gap-total.",
        ))

    # Supply-bucket test.  The July IEF table puts the full rounded 0.8 mb/d
    # IEA-EIA difference in non-DoC supply plus DoC NGLs, not DoC crude.
    outside_doc_diff = 64.9 - 64.1
    residual_doc_side = supply_effect - outside_doc_diff
    rows.extend([
        row(
            row_id="q2-supply-gap-outside-doc", record_type="supply_gap_location_test",
            agency="IEA", comparator_agency="EIA", period="2026Q2",
            metric="non_DoC_supply_plus_DoC_NGL_difference", value_low=outside_doc_diff,
            value_base=outside_doc_diff, value_high=outside_doc_diff, unit="mb/d",
            share_of_net_gap_pct=100 * outside_doc_diff / supply_effect,
            data_status="rounded_IEF_quarterly", evidence_status="published_comparison",
            confidence="medium", source_urls=IEF_URL,
            source_locator="July IEF Table: 64.9 IEA versus 64.1 EIA",
            method="IEA minus EIA outside-DoC supply and DoC NGL level.",
            interpretation="Nearly all of the rounded Q2 supply-level difference sits outside DoC crude.",
            caveat="IEF inputs are rounded to 0.1 mb/d; the residual below is rounding-scale.",
            accounting_rule="Diagnostic allocation of the supply component, not new barrels.",
        ),
        row(
            row_id="q2-supply-gap-doc-residual", record_type="supply_gap_location_test",
            agency="IEA", comparator_agency="EIA", period="2026Q2",
            metric="unallocated_supply_difference_after_outside_DoC", value_low=residual_doc_side,
            value_base=residual_doc_side, value_high=residual_doc_side, unit="mb/d",
            data_status="rounding_residual", evidence_status="derived_difference",
            confidence="low", source_urls=IEF_URL,
            source_locator="Total-supply difference less rounded outside-DoC difference",
            method="0.865 mb/d total-supply gap minus 0.8 mb/d rounded outside-DoC/NGL gap.",
            interpretation="No material public remainder is left that could establish extra IEA Gulf bypass credit.",
            caveat="Not a measured DoC crude difference and too small for causal attribution.",
            accounting_rule="Do not add to the outside-DoC row; together they partition the supply effect.",
        ),
    ])

    # March demand remains unavailable.  Show transparent arithmetic rather
    # than presenting the 1Q average as March.  The low edge uses the published
    # May nadir; the base merely borrows EIA March demand as a neutral scale
    # sensitivity; the high edge is the IEA 1Q average and is not an upper bound.
    eia_draw_mar_jun = sum(
        (eia[p]["demand"] - eia[p]["supply"]) * calendar.monthrange(2026, int(p[-2:]))[1]
        for p in eia
    )
    iea_q2_draw = iea_q2_gap * 91
    march_demands = (97.9, eia["2026-03"]["demand"], 104.2)
    iea_draws = tuple(iea_q2_draw + (demand - 97.0) * 31 for demand in march_demands)
    residuals = tuple(eia_draw_mar_jun - value for value in iea_draws)
    rows.extend([
        row(
            row_id="march-demand-public-gap", record_type="missing_public_input", agency="IEA",
            period="2026-03", metric="global_oil_demand", unit="mb/d",
            data_status="subscriber_monthly_table_not_public", evidence_status="explicit_unavailability",
            confidence="high_for_unavailability", source_urls=f"{IEF_URL} | {IEA_APRIL} | {IEA_JULY}",
            source_locator="July IEF publishes 1Q only; April OMR publishes -0.8 mb/d y/y but no level",
            method="Public-source audit.",
            interpretation="An exact March-June EIA-versus-IEA supply/demand split cannot be recovered publicly.",
            caveat="The 104.2 mb/d 1Q average includes pre-war January and February and must not be substituted for March.",
            accounting_rule="Leave March demand missing; use sensitivity rows only.",
        ),
        row(
            row_id="iea-mar-jun-draw-sensitivity", record_type="March_demand_sensitivity",
            agency="IEA", period="2026-03_to_2026-06", metric="implied_inventory_draw",
            value_low=iea_draws[0], value_base=iea_draws[1], value_high=iea_draws[2], unit="million_bbl",
            data_status="Q2_matched_plus_March_sensitivity", evidence_status="bounded_public_arithmetic",
            confidence="low_medium", source_urls=f"{EIA_URL} | {IEF_URL} | {IEA_APRIL} | {IEA_JULY}",
            source_locator="Q2 public balance plus March demand 97.9 / EIA level / IEA 1Q average",
            method="IEA Q2 draw plus (assumed March demand minus 97.0 IEA March supply)*31.",
            interpretation="Illustrative range replacing the invalid 261.36 mb cross-scope point.",
            caveat="Low and high are scenario anchors, not a statistical confidence interval or strict upper bound.",
            accounting_rule="Do not combine with the retired call-on-DoC reconstruction.",
        ),
        row(
            row_id="eia-minus-iea-mar-jun-gap-sensitivity", record_type="March_demand_sensitivity",
            agency="EIA", comparator_agency="IEA", period="2026-03_to_2026-06",
            metric="implied_draw_difference", value_low=residuals[2], value_base=residuals[1],
            value_high=residuals[0], unit="million_bbl", data_status="Q2_matched_plus_March_sensitivity",
            evidence_status="bounded_public_arithmetic", confidence="low_medium",
            source_urls=f"{EIA_URL} | {IEF_URL} | {IEA_APRIL} | {IEA_JULY}",
            source_locator="606.171 mb EIA draw less IEA sensitivity",
            method="EIA same-vintage draw minus IEA Q2-plus-March-demand sensitivity.",
            interpretation="Public inputs support a materially smaller and wider model gap than the old fixed 344.8 mb EIA-IEA difference.",
            caveat="This is model-comparison sensitivity, not hidden physical inventory.",
            accounting_rule="Separate from the EIA-versus-observed-stock 308.171 mb residual.",
        ),
    ])

    # Demonstrate why the legacy call-on-DoC result cannot be a total balance.
    legacy_draw = 261.36
    required_march_demand = 97.0 + (legacy_draw - iea_q2_draw) / 31
    rows.append(row(
        row_id="legacy-261-cross-scope-rejection", record_type="methodology_guardrail",
        agency="IEA", period="2026-03_to_2026-06", metric="March_demand_required_to_reproduce_legacy_draw",
        value_low=required_march_demand, value_base=required_march_demand, value_high=required_march_demand,
        unit="mb/d", data_status="rejected_cross_scope_reconstruction",
        evidence_status="arithmetic_inconsistency", confidence="high",
        source_urls=f"{IEF_URL} | {IEA_APRIL} | {IEA_JULY}",
        source_locator="Legacy r3v.4 261.36 mb versus public Q2 balance",
        method="Solve 261.36 = Q2 draw + (March demand - 97.0)*31.",
        interpretation="The legacy result would require March demand below the published 97.9 mb/d May nadir; it is not a valid total-oil balance.",
        caveat="This rejects the reconstruction, not the underlying public call-on-DoC data.",
        accounting_rule="Retain only as a deprecated methodology diagnostic.",
    ))

    # OPEC's high demand is not paired with high total supply.  Its call-on-DoC
    # framework uses higher demand and lower outside-DoC supply.
    opec_demand_diff = 103.7 - eia_q2_demand
    opec_outside_supply_diff = 62.9 - 64.1
    rows.extend([
        row(
            row_id="opec-eia-q2-demand-difference", record_type="OPEC_scope_test", agency="OPEC",
            comparator_agency="EIA", period="2026Q2", metric="global_demand_difference",
            value_low=opec_demand_diff, value_base=opec_demand_diff, value_high=opec_demand_diff,
            unit="mb/d", data_status="published_quarterly_comparison", evidence_status="IEF_table",
            confidence="medium_high", source_urls=f"{IEF_URL} | {OPEC_JULY}",
            source_locator="OPEC 103.7 versus EIA calendar-weighted 100.356",
            method="OPEC minus EIA Q2 demand.",
            interpretation=f"Equivalent 91-day scale is {opec_demand_diff * 91:.1f} mb, but it is not a residual mechanism.",
            caveat="Absolute demand definitions and non-OECD modeling differ.",
            accounting_rule="Do not add to observed stocks or the EIA demand-vintage gap.",
        ),
        row(
            row_id="opec-eia-q2-outside-doc-supply-difference", record_type="OPEC_scope_test",
            agency="OPEC", comparator_agency="EIA", period="2026Q2",
            metric="non_DoC_supply_plus_DoC_NGL_difference", value_low=opec_outside_supply_diff,
            value_base=opec_outside_supply_diff, value_high=opec_outside_supply_diff, unit="mb/d",
            data_status="rounded_IEF_quarterly", evidence_status="IEF_table", confidence="medium",
            source_urls=IEF_URL, source_locator="OPEC 62.9 versus EIA 64.1",
            method="OPEC minus EIA outside-DoC supply and NGL level.",
            interpretation="OPEC's comparable outside-DoC supply is lower, not roughly 3 mb/d higher than EIA.",
            caveat="OPEC does not publish the same total-world-supply row used by EIA here.",
            accounting_rule="Use with the call-on-DoC framework, not as total supply.",
        ),
        row(
            row_id="agency-scope-definition-note", record_type="methodology_guardrail",
            agency="IEF synthesis", period="2026", metric="country_supply_scope_convention",
            unit="text", data_status="published_method_note", evidence_status="official_comparison_note",
            confidence="high_for_note", source_urls=IEF_URL, source_locator="July IEF report note",
            method="Transcribe the IEF comparability warning.",
            interpretation="EIA country data include biofuels and processing gains; OPEC includes biofuels; IEA excludes both. IEF says its total non-OPEC rows include both.",
            caveat="This identifies a known scope mechanism but does not numerically explain every agency-level difference.",
            accounting_rule="Do not infer hidden barrels from absolute-level differences across scopes.",
        ),
    ])

    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        raise ValueError(f"Duplicate row IDs: {duplicates}")
    if abs(float(next(r for r in rows if r["row_id"] == "q2-gap-total")["value_base"]) - net_gap) > 1e-6:
        raise ValueError("Q2 total row mismatch")
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
