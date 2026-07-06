---
id: "hormuz-2y7.7"
title: "Produce tracker dataset and publication chart"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "deliverable"
  - "shipping"
  - "tracker"
blocked_by:
  - "hormuz-2y7.5"
  - "hormuz-2y7.6"
  - "hormuz-fyp.7"
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:30Z"
updated_at: "2026-07-06T15:00:00Z"
---

# Produce tracker dataset and publication chart

## Description

Finalize a daily Hormuz ship tracker table and a chart suitable for the blog, including uncertainty and data gaps.

## Acceptance Criteria

Chart and dataset can be regenerated; caveats are short, precise, and source-backed.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-2y7.5` - Validate transit counts against external benchmarks
- Blocked by: `hormuz-2y7.6` - Backfill historical traffic series around prior shocks
- Blocked by: `hormuz-fyp.7` - Define chart and map standards for the project
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline
- Blocks: `hormuz-ccx.3` - Assemble final figure package

## Work Notes

- 2026-07-06: Claimed for deliverable planning only. Final dataset/chart remains blocked on validated counts and chart standards from `hormuz-fyp.7`; use provisional output schemas now and reconcile visual standards later.

### Provisional Deliverable Shape

- Dataset grain: one row per `date_utc` x `direction` x `vessel_class`.
- Required columns: `date_utc`, `direction`, `vessel_class`, `transit_count`, `unique_vessels`, `coverage_flag`, `method_version`, `source`, `confidence`.
- Chart idea: daily merchant transits through Hormuz, split inbound/outbound or shown as total with direction small multiples; uncertainty/coverage flags should be visible rather than hidden in notes.
- Public benchmark chart can be generated from `data/external/portwatch/hormuz_daily_chokepoint.csv` while raw AIS tracker access is unresolved, with clear labeling as PortWatch chokepoint transit calls rather than project-derived AIS crossings.
- Do not finalize chart styling until `hormuz-fyp.7` lands.

### Closeout

- Produced public tracker dataset: `data/derived/hormuz_2y7_public_daily_tracker.csv`.
- Produced chart and figure data: `figures/fig-2y7-public-hormuz-daily-transits.svg` and `figures/fig-2y7-public-hormuz-daily-transits.csv`.
- Chart follows the foundation standard by labeling source, latest observation date, baseline, shock marker, and known/unknown limitations.
