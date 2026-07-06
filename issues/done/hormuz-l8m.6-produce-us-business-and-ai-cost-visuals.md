---
id: "hormuz-l8m.6"
title: "Produce US business and AI cost visuals"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "costs"
  - "prices"
  - "us-business"
  - "visuals"
blocked_by:
  - "hormuz-fyp.7"
  - "hormuz-l8m.5"
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:06Z"
updated_at: "2026-07-06T17:40:00Z"
---

# Produce US business and AI cost visuals

## Description

Create concise visuals showing sector exposure and AI cost-per-token sensitivity under low/base/high scenarios.

## Acceptance Criteria

Charts are interpretable without overstating precision and cite all major assumptions.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-fyp.7` - Define chart and map standards for the project
- Blocked by: `hormuz-l8m.5` - Cross-check against macro inflation and energy models
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline
- Blocks: `hormuz-ccx.3` - Assemble final figure package

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.
- 2026-07-06T17:40Z: Produced two lightweight figure data CSVs and two SVG charts. The sector visual is normalized to a 15% / 25% / 40% direct-energy shock and uses the l8m.2 pass-through bands; the AI visual uses the l8m.4 electricity-only sensitivity band with $3 / $7 / $14 per MWh shocks. The sector chart is intentionally a presentation band, not a final BEA crosswalk.

## Completion Note

- 2026-07-06T17:40Z: Acceptance criteria met. Output paths: `data/derived/hormuz_l8m_6_sector_exposure_bands.csv`, `data/derived/hormuz_l8m_6_ai_electricity_cost_sensitivity.csv`, `figures/hormuz-l8m-6-sector-exposure-pass-through-bands.svg`, and `figures/hormuz-l8m-6-ai-electricity-cost-sensitivity.svg`.
- Source / assumption breadcrumbs: EIA MECS 2022 anchors for sector direct energy spend; l8m.2 pass-through bands (direct fuel/electricity 35% / 60% / 90%, tier-2 inputs and freight 20% / 35% / 55%); l8m.4 energy-intensity and PUE ranges (0.25-4.0 kWh / 1M tokens, PUE 1.1-1.6) with $3 / $7 / $14 per MWh electricity shocks; l8m.5 macro cross-check framing.
