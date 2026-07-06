---
id: "hormuz-4j7.4"
title: "Rank current Hormuz shock against historical analogues"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-4j7"
labels:
  - "analysis"
  - "comparisons"
  - "history"
blocked_by: []
blocks:
  - "hormuz-4j7.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:12Z"
updated_at: "2026-07-06T19:25:00Z"
---

# Rank current Hormuz shock against historical analogues

## Description

Analyze where the current disruption sits relative to prior shocks on severity, duration, substitutability, and macro vulnerability.

## Acceptance Criteria

Ranking is multi-dimensional, transparent, and includes at least one counterintuitive or eye-catching result if supported.

## Dependency Notes

- Parent: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Cleared dependency: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-4j7.5` - Produce historical comparison graphic

## Work Notes

- 2026-07-06T06:32Z: Moved to `issues/blocked/`. This task cannot be done rigorously until `hormuz-4j7.3` produces the cited historical/current metric dataset. Future ranking should wait for normalized metrics, supply/price/inventory/demand data, and RQ1/RQ2/RQ4/RQ5 inputs rather than making qualitative claims from partial evidence.
- 2026-07-06T18:25Z: Advanced blocked task without producing a final ranking. Reviewed `hormuz-4j7.1`, `hormuz-4j7.2`, `hormuz-kmz.6`, `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`, `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`, `data/derived/hormuz_2y7_public_daily_tracker.csv`, and `data/manifest.csv`. This note defines the ranking rubric, candidate hypotheses, and exact data fields needed from `hormuz-4j7.3`. Status remains `blocked` because the normalized historical/current dataset is still missing.
- 2026-07-06T19:10Z: Unblocked after `hormuz-4j7.3` produced `data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv`. Claimed for ranking analysis. Use the panel as the authoritative input for first-pass scoring, not the older template or partial blocker notes.
- 2026-07-06T19:25Z: Completed first-pass ranking tables: `data/derived/hormuz_4j7_4_case_ranking_scores.csv` (170 rows, 20 columns) and `data/derived/hormuz_4j7_4_hormuz_product_ranking_scores.csv` (90 rows, 20 columns). Both parse cleanly. Main supported finding: current Hormuz is not the top crude/oil analogue once oil buffers and partial bypass are included, but LPG/NGL, LNG, and sulphur rank above the crude/oil aggregate because the public panel supports weaker route substitution, thinner replacement options, and less observable buffer cover for those channels.

### Ranking Rubric Draft

Do not rank cases by peak barrels alone. Use a two-layer score: a transparent quantitative score for cases with comparable data, plus qualitative flags where historical data are structurally weaker. Each score should be shown by dimension, not only as a single total, because the current Hormuz shock may rank differently for oil, LNG, fertilizer, and shipping.

Recommended scoring scale for each dimension: `0` = not material or not applicable, `1` = limited, `2` = meaningful but bufferable, `3` = severe, `4` = extreme among historical comparators. Use half-points only if the underlying value falls near a threshold. Mark `NA` rather than forcing a score where the case type does not match the metric, e.g. Ever Given for oil supply loss.

Suggested weighting for a headline "system severity" score, to be tested after `hormuz-4j7.3`:

| Dimension | Weight | Score basis | Why it belongs |
|---|---:|---|---|
| `realized_disruption_share` | 18 | Realized lost/delayed/rerouted flow as percent of global supply, consumption, seaborne trade, or relevant product trade | Prevents nominal mb/d from dominating across eras and products. |
| `disruption_intensity` | 14 | Percent-disrupted times days above threshold, with 5%, 10%, and 20% sensitivity thresholds | Separates Abqaiq-style spikes from persistent closures/sanctions. |
| `route_substitution_constraint` | 12 | Percent not practically bypassable or substitutable within 30/60/90 days; include voyage delay and capacity limits | Critical for Hormuz because crude bypass capacity exists, but LNG and some fertilizer inputs have little/no equivalent route. |
| `spare_capacity_buffer` | 10 | Rapid usable spare capacity divided by disrupted flow; use inverse scoring so lower buffer scores higher severity | Avoids overstating disruptions that are offset by deployable supply. |
| `inventory_cover` | 10 | Commercial and strategic days of cover against disrupted flow and normal demand; use inverse scoring | Explains why similar flow losses create different price/macro effects across decades. |
| `strategic_response_offset` | 8 | Actual emergency stock release, demand restraint, or mandated draw as percent of disrupted flow and public stock | Captures policy cushion and credibility of release announcements. |
| `real_price_response` | 12 | Inflation-adjusted peak and event-average price move versus pre-shock baseline; separate crude, products, LNG/gas, fertilizer, freight | Market response is the observable stress signal, but it is confounded by expectations and macro conditions. |
| `duration_recovery_shape` | 6 | Days to trough, partial recovery, full physical recovery, and price normalization; classify as spike/plateau/rolling/regime shift | Prevents long sanctions or closures from being compressed into peak-loss numbers. |
| `geographic_concentration` | 5 | HHI/top-3/top-5 exposure for origins, destinations, routes, and buffers | Concentrated importer exposure can create severe regional stress even when global share looks smaller. |
| `shipping_insurance_channel` | 5 | War-risk premium, freight uplift, demurrage, vessel-days lost, and security/escort friction | Separates a maritime chokepoint shock from ordinary field outages. |

Headline score formula for later use:

`system_severity_score = sum(weight_i * score_i / 4) / sum(applicable_weights)`

Report confidence beside every dimension: `high`, `medium`, `low`. If more than 25% of applicable weight is low-confidence, label the total score `provisional` and avoid precise ordinal claims.

### Matrix Layout for Final Ranking

Build three linked tables once `hormuz-4j7.3` lands:

| Table | Rows | Columns |
|---|---|---|
| `case_dimension_scores` | Current Hormuz plus selected historical cases from `hormuz-4j7.1` | One row per case/dimension/commodity scope; include raw value, score, weight, confidence, source IDs, and caveat. |
| `headline_case_summary` | One row per case | Total applicable score, score range from low/base/high assumptions, highest-scoring dimensions, lowest-confidence dimensions, and one-sentence interpretation. |
| `product_specific_hormuz_scores` | Oil/crude, refined products, LPG/NGL, LNG, sulfur, urea, ammonia, MAP/DAP, aluminum, petrochemicals if data allow | Same dimensions, but scored against product-specific denominators from `hormuz-kmz.6` and `hormuz-kmz.7`, not summed without de-duplication. |

Do not merge supply-loss cases and route/logistics cases mechanically. Suggested display grouping:

- Primary oil supply comparators: 1973-74 embargo, 1978-79 Iranian Revolution, 1980 Iran-Iraq War outbreak, 1990 Iraq/Kuwait, 2011 Libya, 2019 Abqaiq-Khurais, 2022 Russia/Ukraine sanctions/buyer strike.
- Shipping/route comparators: 1956 Suez, 1967-75 Suez closure, 1984-88 Tanker War, 2021 Ever Given/Suez.
- Control/secondary cases: 2002-03 Venezuela, 2003 Iraq/Nigeria/Venezuela compound shock, 2005 Katrina/Rita.

### Candidate Hypotheses to Test Later

These are hypotheses only, not conclusions:

1. Current Hormuz likely ranks higher on `route_substitution_constraint` than most oil-only shocks because LNG, LPG, sulfur, and some fertilizer inputs have weaker bypass options than crude. This follows from `hormuz-kmz.6`: crude can use limited Saudi/UAE bypass capacity, but Qatar/UAE LNG has no practical alternative route and sulfur/fertilizer shares are large.
2. Current Hormuz may rank near the top on `exposed_flow_share` for seaborne energy trade, but its realized-disruption rank depends entirely on `hormuz-4j7.3` and the RQ1/RQ2 tracker/supply estimates. Exposure is not the same as removed supply.
3. Current Hormuz may look less extreme than 1973-74 or 1978-79 on macro vulnerability if inventories, strategic releases, demand response, and lower oil intensity cushion the shock. This requires consistent historical inventory, spare-capacity, and real-price fields.
4. The 2019 Abqaiq attack should be a methodological warning: it may score very high on peak disruption but low on intensity/duration because repair and stock buffers were rapid.
5. 2022 Russia/Ukraine may be the closest modern analogue for rerouting, sanctions, insurance, buyer self-sanctioning, and strategic stock releases, even though the geography and product mix differ.
6. The "eye-catching" result to test is whether Hormuz ranks more severe for LNG/fertilizer/sulfur market tightness than for headline crude once spare capacity, bypass, and inventory cover are included.

### Exact Fields Needed from `hormuz-4j7.3`

Minimum case identity fields:

| Field | Required format / notes |
|---|---|
| `case_id`, `case_name`, `case_group` | Stable IDs matching `hormuz-4j7.1`; group as primary oil, route/shipping, control, or current. |
| `shock_type` | War, embargo, revolution, sanctions/buyer strike, infrastructure attack, labor strike, weather/refining, route blockage, maritime attacks/insurance. |
| `commodity_scope` | Oil liquids, crude/condensate, refined products, LPG/NGL, LNG/gas, fertilizer/input minerals, aluminum, shipping/logistics. |
| `start_date`, `peak_date`, `end_date`, `recovery_90_date`, `recovery_95_date`, `price_normalization_date` | Allow nulls only with explicit caveat. |
| `baseline_window`, `event_window`, `recovery_threshold` | Must be explicit per case; avoid moving denominators. |

Minimum flow and denominator fields:

| Field | Required format / notes |
|---|---|
| `baseline_global_supply`, `baseline_global_demand`, `baseline_seaborne_trade`, `baseline_regional_exports`, `baseline_regional_imports` | Native units plus normalized unit label. |
| `exposed_flow`, `realized_disrupted_flow`, `lost_flow`, `delayed_flow`, `rerouted_flow`, `at_risk_flow` | Keep exposure separate from observed loss/delay. |
| `peak_disrupted_flow`, `avg_disrupted_flow_30d`, `avg_disrupted_flow_90d`, `cumulative_disrupted_volume` | Needed to distinguish peak from persistence. |
| `disrupted_share_global_supply`, `disrupted_share_seaborne_trade`, `disruption_intensity_percent_days` | Prefer computed fields plus source raw inputs. |
| `bypass_capacity_available`, `substitution_capacity_30d`, `substitution_capacity_90d`, `route_delay_days`, `rerouting_distance_nm` | Critical for Suez/Hormuz/Tanker War/Ever Given comparisons. |

Minimum buffer/adjustment fields:

| Field | Required format / notes |
|---|---|
| `spare_capacity_available`, `spare_capacity_activation_days`, `spare_capacity_confidence` | Use usable capacity, not nameplate. |
| `commercial_inventory_days`, `strategic_inventory_days`, `inventory_location_grade_caveat` | Separate commercial and government/strategic stocks. |
| `stock_release_announced`, `stock_release_actual`, `stock_release_rate`, `stock_release_window` | Separate announcement effect from physical draw. |
| `demand_change_actual`, `demand_change_counterfactual`, `short_run_elasticity_assumption` | Needed for demand destruction and macro comparison. |
| `importer_top5_share`, `origin_top5_share`, `destination_hhi`, `origin_hhi` | Geographic concentration and importer vulnerability. |

Minimum price/freight fields:

| Field | Required format / notes |
|---|---|
| `price_benchmark`, `price_unit`, `pre_shock_price_20d`, `pre_shock_price_3m`, `pre_shock_price_12m` | Use real prices for cross-era comparisons. |
| `peak_price_change_nominal_pct`, `peak_price_change_real_pct`, `avg_price_change_real_pct_30d`, `avg_price_change_real_pct_event` | Keep peak and average separate. |
| `price_per_disrupted_share`, `price_per_percent_day` | Diagnostic only, not causal. |
| `freight_benchmark`, `freight_change_pct`, `war_risk_premium_pre`, `war_risk_premium_peak`, `demurrage_or_vessel_days_lost` | Needed for maritime-channel scoring. |

Minimum provenance fields:

| Field | Required format / notes |
|---|---|
| `main_sources`, `source_quality_tier`, `access_date`, `source_url_or_local_path` | Follow `docs/foundation-research-standards.md`. |
| `confidence`, `known_biases`, `calculation_notes` | Required for each raw metric or computed score. |
| `low_case_value`, `base_case_value`, `high_case_value` | Needed where current Hormuz estimates remain scenario-based rather than observed. |

### Preliminary Source Breadcrumbs

- `hormuz-4j7.1`: selected case universe and inclusion rationale.
- `hormuz-4j7.2`: normalized metric framework and recommended data dictionary.
- `hormuz-kmz.6`: current Hormuz product balance denominators: about 20 mb/d total oil/oil products through Hormuz, about 15 mb/d crude, over 110 bcm/year LNG, large urea/ammonia/MAP-DAP/sulfur trade shares, and limited oil bypass capacity.
- `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`: low/base/high current disruption scenario scaffold. Use only as provisional current-case inputs until `hormuz-4j7.3` produces cited normalized fields.
- `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`: product-specific exposure and surprise-value scaffold. Useful for product-specific scoring, but not a historical ranking table.
- `data/derived/hormuz_2y7_public_daily_tracker.csv`: public PortWatch vessel-class tracker with daily calls, tanker counts, capacity proxies, baseline percentages, and explicit cargo-content caveats. Useful for the shipping/traffic score, not sufficient for cargo volumes.
