---
id: "hormuz-fyp.6"
title: "Inventory market price series and units"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-fyp"
labels:
  - "foundation"
  - "market-data"
  - "prices"
  - "research-design"
blocked_by: []
blocks:
  - "hormuz-4j7.3"
  - "hormuz-kmz.6"
  - "hormuz-l8m.1"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:19Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Inventory market price series and units

## Description

Identify daily/weekly series for Brent, Dubai/Oman, WTI, LNG markers, refined products, freight, insurance, fertilizer, petrochemicals, and power/gas benchmarks relevant to later cost estimates.

## Acceptance Criteria

Price series list includes source, frequency, access limits, units, and baseline/current comparison method.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Blocks: `hormuz-l8m.1` - Define commodity price shock scenarios

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass price-series inventory to subagent Dewey.
- 2026-07-06 subagent pass: added market price-series inventory in `docs/foundation-data-inventory.md`.
  - Public/reproducible priority: EIA/FRED for Brent/WTI/Henry Hub; World Bank Pink Sheet and IMF Primary Commodity Markets for monthly commodity history; CME/ICE/LME public exchange pages where available; Drewry public weekly WCI; LMA JWC public listed-area status.
  - Licensed-critical gaps: daily Dubai/Oman spot, Platts JKM history, Argus/ICIS/CRU fertilizer and sulphur prices, Baltic/Clarksons detailed freight, broker war-risk premium history.
  - Baseline/current method: compare latest/trailing average to the agreed pre-shock baseline from `hormuz-fyp.3`, report absolute change, percent change, z-score versus 2015-2024 history where available, and CPI-deflated values only for historical comparison work.
