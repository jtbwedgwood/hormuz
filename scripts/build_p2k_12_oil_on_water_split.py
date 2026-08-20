#!/usr/bin/env python3
"""Build p2k.12's onshore-accessibility and oil-on-water bridge.

The output keeps two diagnostics separate:

* a *matched-total* accessibility restatement, which asks how much inventory
  left onshore tanks after allowing for the observed oil-on-water change; and
* the global accounting residual, which is not reduced by moving the inventory
  boundary from total stocks to onshore stocks unless the implied-balance side
  is restated on the same boundary too.

Positive inventory changes are builds; negative changes are draws.  Positive
"draw" fields reverse that sign for readability.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_p2k_12_oil_on_water_split.csv"

IEA_APR = "https://www.iea.org/reports/oil-market-report-april-2026"
IEA_MAY = "https://www.iea.org/reports/oil-market-report-may-2026"
IEA_JUN = "https://www.iea.org/reports/oil-market-report-june-2026"
IEA_JUL = "https://www.iea.org/reports/oil-market-report-july-2026"
KPLER = "https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2"
KPLER_METHOD = "https://python-sdk.dev.kpler.com/resources/fleet_metrics_vessels.html"

TOTAL_DRAW_COMPOSITE = 298.0
IMPLIED_DRAW = 606.171053
RESIDUAL = IMPLIED_DRAW - TOTAL_DRAW_COMPOSITE

FIELDS = [
    "row_id", "record_type", "period", "source_vintage", "geography",
    "metric", "value_low_million_bbl", "value_base_million_bbl",
    "value_high_million_bbl", "unit", "direction_convention",
    "evidence_status", "confidence", "source_url", "method",
    "interpretation", "accounting_treatment", "caveat",
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
        raise ValueError(f"unknown fields: {sorted(unknown)}")
    result = {field: "" for field in FIELDS}
    result.update({key: fmt(value) for key, value in values.items()})
    return result


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    monthly = [
        # total change, OOW low/base/high, onshore low/base/high, vintage/source/note
        ("2026-03", -129.0, -117.0, -117.0, -117.0, -12.0, -12.0, -12.0,
         "IEA May OMR", IEA_MAY,
         "May OMR revised the global total to -129 mb and explicitly reports a 12 mb on-land draw and 117 mb oil-on-water fall."),
        ("2026-04", -117.0, 53.0, 53.0, 53.0, -170.0, -170.0, -170.0,
         "IEA May OMR", IEA_MAY,
         "Single-vintage exact split: -170 on land plus +53 on water equals -117 total."),
        ("2026-05", -73.0, -35.0, 0.0, 35.0, -38.0, -73.0, -108.0,
         "IEA July OMR total; project OOW sensitivity", f"{IEA_JUL} | {KPLER}",
         "July revised the total draw to 73 mb but publishes no May onshore/OOW split. The +/-35 mb OOW sensitivity matches Kpler's observed early-May within-month swing; it is not an end-month observation."),
        ("2026-06", 21.0, 117.0, 117.0, 117.0, -96.0, -96.0, -96.0,
         "IEA July OMR", IEA_JUL,
         "Single-vintage exact split: -96 onshore plus +117 on water equals +21 total."),
    ]

    for month, total, owl, owb, owh, osl, osb, osh, vintage, source, note in monthly:
        rows.extend([
            row(
                row_id=f"{month}-total-observed-change", record_type="monthly_observed_bridge",
                period=month, source_vintage=vintage, geography="World",
                metric="total_observed_inventory_change", value_low_million_bbl=total,
                value_base_million_bbl=total, value_high_million_bbl=total,
                unit="million_bbl", direction_convention="positive_build_negative_draw",
                evidence_status="reported_preliminary", confidence="medium_high",
                source_url=source, method="IEA public monthly headline.", interpretation=note,
                accounting_treatment="Included in the published global observed-stock total.",
                caveat="Preliminary monthly estimates can be revised by tens of millions of barrels.",
            ),
            row(
                row_id=f"{month}-oil-on-water-change", record_type="monthly_observed_bridge",
                period=month, source_vintage=vintage, geography="World",
                metric="oil_on_water_change", value_low_million_bbl=owl,
                value_base_million_bbl=owb, value_high_million_bbl=owh,
                unit="million_bbl", direction_convention="positive_build_negative_draw",
                evidence_status="reported" if month != "2026-05" else "bounded_not_observed",
                confidence="medium" if month != "2026-05" else "low",
                source_url=source, method="Direct IEA split except May; May is an explicit sensitivity.",
                interpretation=note,
                accounting_treatment="Nested inside total observed inventory; never add to it.",
                caveat="Oil on water combines ordinary voyage inventory and stationary floating storage.",
            ),
            row(
                row_id=f"{month}-onshore-change", record_type="monthly_accessibility_bridge",
                period=month, source_vintage=vintage, geography="World",
                metric="onshore_inventory_change", value_low_million_bbl=osl,
                value_base_million_bbl=osb, value_high_million_bbl=osh,
                unit="million_bbl", direction_convention="positive_build_negative_draw",
                evidence_status="reported" if month != "2026-05" else "arithmetic_sensitivity",
                confidence="medium" if month != "2026-05" else "low",
                source_url=source, method="Total observed change minus oil-on-water change.",
                interpretation="Onshore is the accessible-tank diagnostic; it is not a substitute global accounting perimeter.",
                accounting_treatment="Memo boundary inside total stocks; do not add to total inventory change.",
                caveat="Onshore stocks also contain working inventory and inaccessible or policy-constrained barrels.",
            ),
        ])

    # March causal bridge: May's -117 global OOW result supersedes the issue's
    # erroneous treatment of the +100 regional Gulf floating build as global.
    rows.extend([
        row(
            row_id="2026-03-voyage-in-transit-contraction", record_type="oil_on_water_causal_component",
            period="2026-03", source_vintage="IEA April OMR", geography="World",
            metric="voyage_float_change", value_low_million_bbl=-181.0,
            value_base_million_bbl=-181.0, value_high_million_bbl=-181.0,
            unit="million_bbl", direction_convention="positive_build_negative_draw",
            evidence_status="reported_earlier_vintage", confidence="medium_high",
            source_url=IEA_APR, method="IEA-reported fall in oil in transit.",
            interpretation="Blocked loadings emptied the ordinary voyage pipeline; this was a one-time delivery of already-loaded cargo, not discretionary headroom.",
            accounting_treatment="Nested inside March global oil-on-water change.",
            caveat="Earlier vintage than the revised -117 mb global OOW result.",
        ),
        row(
            row_id="2026-03-middle-east-floating-storage-build", record_type="oil_on_water_causal_component",
            period="2026-03", source_vintage="IEA April OMR", geography="Middle East Gulf",
            metric="discretionary_floating_storage_change", value_low_million_bbl=100.0,
            value_base_million_bbl=100.0, value_high_million_bbl=100.0,
            unit="million_bbl", direction_convention="positive_build_negative_draw",
            evidence_status="reported_regional", confidence="medium_high", source_url=IEA_APR,
            method="IEA/Kpler floating-storage estimate for the Middle East Gulf.",
            interpretation="Exports were blocked and cargoes accumulated offshore; this +100 is included within, not additional to, the -117 global OOW change.",
            accounting_treatment="Regional component nested inside the global OOW total.",
            caveat="Regional, not global; dwell-time classification is vendor-dependent.",
        ),
        row(
            row_id="2026-03-other-and-vintage-reconciliation", record_type="oil_on_water_causal_component",
            period="2026-03", source_vintage="IEA April and May OMR bridge", geography="World excluding named components",
            metric="unclassified_oil_on_water_change", value_low_million_bbl=-36.0,
            value_base_million_bbl=-36.0, value_high_million_bbl=-36.0,
            unit="million_bbl", direction_convention="positive_build_negative_draw",
            evidence_status="arithmetic_residual", confidence="low", source_url=f"{IEA_APR} | {IEA_MAY}",
            method="Revised global OOW -117 minus (-181 transit +100 Gulf floating).",
            interpretation="Captures other regions, sanctioned cargoes, classification and the revision between vintages.",
            accounting_treatment="Exhaustive residual only within this mixed-vintage March causal bridge.",
            caveat="Not a measured physical category.",
        ),
    ])

    # April: IEA attributed the +53 to bypass loadings and long-haul Atlantic
    # cargoes but did not publish a quantitative voyage/storage split.
    for suffix, low, base, high, metric, interp in [
        ("voyage", 40.0, 53.0, 66.0, "voyage_float_change",
         "Scenario assigns most/all of April's build to longer and newly rerouted voyages."),
        ("discretionary", 13.0, 0.0, -13.0, "discretionary_floating_storage_change",
         "Residual paired with the voyage scenario; negative high-case value means stationary storage was released while voyage float rose faster."),
    ]:
        rows.append(row(
            row_id=f"2026-04-{suffix}-scenario", record_type="oil_on_water_causal_component",
            period="2026-04", source_vintage="IEA May OMR plus project scenario", geography="World",
            metric=metric, value_low_million_bbl=low, value_base_million_bbl=base,
            value_high_million_bbl=high, unit="million_bbl",
            direction_convention="positive_build_negative_draw", evidence_status="scenario_not_observed",
            confidence="low", source_url=f"{IEA_MAY} | {KPLER}",
            method="Paired +/-13 mb sensitivity around an all-voyage central allocation; paired columns sum to +53 mb.",
            interpretation=interp, accounting_treatment="Nested scenario within April global OOW change.",
            caveat="No public end-month vessel-level dwell-time data were available to identify the split.",
        ))

    # June: p2k.13's physical test. Reopening flow increase times a 12-22 day
    # laden journey can refill 66-152 mb of ordinary voyage inventory.
    for suffix, low, base, high, metric, interp in [
        ("voyage", 66.0, 111.6, 152.0, "voyage_float_change",
         "Ordinary transit-pipeline refill alone can explain most or all of June's +117 mb; longer rerouting is not required."),
        ("discretionary", 51.0, 5.4, -35.0, "discretionary_floating_storage_change",
         "Paired residual. IEA's qualitative report of Gulf floating-storage draw favours the upper-voyage/negative-discretionary side."),
    ]:
        rows.append(row(
            row_id=f"2026-06-{suffix}-scenario", record_type="oil_on_water_causal_component",
            period="2026-06", source_vintage="IEA July OMR plus p2k.13 mechanical bound", geography="World",
            metric=metric, value_low_million_bbl=low, value_base_million_bbl=base,
            value_high_million_bbl=high, unit="million_bbl",
            direction_convention="positive_build_negative_draw", evidence_status="mechanical_scenario_not_observed",
            confidence="low_medium", source_url=IEA_JUL,
            method="June Hormuz-flow increase of 5.5/6.2/6.9 mb/d times 12/18/22 laden days; discretionary is the residual to +117.",
            interpretation=interp, accounting_treatment="Nested scenario within June global OOW change.",
            caveat="A stock-at-month-end response is not exactly flow times full voyage days; endpoints, deliveries and route mix matter.",
        ))

    # Cumulative accessibility bridge on the latest explicit public totals.
    onshore_low, onshore_base, onshore_high = 316.0, 351.0, 386.0
    apparent_low = onshore_low - TOTAL_DRAW_COMPOSITE
    apparent_base = onshore_base - TOTAL_DRAW_COMPOSITE
    apparent_high = onshore_high - TOTAL_DRAW_COMPOSITE
    rows.extend([
        row(
            row_id="period-total-observed-draw", record_type="period_summary", period="2026-03-01/2026-06-30",
            source_vintage="May and July IEA public headlines", geography="World",
            metric="total_observed_inventory_draw", value_low_million_bbl=TOTAL_DRAW_COMPOSITE,
            value_base_million_bbl=TOTAL_DRAW_COMPOSITE, value_high_million_bbl=TOTAL_DRAW_COMPOSITE,
            unit="million_bbl", direction_convention="positive_draw", evidence_status="mixed_vintage_composite",
            confidence="medium_low", source_url=f"{IEA_MAY} | {IEA_JUL}",
            method="129 + 117 + 73 - 21.", interpretation="Existing project total-inventory comparator.",
            accounting_treatment="Valid comparator to an implied global total-inventory stock change.",
            caveat="Mixed vintages and preliminary observations.",
        ),
        row(
            row_id="period-onshore-accessible-draw-matched-total", record_type="period_summary",
            period="2026-03-01/2026-06-30", source_vintage="Latest-total composite with May OOW sensitivity", geography="World",
            metric="onshore_accessible_inventory_draw", value_low_million_bbl=onshore_low,
            value_base_million_bbl=onshore_base, value_high_million_bbl=onshore_high,
            unit="million_bbl", direction_convention="positive_draw", evidence_status="reported_except_may_sensitivity",
            confidence="low_medium", source_url=f"{IEA_MAY} | {IEA_JUL} | {KPLER}",
            method="298 mb total draw plus cumulative OOW build of 18/53/88 mb; May OOW is -35/0/+35.",
            interpretation="Accessible onshore tanks drew 316-386 mb, base 351 mb; much less than the issue's crude 568 mb because March global OOW fell 117 mb rather than rising 100 mb.",
            accounting_treatment="Durability/accessibility memo only; changing the stock perimeter prevents direct substitution into the global balance identity.",
            caveat="Does not measure how much onshore inventory was operationally or legally usable.",
        ),
        row(
            row_id="period-apparent-residual-closure", record_type="residual_test",
            period="2026-03-01/2026-06-30", source_vintage="Latest-total composite with May OOW sensitivity", geography="World",
            metric="apparent_residual_closure_from_boundary_change", value_low_million_bbl=apparent_low,
            value_base_million_bbl=apparent_base, value_high_million_bbl=apparent_high,
            unit="million_bbl", direction_convention="positive_apparent_closure", evidence_status="scope_reclassification_not_accounting_closure",
            confidence="high_arithmetic_low_interpretive", source_url=f"{IEA_MAY} | {IEA_JUL}",
            method="Onshore-accessible draw minus 298 mb total observed draw; equals cumulative OOW build.",
            interpretation=f"Mechanically narrows the {RESIDUAL:.3f} mb plug by 18/53/88 mb, or {100*apparent_low/RESIDUAL:.1f}%/{100*apparent_base/RESIDUAL:.1f}%/{100*apparent_high/RESIDUAL:.1f}%.",
            accounting_treatment="Not a valid closure: the implied global balance and observed comparator must use the same total-stock boundary.",
            caveat="Calling these barrels 'missing' would double count a measured oil-on-water asset already inside observed global inventories.",
        ),
        row(
            row_id="period-valid-global-accounting-closure", record_type="residual_test",
            period="2026-03-01/2026-06-30", source_vintage="Accounting identity", geography="World",
            metric="valid_residual_closure_from_oow_restatement", value_low_million_bbl=0.0,
            value_base_million_bbl=0.0, value_high_million_bbl=0.0,
            unit="million_bbl", direction_convention="positive_closure", evidence_status="accounting_boundary_verdict",
            confidence="high", source_url=f"{IEA_MAY} | {IEA_JUL}",
            method="Hold the total-inventory perimeter constant on both implied and observed sides.",
            interpretation="The onshore restatement changes accessibility, not the number of barrels in the world balance; valid closure is zero absent a matched onshore implied-balance series.",
            accounting_treatment="Retain the 308.171 mb global residual; publish 255.171 mb only as an apparent unmatched-boundary diagnostic.",
            caveat="Separate AIS measurement/timing error could still alter the residual, but observed OOW movement by itself does not.",
        ),
        row(
            row_id="period-vintage-expanded-onshore-draw", record_type="sensitivity",
            period="2026-03-01/2026-06-30", source_vintage="May-July public-vintage envelope", geography="World",
            metric="onshore_accessible_inventory_draw", value_low_million_bbl=273.0,
            value_base_million_bbl=351.0, value_high_million_bbl=456.0,
            unit="million_bbl", direction_convention="positive_draw", evidence_status="mixed_vintage_sensitivity",
            confidence="low", source_url=f"{IEA_MAY} | {IEA_JUN} | {IEA_JUL}",
            method="Low uses revised April -74 total and May -73 with -35 OOW; high uses April -117 and earlier May -143 with +35 OOW; March and June splits fixed.",
            interpretation="Public revisions alone widen the onshore diagnostic materially; it must not be presented as a precise observed series.",
            accounting_treatment="Sensitivity only, not additive and not a matched-vintage global ledger.",
            caveat="The retained OOW assumptions may themselves have been revised with the total.",
        ),
        row(
            row_id="period-voyage-float-usable-headroom", record_type="durability_verdict",
            period="2026-03-01/2026-06-30", source_vintage="Project classification", geography="World",
            metric="usable_headroom_credit", value_low_million_bbl=0.0,
            value_base_million_bbl=0.0, value_high_million_bbl=0.0,
            unit="million_bbl", direction_convention="positive_usable_headroom", evidence_status="prudential_classification",
            confidence="medium", source_url=f"{IEA_JUL} | {KPLER_METHOD}",
            method="Credit no voyage-pipeline inventory as discretionary buffer capacity.",
            interpretation="Voyage float is committed cargo required to sustain deliveries; refilling it worsens immediate onshore accessibility even though it is a measured global asset.",
            accounting_treatment="Zero usable-headroom credit; retain inside total observed inventories for global accounting.",
            caveat="Cargo can sometimes be diverted or accelerated, but the system cannot sustainably consume its required pipeline fill.",
        ),
        row(
            row_id="method-floating-storage-threshold", record_type="methodology", period="current methodology",
            source_vintage="Kpler SDK documentation accessed 2026-08-06", geography="Global AIS-covered fleet",
            metric="floating_storage_minimum_dwell_threshold", value_low_million_bbl="",
            value_base_million_bbl="", value_high_million_bbl="", unit="days selectable: 7,10,12,15,20,30,90",
            direction_convention="not_applicable", evidence_status="published_vendor_method", confidence="high",
            source_url=KPLER_METHOD, method="Kpler exposes selectable minimum floating-storage durations rather than one natural boundary.",
            interpretation="Voyage/storage decomposition depends on an analyst-selected dwell threshold; seven days is available but not uniquely correct.",
            accounting_treatment="Method memo only.", caveat="Public documentation does not expose the proprietary IEA monthly vessel-level classification file.",
        ),
    ])
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    ids = [item["row_id"] for item in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate row_id")
    index = {item["row_id"]: item for item in rows}
    for month in ("2026-03", "2026-04", "2026-05", "2026-06"):
        total = float(index[f"{month}-total-observed-change"]["value_base_million_bbl"])
        oow = float(index[f"{month}-oil-on-water-change"]["value_base_million_bbl"])
        onshore = float(index[f"{month}-onshore-change"]["value_base_million_bbl"])
        if abs(total - oow - onshore) > 1e-8:
            raise ValueError(f"monthly bridge does not close: {month}")
    if abs(RESIDUAL - 308.171053) > 1e-8:
        raise ValueError("residual anchor changed")
    for suffix in ("low", "base", "high"):
        field = f"value_{suffix}_million_bbl"
        april = float(index["2026-04-voyage-scenario"][field]) + float(index["2026-04-discretionary-scenario"][field])
        june = float(index["2026-06-voyage-scenario"][field]) + float(index["2026-06-discretionary-scenario"][field])
        if abs(april - 53.0) > 1e-8 or abs(june - 117.0) > 1e-8:
            raise ValueError(f"float scenario does not close: {suffix}")


def main() -> None:
    rows = build()
    validate(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
