---
id: "hormuz-f6r.5"
title: "Quantify replacement supply and demand destruction"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "demand"
  - "importers"
  - "substitution"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-f6r.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:47Z"
updated_at: "2026-07-06T23:58:00Z"
---

# Quantify replacement supply and demand destruction

## Description

Estimate where replacement barrels, LNG cargoes, fertilizer, or other products are coming from and whether consumption is being reduced instead.

## Acceptance Criteria

Low/base/high estimates distinguish substitution, inventory draw, and demand destruction for major importers.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Cleared dependency: `hormuz-f6r.2` - Analyze China exposure and substitution behavior
- Cleared dependency: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Cleared dependency: `hormuz-f6r.4` - Assess Europe and Mediterranean exposure
- Cleared dependency: `hormuz-fyp.2` - Build canonical disruption chronology
- Cleared dependency: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Blocks: `hormuz-f6r.6` - Produce destination flow map and exposure chart

## Work Notes

- 2026-07-06: Claimed after `hormuz-f6r.2` through `.4` landed. Target output is a low/base/high adjustment table distinguishing replacement supply, inventory draw, and demand destruction for major importer/product rows.
- 2026-07-06: Completed current public-source pass and wrote `data/derived/hormuz_f6r_5_replacement_demand_response.csv`.

### Output

| Output | Path | Status |
|---|---|---|
| Replacement supply / inventory draw / demand destruction matrix | `data/derived/hormuz_f6r_5_replacement_demand_response.csv` | complete |

### Method Notes

- Unit convention: numeric rows are near-term daily flow-equivalent ranges. They should be read as scenario allocation bands, not observed cargo accounting and not additive across rows.
- Qualitative rows use explicit ordered bands (`very_low`, `low`, `medium_low`, `medium`, `medium_high`, `high`) where public data are too weak for defensible volumes.
- Oil rows start from `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv` and adjust using public country behavior evidence from `hormuz-f6r.2`, `hormuz-f6r.3`, `hormuz-f6r.4`, and S49 reserve tables.
- LNG/gas rows use F6R exposure rows plus `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv`. Qatar/UAE LNG is treated as hard physical exposure because there is no practical seaborne bypass; replacement is mostly spot supply, storage draw, fuel switching, and demand curtailment.
- Fertilizer, sulfur, petrochemical, and aluminium rows use F6R/KMZ/S49 product exposure evidence but are kept mostly qualitative because public importer inventory and destination data are not strong enough for country-level replacement volumes.
- Observed facts are separated from inference in `evidence_type` and `caveats`: official allocation or stock statements are flagged differently from scenario splits or replacement-origin estimates.

### High-Level Read

- Best quantified substitution case: Japan crude. METI's public statements support a 60-70%+ alternative-procurement bridge against the route-exposed crude volume, with reserves covering much of the residual and little observed demand destruction.
- Best demand-destruction case: India gas/LPG. Official control orders and allocation percentages directly show priority rationing for industrial, fertilizer, refinery, petrochemical, commercial LPG, and booking-gap channels.
- Most opaque large row: China crude. Public data support large exposure, refinery-run cuts, import shifts, and commercial/operational stock use, but not a clean split between replacement supply, commercial inventory, bonded/floating barrels, or government SPR.
- Weakest quantitative rows: Southeast Asia aggregate, sulfur/phosphate chains, and aluminium. These are real exposure channels, but current public inputs support bands rather than volumes.

### Source Breadcrumbs

All source URLs embedded in the CSV were accessed 2026-07-06. Key local anchors:

- `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv`
- `data/derived/hormuz_f6r_2_china_adjustment_matrix.csv`
- `data/derived/hormuz_f6r_4_europe_exposure_matrix.csv`
- `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`
- `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`
- `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv`
- `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv`
- `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv`
- `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv`
- `issues/done/hormuz-f6r.2-analyze-china-exposure-and-substitution-behavior.md`
- `issues/done/hormuz-f6r.3-analyze-japan-korea-india-and-southeast-asia-adjustment.md`
- `issues/done/hormuz-f6r.4-assess-europe-and-mediterranean-exposure.md`

### Completion Note

- 2026-07-06: Acceptance criteria met for current stage. The matrix has low/base/high estimates or qualitative bands for major importer/product rows and distinguishes `replacement_supply`, `inventory_draw`, and `demand_destruction`, with source URLs, evidence type, confidence, and caveats.
