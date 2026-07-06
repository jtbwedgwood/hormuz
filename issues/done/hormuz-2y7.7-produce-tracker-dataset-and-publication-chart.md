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

### Follow-up QA: latest lag, tanker interpretation, and co-movement

- 2026-07-06: Re-queried the live IMF PortWatch `Daily_Chokepoints_Data` ArcGIS endpoint for `chokepoint6`; it still returns 2019-01-01 through 2026-06-28, matching the local source pull. PortWatch docs/FAQ describe daily port and chokepoint datasets as updated weekly, Tuesdays 9 AM ET, so the lag is a weekly release cadence rather than a fixed daily latency. Source: https://portwatch.imf.org/pages/data-and-methodology and https://portwatch.imf.org/pages/faqs.
- Current check date is 2026-07-06, so latest public PortWatch Hormuz observation is 8 calendar days old. Because the service's layer metadata shows `dataLastEditDate` around 2026-07-01 UTC, the dataset appears to have been loaded about 3 days after 2026-06-28; depending on weekday, public lag will likely be roughly 3-10 days.
- Free supplementation: Global Fishing Watch AIS Vessel Presence is potentially usable for a rough recent geofence-derived proxy because it is open and near-real-time with about 72-96 hour delay, but it is hourly/thinned vessel presence, not a PortWatch-equivalent chokepoint transit-count product. AISstream is free and live, useful prospectively only; public MarineTraffic/VesselFinder-style historical extracts are paid or not reliably bulk-free.
- Field arithmetic: `n_total = n_tanker + n_cargo`; `n_cargo` is the aggregate of `n_container + n_dry_bulk + n_general_cargo + n_roro`, not an additional class. Do not sum `n_cargo` with the four underlying non-tanker categories.
- Co-movement QA: daily `n_total` vs `n_tanker` correlation is high in the raw PortWatch series (`r=0.947` for 2019-2024 baseline; `r=0.947` post-2026-02-28; `r=0.961` for June 2026). The chart's 7-day rolling averages make this look even tighter (`r=0.980`, `0.992`, and `0.983` respectively). This is not evidence that tanker is mechanically derived as a fixed fraction of total; raw tanker shares vary materially, especially post-shock. It is mainly the combination of (1) total explicitly containing tanker, (2) Hormuz traffic being tanker-heavy in normal conditions, (3) the shock affecting all commercial transits together, and (4) 7-day smoothing.
