---
id: "hormuz-s49.6"
title: "Estimate stockpile buffer duration by country/product"
type: "task"
priority: "P1"
parent: "hormuz-s49"
labels:
  - "buffer"
  - "energy-security"
  - "modeling"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-4j7.3"
  - "hormuz-ccx.2"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:57Z"
status: "in_progress"
updated_at: "2026-07-06T19:05:00Z"
---

# Estimate stockpile buffer duration by country/product

## Description

Convert inventory and disrupted-flow estimates into days of cover under low/base/high disruption scenarios.

## Acceptance Criteria

Buffer table states assumptions, replenishment limits, demand seasonality, and confidence levels.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Unblocked: `hormuz-fyp.2` - Build canonical disruption chronology
- Unblocked: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Unblocked: `hormuz-s49.2` - Quantify OECD and US reserve response
- Cleared blocker: `hormuz-s49.3` - Evaluate China SPR release claims
- Cleared blocker: `hormuz-s49.4` - Assess LNG and gas storage buffering
- Unblocked: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.
- 2026-07-06: Reviewed the current repo evidence from `hormuz-s49.2`, `hormuz-s49.3`, `hormuz-s49.4`, `hormuz-s49.5`, the kmz derived tables, and the foundation manifest/docs.
- Decision: do **not** close this issue yet. The repo has enough fragments to sketch coverage, but not enough to publish a consolidated conservative buffer table that satisfies the acceptance criteria for all requested regions and products.
- What is currently supportable from the notes:
  - Oil / OECD / US / Japan / Korea / Europe: reserve and release snapshots exist, but the repo does not yet assemble a single common demand denominator or replenishment-limit framework across all regions. The U.S., Japan, and Korea figures in `hormuz-s49.2` are especially useful, but they are not yet normalized into one comparative days-of-cover table.
  - China SPR / commercial crude: `hormuz-s49.3` supports a low-confidence distinction between opaque strategic stocks and visible commercial drawdown, which is not enough to assign a conservative buffer duration for government SPR alone.
  - LNG / gas: `hormuz-s49.4` provides useful partial coverage, including Europe daily storage, Japan ~3 weeks, Korea 37 days on the reserve-rule basis, China a ~19-day upper-bound proxy, and India only a modeled proxy. Europe still needs the same denominator treatment as the others before the table can be called complete.
  - Fertilizer / chemicals: `hormuz-s49.5` gives a defensible India case study and a qualitative global claim that fertilizers lack coordinated strategic reserves, but the broader country/product table is still incomplete and petrochemicals remain qualitative only.
- Precise blocker:
  - The repo currently lacks one consolidated buffer table that harmonizes demand seasonality, replenishment limits, and confidence levels across the requested oil, gas/LNG, China crude, and fertilizer/chemical rows.
  - The open sibling tasks are still the source of truth for the missing pieces: `hormuz-s49.2` for OECD/US/Japan/Korea/Europe oil reserves, `hormuz-s49.3` for China SPR uncertainty, `hormuz-s49.4` for LNG/gas denominators, and `hormuz-s49.5` for fertilizer/chemicals.
- Until those are reconciled into one table, any country-by-product day-count would be stitched together from mixed bases and would not meet the rigor bar for closure.
- 2026-07-06 cleanup status: moved to `blocked`. Removed stale `hormuz-l8m.3` block because RQ5 completed that sensitivity table with stockpile buffering recorded as a caveat rather than a blocker.
- 2026-07-06 F6R follow-up: upstream China and LNG/gas adjustment tasks are now done, and this issue is back in `in-progress`. Remaining work is synthesis, not external unblock: reconcile S49 oil, China, LNG/gas, fertilizer/chemical, and F6R replacement/demand-response rows into one conservative buffer-duration table.
