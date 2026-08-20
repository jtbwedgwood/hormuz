---
id: "hormuz-m8q.4"
title: "Build cumulative oil accounting charts and current-traffic closure scenarios"
type: "task"
status: "in_progress"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "accounting"
  - "visuals"
  - "scenarios"
blocked_by: []
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.4"
  - "hormuz-ccx.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-03T22:57:25Z"
updated_at: "2026-08-05T00:30:00Z"
---

# Build cumulative oil accounting charts and current-traffic closure scenarios

## Description

Integrate the monthly balance, refreshed traffic level, and adjustment-channel evidence into cumulative observed-history charts and provisional future closure scenarios.

## Acceptance Criteria

- Every historical chart is cumulative from 2026-03-01 through a prominently labeled common accounting date.
- Observed/preliminary history includes the June relaxation; estimated or forecast July segments are visually and textually distinguished.
- A physical-disruption chart separates missing Hormuz flow, route preservation/bypass, affected Gulf production loss, and net global supply loss.
- A global-accounting waterfall or Sankey closes within an explicit residual; a simplified pie uses the same exact denominator and machine-readable data.
- Scenario history is frozen. From the scenario start date forward, Strait traffic remains near the refreshed current level through 2026-09-30, 2026-12-31, and 2027-03-31, with uncertainty around the traffic-to-oil mapping.
- Scenario outputs project oil supply and mitigation durability, not price.
- Figure data, scripts, SVGs, source notes, and manifest entries are reproducible and citation-audited.

## Work Notes

- 2026-08-03: Root-owned integration task. Work can begin on definitions and validation, but numeric chart generation waits on `hormuz-m8q.1` through `.3`.
- 2026-08-03: Provisional chart convention: use an accounting horizon of 2026-07-31 if the monthly panel supports a July estimate/forecast. Label the source vintage and status on every July value. For traffic, retain observations through the refreshed PortWatch data-as-of date and nowcast only the remaining July days at the explicitly stated current-regime rate. The graphic must distinguish `accounting through` from `traffic observed through`.
- 2026-08-03: Built the first closed cumulative accounting from the frozen 2026-02-10 and latest 2026-07-07 EIA STEO vintages. March-July supply is 1,724.4 million barrels below the frozen forecast. The arithmetic bridge is 566.4 mb lower consumption, 479.2 mb of expected stock build that did not occur, and 678.8 mb of implied inventory draw. March-June inputs are preliminary estimates; July is an EIA forecast completed July 1. This global balance revision is not a claim that every revision was caused by Hormuz.
- 2026-08-03: Added `scripts/build_m8q_4_cumulative_oil_accounting.py`, `data/derived/hormuz_m8q_4_cumulative_global_oil_accounting.csv`, and companion figure data/SVG. The donut labels the July endpoint and forecast status and closes to zero arithmetic residual. Visual QA passed after replacing SVG `pathLength` dash units with explicit circumference units.
- 2026-08-03: Keep a second stock lens visible in narrative/audit work. Latest IEA observed-stock estimates sum to a 298 mb March-June draw, while EIA's same-period implied balance draws about 606 mb. The cumulative donut uses the internally closed EIA implied balance; it must not be relabeled as observed tank movement.
- 2026-08-03: Integrated `hormuz-m8q.5` into a second cumulative graphic: `figures/fig-m8q-current-traffic-cumulative-scenarios.svg` plus machine-readable figure data and `scripts/build_m8q_4_cumulative_scenario_chart.py`. The stacked base-case market bridge and resilient-to-stress physical-loss whiskers are cumulative from 2026-03-01 through each horizon. The figure states that oil data are preliminary through June, July is forecast/nowcast, PortWatch traffic is observed through 2026-07-23, and the 2026-07-08 through 2026-07-23 regime is then held constant.
- 2026-08-03: Integration QA: scenario figure data reproduce the 2.534/3.647/4.736 billion-barrel base losses through September/December/March; all stacked bars close to those totals; the SVG passed visual inspection. Remaining work before this task can close is the requested physical-disruption panel and a citation/double-counting audit of the full figure package.
- 2026-08-04: Reprioritized per user direction: lock the detailed historical March-July bridge before doing more future-scenario work. The existing scenario outputs remain provisional. Historical integration will consume the new `.6`-.8 country ledgers and produce a country-by-country narrative/bridge whose named components add to one consistent denominator, with a visible unknown rather than forced attribution.
- 2026-08-04: Historical integration completed in `docs/hormuz-historical-oil-accounting-march-july-2026.md`, supported by `.6`-.10 and five reproducible ledgers. The audit separates (A) the physical route/supply diagnostic from (B) the exact global market-clearing bridge, preventing rerouting and replacement supply from being added to stock draws and demand reduction. The March-June physical route bridge has a 64.1 million barrel base residual (roughly zero to 126 million over the bypass sensitivity); the March-July EIA identity closes exactly to 1,724.364 million barrels. Future-scenario work remains paused pending user review of this historical baseline.
- 2026-08-05: Added the deliberately lower-confidence residual-story layer from `.11`-.13. The new synthesis distinguishes physical hidden-stock scenarios from model/coverage discrepancy and partitions regional demand revisions across explicit policy, decentralized behavior/switching, forced constraint/activity loss, and non-causal/unknown categories. All views close to existing denominators and are non-additive alternatives. Scenario projection work remains paused.
