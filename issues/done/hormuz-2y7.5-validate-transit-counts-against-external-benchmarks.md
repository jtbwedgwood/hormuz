---
id: "hormuz-2y7.5"
title: "Validate transit counts against external benchmarks"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "shipping"
  - "tracker"
  - "validation"
blocked_by:
  - "hormuz-2y7.4"
  - "hormuz-fyp.1"
  - "hormuz-fyp.2"
blocks:
  - "hormuz-2y7.7"
  - "hormuz-kmz.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:27Z"
updated_at: "2026-07-06T07:03:00Z"
---

# Validate transit counts against external benchmarks

## Description

Cross-check daily/weekly counts against port calls, EIA/IEA flow estimates, tanker-tracking reports, news snapshots, satellite imagery summaries, or known incident dates.

## Acceptance Criteria

Validation report identifies agreement/disagreement, estimated error bounds, and whether the tracker is blog-worthy.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-2y7.4` - Prototype daily transit count pipeline
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.2` - Build canonical disruption chronology
- Blocks: `hormuz-2y7.7` - Produce tracker dataset and publication chart
- Blocks: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted

## Work Notes

- 2026-07-06: Claimed for validation planning only. Full validation remains materially blocked on `hormuz-2y7.4` outputs and the canonical chronology from `hormuz-fyp.2`.
- 2026-07-06: Coordination note from KMZ support pass: another agent is actively working the broader `hormuz-2y7` tracker. I am not taking over `hormuz-2y7.4` pipeline ownership. I am completing this validation task using that agent's PortWatch fetch, public tracker CSV, and figure output so `hormuz-kmz.3` has a clearer unblock path.

### Provisional Validation Candidates

- Primary public benchmark: IMF PortWatch daily Hormuz chokepoint data. It measures daily UTC transit calls by `n_container`, `n_dry_bulk`, `n_general_cargo`, `n_roro`, `n_tanker`, `n_cargo`, `n_total`, plus estimated metric-ton capacity. Same-ship repeat threshold is 48 hours. Reported API availability in the subagent pull: 2019-01-01 through 2026-06-28, with weekly updates/revisions. Use for daily total and tanker validation; do not convert `capacity_tanker` directly to barrels. Sources: https://portwatch.imf.org/pages/chokepoint6, https://portwatch.imf.org/api/search/v1/collections/dataset/items/3da2b9ca97684916b75c4013f95d18ab, https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query.
- Scale baseline: PortWatch annual-average chokepoint table for 2019-2024 lists Hormuz at 32,496 total ships/year and 19,540 tankers/year, about 89 total/day and 54 tankers/day. Use as scale check, not daily validation. Source: https://portwatch.imf.org/items/fa9a5800b0ee4855af8b2944ab1e07af.
- Secondary presentation: IEA Middle East Maritime Chokepoints Shipping Monitor uses IMF PortWatch for traffic flows since 2026-02-28. Useful citation/chart comparison, not independent validation. Source: https://www.iea.org/data-and-statistics/data-tools/middle-east-maritime-chokepoints-shipping-monitor.
- Compare daily/weekly direction-balanced counts against MarineTraffic/Kpler public snapshots or contracted area historical output if available.
- Reconcile energy-carrier counts against EIA/IEA/OPEC/Kpler/Vortexa flow estimates where licensed or publicly summarized.
- Use the canonical event chronology from `hormuz-fyp.2` to test whether observed count drops align with known closure, rerouting, evacuation, or escalation dates.
- Use AIS coverage diagnostics: daily number of unique vessels in side boxes, share of ambiguous crossings, median inter-ping gaps, and share of interpolated/dark-gap events.

### Spot-Check Sources

- EIA/Vortexa flow estimates: 2024 oil flow through Hormuz about 20 million b/d; more than one-quarter of seaborne oil trade in 2024/1Q25; about one-fifth of global LNG; 84% of crude/condensate and 83% of LNG went to Asia. Use to validate energy-flow plausibility, not ship-count integers. Source: https://www.eia.gov/todayinenergy/detail.php?id=65504.
- Academic SAR + AIS assessment around 2026-02-22 to 2026-03-07 reports roughly 97% traffic decline and AIS from 175 vessels to 6 vessels, with non-Gulf oil/chemical tankers from 50-60 daily crossings to about 2. Use as independent crisis sanity check, especially because SAR can detect some AIS-dark vessels. Sources: https://doi.org/10.1016/j.xinn.2026.101367, https://www.researchgate.net/publication/403388077_Satellite_radar_and_AIS_reveal_a_97_decline_in_shipping_traffic_through_the_Strait_of_Hormuz.
- Kpler-attributed public snapshots: 223 commercial ships during 2026-06-15 to 2026-06-21 vs 343 during 2026-06-22 to 2026-06-28; another snapshot says tanker transits fell to 13 on a Friday from 24 Thursday and 27 Wednesday. Use as secondary weekly/daily checks unless Kpler data are licensed directly. Sources: https://www.aa.com.tr/en/world/commercial-ship-traffic-through-strait-of-hormuz-rises-more-than-50-over-past-week/3982242, https://boereport.com/2026/06/26/traffic-through-strait-of-hormuz-slows-after-attack-on-ship/.
- Lloyd's List Intelligence snapshots: cargo-carrying vessels over 10,000 DWT, including examples of 48 vessels in one week vs 34 prior week and later a 48% weekly slump. Use carefully because it is not all-vessel PortWatch and may include dark-transit estimates. Sources: https://www.lloydslist.com/LL1156756/Subtle-rise-in-non-Iranian-trade-through-Hormuz, https://www.lloydslist.com/LL1157290/Strait-of-Hormuz-traffic-falls-as-reopening-efforts-make-little-headway.

### Local Data Pull

- 2026-07-06: Added `scripts/fetch_portwatch_hormuz.py` and fetched `data/external/portwatch/hormuz_daily_chokepoint.csv`.
- Fetch result: 2,736 daily rows, date range 2019-01-01 to 2026-06-28.
- Quick scale check from local CSV: 2019-2024 average `n_total` = 90.5 ships/day; 2019-2024 average `n_tanker` = 54.8 tankers/day.
- Manifest row added as `imf_portwatch_hormuz_daily`.

### Closeout

- Public tracker is blog-worthy if labeled precisely as IMF PortWatch chokepoint calls.
- Validation against independent public snapshots should be used qualitatively because Kpler/Lloyd's/SAR examples use different scopes: commercial ships, tankers, cargo-carrying vessels over 10,000 DWT, or imagery/AIS combinations.
- Main uncertainty to disclose: public PortWatch validates daily aggregate traffic levels, not vessel-level tracks, direction, or cargo contents.

### Validation Report

- 2026-07-06: Added `data/derived/hormuz_2y7_validation_summary.csv` and registered it in `data/manifest.csv`.
- Rebuilt `data/derived/hormuz_2y7_public_daily_tracker.csv` and `figures/fig-2y7-public-hormuz-daily-transits.csv/svg` from the existing PortWatch pull. Latest observation remains 2026-06-28 with 27 total transits and 12 tanker transits.
- Follow-up `.venv` fix: added pytest to `requirements.txt`, installed it into `.venv`, and verified `.venv/bin/python -m pytest code/hormuz_tracker/test_prototype_daily_transits.py -q`: 1 passed.

| validation check | PortWatch/public tracker result | external benchmark | assessment | confidence | notes |
|---|---:|---:|---|---|---|
| 2019-2024 total-transit scale | 90.5 ships/day | PortWatch annual table: about 89.0 ships/day | agree | high | +1.7% gap, likely rounding/window/leap-day difference. |
| 2019-2024 tanker scale | 54.8 tankers/day | PortWatch annual table: about 53.5 tankers/day | agree | high | +2.4% gap. |
| Early-March crisis collapse, total traffic | 98.4/day pre-shock week to 6.7/day in 2026-03-01 to 2026-03-07, a 93.2% decline | SAR/AIS study reports roughly 97% traffic decline | mostly agree | medium | PortWatch all-vessel decline is slightly less severe than the independent study but direction and order of magnitude match. |
| Early-March crisis collapse, tankers | 54.1/day pre-shock week to 2.1/day in 2026-03-01 to 2026-03-07, a 96.0% decline | SAR/AIS study reports non-Gulf oil/chemical tankers from 50-60/day to about 2/day | agree | medium | This is the strongest independent crisis validation for tanker counts. |
| Late-June weekly recovery | 107 total ships in 2026-06-15 to 2026-06-21; 228 in 2026-06-22 to 2026-06-28 | Kpler-attributed public snapshot: 223 then 343 commercial ships | directional agreement, scale disagreement | medium | Both show recovery; PortWatch is 52% and 34% lower than Kpler snapshots, likely due scope/method differences. |
| 2026-06-20 single-day recovery | 26 total PortWatch transits | USCENTCOM reported 55 merchant ships and >17m barrels | disagreement | medium | Do not use CENTCOM single-day number as exact validation without method/window detail. |
| Latest tracker state | 2026-06-28: 27 total, 12 tankers; 29.8% and 21.9% of baseline | no exact independent same-day benchmark | n/a | high for PortWatch method | Confirms traffic remained far below baseline at latest PortWatch observation. |

### Blog-Worthiness Judgment

- The public PortWatch tracker is blog-worthy as a daily public chokepoint-call tracker from 2019-01-01 to 2026-06-28. It is source-auditable, reproducible, and validated against PortWatch's own annual scale table plus independent crisis-collapse evidence.
- Use it carefully: it validates daily broad vessel-class counts, not direction, vessel identity, AIS-dark activity, exact cargo onboard, or country/product supply loss.
- Practical error bounds: for stable baseline scale, expect low single-digit percentage differences versus PortWatch annual summaries. For live crisis comparisons against commercial/news snapshots, expect large level differences, roughly 30-55% in the late-June checks here, because sources use different vessel scopes, windows, and dark-traffic treatments.
- Downstream implication for `hormuz-kmz.3`: this validation is enough to use PortWatch as a public traffic severity proxy, but not enough by itself to estimate final product/country supply removed. `hormuz-kmz.3` still needs a cargo/class allocation step or licensed AIS/Kpler/Vortexa-style flow data.

### Completion Note

- 2026-07-06: Acceptance criteria met for validation of the public tracker. The report identifies agreements, disagreements, estimated error/gap ranges, and whether the tracker is blog-worthy.
