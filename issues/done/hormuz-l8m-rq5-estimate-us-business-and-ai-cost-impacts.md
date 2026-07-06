---
id: "hormuz-l8m"
title: "RQ5: Estimate US business and AI cost impacts"
type: "epic"
status: "done"
priority: "P1"
parent: null
labels:
  - "ai"
  - "prices"
  - "us-business"
blocked_by: []
blocks:
  - "hormuz-4j7"
  - "hormuz-ccx"
children:
  - "hormuz-l8m.1"
  - "hormuz-l8m.2"
  - "hormuz-l8m.3"
  - "hormuz-l8m.4"
  - "hormuz-l8m.5"
  - "hormuz-l8m.6"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:09Z"
updated_at: "2026-07-06T17:45:00Z"
---

# RQ5: Estimate US business and AI cost impacts

## Description

Translate commodity price shocks into plausible added costs for US businesses, with a focused estimate for AI data center power costs and cost per token sensitivity.

## Acceptance Criteria

Price shock scenarios are defined; US cost pass-through channels are quantified; AI inference/training energy cost sensitivity is estimated with transparent assumptions.

## Dependency Notes

- Upstream `hormuz-kmz` is complete and `hormuz-s49` remains a caveat for the broader stockpile-buffer narrative, not a blocker for this completed scenario-sensitivity package.
- Blocks: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Child: `hormuz-l8m.1` - Define commodity price shock scenarios
- Child: `hormuz-l8m.2` - Estimate added cost to US businesses by sector
- Child: `hormuz-l8m.3` - Estimate US power-price implications for data centers
- Child: `hormuz-l8m.4` - Estimate AI cost-per-token sensitivity
- Child: `hormuz-l8m.5` - Cross-check against macro inflation and energy models
- Child: `hormuz-l8m.6` - Produce US business and AI cost visuals

## Work Notes

- 2026-07-06T16:00Z: Claimed epic for parallel work on RQ5. Upstream `hormuz-kmz` and `hormuz-s49` remain active blockers for final estimates, so current work should produce scenario-ready methods, provisional ranges, and source breadcrumbs rather than final blog claims.
- 2026-07-06T17:45Z: Closed RQ5 after all six child tasks moved to `issues/done/`. The package now includes scenario inputs (`hormuz-l8m.1`), sector cost method/table (`hormuz-l8m.2`), data-center regional power sensitivity (`hormuz-l8m.3`), AI cost-per-token sensitivity (`hormuz-l8m.4`), macro cross-checks (`hormuz-l8m.5`), and two visual/data deliverables (`hormuz-l8m.6`). `hormuz-s49.6` remains open for the broader stockpile-buffer narrative, but `hormuz-l8m.3` records why that is a caveat rather than a blocker for the RQ5 power-price sensitivity table.
- 2026-07-06 cleanup: removed stale `blocked_by` entries after confirming RQ5 was closed as a provisional scenario-sensitivity package, not as a final realized-cost model.

## Completion Note

- Acceptance criteria met: price shock scenarios are defined; U.S. cost pass-through channels are quantified in a scenario-ready sector table; AI inference/training electricity sensitivity is estimated separately from capex/GPU/labor costs with transparent assumptions; and initial publication visuals exist as SVG plus machine-readable CSV.
- Key output paths: `data/derived/hormuz_l8m_6_sector_exposure_bands.csv`, `data/derived/hormuz_l8m_6_ai_electricity_cost_sensitivity.csv`, `figures/hormuz-l8m-6-sector-exposure-pass-through-bands.svg`, and `figures/hormuz-l8m-6-ai-electricity-cost-sensitivity.svg`.
