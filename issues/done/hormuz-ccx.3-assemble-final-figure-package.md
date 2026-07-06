---
id: "hormuz-ccx.3"
title: "Assemble final figure package"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-ccx"
labels:
  - "blog"
  - "figures"
  - "synthesis"
  - "visuals"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:18Z"
updated_at: "2026-07-06T20:25:00Z"
---

# Assemble final figure package

## Description

Collect final tracker, commodity, destination, stockpile, cost, and historical visuals with source notes and reproducible generation paths.

## Acceptance Criteria

Each figure has owner/source/provenance, confidence caveats, and blog-ready export.

## Dependency Notes

- Parent: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Cleared dependency: `hormuz-2y7.7` - Produce tracker dataset and publication chart
- Cleared dependency: `hormuz-4j7.5` - Produce historical comparison graphic
- Cleared dependency: `hormuz-f6r.6` - Produce destination flow map and exposure chart
- Cleared dependency: `hormuz-fyp.7` - Define chart and map standards for the project
- Cleared dependency: `hormuz-kmz.7` - Produce product disruption master table
- Cleared dependency: `hormuz-l8m.6` - Produce US business and AI cost visuals
- Blocks: `hormuz-ccx.5` - Draft blog post from evidence package

## Work Notes

- 2026-07-06T20:25Z: Completed figure-package pass. Regenerated the public tracker, importer-adjustment, and historical-comparison SVGs with shorter visible caveats and centralized figure interpretation in `figures/README.md`. Added two EIA/Vortexa baseline Sankeys: `figures/fig-kmz-oil-hormuz-baseline-sankey.svg` and `figures/fig-kmz-lng-hormuz-baseline-sankey.svg`, each with companion CSVs and generation script `scripts/build_hormuz_baseline_sankeys.py`. The Sankeys use EIA origin totals and destination totals separately; they are not cargo-pair matrices.
