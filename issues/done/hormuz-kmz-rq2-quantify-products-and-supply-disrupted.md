---
id: "hormuz-kmz"
title: "RQ2: Quantify products and supply disrupted"
type: "epic"
status: "done"
priority: "P0"
parent: null
labels:
  - "commodities"
  - "supply"
blocked_by: []
blocks:
  - "hormuz-4j7"
  - "hormuz-ccx"
  - "hormuz-f6r"
  - "hormuz-l8m"
children:
  - "hormuz-kmz.1"
  - "hormuz-kmz.2"
  - "hormuz-kmz.3"
  - "hormuz-kmz.4"
  - "hormuz-kmz.5"
  - "hormuz-kmz.6"
  - "hormuz-kmz.7"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:06Z"
updated_at: "2026-07-06T07:03:00Z"
---

# RQ2: Quantify products and supply disrupted

## Description

Identify the major products normally moved through Hormuz and estimate how much supply has been removed, delayed, rerouted, or substituted under the closure/disruption scenario.

## Acceptance Criteria

Commodity list is comprehensive enough for publication; normal baseline flows and disrupted volumes are estimated with citations; uncertainty and double-counting risks are documented.

## Dependency Notes

- Former blocker resolved: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Former blocker resolved: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Blocks: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Blocks: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Child: `hormuz-kmz.1` - Estimate normal Hormuz export flows by country and product
- Child: `hormuz-kmz.2` - Map bypass routes and non-Hormuz export capacity
- Child: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Child: `hormuz-kmz.4` - Investigate non-obvious disrupted products
- Child: `hormuz-kmz.5` - Quantify freight, insurance, and war-risk disruption
- Child: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Child: `hormuz-kmz.7` - Produce product disruption master table

## Work Notes

- 2026-07-06: Claimed the epic and child tasks despite upstream `hormuz-fyp` and `hormuz-2y7` dependencies still in progress. Proceeding with public EIA/IEA anchors and marking tracker-dependent values as preliminary rather than blocked.
- 2026-07-06: Delegated independent research slices to subagents: `hormuz-kmz.1` baseline flows, `hormuz-kmz.2` bypass capacity, `hormuz-kmz.4` non-obvious products, `hormuz-kmz.5` freight/insurance, and `hormuz-kmz.6` market balances. Local work owns `hormuz-kmz.3` preliminary disruption scenarios and `hormuz-kmz.7` master-table scaffold.
- 2026-07-06: Current central framing: use `docs/foundation.md` and `docs/foundation-chronology-and-scenarios.md`; treat the shock as effective disruption with fragile partial recovery, not a binary closure. Key public anchors are EIA's 2024 20 mb/d Hormuz oil flow and 2026 STEO near-term effective-closure assumption, plus IEA's 2025 >110 bcm LNG-through-Hormuz estimate and >300 mcm/d LNG supply loss since 2026-03-01.

### Coordination Notes

- Do not wait on final chart standards before building source-backed tables. Required later repairs: citation row normalization, confidence taxonomy reconciliation, and figure/table naming once `hormuz-fyp.1`/`.7` finish.
- Keep oil `traffic`, `transit flow`, `production shut-in`, `inventory draw`, and `market supply loss` separate. EIA/IEA public numbers currently mix those concepts at different stages of the shock.
- Main double-counting risk: LPG/NGLs and refined products may already be included in broad petroleum liquids totals depending on source definition. The master table should keep them separate for narrative analysis but avoid summing them into a single "barrels removed" headline until definitions are reconciled.

### Status Update

- 2026-07-06: Completed six child tasks and moved them to `issues/done/`: `hormuz-kmz.1`, `hormuz-kmz.2`, `hormuz-kmz.4`, `hormuz-kmz.5`, `hormuz-kmz.6`, and `hormuz-kmz.7`.
- 2026-07-06: Moved `hormuz-kmz.3` to `issues/blocked/`. The blocker is specific: final low/base/high disrupted supply by product and country needs validated `hormuz-2y7.5` ship-tracker output by vessel class/direction. A preliminary bridge table exists at `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`.
- 2026-07-06: Keep this epic in progress until `hormuz-kmz.3` is unblocked or the project decides that modeled public-source disruption ranges are sufficient for the blog.
- 2026-07-06: Follow-up pass fixed the `.venv` pytest setup, completed `hormuz-2y7.5`, confirmed the other `hormuz-kmz.3` blockers were already done, and completed `hormuz-kmz.3` with a modeled country/product disruption table at `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`.

### Completion Note

- 2026-07-06: All child tasks are complete. The epic acceptance criteria are met for current project stage: commodity list is comprehensive enough for publication, normal baseline flows and disrupted volumes are estimated with citations, and uncertainty/double-counting risks are documented. Future licensed cargo-flow data should refresh the estimates, but no active local issue dependency remains.
