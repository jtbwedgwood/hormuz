---
id: "hormuz-2y7.4"
title: "Prototype daily transit count pipeline"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "pipeline"
  - "shipping"
  - "time-series"
  - "tracker"
blocked_by:
  - "hormuz-2y7.1"
  - "hormuz-2y7.2"
  - "hormuz-2y7.3"
  - "hormuz-fyp.3"
blocks:
  - "hormuz-2y7.5"
  - "hormuz-2y7.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:26Z"
updated_at: "2026-07-06T07:03:00Z"
---

# Prototype daily transit count pipeline

## Description

Create the first reproducible workflow for converting raw or sampled vessel data into daily counts by direction and vessel class.

## Acceptance Criteria

Pipeline produces a date-indexed table with counts, vessel class, direction, coverage flags, and clear provenance.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-2y7.1` - Evaluate AIS and vessel-position data sources
- Blocked by: `hormuz-2y7.2` - Define Strait of Hormuz transit geofence and counting rules
- Blocked by: `hormuz-2y7.3` - Map vessel classes to commodity categories
- Blocked by: `hormuz-fyp.3` - Define baseline periods and scenario taxonomy
- Blocks: `hormuz-2y7.5` - Validate transit counts against external benchmarks
- Blocks: `hormuz-2y7.6` - Backfill historical traffic series around prior shocks

## Work Notes

- 2026-07-06: Claimed. Actual counts remain blocked on data-source access and final counting rules, but a source-agnostic prototype can proceed with a documented input schema, crossing-line algorithm, direction classification, and output schema.
- 2026-07-06: Added prototype source-agnostic counter under `code/hormuz_tracker/`. It reads normalized AIS-like positions, detects line crossings, interpolates crossing time, assigns direction, filters low-speed/stale track segments, deduplicates repeat crossings within 6 hours, and writes daily counts by `date_utc`, `direction`, and `vessel_class`.
- 2026-07-06: Current default crossing line uses the provisional `hormuz-2y7.2` throat gate `(26.24, 56.50)` to `(26.56, 56.50)`, but still needs validation against AIS samples and current chart/ENC layers. Current output `coverage_flag` is hard-coded to `prototype_unvalidated`.
- 2026-07-06: Audited checked-in Python code for `.venv` use and dependencies. Runtime tracker scripts use only the Python standard library. `requirements.txt` now includes pytest as test tooling so `.venv/bin/python -m pytest ...` works consistently. The unit test invokes `sys.executable` so subprocess coverage stays inside the active `.venv`.
- 2026-07-06: Verified `.venv/bin/python -m pytest code/hormuz_tracker/test_prototype_daily_transits.py -q`: 1 passed.

### Prototype Input Schema

Required columns: `timestamp_utc`, `lat`, `lon`, and at least one of `vessel_id`, `imo`, or `mmsi`.

Recommended columns: `sog_knots`, `ship_type`, `vessel_class`, `source`.

### Prototype Output Schema

Columns: `date_utc`, `direction`, `vessel_class`, `transit_count`, `unique_vessels`, `coverage_flag`.

### Known Gaps Before Real Use

- Add side-confirmation boxes from `hormuz-2y7.2`; current prototype counts any crossing of the line.
- Add identity reconciliation across MMSI/IMO/name/callsign/dimensions.
- Add impossible-speed track splitting and provider duplicate handling.
- Add confidence flags: confirmed, interpolated, probable-dark-gap, ambiguous, local-or-aborted, outside-TSS.
- Add source-specific import adapters once data access is selected.

### Closeout

- Source-agnostic raw-AIS prototype exists in `code/hormuz_tracker/prototype_daily_transits.py` with a pytest-verified smoke test and synthetic data.
- Public-only production path is `scripts/fetch_portwatch_hormuz.py` plus `scripts/build_public_hormuz_tracker.py`, producing `data/derived/hormuz_2y7_public_daily_tracker.csv`.
- Real vessel-level production with direction and vessel identities is not possible under the no-paid-data constraint; tracked separately as blocked issue `hormuz-2y7.8`.
