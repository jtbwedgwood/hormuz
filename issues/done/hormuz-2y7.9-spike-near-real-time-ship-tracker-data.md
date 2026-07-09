---
id: "hormuz-2y7.9"
title: "Spike near-real-time data options for the ship tracker"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "etl"
  - "shipping"
  - "tracker"
blocked_by: []
blocks: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-07T00:00:00Z"
updated_at: "2026-07-07T00:00:00Z"
---

# Spike near-real-time data options for the ship tracker

## Description

Evaluate how to keep the daily Strait of Hormuz ship tracker current between IMF PortWatch releases, accepting a heterogeneous provisional data layer for the most recent days if it is clearly labeled and later replaced by PortWatch.

## Acceptance Criteria

Practical recommendation identifies candidate sources, freshness, metric compatibility with PortWatch, ETL architecture, and caveats for a nightly/continuous job.

## Work Notes

- 2026-07-07: Current production path is `scripts/fetch_portwatch_hormuz.py` plus `scripts/build_public_hormuz_tracker.py`; current raw-AIS prototype is `code/hormuz_tracker/prototype_daily_transits.py`, which can ingest normalized AIS positions and count line crossings.
- 2026-07-07: IMF PortWatch remains the best public canonical series. PortWatch FAQ says port/chokepoint activity and transit volume estimates are updated weekly on Tuesdays at 9 AM ET; local validation found a roughly 3-10 day public lag. Source: https://portwatch.imf.org/pages/faqs.
- 2026-07-07: AISstream is a plausible free live feed, but it is a live WebSocket, not a backfill API. The docs require a backend-held API key, a bounding-box subscription to `wss://stream.aisstream.io/v0/stream`, and optional filters such as `FilterMessageTypes`; messages include `MessageType`, `Message`, and metadata such as MMSI, ship name, latitude, longitude, and `time_utc`. Source: https://aisstream.io/documentation.
- 2026-07-07: AISstream is useful only if we run a continuous collector. A nightly cron job that connects for a few minutes would produce a sampling index, not a daily transit count. If the collector is down, there is no free AISstream backfill to repair the gap.
- 2026-07-07: Global Fishing Watch AIS Vessel Presence is the best public near-real-time backfill candidate, but it is not a direct transit-count series. GFW says AIS vessel presence uses one position per hour per vessel, includes all vessel types, supports filters such as `vessel_type` and speed, and is available to about 96 hours ago / with about 72-hour delay depending on page. Sources: https://globalfishingwatch.org/our-apis/documentation and https://globalfishingwatch.org/global-fishing-watch-data-availability/.
- 2026-07-07: GFW API use requires a bearer token and explicitly warns not to expose tokens in public web interfaces. Source: https://globalfishingwatch.org/our-apis/documentation.

## Spike Result

Recommended data tiers:

| Tier | Source | Freshness | Metric | Use in tracker |
|---|---|---:|---|---|
| Canonical | IMF PortWatch Daily_Chokepoints_Data | Weekly release; observed lag about 3-10 days | Daily chokepoint transit calls by broad class | Replace provisional rows when available. This remains the historical/caption baseline. |
| Provisional count | AISstream live WebSocket captured continuously | Live to T-1 if collector is healthy | Deduplicated vessel crossing count from raw AIS-like positions | Best way to keep the chart current for yesterday/today. Must be labeled `provisional_aisstream_crossing_count`. |
| Provisional proxy | Global Fishing Watch AIS Vessel Presence | About T-3/T-4 | Vessel presence / vessel-hours in Hormuz gate/core by vessel type/speed | Good fallback/QA layer, but not numerically comparable to PortWatch counts without calibration. Label as presence proxy. |
| Paid robust path | Kpler/Vortexa/MarineTraffic/Spire/exactEarth-style historical AIS/cargo products | Provider-specific; often near-real-time with backfill | Vessel/cargo-level transit reconstruction | Best publication-grade live tracker if budget allows; already conceptually covered by deferred vessel-level paid AIS issue. |

Recommended ETL design:

1. Keep the PortWatch pipeline as the canonical replace-on-release source.
2. Add an always-on AISstream collector, not just a nightly cron. It should subscribe to a Hormuz bounding box large enough for the core gate and both confirmation sides from `hormuz-2y7.2`, filter to position/static messages where possible, and write append-only NDJSON partitioned by UTC day under `data/raw/aisstream/YYYY/MM/DD.ndjson` or an untracked production bucket.
3. Run a nightly ETL that converts the previous UTC day of AISstream messages into the normalized schema expected by `code/hormuz_tracker/prototype_daily_transits.py`, then writes `data/derived/hormuz_2y7_realtime_overlay.csv` with `source`, `coverage_flag`, `is_provisional`, `collector_uptime_pct`, and `count_method`.
4. Optionally run a separate GFW job for the trailing 4-10 day window as a QA/proxy layer. Do not splice GFW vessel-hours into the same y-axis as PortWatch transit calls unless the chart explicitly switches metric labels.
5. The public widget should render one continuous line only if rows are visually/metadata-labeled by source and confidence; otherwise use a shaded provisional tail for AISstream/GFW.

Implementation notes:

- Environment variables: `AISSTREAM_API_KEY` for the live collector; `GFW_API_TOKEN` if the GFW API is used.
- Suggested AISstream message filters: `PositionReport`, `StandardClassBPositionReport`, `ExtendedClassBPositionReport`, `ShipStaticData`, and `StaticDataReport`.
- Suggested bounding geometry: start with the `HORMUZ_CORE`, `GULF_OF_OMAN_SIDE`, and `PERSIAN_GULF_SIDE` boxes already recorded in `hormuz-2y7.2`; avoid a tiny throat-only box because direction and true transit confirmation need side evidence.
- Minimum quality flags: collector uptime, messages received, unique MMSI count, static-data coverage share, ambiguous crossing share, repeated-crossing dedupe count, and PortWatch calibration error once overlapping dates arrive.
- Main caveat: AISstream and GFW do not see AIS-dark vessels reliably. In a Hormuz crisis this is not a minor caveat; the near-real-time tail should be treated as observed AIS behavior, not definitive commercial traffic.

## Completion Note

Spike complete. Recommendation is to use a two-part near-real-time path: continuous AISstream capture for T-0/T-1 provisional counts, plus optional GFW AIS Vessel Presence for delayed public QA/proxy, with PortWatch replacing provisional rows after weekly release.
