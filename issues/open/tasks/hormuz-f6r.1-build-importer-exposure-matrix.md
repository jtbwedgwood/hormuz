---
id: "hormuz-f6r.1"
title: "Build importer exposure matrix"
type: "task"
status: "open"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "importers"
  - "tradeflows"
blocked_by:
  - "hormuz-fyp.1"
  - "hormuz-fyp.5"
  - "hormuz-kmz.1"
blocks:
  - "hormuz-f6r.2"
  - "hormuz-f6r.3"
  - "hormuz-f6r.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:42Z"
updated_at: "2026-07-06T06:09:42Z"
---

# Build importer exposure matrix

## Description

For each major Hormuz-linked product, identify top destination countries and regions before the disruption and their dependence on affected flows.

## Acceptance Criteria

Matrix includes product, exporter, importer, volume/value, share of importer demand, baseline period, and source confidence.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Blocked by: `hormuz-kmz.1` - Estimate normal Hormuz export flows by country and product
- Blocks: `hormuz-f6r.2` - Analyze China exposure and substitution behavior
- Blocks: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Blocks: `hormuz-f6r.4` - Assess Europe and Mediterranean exposure

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.
