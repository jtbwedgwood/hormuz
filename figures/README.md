# Figure Notes

Last updated: 2026-07-06.

This directory contains blog-candidate SVG figures plus machine-readable figure data where available. The SVGs are intentionally kept light on caveats; use this README as the common interpretation layer.

## Shared Caveats

- Public PortWatch traffic counts are not cargo manifests. They support transit-count and broad vessel-class claims, not exact barrels, cargo contents, destinations, or AIS-dark movements.
- EIA/Vortexa Hormuz oil and LNG figure data provide separate origin totals and destination totals. The Sankey diagrams are origin -> Hormuz -> destination summaries, not country-pair cargo matching.
- Scenario figures are not realized-loss accounting. Current Hormuz disruption rows combine observed baselines, modeled low/base/high assumptions, and source confidence flags.
- Product rows are not additive. Crude, refined products, LPG/NGL, petrochemicals, fertilizer inputs, sulphur, aluminium, and freight/insurance channels overlap.
- Route/logistics shocks and physical supply outages are different. Historical comparison scores keep them visible together, but they should not be read as one mechanical barrel-equivalent table.
- Low-confidence or proxy rows are kept because they are useful for synthesis, but final blog claims should foreground high and medium-confidence values.

## Figures

| Figure | Main Use | Key Caveat |
|---|---|---|
| `fig-2y7-public-hormuz-daily-transits.svg` | Daily public Strait of Hormuz transit tracker. | Counts broad chokepoint calls, not cargoes or vessel identities. |
| `fig-kmz-oil-hormuz-baseline-sankey.svg` | 2024 crude/condensate origin and destination baseline through Hormuz. | Origin and destination totals are separate EIA aggregates, not pairwise cargo routes. |
| `fig-kmz-lng-hormuz-baseline-sankey.svg` | 2024 LNG origin and destination baseline through Hormuz. | Same origin/destination caveat; Qatar dominates exports, but exact Qatar-to-importer pairings are not public in this figure data. |
| `fig-f6r-crude-importer-adjustment.svg` | Base-case importer adjustment buckets for direct crude/product exposure. | Scenario bridge estimates, not cargo-by-cargo replacement accounting. |
| `fig-4j7-historical-shock-comparison.svg` | Historical comparison matrix and current Hormuz product ranking. | Scores are rubric-based and provisional where duration or price response is missing. |
| `hormuz-l8m-6-sector-exposure-pass-through-bands.svg` | U.S. sector cost exposure bands. | Direct-energy scenario band, not a final BEA input-output estimate. |
| `hormuz-l8m-6-ai-electricity-cost-sensitivity.svg` | AI electricity-only cost-per-token sensitivity. | Electricity-only; excludes GPU capex, networking, storage, labor, utilization, and margin. |

## Source Pattern

Every final blog figure should trace to either a figure-data CSV in this directory or a derived data file listed in `data/manifest.csv`. The visible source line on each SVG is intentionally short; use the issue files and docs for full source trails.

Primary source families used here:

- EIA Today in Energy Hormuz oil and LNG figure data, based on Vortexa.
- IMF PortWatch daily chokepoint data.
- Project derived tables from RQ2, RQ3, RQ5, and RQ6.
- EIA MECS and project scenario tables for U.S. cost sensitivity.

The LNG Sankey groups the small non-Qatar/UAE origin rows from the EIA workbook into `Other origins` for readability. The companion CSV preserves the grouped value and source URL.
