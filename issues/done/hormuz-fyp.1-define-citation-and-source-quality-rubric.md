---
id: "hormuz-fyp.1"
title: "Define citation and source-quality rubric"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-fyp"
labels:
  - "citations"
  - "foundation"
  - "research-design"
  - "sources"
blocked_by: []
blocks:
  - "hormuz-2y7.1"
  - "hormuz-2y7.2"
  - "hormuz-2y7.3"
  - "hormuz-2y7.5"
  - "hormuz-4j7.1"
  - "hormuz-4j7.2"
  - "hormuz-ccx.1"
  - "hormuz-f6r.1"
  - "hormuz-kmz.1"
  - "hormuz-kmz.2"
  - "hormuz-kmz.4"
  - "hormuz-l8m.1"
  - "hormuz-s49.1"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:12Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Define citation and source-quality rubric

## Description

Create a project-wide rubric for official statistics, AIS providers, commercial reports, news claims, satellite imagery, and analyst estimates. Include how to cite, archive, and rank confidence.

## Acceptance Criteria

Rubric includes source tiers, recency rules, citation fields, archival expectations, and handling of paywalled or unverifiable claims.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-2y7.1` - Evaluate AIS and vessel-position data sources
- Blocks: `hormuz-2y7.2` - Define Strait of Hormuz transit geofence and counting rules
- Blocks: `hormuz-2y7.3` - Map vessel classes to commodity categories
- Blocks: `hormuz-2y7.5` - Validate transit counts against external benchmarks
- Blocks: `hormuz-4j7.1` - Select historical shock comparison cases
- Blocks: `hormuz-4j7.2` - Define normalized comparison metrics
- Blocks: `hormuz-ccx.1` - Maintain claim register with confidence levels
- Blocks: `hormuz-f6r.1` - Build importer exposure matrix
- Blocks: `hormuz-kmz.1` - Estimate normal Hormuz export flows by country and product
- Blocks: `hormuz-kmz.2` - Map bypass routes and non-Hormuz export capacity
- Blocks: `hormuz-kmz.4` - Investigate non-obvious disrupted products
- Blocks: `hormuz-l8m.1` - Define commodity price shock scenarios
- Blocks: `hormuz-s49.1` - Inventory reserve and stockpile data sources

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass source/citation rubric to subagent Nash for parallel research.
- 2026-07-06: Added project-wide source-quality and citation standards to `docs/foundation-research-standards.md`.
- Key decisions: tier sources from primary official/operational data through transparent institutional analysis, commercial estimates, reputable news, and unverified leads; require citation fields for claim/figure ID, source, title/dataset, release/access date, URL/DOI/archive, version/query/geography/units, transformations, confidence, and access/paywall status; label confidence as `high`, `medium`, `low`, or `speculative`.
- Source anchors used: EIA chokepoint/Hormuz pages, DataCite Metadata Schema, NOAA Data Citation Procedural Directive, Internet Archive Wayback guidance, Reuters Trust Principles and standards, IPCC uncertainty guidance.
