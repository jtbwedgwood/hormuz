---
id: "hormuz-fyp"
title: "Foundation: shared research infrastructure and assumptions"
type: "epic"
status: "done"
priority: "P0"
parent: null
labels:
  - "foundation"
  - "research-design"
blocked_by: []
blocks:
  - "hormuz-2y7"
  - "hormuz-kmz"
children:
  - "hormuz-fyp.1"
  - "hormuz-fyp.2"
  - "hormuz-fyp.3"
  - "hormuz-fyp.4"
  - "hormuz-fyp.5"
  - "hormuz-fyp.6"
  - "hormuz-fyp.7"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:08:47Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Foundation: shared research infrastructure and assumptions

## Description

Establish the common research spine for the Hormuz project: source standards, event timeline, commodity taxonomy, baseline period definitions, and reproducible data layout. This epic should unblock every substantive research question without becoming a prose draft.

## Acceptance Criteria

Shared standards and baseline assumptions are recorded in issue files; source and data directories are sketched; downstream epics have explicit dependencies on the foundation items they need.

## Dependency Notes

- Blocks: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocks: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Child: `hormuz-fyp.1` - Define citation and source-quality rubric
- Child: `hormuz-fyp.2` - Build canonical disruption chronology
- Child: `hormuz-fyp.3` - Define baseline periods and scenario taxonomy
- Child: `hormuz-fyp.4` - Set up reproducible data inventory structure
- Child: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Child: `hormuz-fyp.6` - Inventory market price series and units
- Child: `hormuz-fyp.7` - Define chart and map standards for the project

## Work Notes

- 2026-07-06T06:23Z: Claimed with child tasks `hormuz-fyp.1` through `hormuz-fyp.7`.
- Working approach: keep detailed source breadcrumbs in child issue files; publish only compact, reusable foundation outputs in `docs/`.
- 2026-07-06T07:35Z: Completed foundation outputs:
  - `docs/foundation.md` for the compact foundation summary.
  - `docs/foundation-research-standards.md` for source/citation and chart/map standards.
  - `docs/foundation-chronology-and-scenarios.md` for chronology, baselines, and scenario taxonomy.
  - `docs/foundation-data-inventory.md` plus `data/manifest.csv` for data layout, commodity taxonomy, and price-series inventory.
