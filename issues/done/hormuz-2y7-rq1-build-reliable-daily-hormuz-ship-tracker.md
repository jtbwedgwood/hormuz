---
id: "hormuz-2y7"
title: "RQ1: Build reliable daily Hormuz ship tracker"
type: "epic"
status: "done"
priority: "P0"
parent: null
labels:
  - "ais"
  - "shipping"
  - "tracker"
blocked_by:
  - "hormuz-fyp"
blocks:
  - "hormuz-ccx"
  - "hormuz-kmz"
children:
  - "hormuz-2y7.1"
  - "hormuz-2y7.2"
  - "hormuz-2y7.3"
  - "hormuz-2y7.4"
  - "hormuz-2y7.5"
  - "hormuz-2y7.6"
  - "hormuz-2y7.7"
  - "hormuz-2y7.8"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:05Z"
updated_at: "2026-07-06T16:00:00Z"
---

# RQ1: Build reliable daily Hormuz ship tracker

## Description

Determine whether a reliable daily tracker of Strait of Hormuz vessel transits can be produced with historical data, including coverage limits, vessel class definitions, and validation against external counts.

## Acceptance Criteria

Daily transit methodology is specified; candidate data sources are evaluated; reproducible count pipeline and validation plan are defined; uncertainty bands and known gaps are explicit.

## Dependency Notes

- Blocked by: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-ccx` - Synthesis: blog-ready argument, visuals, and uncertainty
- Blocks: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Child: `hormuz-2y7.1` - Evaluate AIS and vessel-position data sources
- Child: `hormuz-2y7.2` - Define Strait of Hormuz transit geofence and counting rules
- Child: `hormuz-2y7.3` - Map vessel classes to commodity categories
- Child: `hormuz-2y7.4` - Prototype daily transit count pipeline
- Child: `hormuz-2y7.5` - Validate transit counts against external benchmarks
- Child: `hormuz-2y7.6` - Backfill historical traffic series around prior shocks
- Child: `hormuz-2y7.7` - Produce tracker dataset and publication chart

## Work Notes

- 2026-07-06: Claimed early despite formal `hormuz-fyp` prerequisite, per user instruction. Treat `hormuz-fyp.1` citation/source rubric, `hormuz-fyp.3` baselines, `hormuz-fyp.5` taxonomy, and `hormuz-fyp.7` chart standards as provisional dependencies unless they materially affect a decision.
- 2026-07-06: Parallelized first-pass research for `hormuz-2y7.1` data sources, `hormuz-2y7.2` geofence/counting rules, and `hormuz-2y7.3` vessel class mapping. Local work focuses on claim/setup, pipeline skeleton, and blocker triage.
- 2026-07-06: Added validation/backfill research. Key finding: IMF PortWatch appears to provide the most useful public daily Hormuz benchmark from 2019 onward, including total and tanker transit calls and a 48-hour repeat threshold. This materially reduces the risk that the project must rely only on paid AIS for a blog-worthy daily tracker.
- 2026-07-06: KMZ support pass completed `hormuz-2y7.5` using the PortWatch fetch/public tracker outputs already produced in this workstream. This was coordinated as support, not a takeover of `hormuz-2y7.4` pipeline ownership. Remaining KMZ need is product/country supply allocation, not aggregate count validation.
- 2026-07-06: User decision: do not spend $200+ on commercial ship-tracker data for a blog post. Public-only deliverable is now the project default.
- Public-only answer: we can make a credible daily Hormuz traffic tracker using IMF PortWatch chokepoint calls from 2019-01-01 through the current public lag. Known: daily calls by broad class (`n_total`, `n_tanker`, container, dry bulk, etc.) and estimated metric-ton capacity. Unknown without paid/raw AIS: vessel identities, direction, exact gate-crossing tracks, AIS-dark movements, and actual cargo onboard.
- Outputs produced: `data/derived/hormuz_2y7_public_daily_tracker.csv`, `figures/fig-2y7-public-hormuz-daily-transits.svg`, and `figures/fig-2y7-public-hormuz-daily-transits.csv`.
- Added blocked child `hormuz-2y7.8` for paid/raw vessel-level AIS reconstruction, so the public tracker can advance without pretending that vessel-level questions are solved.
- 2026-07-06 closeout: Epic completed for public-only blog scope. Child tasks `hormuz-2y7.1` through `hormuz-2y7.7` are done; `hormuz-2y7.8` was moved to `issues/deferred/` because paid/raw AIS reconstruction is explicitly out of scope. User-facing summary is `docs/hormuz-ship-tracker.md`.
