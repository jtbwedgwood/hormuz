---
id: "hormuz-s49"
title: "RQ4: Assess strategic stockpiles and reserve releases"
type: "epic"
status: "blocked"
priority: "P1"
parent: null
labels:
  - "energy-security"
  - "spr"
  - "stockpiles"
blocked_by:
  - "hormuz-f6r"
blocks:
  - "hormuz-4j7"
  - "hormuz-ccx"
children:
  - "hormuz-s49.1"
  - "hormuz-s49.2"
  - "hormuz-s49.3"
  - "hormuz-s49.4"
  - "hormuz-s49.5"
  - "hormuz-s49.6"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:07Z"
updated_at: "2026-07-06T07:45:00Z"
---

# RQ4: Assess strategic stockpiles and reserve releases

## Description

Estimate the role of strategic petroleum reserves, commercial inventories, LNG storage, and other stockpiles in cushioning the shock, with special scrutiny of China SPR claims.

## Acceptance Criteria

Reserve and inventory sources are inventoried; releases or drawdowns are quantified where possible; China SPR claims are evaluated with source quality notes.

## Dependency Notes

- Blocked by: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Blocks: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Cleared downstream dependency: `hormuz-l8m` - RQ5 completed with stockpile buffering treated as a caveat rather than a blocker.
- Child: `hormuz-s49.1` - Inventory reserve and stockpile data sources
- Child: `hormuz-s49.2` - Quantify OECD and US reserve response
- Child: `hormuz-s49.3` - Evaluate China SPR release claims
- Child: `hormuz-s49.4` - Assess LNG and gas storage buffering
- Child: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers
- Child: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Claimed epic for partial parallel start. `hormuz-s49.1` through `hormuz-s49.5` moved to `issues/in-progress/`; `hormuz-s49.6` remains open because it depends on upstream quantified reserve/gas/fertilizer findings and disrupted-flow estimates.
- 2026-07-06: Spawned independent subagents for source inventory (`s49.1`), OECD/US reserve response (`s49.2`), China SPR claims (`s49.3`), LNG/gas storage buffering (`s49.4`), and fertilizer/chemical inventory buffers (`s49.5`). Downstream tasks should treat `s49.2`-`s49.5` notes as preliminary until `s49.1` source inventory is reconciled.
- 2026-07-06: Second parallel push launched for `s49.2`-`s49.5` after `s49.1` completion. Target outputs are issue-note conclusions plus table-ready derived CSVs where useful: reserve response, China SPR evidence matrix, LNG/gas buffer table, and fertilizer/chemical buffer table.
- 2026-07-06: Post-swarm cleanup moved the epic from `in-progress` to `blocked`. Useful partial outputs exist, but final closure depends on importer-adjustment work under `hormuz-f6r` and a consolidated `hormuz-s49.6` buffer table.
