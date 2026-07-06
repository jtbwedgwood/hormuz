---
id: "hormuz-2y7.6"
title: "Backfill historical traffic series around prior shocks"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "historical"
  - "shipping"
  - "tracker"
blocked_by:
  - "hormuz-2y7.4"
blocks:
  - "hormuz-2y7.7"
  - "hormuz-4j7.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:29Z"
updated_at: "2026-07-06T15:00:00Z"
---

# Backfill historical traffic series around prior shocks

## Description

Assess whether the same tracker can produce historical comparison windows for earlier disruptions or at least representative baselines.

## Acceptance Criteria

Historical availability and comparability are documented; usable windows are marked for the historical comparison epic.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-2y7.4` - Prototype daily transit count pipeline
- Blocks: `hormuz-2y7.7` - Produce tracker dataset and publication chart
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data

## Work Notes

- 2026-07-06: Claimed for availability planning only. Backfill is materially blocked until the tracker pipeline and data source access are selected, but historical comparability requirements can be collected now.

### Provisional Backfill Feasibility Notes

- Best public backfill window: IMF PortWatch daily Hormuz chokepoint series from 2019-01-01 onward. This covers 2019 tanker tensions, COVID, 2024 Red Sea rerouting spillovers, and the 2026 crisis with one consistent public method. Sources: https://portwatch.imf.org/pages/chokepoint6, https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query.
- 2019 May-July tanker-attack comparator: subagent query found Hormuz average about 85.2 total ships/day, min 42, max 123 in PortWatch. Treat as a security-shock-without-full-closure comparator after reproducing the query locally.
- 2024 Red Sea disruption spillover: EIA says Saudi shifted some seaborne crude flows away from Hormuz via the East-West pipeline during Bab al-Mandeb disruptions. Use as a flow-composition comparator, not a pure Hormuz security shock. Source: https://www.eia.gov/todayinenergy/detail.php?id=65504.
- Public/free historical route likely starts with Global Fishing Watch AIS Vessel Presence from 2012 onward, but comparability to exact transit counts is uncertain because it is hourly standardized presence rather than raw tracks.
- MarineTraffic/Kpler or equivalent paid AIS is the likely path for raw event backfill. MarineTraffic documentation indicates historical positions from January 2015; Kpler markets 10+ years of historical AIS.
- Pre-2012/2015 shock windows will likely require non-AIS proxies: port calls, commodity flow estimates, reported tanker movements, insurance/freight records, or contemporaneous news/official summaries.
- Pre-2019 shocks have no PortWatch daily series. Use EIA/IEA/OPEC historical flow estimates, Tanker War/Gulf War narrative sources, insurance/freight data, and news archives only as lower-resolution comparators; do not present them as directly comparable to daily AIS/PortWatch counts.
- Any historical comparison must separate true traffic change from AIS coverage changes and data-provider archive changes.

### Local Backfill Dataset

- 2026-07-06: `scripts/fetch_portwatch_hormuz.py` writes the current public PortWatch Hormuz daily series to `data/external/portwatch/hormuz_daily_chokepoint.csv`.
- Current local pull spans 2019-01-01 to 2026-06-28. This is now the default public backfill spine until/unless paid AIS access is secured.

### Closeout

- Usable historical daily window: 2019-01-01 onward via IMF PortWatch.
- Pre-2019 comparisons are not directly comparable daily ship-count series under the public-only constraint. They should be lower-resolution historical analogues using flows, prices, inventories, news, or war-risk proxies.
