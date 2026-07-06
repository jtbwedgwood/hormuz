---
id: "hormuz-fyp.7"
title: "Define chart and map standards for the project"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-fyp"
labels:
  - "design"
  - "foundation"
  - "research-design"
  - "visuals"
blocked_by: []
blocks:
  - "hormuz-2y7.7"
  - "hormuz-4j7.5"
  - "hormuz-ccx.3"
  - "hormuz-f6r.6"
  - "hormuz-l8m.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:20Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Define chart and map standards for the project

## Description

Set standards for chart reproducibility, uncertainty display, map projections/labels, and visual audit so final outputs are consistent and defensible.

## Acceptance Criteria

Standards cover chart source footnotes, confidence bands, missing-data treatment, and export formats for blog use.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions
- Blocks: `hormuz-2y7.7` - Produce tracker dataset and publication chart
- Blocks: `hormuz-4j7.5` - Produce historical comparison graphic
- Blocks: `hormuz-ccx.3` - Assemble final figure package
- Blocks: `hormuz-f6r.6` - Produce destination flow map and exposure chart
- Blocks: `hormuz-l8m.6` - Produce US business and AI cost visuals

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass chart/map standards to subagent Nash.
- 2026-07-06: Added chart/map standards to `docs/foundation-research-standards.md`.
- Key decisions: require figure metadata and source footnotes; display uncertainty with labeled bands/ranges and non-color encodings; preserve missing observations as gaps unless justified; footnote AIS/shadow-fleet/reporting/classification blind spots; use Natural Earth basemaps for general context; export PNG at 2x blog width plus SVG/PDF where reliable and machine-readable figure data alongside figures.
- Source anchors used: IPCC uncertainty guidance, Datawrapper accessibility/colorblind guidance, Natural Earth public-domain map data and terms.
