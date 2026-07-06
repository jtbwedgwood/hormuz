---
id: "hormuz-f6r.6"
title: "Produce destination flow map and exposure chart"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-f6r"
labels:
  - "importers"
  - "maps"
  - "tradeflows"
  - "visuals"
blocked_by: []
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:48Z"
updated_at: "2026-07-06T06:09:48Z"
---

# Produce destination flow map and exposure chart

## Description

Create maps or Sankey-style visuals showing pre-disruption flows and post-disruption adjustment for the most important commodities.

## Acceptance Criteria

Visuals are source-backed, readable, and limited to flows whose confidence supports publication.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Cleared dependency: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Cleared dependency: `hormuz-fyp.7` - Define chart and map standards for the project
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline
- Blocks: `hormuz-ccx.3` - Assemble final figure package

## Work Notes

- 2026-07-06: Completed a publication-ready exposure/adjustment chart rather than a literal route map, because the public data support importer/channel magnitudes and adjustment bands better than exact cargo routes.

## Outputs

| Output | Path | Status |
|---|---|---|
| Crude importer adjustment figure | `figures/fig-f6r-crude-importer-adjustment.svg` | complete |
| Machine-readable figure data | `figures/fig-f6r-crude-importer-adjustment-data.csv` | complete |
| Generator script | `scripts/build_f6r_destination_exposure_chart.py` | complete |

## Work Notes

- Figure scope: direct 2024 crude/product route exposure for China, India, Japan, South Korea, Europe/Mediterranean, and the United States, with base-case adjustment buckets for replacement supply, inventory draw, demand reduction, and residual unresolved exposure.
- Source basis: `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv` and `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, with upstream source trails embedded there.
- Caveat: this is not a vessel-route map and should not be read as exact cargo accounting. LNG, LPG, fertilizer, sulfur, aluminium, and petrochemical channels are important but use mixed units or qualitative bands, so they are not merged into this mb/d crude chart.

## Completion Note

- Acceptance criteria met for current public-source stage: visual is source-backed, readable, reproducible from committed CSV inputs, and limited to rows whose confidence supports publication as scenario estimates.
