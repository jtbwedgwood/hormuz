---
id: "hormuz-fyp.4"
title: "Set up reproducible data inventory structure"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-fyp"
labels:
  - "data"
  - "foundation"
  - "reproducibility"
  - "research-design"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:16Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Set up reproducible data inventory structure

## Description

Specify lightweight directories or manifests for raw data, derived data, notebooks/scripts, chart outputs, and source notes without creating unnecessary narrative docs.

## Acceptance Criteria

Data inventory approach is clear; filenames and provenance fields are standardized; sensitive or licensed data handling is noted.

## Dependency Notes

- Parent: `hormuz-fyp` - Foundation: shared research infrastructure and assumptions

## Work Notes

- 2026-07-06T06:23Z: Claimed under `hormuz-fyp`; delegated first-pass inventory structure to subagent Dewey.
- 2026-07-06 subagent pass: added implementation-ready scheme in `docs/foundation-data-inventory.md`.
  - Proposed paths: `data/raw/{source}/{dataset}/{YYYY-MM-DD}/`, `data/interim/`, `data/derived/`, `notebooks/`, `scripts/`, `outputs/figures/`, `data/manifests/sources.yaml`, `data/manifests/series.yaml`.
  - Required provenance fields cover source URL/type, access/license/redistribution, vintage/frequency, geography/commodity/units, transform/checksum/schema, quality tier, limitations, and citation.
  - Handling rule: do not commit raw subscription exports from AIS/Kpler/Vortexa/Argus/Platts/ICIS/Clarksons/Lloyd's List unless redistribution is allowed; commit manifests and reproducible transforms.
- 2026-07-06 closeout: integrated convention uses committed top-level `data/raw/`, `data/external/`, `data/derived/`, `notebooks/`, `scripts/`, and `figures/` plus `data/manifest.csv`.
