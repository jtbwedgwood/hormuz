from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KMZ3 = ROOT / "data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv"
F6R5 = ROOT / "data/derived/hormuz_f6r_5_replacement_demand_response.csv"
OUT_CSV = ROOT / "data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv"
OUT_MD = ROOT / "docs/hormuz-global-energy-shock-accounting.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row[key] == value:
            return row
    raise KeyError(f"missing {key}={value} in {rows!r}")


def as_float(value: str) -> float:
    return float(value)


def fmt(value: float) -> str:
    return f"{value:.2f}"


def sum_base(rows: list[dict[str, str]], product_names: set[str], field: str) -> float:
    total = 0.0
    for row in rows:
        if row["product_or_channel"] in product_names:
            total += as_float(row[field])
    return total


def build_rows() -> list[dict[str, str]]:
    kmz = read_rows(KMZ3)
    f6r = read_rows(F6R5)

    oil = find_row(kmz, "scenario_id", "kmz3-oil-total-2026-closure")
    oil_bypass = find_row(kmz, "scenario_id", "kmz3-oil-bypass-sensitivity")
    oil_stock = find_row(kmz, "scenario_id", "kmz3-oil-products-inventory-draw-check")
    lng = find_row(kmz, "scenario_id", "kmz3-lng-2026-closure")
    lpg = find_row(kmz, "scenario_id", "kmz3-lpg-2026-closure")

    oil_products = {
        "crude oil and condensate",
        "crude oil and refined products",
        "crude oil and petroleum liquids",
    }
    oil_replacement = sum_base(f6r, oil_products, "replacement_supply_base")
    oil_inventory_importer = sum_base(f6r, oil_products, "inventory_draw_base")
    oil_demand = sum_base(f6r, oil_products, "demand_destruction_base")
    oil_residual_importer_basis = (
        as_float(oil["base_disrupted_volume"])
        - oil_replacement
        - oil_inventory_importer
        - oil_demand
    )
    oil_residual_global_stock_basis = (
        as_float(oil["base_disrupted_volume"])
        - oil_replacement
        - as_float(oil_stock["base_disrupted_volume"])
        - oil_demand
    )

    lng_row = find_row(f6r, "importer_or_region", "Asia aggregate")
    lng_replacement = as_float(lng_row["replacement_supply_base"])
    lng_inventory = as_float(lng_row["inventory_draw_base"])
    lng_demand = as_float(lng_row["demand_destruction_base"])
    lng_residual = (
        as_float(lng["base_disrupted_volume"])
        - lng_replacement
        - lng_inventory
        - lng_demand
    )

    lpg_row = find_row(f6r, "product_or_channel", "LPG and NGL feedstocks")
    lpg_replacement = as_float(lpg_row["replacement_supply_base"])
    lpg_inventory = as_float(lpg_row["inventory_draw_base"])
    lpg_demand = as_float(lpg_row["demand_destruction_base"])
    lpg_residual = (
        as_float(lpg["base_disrupted_volume"])
        - lpg_replacement
        - lpg_inventory
        - lpg_demand
    )

    return [
        {
            "row_id": "ccx8-oil-products-global-frame",
            "product_scope": "oil and petroleum liquids",
            "accounting_scope": "global market frame plus major-importer bridge diagnostic",
            "unit": "mb/d flow-equivalent",
            "baseline_exposure": f"{oil['baseline_flow']} {oil['baseline_unit']} in {oil['baseline_period']}; IEA 2025 total is 19.87 mb/d",
            "gross_loss_low": oil["low_disrupted_volume"],
            "gross_loss_base": oil["base_disrupted_volume"],
            "gross_loss_high": oil["high_disrupted_volume"],
            "bypass_or_route_preservation": (
                f"{oil_bypass['low_disrupted_volume']}-{oil_bypass['high_disrupted_volume']} mb/d "
                "Saudi/UAE pipeline bypass sensitivity; this is preserved route capacity, not new supply"
            ),
            "replacement_or_redirected_supply_base": (
                f"{fmt(oil_replacement)} mb/d sum of quantified major-importer bridge rows; "
                "mostly diverted/reallocated cargoes, not proven new output"
            ),
            "inventory_draw_base": (
                f"{oil_stock['base_disrupted_volume']} mb/d global oil-stock draw check; "
                f"{fmt(oil_inventory_importer)} mb/d sum of quantified importer inventory bridge rows"
            ),
            "demand_reduction_base": (
                f"{fmt(oil_demand)} mb/d sum of quantified major-importer demand-response rows"
            ),
            "arithmetic_residual_base": (
                f"{fmt(oil_residual_importer_basis)} mb/d using importer inventory rows; "
                f"{fmt(oil_residual_global_stock_basis)} mb/d if substituting the global stock-draw check"
            ),
            "balance_read": (
                "Oil clears through a mix of route preservation, reserve/commercial stock draw, demand response, "
                "and cargo redirection. Public data do not isolate genuinely new non-Hormuz production from "
                "redirected cargoes."
            ),
            "double_counting_risk": (
                "High. F6R importer rows are scenario allocations and overlap with the global stock-draw check; "
                "replacement supply may be another buyer's displaced consumption."
            ),
            "confidence": "medium",
            "source_anchors": (
                "data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv | "
                "data/derived/hormuz_f6r_5_replacement_demand_response.csv | "
                "https://www.eia.gov/todayinenergy/detail.php?id=65504 | "
                "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz"
            ),
            "notes": (
                "Use as a blog accounting frame, not a closed balance sheet. LPG and refined-product slices overlap "
                "with total petroleum liquids unless the final taxonomy explicitly nets them out."
            ),
        },
        {
            "row_id": "ccx8-lng-global-frame",
            "product_scope": "LNG",
            "accounting_scope": "Qatar/UAE no-bypass loss and Asia aggregate adjustment bridge",
            "unit": "bcm/d flow-equivalent",
            "baseline_exposure": f"{lng['baseline_flow']} {lng['baseline_unit']} in {lng['baseline_period']}",
            "gross_loss_low": lng["low_disrupted_volume"],
            "gross_loss_base": lng["base_disrupted_volume"],
            "gross_loss_high": lng["high_disrupted_volume"],
            "bypass_or_route_preservation": "no practical seaborne bypass for Qatar/UAE LNG",
            "replacement_or_redirected_supply_base": f"{fmt(lng_replacement)} bcm/d Asia aggregate replacement/spot supply proxy",
            "inventory_draw_base": f"{fmt(lng_inventory)} bcm/d Asia aggregate storage draw proxy",
            "demand_reduction_base": f"{fmt(lng_demand)} bcm/d Asia aggregate fuel switching or curtailment proxy",
            "arithmetic_residual_base": f"{fmt(max(lng_residual, 0.0))} bcm/d",
            "balance_read": (
                "LNG is the cleanest hard-loss row: the modeled base loss is close to the whole Qatar/UAE flow, "
                "and clearing depends mainly on scarce flexible cargoes, storage, and demand curtailment."
            ),
            "double_counting_risk": (
                "Medium. The Asia aggregate row overlaps with China/Japan/Korea qualitative LNG rows; do not add "
                "those country rows to this aggregate."
            ),
            "confidence": "medium_high",
            "source_anchors": (
                "data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv | "
                "data/derived/hormuz_f6r_5_replacement_demand_response.csv | "
                "https://www.eia.gov/todayinenergy/detail.php?id=65584 | "
                "https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz"
            ),
            "notes": (
                "The residual is a model artifact, not measured lost demand. Europe storage rows are useful context "
                "but are not added to the Asia aggregate adjustment."
            ),
        },
        {
            "row_id": "ccx8-lpg-global-frame",
            "product_scope": "LPG / NGL feedstocks",
            "accounting_scope": "Gulf LPG exposure with India-visible adjustment lower bound",
            "unit": "mb/d flow-equivalent",
            "baseline_exposure": f"{lpg['baseline_flow']} {lpg['baseline_unit']} in {lpg['baseline_period']}",
            "gross_loss_low": lpg["low_disrupted_volume"],
            "gross_loss_base": lpg["base_disrupted_volume"],
            "gross_loss_high": lpg["high_disrupted_volume"],
            "bypass_or_route_preservation": "no clean public bypass estimate; some cargo rerouting and stock draw likely",
            "replacement_or_redirected_supply_base": f"{fmt(lpg_replacement)} mb/d India-visible replacement proxy",
            "inventory_draw_base": f"{fmt(lpg_inventory)} mb/d India-visible inventory/operational draw proxy",
            "demand_reduction_base": f"{fmt(lpg_demand)} mb/d India-visible rationing or demand-management proxy",
            "arithmetic_residual_base": f"{fmt(max(lpg_residual, 0.0))} mb/d not allocated by public global evidence",
            "balance_read": (
                "LPG/NGL clearing is under-observed. India gives a visible rationing and replacement case, but "
                "global displacement among household fuel, petrochemicals, and poorer importers remains mostly opaque."
            ),
            "double_counting_risk": (
                "High. LPG may be included in petroleum liquids/product aggregates and overlaps with petrochemical "
                "feedstock rows; India-visible adjustment is not a global total."
            ),
            "confidence": "medium_low",
            "source_anchors": (
                "data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv | "
                "data/derived/hormuz_f6r_5_replacement_demand_response.csv | "
                "https://www.iea.org/topics/the-middle-east-and-global-energy-markets"
            ),
            "notes": (
                "This row should be read as a lower-bound visible bridge plus an explicit unallocated residual, "
                "not as proof that the residual disappeared."
            ),
        },
    ]


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    lines = [
        "# Hormuz Global Energy Shock Accounting",
        "",
        "Last updated: 2026-07-07.",
        "",
        "## Bottom Line",
        "",
        (
            "The public evidence supports an accounting frame, not a closed world balance sheet. Oil has the "
            "largest gross barrel shock, but public replacement rows mix genuinely new supply, bypassed flows, "
            "redirected cargoes, reserve draws, and poorer buyers being priced out. LNG is cleaner physically "
            "because Qatar/UAE cargoes have no practical bypass; LPG is important but much less observable."
        ),
        "",
        "## Concise Balance Table",
        "",
        "| Product | Gross Loss, Base | Replacement / Redirection | Inventory Draw | Demand Reduction | Residual / Read | Confidence |",
        "|---|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {product_scope} | {gross_loss_base} {unit} | {replacement_or_redirected_supply_base} | "
            "{inventory_draw_base} | {demand_reduction_base} | {arithmetic_residual_base}; {balance_read} | "
            "{confidence} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Blog-Ready Caveat",
            "",
            (
                "These rows should not be summed across countries or products. The importer adjustment rows are "
                "scenario bridges, not cargo-by-cargo world accounting: a barrel counted as Japan's replacement "
                "supply may be a cargo diverted from another buyer, and the global oil-stock draw overlaps with "
                "country inventory-draw assumptions."
            ),
            "",
            "## Double-Counting Risks",
            "",
        ]
    )
    for row in rows:
        lines.append(f"- {row['product_scope']}: {row['double_counting_risk']}")

    lines.extend(
        [
            "",
            "## Sources",
            "",
            "- EIA, Strait of Hormuz oil chokepoint route data: https://www.eia.gov/todayinenergy/detail.php?id=65504",
            "- EIA, Hormuz LNG route data: https://www.eia.gov/todayinenergy/detail.php?id=65584",
            "- IEA, Strait of Hormuz factsheet: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz",
            "- IEA, Middle East and global energy markets: https://www.iea.org/topics/the-middle-east-and-global-energy-markets",
            "- Local inputs: `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`, `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, and `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`.",
            "",
            "## Files",
            "",
            f"- Accounting table: `{OUT_CSV.relative_to(ROOT)}`",
            f"- Builder script: `scripts/{Path(__file__).name}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
