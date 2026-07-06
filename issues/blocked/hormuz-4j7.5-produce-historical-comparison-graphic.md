---
id: "hormuz-4j7.5"
title: "Produce historical comparison graphic"
type: "task"
status: "blocked"
priority: "P2"
parent: "hormuz-4j7"
labels:
  - "comparisons"
  - "history"
  - "visuals"
blocked_by:
  - "hormuz-4j7.4"
  - "hormuz-4j7.3"
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:13Z"
updated_at: "2026-07-06T09:30:00Z"
---

# Produce historical comparison graphic

## Description

Create a chart that compares the current Hormuz disruption to selected historical shocks using normalized metrics.

## Acceptance Criteria

Graphic is publication-ready and includes caveats for non-comparable dimensions.

## Dependency Notes

- Parent: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Blocked by: `hormuz-4j7.4` - Rank current Hormuz shock against historical analogues
- Blocked by: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Cleared dependency: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Cleared dependency: `hormuz-fyp.7` - Define chart and map standards for the project
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline
- Blocks: `hormuz-ccx.3` - Assemble final figure package

## Work Notes

- 2026-07-06T06:32Z: Moved to `issues/blocked/`. This task should remain blocked until `hormuz-4j7.4` produces the multi-dimensional ranking and `hormuz-fyp.7` chart standards are applied to a real figure dataset. No graphic should be produced from placeholder values.
- 2026-07-06T09:30Z: Advanced the publication figure specification without generating a placeholder chart. `hormuz-fyp.7` is now done and its chart standards can be applied, but this issue must remain blocked until `hormuz-4j7.4` ranks the current Hormuz shock using real historical/current data. The real-data blocker is currently `hormuz-4j7.3` for historical supply/price/inventory/demand fields and buffer-duration values.

### Publication-Ready Figure Concept

Working title: **How Hormuz differs from earlier oil shocks**.

Core form: one wide, blog-ready comparison matrix with small horizontal range bars, not a single barrel-loss ranking. Rows are selected events from `hormuz-4j7.1`; columns are normalized dimensions from `hormuz-4j7.2`. The intended first-release row set is: 1973-74 Arab oil embargo, 1978-79 Iranian Revolution, 1980 Iran-Iraq War outbreak, 1990 Iraq/Kuwait, 2011 Libya, 2019 Abqaiq-Khurais, 2022 Russia/Ukraine sanctions/buyer strike, and Current Hormuz. Add a separate lower "route/logistics analogues" band for 1956 Suez, 1967 Suez closure, Tanker War, and 2021 Ever Given only if their fields can be coded as route/disruption metrics rather than oil supply-loss metrics.

Recommended dimensions:

- Desktop master: 1600 x 1000 px PNG at 2x blog width, plus SVG/PDF if labels render cleanly.
- Mobile derivative: 900 x 1400 px, split into two stacked panels if needed.
- Minimum reproducible outputs once unblocked: `figures/fig-XX-historical-shock-comparison-YYYY-MM-DD.{png,svg}` plus `figures/fig-XX-historical-shock-comparison-data.csv`.

### Required Data Fields

Minimum event fields:

| field | purpose |
| --- | --- |
| `case_id`, `case_name`, `case_group`, `start_date`, `end_date`, `duration_days` | Stable identity, ordering, and route/supply grouping. |
| `shock_type` | Producer outage, embargo/allocation, chokepoint closure, infrastructure attack, sanctions/rerouting, logistics obstruction. |
| `commodity_scope` | Oil, oil products, LNG/gas, shipping/logistics, fertilizer/input minerals, or mixed. |
| `baseline_window`, `event_window`, `latest_observation_date` | Prevents hidden denominator/window shifts. |
| `exposed_flow_native`, `realized_disrupted_flow_native`, `rerouted_or_delayed_flow_native`, `unit` | Separates at-risk flow from confirmed loss and logistics adjustment. |
| `disrupted_share_global_pct`, `disrupted_share_relevant_trade_pct` | Normalized exposure; use both when global supply and seaborne trade tell different stories. |
| `disruption_intensity_pct_days` | Depth multiplied by persistence. |
| `spare_capacity_buffer_ratio`, `inventory_cover_days`, `strategic_stock_response_pct_of_disruption` | Buffer and policy context. |
| `route_substitution_score`, `extra_voyage_days_or_cost_pct` | Rerouting/substitution constraint, especially for Hormuz, Suez, Tanker War, and Russia 2022. |
| `peak_real_price_change_pct`, `avg_event_real_price_change_pct` | Market response in real percentage terms, not nominal prices. |
| `product_breadth_score`, `non_oil_material_flags` | Hormuz-specific multi-commodity breadth: LNG, LPG/NGLs, sulphur, aluminium, urea/ammonia, petrochemicals, freight/war risk. |
| `low_estimate`, `central_estimate`, `high_estimate`, `confidence`, `main_sources`, `known_biases` | Uncertainty and auditability. |

Current-Hormuz rows should ingest RQ2 product breadth rather than collapse everything into an oil-equivalent number. At minimum, the current row needs separate flags/fields for crude/condensate, refined products, LNG, LPG/NGLs, sulphur, aluminium, fertilizer/ammonia/urea, petrochemicals/plastics, and shipping/insurance. `hormuz-kmz.1`, `hormuz-kmz.4`, and `hormuz-kmz.7` provide the product universe and baseline anchors; `hormuz-kmz.3` still needs to provide the de-duplicated low/base/high disrupted or delayed supply values.

### Encoding

- Row order: primary oil/energy shocks by event date or by final `hormuz-4j7.4` rank; keep route/logistics analogues in a visually separated section.
- Columns:
  - `Disrupted share`: horizontal range bar in percent of relevant global supply/trade, with a central dot when available.
  - `Duration/intensity`: compact range bar or lollipop for percent-days; log scale only if values span too widely and the subtitle says so.
  - `Buffers`: paired glyphs for spare-capacity buffer and inventory/stock cover, labeled in ratios/days.
  - `Route constraint`: categorical marker with direct label: low, medium, high, extreme.
  - `Price response`: horizontal range bar for real peak/average percent price change.
  - `Product breadth`: small labeled chips or tick marks for oil, products, LNG, LPG, fertilizer/chemicals, metals/minerals, and shipping/insurance.
- Use direct labels and symbols in addition to color. Use hatching or hollow markers for low-confidence/proxy values. Leave cells blank or marked `n/a` when the metric is not meaningful rather than forcing false comparability.
- Quantitative bar axes should start at zero. If using a log or indexed panel for duration/intensity, label it explicitly and keep raw values in the figure CSV.

### Caveats and Uncertainty Treatment

- Do not plot nominal barrels alone. Barrel counts must be normalized by the event's market size, duration, available spare capacity, inventory cover, stock-release response, route substitutability, and price response.
- Separate `exposed`, `realized disrupted`, `rerouted`, and `delayed` flows. A Suez-style route closure, Tanker War risk premium, Russia-style sanctions rerouting, and Abqaiq-style short physical outage are not the same kind of shock.
- Do not sum RQ2 current-Hormuz product rows. Crude, refined products, LPG/NGLs, petrochemicals, ammonia, urea, MAP/DAP, sulphur, and freight/insurance channels overlap through feedstock and production chains.
- Treat LNG and fertilizer/industrial inputs in native units where possible. If an editorial oil-equivalent sensitivity is later added, it should be an appendix or faint secondary annotation, not the visual ranking basis.
- Show uncertainty as source ranges or low/base/high scenario ranges. Label the range type in the legend or directly in the column header. Missing values remain missing; they are not zeros.
- Confidence: use `high/medium/low` from `docs/foundation-research-standards.md`; display low confidence with hollow markers or a dagger note, not only with color.

### Source Footnote Pattern

Figure caption/footnote template:

`Source: IEA major oil supply disruption and emergency response publications; EIA country/chokepoint briefs and price/flow data; World Bank/IMF commodity prices; UNCTAD/Clarksons/Drewry/Lloyd's List where used for freight and route metrics; UN Comtrade/IFASTAT/USGS/company reports for non-oil Hormuz product baselines; calculations by author. Live or changing pages accessed YYYY-MM-DD.`

For the final chart, every plotted value must trace to either a manifest-listed data file or an issue-note source breadcrumb. Central quantitative claims need Tier A support or two independent lower-tier sources per `docs/foundation-research-standards.md`.

### Why This Avoids Naive Barrel-Only Comparisons

The figure treats `mb/d lost` as one input, not the answer. It compares shocks across:

- scale: disrupted share of global or relevant seaborne trade;
- persistence: duration and disruption intensity;
- buffers: spare capacity, inventories, and strategic stock releases;
- substitutability: rerouting, grade/contract constraints, and bypass capacity;
- market response: real price changes and freight/insurance costs;
- breadth: Hormuz's oil, LNG, LPG, sulphur, aluminium, fertilizer, petrochemical, and shipping channels.

This framing lets a short 5.7 mb/d Abqaiq outage, a long sanctions/rerouting shock, a Suez logistics obstruction, and a multi-product Hormuz disruption appear different in the ways that actually drive economic impact. It also prevents the current shock from being reduced to a misleading "how many barrels?" headline when RQ2 shows that LNG, LPG/NGLs, sulphur, aluminium, fertilizer inputs, petrochemicals, and freight/war-risk costs are part of the exposure story.

### Source Breadcrumbs Read for This Spec

- `hormuz-4j7.1`: selected historical comparison cases and split core oil/energy shocks from route/shipping analogues.
- `hormuz-4j7.2`: normalized metric framework, required data fields, and methodological cautions about production loss versus transit exposure.
- `hormuz-fyp.7` and `docs/foundation-research-standards.md`: chart metadata, source footnote, uncertainty, missing-data, accessibility, and export standards.
- `hormuz-kmz.1`: current Hormuz baseline export/product fields, including 2024 oil flow, LNG, fertilizer, sulphur, aluminium, and double-counting warnings.
- `hormuz-kmz.4`: non-obvious disrupted products; strongest publication leads are sulphur, aluminium, LPG/naphtha, petrochemicals, and shipping services.
- `hormuz-kmz.7`: preliminary product disruption master-table schema and non-additivity warning.
