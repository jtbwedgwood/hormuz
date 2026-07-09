---
id: "hormuz-ccx.7"
title: "Produce supplier-side cushioning diagram"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-ccx"
labels:
  - "figures"
  - "supply"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "codex"
created_at: "2026-07-06T00:00:00Z"
updated_at: "2026-07-07T00:00:00Z"
---

# Produce supplier-side cushioning diagram

## Description

Create a supplier-side analogue to the demand-side cushioning diagram, showing how Saudi Arabia, UAE, Iraq, Qatar, Kuwait, and other exporters absorb the shock through bypass pipelines, shut-ins, storage, delayed cargoes, rerouting, price gains, and unreplaced losses.

## Acceptance Criteria

- Diagram uses the same visual grammar as the importer cushioning figure where practical.
- Supplier countries are grouped by adjustment mechanism and commodity.
- Source footnotes distinguish observed route capacity from modeled disruption and inferred shut-in/delay.

## Work Notes

- 2026-07-06: Filed from follow-up synthesis. Existing data support a rough table, but a publishable diagram needs explicit design and data preparation.
- 2026-07-07: Claimed for figure production. Plan is to use `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv` for modeled low/base/high disruption rows, and `hormuz-kmz.2` route-capacity notes for the separate observed/infrastructure bypass anchors.
- 2026-07-07: Produced `figures/fig-ccx-supplier-side-cushioning.svg`, `figures/fig-ccx-supplier-side-cushioning-data.csv`, and reproducible builder `scripts/build_ccx_supplier_side_cushioning.py`.
- 2026-07-07: Design choice: bars compare base disrupted share of each row's normal exposed baseline rather than additive volumes, because the rows mix `mb/d`, `Bcf/d`, and `Mt/year`. The CSV keeps units and double-counting notes explicit.
- 2026-07-07: Source/evidence split used in the figure: top callouts are observed or reported infrastructure/route-capacity anchors from `hormuz-kmz.2`; bar values are modeled base-case disruptions from `hormuz-kmz.3`; shut-in/delay/reroute labels are inferred from route constraints and traffic severity, not cargo-level manifests.
- 2026-07-07: Main sources carried through from upstream issue files: EIA/Vortexa Hormuz oil/LNG baseline figure data; IEA/EIA Hormuz and Middle East market notes; Aramco/ADNOC/operator route-capacity evidence via `hormuz-kmz.2`; WITS/UN Comtrade, USGS, and QAFCO for fertilizer/sulphur/aluminium baselines.
- 2026-07-07: Validation run: `.venv/bin/python scripts/build_ccx_supplier_side_cushioning.py`; rendered with headless Chrome at 1440x1180 to `/tmp/fig-ccx-supplier-side-cushioning.png` and visually checked for professional readability, label clipping, and legend/axis overlap.
