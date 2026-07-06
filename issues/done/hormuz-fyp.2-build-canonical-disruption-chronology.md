---
id: "hormuz-fyp.2"
title: "Build canonical disruption chronology"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-fyp"
labels:
  - "events"
  - "foundation"
  - "research-design"
  - "timeline"
blocked_by: []
blocks:
  - "hormuz-2y7.5"
  - "hormuz-4j7.3"
  - "hormuz-f6r.5"
  - "hormuz-kmz.3"
  - "hormuz-kmz.5"
  - "hormuz-l8m.1"
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:13Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Build canonical disruption chronology

## Description

Create a bead-backed chronology of closure/disruption events, policy announcements, attacks, rerouting advisories, and market-relevant timestamps using absolute dates and UTC/local time where material.

## Acceptance Criteria

Chronology covers pre-shock baseline, onset, escalation/de-escalation, and current status; each event has citations and confidence level.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-2y7.5` - Validate transit counts against external benchmarks
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Blocks: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocks: `hormuz-kmz.5` - Quantify freight, insurance, and war-risk disruption
- Blocks: `hormuz-l8m.1` - Define commodity price shock scenarios
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass current chronology and source search to subagent Mendel.
- 2026-07-06T07:10Z: Subagent pass produced canonical chronology in `docs/foundation-chronology-and-scenarios.md`. Core sources: EIA Today in Energy/STEO, UKMTO/JMIC advisories, AP, CFR, Guardian, WSJ. Main uncertainty: daily traffic and route shares require AIS/vendor validation.
