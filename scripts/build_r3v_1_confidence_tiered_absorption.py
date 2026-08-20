#!/usr/bin/env python3
"""Build the August-vintage Hormuz absorption bridges and waist-node Sankey.

The market-clearing identity is produced for March-June and March-July.  The
route bridge and Sankey remain March-June because no period-matched public July
route reconstruction exists.  Inputs are the completed a4d.1/.2/.5 artifacts;
this builder does not alter demand-specific a4d.8 outputs.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A4D2 = ROOT / "data/derived/hormuz_a4d_2_august_steo_comparison.csv"
RESIDUALS = ROOT / "data/derived/hormuz_a4d_1_august_omr_residuals.csv"
NATIONAL = ROOT / "data/derived/hormuz_r3v_2_period_matched_national_stocks.csv"
R3V7 = ROOT / "data/derived/hormuz_r3v_7_interagency_balance_decomposition.csv"
BRIDGE_OUT = ROOT / "data/derived/hormuz_a4d_6_august_absorption_bridge.csv"
LEDGER_OUT = ROOT / "data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv"
FIG_DATA_OUT = ROOT / "figures/fig-r3v-hormuz-absorption-sankey-data.csv"
FIG_SVG_OUT = ROOT / "figures/fig-r3v-hormuz-absorption-sankey.svg"

FEB = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
AUG = "https://www.eia.gov/outlooks/steo/archives/aug26_base.xlsx"
OMR = "https://www.iea.org/reports/oil-market-report-august-2026"
GLOSSARY = "https://www.iea.org/articles/oil-market-report-glossary"
ROUTE = "https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock"
GAO = "https://www.gao.gov/assets/rced-99-142.pdf"

FRAMES = {
    "march_june": {"period": "2026-03-01_to_2026-06-30", "days": 122},
    "march_july": {"period": "2026-03-01_to_2026-07-31", "days": 153},
}
TIER_LABELS = {"T1": "Directly observed", "T2": "Reasonably assumed", "T3": "Educated guess", "T4": "Unknown"}
TIER_COLORS = {"T1": "#2f7d48", "T2": "#315c99", "T3": "#b56b12", "T4": "#6b7280"}

BRIDGE_FIELDS = [
    "row_id", "frame", "record_type", "component", "value_million_bbl",
    "rate_mb_per_day", "share_pct", "evidence_tier", "data_status",
    "source_url", "method", "interpretation", "caveat", "accounting_rule",
]
LEDGER_FIELDS = [
    "row_id", "frame", "record_type", "component", "parent_node",
    "value_million_bbl", "value_low_million_bbl", "value_base_million_bbl",
    "value_high_million_bbl", "share_of_net_supply_loss", "evidence_tier",
    "evidence_tier_label", "tier_rationale", "underlying_confidence",
    "source_url", "double_counting_rule",
]
FIG_FIELDS = ["figure_id", "stage", "source", "target", "value_million_bbl", "evidence_tier", "evidence_tier_label", "source_url", "caveat"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def a4d2_values() -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    headlines: dict[str, dict[str, float]] = {frame: {} for frame in FRAMES}
    route: dict[str, float] = {}
    for row in read_rows(A4D2):
        if row["record_type"] == "headline_component":
            headlines[row["frame"]][row["metric"]] = float(row["august_value"])
        elif row["record_type"] == "route_bridge":
            route[row["metric"]] = float(row["august_value"])
    return headlines, route


def observed_values() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_rows(RESIDUALS):
        frame = "march_june" if row["period"].endswith("06") else "march_july"
        output[frame] = {
            "observed": float(row["iea_observed_draw_mb"]),
            "residual": float(row["residual_mb"]),
        }
    # The a4d.1 handoff publishes residuals to 0.001 mb. Recover the unrounded
    # closing plug from a4d.2's six-decimal implied draw and the exact OMR aggregate.
    headlines, _ = a4d2_values()
    for frame in output:
        exact = headlines[frame]["implied_inventory_draw"] - output[frame]["observed"]
        assert abs(exact - output[frame]["residual"]) < 0.00051
        output[frame]["residual"] = exact
    return output


def national_t1() -> tuple[float, str]:
    rows = [r for r in read_rows(NATIONAL) if r["include_in_r3v1_t1"] == "yes"]
    value = sum(float(r["net_draw_million_bbl"]) for r in rows)
    return value, " | ".join(sorted({r["source_url"] for r in rows}))


def q2_july_reference() -> dict[str, float]:
    wanted = {"q2-gap-total", "q2-gap-demand-component", "q2-gap-supply-component"}
    return {r["row_id"]: float(r["value_base"]) for r in read_rows(R3V7) if r["row_id"] in wanted}


def bridge_row(row_id: str, frame: str, record_type: str, component: str, value: float | None,
               tier: str = "", status: str = "", source: str = "", method: str = "",
               interpretation: str = "", caveat: str = "", rule: str = "",
               denominator: float | None = None) -> dict[str, str]:
    days = FRAMES.get(frame, {}).get("days")
    return {
        "row_id": row_id, "frame": frame, "record_type": record_type,
        "component": component,
        "value_million_bbl": "" if value is None else f"{value:.6f}",
        "rate_mb_per_day": "" if value is None or not days else f"{value / days:.6f}",
        "share_pct": "" if value is None or not denominator else f"{value / denominator * 100:.6f}",
        "evidence_tier": tier, "data_status": status, "source_url": source,
        "method": method, "interpretation": interpretation, "caveat": caveat,
        "accounting_rule": rule,
    }


def ledger_row(row_id: str, frame: str, record_type: str, component: str, parent: str,
               value: float, total: float, tier: str, rationale: str, confidence: str,
               source: str, rule: str) -> dict[str, str]:
    return {
        "row_id": row_id, "frame": frame, "record_type": record_type,
        "component": component, "parent_node": parent,
        "value_million_bbl": f"{value:.6f}", "value_low_million_bbl": f"{value:.6f}",
        "value_base_million_bbl": f"{value:.6f}", "value_high_million_bbl": f"{value:.6f}",
        "share_of_net_supply_loss": f"{value / total:.6f}", "evidence_tier": tier,
        "evidence_tier_label": TIER_LABELS[tier], "tier_rationale": rationale,
        "underlying_confidence": confidence, "source_url": source,
        "double_counting_rule": rule,
    }


def build() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, dict[str, float]], dict[str, float]]:
    headlines, route = a4d2_values()
    observed = observed_values()
    national, national_sources = national_t1()
    old_q2 = q2_july_reference()
    bridge: list[dict[str, str]] = []
    ledger: list[dict[str, str]] = []

    for frame, meta in FRAMES.items():
        h, o = headlines[frame], observed[frame]
        total = h["global_supply_shortfall"]
        values = {
            "consumption_reduction": h["global_consumption_reduction"],
            "foregone_expected_inventory_build": h["foregone_expected_inventory_build"],
            "observed_global_inventory_draw": o["observed"],
            "unreconciled_balance_plug": o["residual"],
        }
        tiers = {
            "consumption_reduction": "T3", "foregone_expected_inventory_build": "T2",
            "observed_global_inventory_draw": "T1", "unreconciled_balance_plug": "T4",
        }
        rationales = {
            "consumption_reduction": "Exact February-August EIA vintage difference, but causal and mechanism attribution remains uncertain.",
            "foregone_expected_inventory_build": "Exact frozen-February counterfactual arithmetic; the barrels never physically entered tanks.",
            "observed_global_inventory_draw": "Direct same-vintage public IEA aggregate, replacing the earlier mixed-vintage monthly composite.",
            "unreconciled_balance_plug": "EIA implied draw less the same-vintage IEA observed aggregate; it mixes unobserved stocks and all balance errors.",
        }
        for component, value in values.items():
            source = OMR if component in {"observed_global_inventory_draw", "unreconciled_balance_plug"} else f"{FEB} | {AUG}"
            bridge.append(bridge_row(
                f"market-{frame}-{component}", frame, "market_clearing_component", component,
                value, tiers[component], "august_2026_same_vintage_inputs", source,
                "Calendar-integrated February-August EIA revision; observed draw from the 12 August IEA OMR aggregate."
                if component != "unreconciled_balance_plug" else "EIA implied draw minus IEA observed stock draw.",
                rationales[component],
                "The EIA and IEA aggregates are independently revised preliminary systems; the residual is diagnostic, not hidden barrels."
                if component == "unreconciled_balance_plug" else "Preliminary estimates remain revisable.",
                "The four market-clearing components sum to net global supply loss.", total,
            ))
            ledger.append(ledger_row(
                f"{frame}-{component}", frame, "absorption_slice", component.replace("_", " "),
                f"{frame}-net-supply-loss", value, total, tiers[component], rationales[component],
                "high_arithmetic_medium_measurement" if tiers[component] != "T4" else "low_for_physical_interpretation",
                source, "Top-level slice; do not add to another slice.",
            ))
        bridge.append(bridge_row(
            f"market-{frame}-net-supply-loss", frame, "market_clearing_total", "net_global_supply_loss",
            total, "T2", "august_2026_same_vintage_inputs", f"{FEB} | {AUG}",
            "Frozen-February minus August EIA world liquids supply, integrated over calendar days.",
            "Accounting waist, not proof every revision was caused by Hormuz.",
            "EIA past-month international values are preliminary estimates.",
            "Equals the sum of the four market-clearing components.", total,
        ))
        for tier in ("T1", "T2", "T3", "T4"):
            component = next(k for k, v in tiers.items() if v == tier)
            value = values[component]
            ledger.append(ledger_row(
                f"{frame}-tier-total-{tier.lower()}", frame, "tier_total",
                f"{TIER_LABELS[tier]} ({tier}) share of net global supply loss",
                f"{frame}-net-supply-loss", value, total, tier,
                "One top-level component per tier in the August consolidation; no nested national or mechanism detail is double counted.",
                "arithmetic", f"{FEB} | {AUG} | {OMR}",
                "The four tier totals sum to the net global supply loss.",
            ))

    # Exact national observations are useful validation, but are nested inside IEA totals.
    mj_total = headlines["march_june"]["global_supply_shortfall"]
    ledger.append(ledger_row(
        "march_june-memo-exact-national-stock-change", "march_june", "memo_suballocation_not_additive",
        "Exact Japan plus usable Eurostat national net stock draw", "march_june-observed_global_inventory_draw",
        national, mj_total, "T1", "Exact February-June national endpoints promoted by a4d.5.",
        "high_native_medium_conversion", national_sources,
        "Nested inside the 341 mb IEA global observed draw; never add to it or to gross emergency-release delivery.",
    ))

    # Route bridge is only supportable through June.
    for metric in ("gross_missing_hormuz_transit", "incremental_bypass", "non_gulf_and_oman_supply_revision", "global_supply_shortfall", "route_taxonomy_timing_residual"):
        bridge.append(bridge_row(
            f"route-march_june-{metric}", "march_june", "route_bridge", metric, route[metric],
            "T3" if metric == "incremental_bypass" else "T4" if metric == "route_taxonomy_timing_residual" else "T2",
            "mixed_route_estimate_and_august_eia_revision", f"{FEB} | {AUG} | {ROUTE}",
            "Imported from the validated a4d.2 March-June route bridge.",
            "Upstream route accounting; July is not extrapolated.",
            "No period-matched public July route-flow reconstruction exists. EIA's Gulf total also exceeds its seven displayed country rows by 110.4 mb through July; that source discrepancy is not allocated here.",
            "Missing transit minus bypass minus non-Gulf/Oman supply equals shortfall plus route residual.",
            route["gross_missing_hormuz_transit"],
        ))

    # Historical and interagency audit rows.
    for frame in FRAMES:
        residual = observed[frame]["residual"]
        rate = residual / FRAMES[frame]["days"]
        inside = 0.30 <= rate <= 1.30
        bridge.append(bridge_row(
            f"history-{frame}-residual-rate", frame, "historical_residual_benchmark",
            "unreconciled_balance_plug_daily_rate", residual, "T4", "august_cross_system_diagnostic",
            f"{OMR} | {AUG} | {GAO}", "Residual divided by frame calendar days.",
            f"{rate:.3f} mb/d is {'inside' if inside else 'above'} the documented 0.30-1.30 mb/d annual interagency range and {'below' if rate < 1.799448 else 'above'} the 1998 H1 1.799 mb/d rate.",
            "Historical signs, coverage and durations differ; this is scale context, not a probability distribution.",
            "Do not add historical comparators to current barrels.",
            headlines[frame]["global_supply_shortfall"],
        ))

    bridge.extend([
        bridge_row("interagency-july-vintage-q2-total", "reference_q2_july_vintage", "interagency_reference", "EIA_minus_IEA_implied_draw_rate", old_q2["q2-gap-total"], status="retained_july_vintage_reference", source=str(R3V7.relative_to(ROOT)), interpretation="Last exact public Q2 decomposition: 2.110 mb/d.", caveat="Not August-vintage; retained only as a historical reference.", rule="Demand and supply components sum to this reference."),
        bridge_row("interagency-july-vintage-q2-demand", "reference_q2_july_vintage", "interagency_reference", "lower_IEA_demand_component", old_q2["q2-gap-demand-component"], status="retained_july_vintage_reference", source=str(R3V7.relative_to(ROOT)), interpretation="July-vintage demand component: 1.254 mb/d (59.4%).", caveat="Not August-vintage.", rule="Reference only."),
        bridge_row("interagency-july-vintage-q2-supply", "reference_q2_july_vintage", "interagency_reference", "higher_IEA_supply_component", old_q2["q2-gap-supply-component"], status="retained_july_vintage_reference", source=str(R3V7.relative_to(ROOT)), interpretation="July-vintage supply component: 0.856 mb/d (40.6%).", caveat="Not August-vintage.", rule="Reference only."),
        bridge_row("interagency-august-q2-unavailable", "august_q2", "source_access_limitation", "matched_EIA_IEA_q2_decomposition", None, status="not_publicly_recoverable", source=OMR, method="Public-source audit from a4d.1.", interpretation="No August-vintage Q2 decomposition is published because the public OMR omits Q2 supply and demand levels.", caveat="Do not combine August EIA inputs with July IEA levels and label the result August-vintage.", rule="Leave null until a licensed or public same-vintage IEA table is available."),
        bridge_row("interagency-august-q3-unavailable", "august_q3", "source_access_limitation", "matched_EIA_IEA_q3_decomposition", None, status="not_publicly_recoverable", source=OMR, method="Public-source audit from a4d.1.", interpretation="Q3 cannot be decomposed from the public August OMR: it reports a 2.8 mb/d year-on-year demand contraction and 1.8 mb/d deficit, not matched supply and demand levels.", caveat="Changes and deficits are not substitutes for same-scope levels.", rule="No invented Q3 decomposition."),
        bridge_row("source-discrepancy-eia-gulf", "march_july", "source_reconciliation", "EIA_published_Gulf_total_minus_displayed_country_rows", 110.4, status="published_source_discrepancy", source="https://www.eia.gov/outlooks/steo/archives/aug26.pdf", method="Published total integration minus seven displayed country rows.", interpretation="The EIA Gulf table does not reconcile; the 110.4 mb difference is preserved unallocated.", caveat="Could be omitted production or a table error; EIA does not explain it.", rule="Not additive to the global supply loss or route residual."),
    ])

    fig: list[dict[str, str]] = []
    def link(stage: str, source: str, target: str, value: float, tier: str, url: str, caveat: str) -> None:
        fig.append({"figure_id": "fig-r3v-hormuz-absorption-sankey", "stage": stage, "source": source, "target": target, "value_million_bbl": f"{value:.6f}", "evidence_tier": tier, "evidence_tier_label": TIER_LABELS[tier], "source_url": url, "caveat": caveat})
    src, waist = "Expected Hormuz transit that did not occur", "Net global oil supply loss"
    link("upstream_of_waist", src, "Preserved by Gulf bypass routes", route["incremental_bypass"], "T3", ROUTE, "Route estimate; not cargo-by-cargo.")
    link("upstream_of_waist", src, "Offset by non-Gulf and Oman production", route["non_gulf_and_oman_supply_revision"], "T2", f"{FEB} | {AUG}", "Exact vintage arithmetic; causal attribution is not identified.")
    link("upstream_of_waist", src, "Route/taxonomy/timing residual", route["route_taxonomy_timing_residual"], "T4", f"{FEB} | {AUG}", "Diagnostic residual; includes mismatched route and production scopes.")
    link("upstream_of_waist", src, waist, route["global_supply_shortfall"], "T2", f"{FEB} | {AUG}", "March-June August-vintage waist.")
    mj = headlines["march_june"]
    for target, value, tier, url, caveat in [
        ("Lower consumption", mj["global_consumption_reduction"], "T3", f"{FEB} | {AUG}", "Vintage difference; mechanisms not identified."),
        ("Expected build that never happened", mj["foregone_expected_inventory_build"], "T2", FEB, "Counterfactual; never physically in a tank."),
        ("Observed inventory draw", observed["march_june"]["observed"], "T1", OMR, "Direct same-vintage IEA aggregate."),
        ("Unreconciled balance plug", observed["march_june"]["residual"], "T4", f"{OMR} | {GLOSSARY}", "Not a kind of stock movement."),
    ]:
        link("downstream_of_waist", waist, target, value, tier, url, caveat)
    return bridge, ledger, fig, headlines, route


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def svg(headlines: dict[str, dict[str, float]], route: dict[str, float], observed: dict[str, dict[str, float]]) -> str:
    total = headlines["march_june"]["global_supply_shortfall"]
    right = [
        ("Lower consumption", headlines["march_june"]["global_consumption_reduction"], "T3"),
        ("Expected build that never happened", headlines["march_june"]["foregone_expected_inventory_build"], "T2"),
        ("Observed inventory draw", observed["march_june"]["observed"], "T1"),
        ("Unreconciled balance plug", observed["march_june"]["residual"], "T4"),
    ]
    upstream = [
        ("Preserved by Gulf bypass", route["incremental_bypass"], "T3"),
        ("Non-Gulf + Oman production", route["non_gulf_and_oman_supply_revision"], "T2"),
        ("Route/taxonomy/timing residual", route["route_taxonomy_timing_residual"], "T4"),
    ]
    def esc(x: str) -> str: return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="920" viewBox="0 0 1800 920">', '<rect width="1800" height="920" fill="#f6f7f9"/>', '<rect x="24" y="24" width="1752" height="872" rx="8" fill="white" stroke="#dfe4ec"/>', '<style>text{font-family:Inter,system-ui,sans-serif;fill:#172033}.title{font-size:28px;font-weight:760}.sub{font-size:15px;fill:#5d687a}.lab{font-size:15px;font-weight:720}.val{font-size:13px;fill:#5d687a}</style>', '<text x="64" y="68" class="title">Where the Hormuz barrels went, March-June 2026</text>', '<text x="64" y="94" class="sub">August-vintage market balance; million barrels. Rerouting is upstream of the waist and is not added to downstream market clearing.</text>']
    # A compact true waist-node flow diagram: scaled bars plus connecting ribbons.
    scale = 0.33; x0, x1, x2 = 260, 790, 1250; top = 170
    missing = route["gross_missing_hormuz_transit"]
    parts.append(f'<rect x="{x0}" y="{top}" width="30" height="{missing*scale:.2f}" fill="#172033" opacity=".82" rx="3"/>')
    parts.append(f'<text x="242" y="{top+missing*scale/2-10:.1f}" text-anchor="end" class="lab">Expected transit absent</text><text x="242" y="{top+missing*scale/2+10:.1f}" text-anchor="end" class="val">{missing:,.1f} mb</text>')
    y = top
    for name, value, tier in upstream:
        h=value*scale; color=TIER_COLORS[tier]
        parts.append(f'<path d="M290 {y:.1f} C500 {y:.1f} 570 {y:.1f} 790 {y:.1f} L790 {y+h:.1f} C570 {y+h:.1f} 500 {y+h:.1f} 290 {y+h:.1f}Z" fill="{color}" opacity=".30"/>')
        parts.append(f'<rect x="790" y="{y:.1f}" width="30" height="{h:.1f}" fill="{color}" rx="3"/><text x="835" y="{y+h/2-2:.1f}" class="lab">{esc(name)}</text><text x="835" y="{y+h/2+17:.1f}" class="val">{value:,.1f} mb</text>')
        y += h
    waist_y=y; waist_h=total*scale
    parts.append(f'<path d="M290 {y:.1f} C500 {y:.1f} 570 {waist_y:.1f} 790 {waist_y:.1f} L790 {waist_y+waist_h:.1f} C570 {waist_y+waist_h:.1f} 500 {y+waist_h:.1f} 290 {y+waist_h:.1f}Z" fill="#315c99" opacity=".28"/>')
    parts.append(f'<rect x="790" y="{waist_y:.1f}" width="30" height="{waist_h:.1f}" fill="#172033" opacity=".85" rx="3"/><text x="835" y="{waist_y+waist_h/2-4:.1f}" class="lab">Net global supply loss</text><text x="835" y="{waist_y+waist_h/2+17:.1f}" class="val">{total:,.1f} mb · the waist</text>')
    yr=waist_y
    for name,value,tier in right:
        h=value*scale; color=TIER_COLORS[tier]
        parts.append(f'<path d="M820 {yr:.1f} C970 {yr:.1f} 1080 {yr:.1f} 1250 {yr:.1f} L1250 {yr+h:.1f} C1080 {yr+h:.1f} 970 {yr+h:.1f} 820 {yr+h:.1f}Z" fill="{color}" opacity=".34"/>')
        parts.append(f'<rect x="1250" y="{yr:.1f}" width="30" height="{h:.1f}" fill="{color}" rx="3"/><text x="1295" y="{yr+h/2-2:.1f}" class="lab">{esc(name)}</text><text x="1295" y="{yr+h/2+17:.1f}" class="val">{value:,.1f} mb · {value/total*100:.1f}%</text>')
        yr += h
    lx=64
    for tier in ("T1","T2","T3","T4"):
        parts.append(f'<rect x="{lx}" y="118" width="26" height="11" fill="{TIER_COLORS[tier]}"/><text x="{lx+34}" y="128" class="val">{TIER_LABELS[tier]}</text>'); lx += 230
    parts.append(f'<text x="64" y="858" class="sub">The downstream identity closes exactly: {headlines["march_june"]["global_consumption_reduction"]:,.1f} + {headlines["march_june"]["foregone_expected_inventory_build"]:,.1f} + {observed["march_june"]["observed"]:,.1f} + {observed["march_june"]["residual"]:,.1f} = {total:,.1f} mb.</text>')
    parts.append('<text x="64" y="880" class="val">Sources: EIA February/August 2026 STEO; IEA August 2026 OMR and route commentary. July route flows are not extrapolated.</text></svg>')
    return "\n".join(parts)


def validate(bridge: list[dict[str, str]], ledger: list[dict[str, str]], headlines: dict[str, dict[str, float]], route: dict[str, float]) -> None:
    observed = observed_values()
    for frame in FRAMES:
        h, o = headlines[frame], observed[frame]
        close = h["global_consumption_reduction"] + h["foregone_expected_inventory_build"] + o["observed"] + o["residual"]
        assert abs(close - h["global_supply_shortfall"]) < 0.0011, (frame, close)
        tiers = [r for r in ledger if r["frame"] == frame and r["record_type"] == "tier_total"]
        assert len(tiers) == 4
        assert abs(sum(float(r["value_million_bbl"]) for r in tiers) - h["global_supply_shortfall"]) < 0.0011
    route_close = route["incremental_bypass"] + route["non_gulf_and_oman_supply_revision"] + route["global_supply_shortfall"] + route["route_taxonomy_timing_residual"]
    assert abs(route_close - route["gross_missing_hormuz_transit"]) < 1e-5
    assert abs(observed["march_june"]["residual"] / 122 - 1.514641) < 1e-5
    assert abs(observed["march_july"]["residual"] / 153 - 0.849758) < 1e-5
    assert len({r["row_id"] for r in bridge}) == len(bridge)
    assert len({r["row_id"] for r in ledger}) == len(ledger)


def main() -> None:
    bridge, ledger, fig, headlines, route = build()
    validate(bridge, ledger, headlines, route)
    write_csv(BRIDGE_OUT, BRIDGE_FIELDS, bridge)
    write_csv(LEDGER_OUT, LEDGER_FIELDS, ledger)
    write_csv(FIG_DATA_OUT, FIG_FIELDS, fig)
    FIG_SVG_OUT.write_text(svg(headlines, route, observed_values()), encoding="utf-8")
    print(f"wrote {BRIDGE_OUT.relative_to(ROOT)}")
    print(f"wrote {LEDGER_OUT.relative_to(ROOT)}")
    print(f"wrote {FIG_DATA_OUT.relative_to(ROOT)}")
    print(f"wrote {FIG_SVG_OUT.relative_to(ROOT)}")
    for frame in FRAMES:
        rows = [r for r in ledger if r["frame"] == frame and r["record_type"] == "tier_total"]
        print(frame, ", ".join(f"{r['evidence_tier']}={float(r['value_million_bbl']):.1f} mb" for r in rows))


if __name__ == "__main__":
    main()
