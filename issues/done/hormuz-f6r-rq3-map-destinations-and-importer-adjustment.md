---
id: "hormuz-f6r"
title: "RQ3: Map destinations and importer adjustment"
type: "epic"
status: "done"
priority: "P1"
parent: null
labels:
  - "importers"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-ccx"
  - "hormuz-s49"
children:
  - "hormuz-f6r.1"
  - "hormuz-f6r.2"
  - "hormuz-f6r.3"
  - "hormuz-f6r.4"
  - "hormuz-f6r.5"
  - "hormuz-f6r.6"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:07Z"
updated_at: "2026-07-06T06:09:07Z"
---

# RQ3: Map destinations and importer adjustment

## Description

Trace where Hormuz-linked exports usually go and assess how major importers are replacing, drawing down, or reducing consumption of energy and other disrupted products.

## Acceptance Criteria

Importer exposure table is built; alternative supply and demand response evidence is cited; country-level adjustment narratives are backed by data where available.

## Dependency Notes

- Cleared dependency: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Blocks: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Child: `hormuz-f6r.1` - Build importer exposure matrix
- Child: `hormuz-f6r.2` - Analyze China exposure and substitution behavior
- Child: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Child: `hormuz-f6r.4` - Assess Europe and Mediterranean exposure
- Child: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Child: `hormuz-f6r.6` - Produce destination flow map and exposure chart

## Work Notes

- 2026-07-06: Claimed for coordinated parallel pass after `hormuz-kmz` completion. Initial focus is `hormuz-f6r.1` exposure matrix plus preliminary regional analyses in `hormuz-f6r.2` through `hormuz-f6r.4`.
- 2026-07-06: Completed all child tasks for the current public-source stage. Outputs now cover importer exposure, China adjustment, Asia adjustment, Europe/Mediterranean exposure, replacement/inventory/demand-response estimates, and a reproducible crude-importer adjustment figure.

## Completion Note

- Acceptance criteria met: importer exposure table exists, alternative supply and demand response evidence is cited, and country/regional adjustment narratives are backed by public data with caveats where public observability is weak.
- Key outputs: `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv`, `data/derived/hormuz_f6r_2_china_adjustment_matrix.csv`, `data/derived/hormuz_f6r_4_europe_exposure_matrix.csv`, `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, and `figures/fig-f6r-crude-importer-adjustment.svg`.
