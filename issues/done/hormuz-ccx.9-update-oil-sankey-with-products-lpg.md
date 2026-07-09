---
id: "hormuz-ccx.9"
title: "Update oil-through-Hormuz diagram with refined products and LPG split"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-ccx"
labels:
  - "figures"
  - "oil"
  - "products"
  - "blog"
blocked_by: []
blocks: []
children: []
owner: "codex"
created_at: "2026-07-09T00:00:00Z"
updated_at: "2026-07-09T00:00:00Z"
---

# Update oil-through-Hormuz diagram with refined products and LPG split

## Description

Revise the 2024 oil flow Sankey so it shows crude/condensate plus refined products/LPG in one diagram, with each origin band split visually by product category where the data support it.

## Acceptance Criteria

- Existing oil Sankey generator remains reproducible.
- Figure data CSV records the crude/condensate and refined/LPG components with source URLs and caveats.
- SVG clearly distinguishes crude/condensate from refined/LPG while retaining country origin and destination context.
- Source and uncertainty notes are captured here and in figure documentation where needed.

## Work Notes

- 2026-07-09: Created issue for user-requested figure update.
- 2026-07-09: Updated `scripts/build_hormuz_baseline_sankeys.py` so the oil Sankey now combines EIA/Vortexa fig3 crude/condensate origin and destination totals with EIA fig1's 2024 aggregate petroleum-products total. The generated figure reconciles to 20.261742 mb/d, split into 14.318614 mb/d crude/condensate and 5.943128 mb/d refined products/LPG.
- 2026-07-09: Product/LPG country-origin split is intentionally marked as indicative. It uses country product-export proxies from `hormuz-kmz.1` for Saudi Arabia, UAE, Iraq, Qatar, and Iran, with Kuwait as the residual needed to reconcile to EIA's aggregate petroleum-products route total. The public EIA workbook does not provide product destinations, so the right side groups products into a single "destination split not public" node.
- 2026-07-09: Regenerated `figures/fig-kmz-oil-hormuz-baseline-sankey.svg` and companion CSV. Rendered the SVG via `sips` to `/tmp/oil-sankey-sips.png` for visual QA; labels and hatching are readable. Updated `figures/README.md` and `data/manifest.csv` caveats.

### Source Breadcrumbs

- EIA Today in Energy article: `https://www.eia.gov/todayinenergy/detail.php?id=65504`
- EIA fig1 aggregate oil/products workbook: `https://www.eia.gov/todayinenergy/images/2025.06.16/fig1.xlsx`
- EIA fig3 crude/condensate origin and destination workbook: `https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx`
- Product proxy notes: `issues/done/hormuz-kmz.1-estimate-normal-hormuz-export-flows-by-country-and-product.md`
