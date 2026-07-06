---
id: "hormuz-kmz.7"
title: "Produce product disruption master table"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "deliverable"
  - "supply"
blocked_by:
  - "hormuz-kmz.4"
  - "hormuz-kmz.6"
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:40Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Produce product disruption master table

## Description

Create a blog-ready table ranking products by disrupted volume, economic importance, confidence, and surprise value.

## Acceptance Criteria

Table is source-backed, sortable, and includes caveats for unknowable or ambiguous flows.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-kmz.4` - Investigate non-obvious disrupted products
- Blocked by: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline
- Blocks: `hormuz-ccx.3` - Assemble final figure package

## Work Notes

- 2026-07-06: Started a preliminary master-table scaffold before `hormuz-kmz.4` and `hormuz-kmz.6` complete so downstream tasks can see the intended schema. Created `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv` and registered it in `data/manifest.csv`.
- 2026-07-06: Integrated `hormuz-kmz.4` and `hormuz-kmz.5` findings. Upgraded sulphur, aluminium, LPG/NGLs, and shipping services from placeholders to explicit candidate rows. Keep freight/war-risk as a delivered-cost and availability amplifier, not a physical product.
- 2026-07-06: Integrated `hormuz-kmz.1` high-confidence baselines for oil and LNG. Master table now uses 14.95 mb/d crude through Hormuz in 2025 as the crude denominator and records Qatar+UAE LNG at 9.98 Bcf/d in 2024 and 11.43 Bcf/d in 1Q25 in the headline metric.

### Candidate Blog Table Schema

| Field | Purpose |
|---|---|
| `rank` | Editorial sorting, not a claim of exact economic damage. |
| `product` | Commodity/service bucket aligned to foundation taxonomy. |
| `headline_metric` | Human-readable reason this row matters. |
| `baseline_or_market_denominator` | Normal flow or market denominator used for scale. |
| `estimated_disrupted_volume` | Low/base/high or current best point estimate. |
| `unit` | Keep mixed-unit rows visible; do not sum across units. |
| `global_or_regional_share` | Share of relevant global/regional market where defensible. |
| `confidence` | Project confidence label. |
| `surprise_value` | Editorial flag for non-obvious/eye-catching rows. |
| `primary_sources` | Short source names; full source details stay in issue notes/manifest. |
| `core_caveat` | One-line uncertainty or double-counting warning. |
| `next_issue_owner` | Upstream issue expected to firm up the row. |

### Preliminary Ranking

1. Crude/condensate: largest direct barrel exposure; IEA/kmz.6 denominator is about 14.95 mb/d in 2025, with Saudi alone at 5.48 mb/d in EIA 2024 figure data.
2. LNG: no practical bypass; IEA reports >300 mcm/d supply loss and >110 bcm 2025 Hormuz transit; EIA figure data puts Qatar+UAE at 9.98 Bcf/d in 2024 and 11.43 Bcf/d in 1Q25.
3. Refined products: middle distillates/jet fuel channel may be more directly inflationary than crude alone.
4. LPG/NGLs: potentially important for petrochemicals and residential fuel, but definition/double-counting needs care.
5. Sulphur: about half of global seaborne sulphur trade moves through Hormuz per IEA; this is the best surprising industrial-input row.
6. Aluminium: IEA/World Bank evidence supports about 5 Mt/year shipped through Hormuz and about 8% Gulf share of global supply.
7. Petrochemicals/plastics: important mechanism story through LPG/naphtha feedstock scarcity, but weaker public volume splits.
8. Urea: IFASTAT says upstream Hormuz countries account for 34% of global urea trade.
9. Ammonia: IFASTAT says upstream Hormuz countries account for 23% of global ammonia trade; do not double-count as both product and input.
10. MAP/DAP phosphate fertilizer: IFASTAT gives an 18% global trade share, with sulphur/ammonia constraints as additional upstream pressure.
11. Freight/war-risk insurance: not a product, but belongs in the table as an amplifier because insurance/freight affects delivered supply even when cargoes physically move.

### Non-Additivity Warning

- Do not sum all rows. Oil, refined products, LPG, petrochemicals, ammonia, urea, and MAP/DAP overlap through feedstock and production chains.
- Use the table for ranking exposure channels and identifying surprising bottlenecks. Use `hormuz-kmz.3` and `hormuz-kmz.6` for any de-duplicated supply-loss total.

### Completion Note

- 2026-07-06: Acceptance criteria met for a preliminary blog-ready sortable table. `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv` is source-backed, includes caveats for ambiguous flows, and ranks products by scale, confidence, and surprise value.
- Remaining polish: apply final source/citation normalization from `hormuz-fyp.1` and table/figure standards from `hormuz-fyp.7` before publication. This is a publication polish dependency, not a blocker for closing the research task.
