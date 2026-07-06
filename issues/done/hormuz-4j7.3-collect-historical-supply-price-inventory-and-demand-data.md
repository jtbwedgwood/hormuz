---
id: "hormuz-4j7.3"
title: "Collect historical supply, price, inventory, and demand data"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-4j7"
labels:
  - "comparisons"
  - "data"
  - "history"
blocked_by: []
blocks:
  - "hormuz-4j7.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:10Z"
updated_at: "2026-07-06T19:10:00Z"
---

# Collect historical supply, price, inventory, and demand data

## Description

Gather the data needed to compute normalized metrics for selected historical cases and the current Hormuz event.

## Acceptance Criteria

Dataset has cited values for each metric, with confidence flags and missing-data notes.

## Dependency Notes

- Parent: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Cleared dependency: `hormuz-2y7.6` - Backfill historical traffic series around prior shocks
- Cleared dependency: `hormuz-4j7.2` - Define normalized comparison metrics
- Cleared dependency: `hormuz-fyp.2` - Build canonical disruption chronology
- Cleared dependency: `hormuz-fyp.3` - Define baseline periods and scenario taxonomy
- Cleared dependency: `hormuz-fyp.6` - Inventory market price series and units
- Cleared dependency: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Cleared dependency: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Cleared dependency: `hormuz-l8m.1` - Define commodity price shock scenarios
- Cleared dependency: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product
- Blocks: `hormuz-4j7.4` - Rank current Hormuz shock against historical analogues

## Work Notes

- 2026-07-06T15:30Z: Moved to `issues/blocked/` because the acceptance criterion requires a cited metric dataset, but key upstream inputs are not ready. This note intentionally does **not** claim the dataset is complete; it is a bounded source map and schema proposal for the next pass.
- 2026-07-06T15:55Z: Partial collection plan updated after reading completed `hormuz-4j7.1`, `hormuz-4j7.2`, `hormuz-kmz.6`, `hormuz-kmz.7`, `hormuz-s49.1`, and available derived data. Created `data/derived/hormuz_4j7_metric_collection_template.csv` as a small collection template only; it is **not** completed data and should not be used as a final evidence table.
- 2026-07-06: Refreshed blockers after more upstream work landed. `hormuz-2y7.6` is now done and provides the public historical-traffic availability boundary: daily IMF PortWatch Hormuz traffic is usable from 2019-01-01 onward, while pre-2019 analogues require lower-resolution flow/price/inventory/news/insurance proxies. `hormuz-kmz.3` is now done and provides current-stage low/base/high country-product disruption estimates. `hormuz-l8m.1` is now done and provides low/base/high price-scenario inputs for oil, refined products, gas/electricity, fertilizer, aluminium/metals, freight, and war-risk insurance. `hormuz-s49.2` is done and provides OECD/U.S. reserve-response rows, while `s49.3`-`s49.5` have useful provisional derived tables but are blocked pending importer-adjustment reconciliation. The task remains blocked by stockpile buffer-duration values from `hormuz-s49.6`.

### Current Blockers

| Blocker | Current repo state | What it should contribute before this task can finish |
|---|---:|---|
| No external blocker remains | `done` | Built the cited metric panel using completed RQ1/RQ2/RQ3/RQ4/RQ5 inputs plus historical source collection. |

Cleared inputs now usable in the collection plan: `hormuz-2y7.6`, `hormuz-4j7.2`, `hormuz-fyp.2`, `hormuz-fyp.3`, `hormuz-fyp.6`, `hormuz-kmz.6`, and `hormuz-l8m.1`.

- 2026-07-06: S49 is now complete and `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv` is available. Claimed this task for active historical/current metric collection.
- 2026-07-06T19:10Z: Completed the first cited metric panel for RQ6. Three subagents collected disjoint slices for historical oil shocks, historical route/shipping shocks, and current Hormuz multi-product exposure. Normalized them into `data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv` with 24 rows and 24 columns, preserving source-slice provenance, confidence, source URLs, and caveats. Supporting slice files are `data/derived/hormuz_4j7_3_oil_shock_metric_slice.csv`, `data/derived/hormuz_4j7_3_route_shock_metric_slice.csv`, and `data/derived/hormuz_4j7_3_current_hormuz_metric_slice.csv`. CSV validation passed for all four files. Remaining caveats: historical oil denominators are harmonized enough for ranking but not a definitive total-liquids reconstruction; route shocks are not physical supply-loss analogues; current Hormuz rows are scenario/exposure rows and overlapping product chains should not be summed.

### Partial Collection Plan From Newly Available Inputs

`hormuz-4j7.3` is now ready for a first long-panel collection pass for the current Hormuz case, but not for closure. The historical comparison rows still need source-by-source collection, and several current adjustment channels remain upstream blockers.

| Dataset / issue | Fields that can now be populated | Use in `4j7.3` | Confidence / caveat |
|---|---|---|---|
| `hormuz-4j7.1` | `case_id`, `case_name`, `shock_type`, core/route/control grouping, initial event dates/durations, inclusion rationale, headline affected-supply facts for selected historical cases. | Seed one collection row block per selected case: primary oil shocks, route/shipping shocks, controls, and current Hormuz. | Good for case universe and narrative labels; not enough for normalized denominators or full metric values. |
| `hormuz-4j7.2` | `metric_family`, `metric_name`, metric definitions, units, baseline/event/recovery windows, confidence caveats. | Use as the data dictionary for the collection panel. Priority metrics: `disrupted_share`, `disruption_intensity`, `spare_capacity_buffer`, `inventory_cover`, `strategic_stock_response`, `route_substitution_constraint`, `real_price_response`, `duration_recovery_shape`, `geographic_concentration`, `shipping_insurance_channel`. | Cleared blocker. Keep price and duration metrics separate from physical flow metrics to avoid misleading rankings. |
| `data/derived/hormuz_2y7_public_daily_tracker.csv` | `date`, vessel counts by class, tanker capacity metric tons, 7-day averages, `pct_baseline_total`, `pct_baseline_tanker`, source/confidence note. Coverage: 2,736 daily rows, 2019-01-01 through 2026-06-28. | Populate current Hormuz `traffic` and `route_substitution_constraint` observations at daily frequency; provide baseline-normalized transit intensity and tanker-specific traffic shock indicators. | High for public chokepoint calls; low for cargo contents, direction, dark AIS, and exact commodity mapping. This supports traffic metrics, not barrels removed. |
| `data/external/portwatch/hormuz_daily_chokepoint.csv` | Raw IMF PortWatch Strait of Hormuz daily calls and capacity fields by vessel class, same 2019-01-01 through 2026-06-28 coverage. | Use as the raw-source lineage behind the public tracker; retain fields for reproducibility and any recalculation of baselines. | Public AIS-derived operational data; cargo classification remains unavailable. |
| `hormuz-2y7.6` | Historical traffic availability rules: public daily PortWatch backfill starts 2019-01-01; pre-2019 comparisons cannot be direct daily ship-count analogues under public-only data. | Set the traffic-comparability flag for each case. Use PortWatch daily rows for 2019+ route/security/COVID/current cases; use lower-resolution non-AIS proxies for 1956, 1967, 1973-74, 1978-79, 1980, 1990, 2002-03, 2005, and 2011 cases. | Important cleared blocker, but it narrows rather than solves historical traffic comparability. |
| `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv` | Current-scenario rows for total oil/products, crude/condensate, refined products, LPG, LNG, bypass offset, and oil inventory draw check; includes low/base/high disrupted volumes, baseline flows, units, source basis, confidence, notes. | Populate current Hormuz `exposed_flow`, `realized_disrupted_flow` or `removed_or_delayed` scenario values, `bypass_offset`, and inventory-draw consistency-check rows. | Scenario data, not observed final data. Use `is_forecast`, `is_inferred`, or `is_provisional` flags; do not mix with historical observed actuals without labels. |
| `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv` | Product rankings and preliminary baseline/share rows for crude/condensate, LNG, refined products, LPG/NGLs, sulphur, aluminium, petrochemicals, urea, ammonia, MAP/DAP, and freight/war-risk insurance. | Populate `commodity`, `product_detail`, `baseline_or_market_denominator`, `global_or_regional_share`, `source_provider/title`, and caveat fields for the current Hormuz case. | Blog-ready preliminary ranking, not a de-duplicated supply-loss total. Do not sum rows because feedstock/product chains overlap. |
| `hormuz-kmz.6` | Current-Hormuz global-market denominators and offset mechanisms: crude trade share, total liquids share, LNG trade share, refined product proxy share, fertilizer/sulphur/aluminium shares, bypass/spare-capacity notes. | Main denominator source for comparing current Hormuz against historical shocks. Carry into `baseline_global_supply`, `baseline_seaborne_trade`, `baseline_regional_imports`, `substitution_capacity`, and `known_biases`. | Strongest for oil and LNG, medium/high for fertilizers and aluminium, weakest for petrochemical feedstock split. |
| `hormuz-kmz.7` | Product-level caveats, surprise value, source shorthand, and editorial ranking. | Helps decide which current-Hormuz products need historical analog rows and which should be treated as transmission channels. | Use as prioritization/caveat layer, not final metric evidence. |
| `hormuz-s49.1` | Source map for U.S. SPR/commercial oil stocks, IEA/OECD stocks, JODI oil/gas stocks, GIE gas storage, China apparent-balance inputs, fertilizer/chemical inventory proxies. | Populate source-provider rows for `inventory_cover` and `strategic_stock_response`; pre-wire source URLs/frequency/lag/caveats before `s49.6` computes days of cover. | Source inventory only. It does not supply final stockpile-buffer values; China SPR and fertilizer/chemical inventories remain especially uncertain. |
| `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv` / `hormuz-s49.2` | Official/provisional reserve-response rows for U.S., IEA/OECD collective action, EU, Japan, and Korea; separates strategic releases, obligated/private relief, commercial draws, seasonal/baseline movements, and reporting lags. | Populate `strategic_stock_response`, `stock_release_announced`, `stock_release_actual`, `stock_release_window`, `source_provider`, and caveat fields for oil reserve-response metrics. | Done and usable, but not a complete stockpile-buffer-duration table. Announcement volumes, exchanges, observed stock draws, and actual net supply additions must remain distinct. |
| `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv` | Evidence matrix on China SPR/commercial-stock claims. Current synthesis: large government SPR-release claim is not supported; commercial/operational stock draw and stock/balance management are better supported. | Use only as a provisional confidence/caveat source for China reserve-response rows until `hormuz-s49.3` is done. | Issue remains in progress; do not convert into a precise China SPR volume. |
| `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv` | Provisional LNG/gas storage buffer days and caveats for Europe, Japan, Korea, China, and India. | Candidate inputs for `inventory_cover` and `route_substitution_constraint` in LNG/gas rows after `s49.4`/`s49.6` finalize. | Issue remains in progress; values should be treated as provisional and region-specific, not global LNG buffer truth. |
| `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv` | Provisional fertilizer/chemical buffer assessment for urea, ammonia, sulfur, DAP/phosphates, MOP/potash, and petrochemicals. | Candidate inputs for `inventory_cover`, `product_criticality`, and caveats on fertilizer/sulfur/petrochemical rows after `s49.5`/`s49.6` finalize. | Issue remains in progress; most rows are qualitative or country-specific proxies, not global days-of-cover. |
| `hormuz-l8m.1` | Scenario-ready low/base/high price inputs: Brent, U.S. gasoline/diesel/jet wholesale deltas, Henry Hub/electricity sensitivity, fertilizer, aluminium/metals, freight, and war-risk insurance. | Populate current-Hormuz `price_response`, `real_price_response`, `freight_insurance_channel`, and `price_per_unit_of_disruption` scenario fields, while keeping observed, official forecast, and speculative tail values in separate columns. | Cleared blocker for current price-scenario inputs. Historical analogue price series still need direct collection from EIA/FRED/World Bank/IMF and inflation deflation. |

### Current-Hormuz Denominators To Carry Into Historical Comparison

Use these as the current case's denominators and scenario anchors when ranking against historical shocks. Keep native units visible and avoid summing overlapping product rows.

| Commodity / channel | Current-Hormuz denominator or scenario anchor | Candidate `4j7.3` field(s) | Source breadcrumb | Confidence / caveat |
|---|---:|---|---|---|
| Total oil and petroleum liquids | 20.26 mb/d 2024 Hormuz oil traffic; low/base/high scenario 11.0/15.06/20.26 mb/d removed or delayed. | `baseline_global_supply`, `exposed_flow`, `realized_disrupted_flow`, `disrupted_share_global`, `disruption_intensity`. | `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`; EIA Today in Energy 2025-06-16; EIA STEO cited in `kmz.3`. | Medium. Scenario values need reconciliation with AIS, bypass use, and actual shut-ins. |
| Crude oil and condensate | 14.95 mb/d 2025 Hormuz crude/condensate transit; base scenario 12.35 mb/d after 2.6 mb/d bypass offset; about 34% of global crude trade per `kmz.6`. | `baseline_seaborne_trade`, `exposed_flow`, `rerouted_flow`, `substitution_capacity`, `disrupted_share_trade`. | `kmz.3`, `kmz.6`, `kmz.7`; IEA Strait of Hormuz page; EIA Today in Energy. | Medium/high for denominator; medium for realized disruption. |
| Saudi/UAE bypass capacity | 2.6 mb/d EIA spare bypass estimate; 3.5-5.5 mb/d IEA available-capacity range. | `substitution_capacity`, `route_substitution_constraint`, `spare_capacity_buffer`. | `kmz.3` bypass-sensitivity row; `kmz.6`; EIA Today in Energy; IEA topic page. | Medium. Treat as offset capacity, not new supply; utilization and route constraints matter. |
| Refined products | 3.3 mb/d Gulf refined-product exports in 2025; base scenario 2.4 mb/d removed/delayed. | `exposed_flow`, `realized_disrupted_flow`, `product_criticality`, `shipping_insurance_channel`. | `kmz.3`, `kmz.6`, `kmz.7`; IEA Middle East and Global Energy Markets. | Medium. Gulf export figure is not necessarily all Hormuz-routed. |
| LPG/NGLs | 1.5 mb/d Gulf LPG exports in 2025; base scenario 1.2 mb/d; 30% of seaborne LPG exports via Hormuz per `kmz.7`. | `exposed_flow`, `disrupted_share_trade`, `product_criticality`. | `kmz.3`, `kmz.7`; IEA Middle East and Global Energy Markets. | Medium/high for exposure; double-counting risk with petroleum-liquids total. |
| LNG | >110 bcm/year through Hormuz in 2025; base disruption 0.30 bcm/d; almost one-fifth of global LNG trade. | `baseline_global_trade`, `realized_disrupted_flow`, `route_substitution_constraint`, `inventory_cover`. | `kmz.3`, `kmz.6`, `kmz.7`; IEA Strait/Hormuz and Middle East topic pages; EIA LNG figure data. | High. No practical bypass for Qatar/UAE LNG, but outage duration and storage buffering remain separate. |
| Urea | 34% of global urea trade from upstream Hormuz countries. | `disrupted_share_trade`, `product_criticality`, `geographic_concentration`. | `kmz.6`, `kmz.7`; IFASTAT Hormuz page; World Bank fertilizer blog. | High for share; tonnage and importer split still pending. |
| Ammonia | 23% of global ammonia trade from upstream Hormuz countries. | `disrupted_share_trade`, `product_criticality`, `geographic_concentration`. | `kmz.6`, `kmz.7`; IFASTAT; World Bank fertilizer blog. | High for share; avoid double-counting as both product and urea/phosphate input. |
| MAP/DAP phosphate | 18% of global MAP+DAP trade from upstream Hormuz countries. | `disrupted_share_trade`, `product_criticality`, `geographic_concentration`. | `kmz.6`, `kmz.7`; IFASTAT; World Bank fertilizer blog. | Medium/high; seasonal demand context still needed. |
| Sulphur | About half of global seaborne sulphur trade moves through Hormuz. | `disrupted_share_trade`, `product_criticality`, `geographic_concentration`. | `kmz.6`, `kmz.7`; IEA Middle East and Global Energy Markets; IFASTAT. | Medium/high. Needs tonnage and importer mapping. |
| Aluminium | About 5 Mt/year shipped through Hormuz; Gulf about 8% of global aluminium supply. | `exposed_flow`, `disrupted_share_global`, `product_criticality`. | `kmz.6`, `kmz.7`; IEA Middle East topic page; World Bank commodity blog. | Medium/high for scale; route shares and rerouting need confirmation. |
| Freight / war-risk insurance | Pre-war additional war risk premium 0.1-0.15% hull value; cited shock range 1-3% hull value. | `shipping_insurance_channel`, `freight_insurance_cost_change`, `delivered_cost_uplift`. | `kmz.7` row citing `kmz.5`, S&P Global, Reuters, EIA. | Medium/high, but not a physical supply-loss row. Model as cost/friction. |
| Daily transit traffic | 2,736 daily rows from 2019-01-01 to 2026-06-28; average `n_total` 86.82 and `n_tanker` 51.86; tracker includes baseline percentages and 7-day averages. | `traffic`, `disruption_intensity`, `duration_recovery_shape`, `route_substitution_constraint`. | `data/derived/hormuz_2y7_public_daily_tracker.csv`; raw `data/external/portwatch/hormuz_daily_chokepoint.csv`; IMF PortWatch. | High for calls/capacity by broad vessel class; not cargo/direction. |

### Metric-By-Metric Source Map

| Metric family / metric | Current-Hormuz source path now available | Historical source path still needed | Collection priority |
|---|---|---|---|
| `disrupted_share_global` / `disrupted_share_trade` | `kmz.3`, `kmz.6`, `kmz.7` for oil, crude, LNG, LPG, refined products, fertilizer, sulphur, aluminium. | IEA 2012 emergency response table; EIA historical Today in Energy; IEA/OPEC/EIA global liquids denominators; JODI for 2002+ monthly balances; UN Comtrade/BACI for fertilizer/metals. | High. This is the core ranking metric. |
| `disruption_intensity` | `kmz.3` scenario low/base/high flows plus PortWatch daily traffic to compute percent-days; current physical-flow duration still scenario-bound. | Case-specific onset/recovery dates from `4j7.1` sources and IEA/EIA chronologies. `2y7.6` confirms direct public daily traffic comparability only from 2019-01-01 onward; pre-2019 route cases need lower-resolution proxies. | High. Needs consistent thresholds: 5%, 10%, 20% below baseline. |
| `duration_recovery_shape` | PortWatch daily current tracker and scenario chronology from foundation docs. | Event chronologies from IEA/EIA/official histories for oil shocks; PortWatch/AIS backfill for route shocks after 2019; archival sources for pre-2019 route cases. | High. Historical recovery definitions remain judgment-heavy. |
| `spare_capacity_buffer` | `kmz.3` bypass sensitivity and `kmz.6` notes on >4 mb/d world spare crude capacity and 3.5-5.5 mb/d alternative Gulf export capacity. | EIA/IEA/OPEC spare-capacity estimates for each historical oil shock; limited analogs for LNG/fertilizer. | High for oil, medium for other products. |
| `inventory_cover` | `s49.1` source map, provisional `s49.4` LNG/gas buffer table, provisional `s49.5` fertilizer/chemical buffer table, and `kmz.3` oil inventory draw check; no finalized cross-product days-of-cover table yet. | `s49.6` days-of-cover values; EIA WPSR/PSM/SPR, IEA OECD oil stocks, JODI oil/gas, GIE AGSI, national data, inferred China balances. | High blocker. Do not finalize without `s49.6`. |
| `strategic_stock_response` | `s49.2` provides usable OECD/U.S./Japan/EU/Korea reserve-response rows; `s49.3` provides provisional China evidence/caveats. | IEA collective-action notices for 1991, 2005, 2011, 2022/current; DOE SPR release history; national release data. | Partly available for current oil reserve response; still needs `s49.6` to translate into buffer duration and comparability. |
| `route_substitution_constraint` | `kmz.3` bypass rows, `kmz.6` offset notes, PortWatch traffic, `kmz.7` no-bypass LNG caveat, and `2y7.6` traffic-comparability limits. | EIA/IEA chokepoint briefs; Suez/SUMED/route-capacity sources; tanker-war public sources; PortWatch for 2019+ analogues. | High for current Hormuz and 2019+ public daily traffic; medium/lower for older route analogues. |
| `price_response` / `real_price_response` | `l8m.1` provides low/base/high current price inputs for Brent, products, gas/electricity, fertilizer, aluminium/metals, freight, and war-risk insurance. | Pull historical Brent/WTI/Arabian Light/Dubai/Oman where available; World Bank Pink Sheet/IMF commodity prices for fertilizer/metals/gas; CPI deflators. | Current scenario input is available; historical price collection remains high priority. |
| `price_per_unit_of_disruption` | Combine `l8m.1` current price scenarios with `kmz.3/kmz.6` denominators, once `kmz.3` current disruption values are finalized. | Combine historical price series with disruption-intensity rows. | Medium/high. Must be caveated as sensitivity, not causal estimate. |
| `demand_elasticity` / `demand_destruction` | No completed derived current table yet. | IEA OMR/GMR demand revisions, EIA STEO, historical consumption series, macro controls. | Medium. Useful but attribution risk is high. |
| `geographic_concentration` | `kmz.7` product rows and `kmz.6` product shares; importer flows still need `f6r` tasks. | UN Comtrade/BACI, EIA/IEA country flow matrices, JODI, AIS/cargo databases if available. | Medium/high. Needed for destination and exposure story. |
| `shipping_insurance_channel` | `kmz.7` freight/war-risk row and `kmz.5` source breadcrumbs via that row. | Baltic/Clarksons/Drewry/Broker/war-risk public reports; Tanker War and Red Sea analogs. | Medium. Treat as delivered-cost channel. |
| `product_criticality` | `kmz.7` surprise/caveat rows for LNG, sulphur, fertilizers, LPG/NGLs, aluminium, petrochemicals. | BEA/OECD/WIOD input-output, USDA/FAO/World Bank fertilizer chains, sectoral energy-use data. | Medium. Main use is blog framing and downstream-exposure context. |

### Remaining Blockers Before Acceptance Criteria Can Be Met

- Historical traffic/backfill: `hormuz-2y7.6` is done and establishes that public daily traffic comparability starts in 2019. Pre-2019 route/supply analogues still need lower-resolution flow, price, inventory, news, and insurance proxies; do not label them directly comparable daily AIS/PortWatch series.
- Price paths and scenario windows: `hormuz-l8m.1` is done for current scenario inputs. Historical price-response rows still need direct collection and deflation by case.
- Stockpile buffer values: `hormuz-s49.6` is in progress. `s49.1` provides sources and `s49.2` provides usable OECD/U.S. reserve-response rows; `s49.3`-`s49.5` provide provisional stockpile/buffer evidence. This still blocks final inventory-cover and strategic-stock-response comparability because days-of-cover and product/country buffer durations are not finalized.
- Current realized disruption still provisional: `kmz.3` is still blocked/incomplete, so `kmz.3` scenario rows should remain provisional even though `kmz.6` and `kmz.7` can supply denominators and product priorities.
- Historical denominators still need direct collection: `4j7.1` selected cases and headline losses, but `4j7.3` still needs global liquids demand/trade, spare capacity, inventories, demand context, and real price baselines at each event date.
- Product overlap / double-counting: current rows for total petroleum liquids, crude, refined products, LPG, petrochemicals, ammonia, urea, and MAP/DAP overlap. The collection table must preserve product rows but avoid summing them into a single disruption total.
- Licensed data gaps remain: LNG cargo destinations/prices, Dubai/Oman sour crude, war-risk premia/freight routes, fertilizer/sulphur/petrochemical market data, and China SPR/commercial stock evidence may require licensed/vendor sources or explicit low-confidence inference.

### Candidate Public And Primary Source Families

Use the project source rubric from `docs/foundation-research-standards.md`: official/statistical or operational sources first; transparent institutional analysis second; vendor/news only when primary data are unavailable and clearly labeled.

| Data family | Candidate series / fields | Source links | Source-quality notes |
|---|---|---|---|
| Current Hormuz exposure anchors | Annual and quarterly oil/LNG volumes through Hormuz; destination shares; bypass pipeline capacity. | EIA World Oil Transit Chokepoints: https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints; EIA Hormuz note: https://www.eia.gov/todayinenergy/detail.php?id=65504 | High for public chokepoint baselines and definitions; usually annual/periodic rather than daily. Keep "transit volume" separate from production shut-ins. |
| Current oil supply, demand, inventories, prices | STEO global oil production, consumption, inventories, Brent/WTI forecasts; EIA scenario assumptions for shut-ins and recovery. | EIA STEO: https://www.eia.gov/outlooks/steo/; global oil page: https://www.eia.gov/outlooks/steo/report/global_oil.php | High for public U.S. government forecast assumptions; not ground truth for real-time physical flows. Record release month/version. |
| Historical global oil balances | Monthly/annual production, consumption/demand, stock changes, refinery throughput, product balances by country/product. | JODI Oil: https://www.jodidata.org/oil/; JODI data availability: https://www.jodidata.org/oil/support/user-guide/data-available-in-the-jodi-oil-world-database.aspx; OPEC MOMR: https://www.opec.org/monthly-oil-market-report.html; EIA Open Data: https://www.eia.gov/opendata/ | JODI is public and monthly from 2002 forward with country reporting gaps/revisions; EIA/OPEC are strong cross-checks but definitions differ. Pre-2002 shocks need EIA historical tables, IEA/OECD publications, BP/EI Statistical Review, academic datasets, or archived official reports. |
| U.S. oil/product stocks and reserve releases | Weekly SPR crude stocks `WCSSTUS1`; U.S. crude/product commercial stocks; product supplied; imports/exports; refinery runs. | EIA SPR weekly history: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1; EIA stocks overview: https://www.eia.gov/dnav/pet/pet_stoc_wstk_dcu_nus_w.htm; DOE SPR facts and historical releases: https://www.energy.gov/hgeo/opr/spr-quick-facts; EIA Petroleum Supply Monthly: https://www.eia.gov/petroleum/supply/monthly/ | High for U.S. weekly history and SPR drawdowns; U.S. series are not a global inventory proxy. Use EIA series IDs/API paths when loaders are written. |
| OECD/IEA emergency stocks | Days of net imports; OECD oil stock levels/changes; emergency reserve releases. | IEA Oil Stocks of IEA Countries: https://www.iea.org/data-and-statistics/data-tools/oil-stocks-of-iea-countries; IEA Monthly Oil Statistics: https://www.iea.org/data-and-statistics/data-product/monthly-oil-statistics; IEA OMR public pages such as June 2026: https://www.iea.org/reports/oil-market-report-june-2026 | IEA oil-stock tool is public/CC BY for days of net imports; detailed MODS/monthly stock datasets may require subscription. Public OMR highlights are useful but not enough for a full panel dataset. |
| China/non-OECD stocks and SPR | Apparent crude stock change from production + imports - refinery runs - exports; visible commercial/onshore stocks; official reserve statements where available. | JODI Oil: https://www.jodidata.org/oil/; EIA International/EIA API: https://www.eia.gov/opendata/; IEA OMR public highlights: https://www.iea.org/reports/oil-market-report-june-2026 | Medium to low unless sourced from official releases; China SPR is opaque. Keep inferred stock changes separate from verified strategic releases and tag methodology. |
| Spare capacity and supply cushion | OPEC crude production capacity, effective spare capacity, maximum sustainable capacity, non-OPEC supply growth. | EIA Today in Energy on OPEC capacity definitions: https://www.eia.gov/todayinenergy/detail.php?id=66904; EIA crude supply/OPEC explainer: https://www.eia.gov/finance/markets/crudeoil/supply-opec.php; OPEC MOMR: https://www.opec.org/monthly-oil-market-report.html | Medium-high for EIA/OPEC estimates, but capacity is modelled and politically sensitive. Record definition: able to come online within 30 days and sustain 90 days where using EIA spare-capacity concept. |
| Oil and product prices | Brent `DCOILBRENTEU`, WTI `DCOILWTICO`, Brent-WTI spread, EIA petroleum spot prices for gasoline/diesel/jet/fuel oil. | FRED Brent/WTI graph: https://fred.stlouisfed.org/graph/?id=DCOILWTICO,DCOILBRENTEU; EIA petroleum spot prices: https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm; World Bank Commodity Markets/Pink Sheet: https://www.worldbank.org/en/research/commodity-markets | High for public crude/product benchmarks; daily public history is strong for Brent/WTI but weaker for Dubai/Oman sour crude and product cracks outside U.S. hubs. |
| Gas/LNG supply, demand, inventories, prices | JODI-Gas production/imports/exports/stocks/demand; European gas storage; Henry Hub; TTF; JKM if licensed. | JODI-Gas portal: https://www.jodidata.org/gas/; GIE AGSI storage: https://agsi.gie.eu/; EIA natural gas data: https://www.eia.gov/naturalgas/data.php | Public physical gas series are useful but LNG cargo flows and JKM price history are often licensed. Qatar LNG exposure should be validated with Kpler/Vortexa/IEA if available. |
| Fertilizer and chemical shocks | Monthly urea, DAP, TSP, phosphate rock, potassium chloride; ammonia if available; trade quantities by exporter/importer. | World Bank Commodity Markets/Pink Sheet: https://www.worldbank.org/en/research/commodity-markets; FAOSTAT fertilizers by nutrient/product: https://www.fao.org/faostat/en/#data/RFB; UN Comtrade: https://comtradeplus.un.org/; USDA ERS fertilizer market report: https://www.ers.usda.gov/publications/pub-details?pubid=110210 | Public prices are monthly and not always Gulf-specific. Gulf export quantities likely require UN Comtrade/FAOSTAT lagged annual data plus vendor/news checks for current outages. |
| Metals/petrochemicals beyond oil | Aluminium prices and Gulf exports; sulphur, polymers, methanol/chemicals where material. | World Bank Commodity Markets: https://www.worldbank.org/en/research/commodity-markets; UN Comtrade: https://comtradeplus.un.org/; International Aluminium Institute statistics: https://international-aluminium.org/statistics/ | Public commodity-price coverage is decent for aluminium, thin for sulphur/petrochemicals. ICIS/Argus/CRU likely needed for current market-specific price/disruption claims. |
| Shipping/logistics shock comparisons | Daily chokepoint transit calls and trade volumes; port activity; AIS-derived Red Sea/Suez/Panama comparison baselines. | IMF PortWatch: https://portwatch.imf.org/; IMF PortWatch methodology/API: https://portwatch.imf.org/pages/data-and-methodology; IMF PortWatch FAQ: https://portwatch.imf.org/pages/faqs; UN AIS Task Team: https://unstats.un.org/bigdata/task-teams/ais/index.cshtml | IMF PortWatch is public and designed for disruption monitoring, with AIS data supplied by Kpler. Good for shipping/logistics comparisons, but not enough to classify cargoes as precisely as vendor AIS/cargo databases. |
| Historical macro/demand context | GDP, CPI/deflators, industrial production, oil intensity, global consumption denominators. | World Bank WDI: https://databank.worldbank.org/source/world-development-indicators; IMF WEO: https://www.imf.org/en/Publications/WEO/weo-database; FRED: https://fred.stlouisfed.org/ | Use to normalize old shocks by real prices, oil intensity, and demand share. Revisions and annual frequency matter for event-month precision. |

### Likely Licensed Or Paywalled Gaps

- AIS/cargo classification: exact historical Hormuz transits by vessel class, laden/ballast status, cargo, destination, and dark-ship behavior likely require Kpler, Vortexa, MarineTraffic, Lloyd's List Intelligence, Spire, Windward, Clarksons, or similar. IMF PortWatch is public but aggregated.
- LNG cargoes and prices: Platts JKM history, detailed LNG voyage data, Qatar cargo destinations, and forward curves are usually licensed through S&P Global, ICE/CME history, Kpler, ICIS, Argus, or LSEG/Bloomberg.
- Dubai/Oman/sour crude and refined-product cracks: reliable daily history outside headline Brent/WTI often requires Platts/Argus/OPIS/LSEG/Bloomberg.
- War-risk insurance and freight: broker quotes, P&I/war-risk premium series, Baltic Exchange tanker routes, and Clarksons/SSY tanker rates are often proprietary; public news can support narrative but should be tagged lower confidence.
- Fertilizer, sulphur, and petrochemical prices/flows: current urea/ammonia/sulphur/polymer market disruptions are likely best covered by Argus, ICIS, CRU, Fertecon, S&P Global, and customs datasets; public sources may lag or lack Gulf specificity.
- China SPR/commercial stocks: official transparency is limited. Any "China released X barrels" claim needs a source-quality warning unless tied to verifiable customs/refinery-run/storage-tank estimates and a transparent inference.

### Proposed Future Dataset Schema

Build one long panel rather than separate case spreadsheets. One row should represent one metric observation for one case, geography, commodity, source, and date/window.

| Field | Purpose |
|---|---|
| `case_id` | Stable historical/current shock ID from `hormuz-4j7.1`. |
| `case_name` | Human-readable shock name. |
| `event_date`, `window_start`, `window_end`, `baseline_start`, `baseline_end` | Absolute dates for event and comparison windows. |
| `metric_family` | `supply`, `price`, `inventory`, `spare_capacity`, `demand`, `traffic`, `freight_insurance`, `macro_context`. |
| `metric_name` | Final metric from `hormuz-4j7.2`, e.g. `disrupted_supply_share_global`, `inventory_days_cover`, `real_price_change_pct`. |
| `commodity`, `product_detail` | Crude, refined products, LNG, LPG, urea, ammonia, sulphur, aluminium, etc. |
| `geography`, `exporter`, `importer`, `route_or_chokepoint` | Country/region and route dimensions where known. |
| `value`, `unit`, `frequency`, `aggregation_method` | Numeric value, units, daily/weekly/monthly/annual, and transformation from raw source. |
| `baseline_value`, `delta_abs`, `delta_pct`, `z_score`, `real_price_basis` | Normalized comparison outputs where applicable. |
| `source_provider`, `source_title`, `source_url`, `source_release_date`, `accessed_at`, `source_version` | Citation and reproducibility fields. |
| `source_tier`, `confidence`, `access_type` | `primary_official`, `institutional_analysis`, `vendor_estimate`, `reputable_news`, `inference`; confidence `high`/`medium`/`low`/`speculative`; access `public`/`free_account`/`licensed`/`paywalled`. |
| `is_forecast`, `is_inferred`, `is_provisional`, `is_paywalled_gap` | Boolean flags to prevent forecasts/inferences from being mixed with observed data. |
| `missingness_note`, `method_note`, `caveat` | Explicit caveats, especially for China stocks, dark AIS, cargo classification, and historical pre-2002 data. |

Minimum confidence rule for publication charts: use `high` or `medium` rows for main claims; `low` or `speculative` rows can appear only as sensitivity ranges or clearly labeled open questions.
