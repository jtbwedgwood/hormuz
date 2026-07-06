---
id: "hormuz-fyp.5"
title: "Create Hormuz commodity taxonomy"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-fyp"
labels:
  - "commodities"
  - "foundation"
  - "research-design"
  - "taxonomy"
blocked_by: []
blocks:
  - "hormuz-2y7.3"
  - "hormuz-f6r.1"
  - "hormuz-kmz.1"
  - "hormuz-kmz.4"
  - "hormuz-s49.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:17Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Create Hormuz commodity taxonomy

## Description

Define the product universe moving through Hormuz: crude oil, condensate, refined products, LNG, LPG, petrochemicals, sulfur, fertilizers/ammonia/urea, metals/minerals, food or containerized categories if material.

## Acceptance Criteria

Taxonomy includes units, likely vessels, exporters, importers, candidate data sources, and inclusion/exclusion rationale.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-2y7.3` - Map vessel classes to commodity categories
- Blocks: `hormuz-f6r.1` - Build importer exposure matrix
- Blocks: `hormuz-kmz.1` - Estimate normal Hormuz export flows by country and product
- Blocks: `hormuz-kmz.4` - Investigate non-obvious disrupted products
- Blocks: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass commodity taxonomy to subagent Dewey.
- 2026-07-06 subagent pass: added concise commodity taxonomy in `docs/foundation-data-inventory.md`.
  - Included core categories: crude/condensate, refined products, LNG, LPG/NGLs, urea/ammonia, phosphate fertilizers, sulphur, petrochemicals/methanol, aluminium, containers/general cargo.
  - Key source breadcrumbs: EIA Hormuz oil and LNG notes; IEA Middle East/Hormuz topic page; IFASTAT; WITS/Comtrade HS 250310; QAFCO capacity page; OECD Ecoscope beyond-energy note.
  - Important sourced anchors: EIA estimates 2024 Hormuz oil flows at about 20 mb/d and about 20% of global petroleum liquids consumption; EIA estimates about 20% of global LNG trade through Hormuz in 2024; IEA flags more than 30% of global urea trade, about 20% of ammonia/phosphate trade, about 5 Mt/y aluminium, and around half of global seaborne sulphur trade moving through Hormuz.
