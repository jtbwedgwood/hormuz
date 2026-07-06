---
id: "hormuz-fyp.3"
title: "Define baseline periods and scenario taxonomy"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-fyp"
labels:
  - "baselines"
  - "foundation"
  - "methods"
  - "research-design"
blocked_by: []
blocks:
  - "hormuz-2y7.4"
  - "hormuz-4j7.3"
  - "hormuz-kmz.3"
  - "hormuz-l8m.1"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:15Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Define baseline periods and scenario taxonomy

## Description

Decide which baseline windows are used for normal traffic, commodity flows, prices, inventories, and demand. Define disruption scenarios such as closure, partial closure, insurance shock, and rerouting delay.

## Acceptance Criteria

Baseline windows and scenarios are recorded with rationale; downstream tasks can reference them without redefining assumptions.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-2y7.4` - Prototype daily transit count pipeline
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocks: `hormuz-l8m.1` - Define commodity price shock scenarios

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass baseline/scenario taxonomy to subagent Mendel.
- 2026-07-06T07:10Z: Subagent pass recorded baseline windows and scenario taxonomy in `docs/foundation-chronology-and-scenarios.md`. Recommended day 0 is 2026-02-28; primary traffic baseline ends 2026-02-27; current best-fit scenario is fragile reopening with reversal risk through the 60-day clock from 2026-06-17.
