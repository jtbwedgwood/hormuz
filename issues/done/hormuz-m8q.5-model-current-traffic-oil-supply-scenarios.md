---
id: "hormuz-m8q.5"
title: "Model provisional current-traffic oil-supply scenarios"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "scenarios"
  - "traffic"
  - "durability"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-03T22:57:25Z"
updated_at: "2026-08-03T23:19:34Z"
---

# Model provisional current-traffic oil-supply scenarios

## Description

Build a transparent low/base/high oil-supply scenario model that preserves observed history including the June relaxation, uses July estimates or forecasts with labels, and then holds Strait traffic around the refreshed July 8-23 regime through the September, December, and March horizons.

## Acceptance Criteria

- Scenario assumptions distinguish observed history, July nowcast/forecast, and future modeled periods.
- PortWatch call rates are not mechanically converted to mb/d; mapping is calibrated or bounded using contemporaneous IEA/EIA Gulf/Hormuz/export anchors and includes an explicit residual for AIS-dark/cargo uncertainty.
- Gulf bypass, non-Gulf production, government stocks, commercial stocks, demand response, and residual each have a durability rule and no double counting.
- Outputs include cumulative million-barrel effects through 2026-09-30, 2026-12-31, and 2027-03-31 with low/base/high uncertainty.
- No price forecast is produced.

## Work Notes

- 2026-08-03: Started after `hormuz-m8q.2` produced the July 8-23 current-traffic regime and July 24-31 nowcast. Proposed output: `data/derived/hormuz_m8q_5_current_traffic_oil_scenarios.csv`. Do not edit sibling input datasets or chart files.
- 2026-08-03: Added `scripts/build_m8q_5_current_traffic_oil_scenarios.py` and generated `data/derived/hormuz_m8q_5_current_traffic_oil_scenarios.csv` (369 data rows). Registered the output in `data/manifest.csv`. The builder reads all three sibling inputs and fails if the 3.5 tanker-calls/day PortWatch anchor or required adjustment-evidence rows change unexpectedly.

## Method

The output deliberately contains two different accounting frames:

1. `physical_supply_bridge`: gross missing Hormuz flow minus incremental Gulf bypass and incremental non-Gulf production equals net global supply loss. These are alternatives within one identity, not additive categories.
2. `market_clearing_bridge`: foregone counterfactual stock build plus government/obligated emergency releases, commercial/other stock draws, demand reduction, and residual equals the same net global supply loss. These components must not be added to the physical bridge.

Historical March-June net global supply loss uses the frozen February EIA STEO monthly supply forecast minus the July STEO's preliminary monthly supply estimate. This preserves seasonal variation and produces 9.80, 12.58, 14.13, and 10.74 mb/d losses in March-June. Public IEA level/change estimates of 10.1, 12.8, 13.6, and 9.4 mb/d are retained as cross-checks. June therefore remains a real relaxation rather than being overwritten by a constant-closure assumption.

Historical demand reduction is the frozen February EIA monthly consumption forecast minus the July-vintage estimate. The avoided pre-war build is February-vintage supply minus consumption. Historical total-stock flow uses the latest public IEA monthly ledger: 129 mb March draw, 117 mb April draw, 73 mb revised May draw, and 21 mb June net build. July uses a visibly labeled low-confidence proxy of 68.2 mb, derived from EIA's 2.2 mb/d 3Q draw forecast. The mismatch between EIA's modeled balance and IEA's observed-stock ledger remains in the residual.

July 1-7 retains the EIA July forecast completed on July 1. July 8-31 switches to the current-traffic nowcast after renewed escalation. PortWatch is observed only through July 23; July 24-31 holds the July 8-23 average and is not described as actual oil flow. The resulting full-July net-supply-loss range is 9.65-12.59 mb/d, with an 11.43 mb/d base estimate.

## Current-Traffic Oil Mapping

PortWatch's July 8-23 mean is 3.5 tanker calls/day, or 6.4% of its 2019-2024 call baseline. This rate selects the traffic regime but is never multiplied by a cargo-size factor. The oil mapping instead uses:

- IEA pre-war Hormuz flow of about 20 mb/d;
- March-May Hormuz flow averaging 2.7 mb/d;
- current IEA description on July 21: below late-June highs but considerably above early-March to mid-June levels;
- alternative-route exports of 7.2 mb/d in early April versus less than 4 mb/d pre-war;
- June total Gulf exports of 16.1 mb/d versus 24 mb/d pre-war, which is treated as a temporary-reopening outcome rather than the current baseline;
- the IEA's 0.6 mb/d upward revision to Americas supply growth as the central near-term non-Gulf production response.

The resulting current-state assumptions are:

| Case | Inferred Hormuz oil flow | Incremental Gulf bypass | Incremental non-Gulf supply | Net global supply loss |
|---|---:|---:|---:|---:|
| low supply / stress | 3.0 mb/d | 3.0 mb/d | 0.4 mb/d | 13.6 mb/d |
| base | 4.0 mb/d | 3.3 mb/d | 0.6 mb/d | 12.1 mb/d |
| high supply / resilient | 5.5 mb/d | 3.8 mb/d | 0.9 mb/d | 9.8 mb/d |

The range is intentionally wider than PortWatch's sampling interval. It covers AIS-dark movements, direction and loading ambiguity, cargo mix, barrels drawn from Gulf inventories, and the fact that production can lag exports.

## Durability Rules

- Gulf bypass: demonstrated infrastructure continues, but incremental throughput tapers across Q4 and Q1 for maintenance, terminal, security, and Bab el-Mandeb risk. Base incremental bypass is 3.3 mb/d through September, 3.1 mb/d in Q4, and 2.9 mb/d in 1Q27.
- Non-Gulf supply: only incremental production versus the frozen outlook is credited. Base supply rises from 0.6 mb/d through September to 0.8 mb/d in Q4 and 1.0 mb/d in 1Q27. The 3.5 mb/d Atlantic Basin export shift is not counted as new production.
- Government and obligated emergency stocks: July-end history uses the evidence table's 290/315/330 mb range. Future base releases taper from 1.4 mb/d through September to 0.6 mb/d in Q4 and 0.3 mb/d in 1Q27. Base cumulative releases reach 483 mb by March, still below the IEA's gross lower bound of more than 1 billion barrels of government-controlled stocks; the model does not assume all of that gross stock is usable.
- Commercial and other stocks: future draw rates taper as working inventories approach operational minima. China government ownership is not inferred from aggregate stock movement. Oil on water is not counted as new supply.
- Demand: base reduction is 4.5 mb/d through September, 4.8 mb/d in Q4, and 5.2 mb/d in 1Q27. This includes involuntary shortage and conservation. Refinery cuts and unquantified fuel switching are not separate additive buckets.
- Residual: absorbs statistical discrepancy, EIA/IEA balance differences, unobserved stocks, cargo timing, and future under-adjustment. It widens with the horizon instead of being assigned mechanically to demand or stocks.

## Provisional Results

All volumes below are cumulative from 2026-03-01, not incremental from July:

| Horizon | Low-supply loss | Base loss | High-supply loss | Base residual |
|---|---:|---:|---:|---:|
| 2026-09-30 | 2,661 mb | 2,534 mb | 2,338 mb | 410 mb |
| 2026-12-31 | 3,931 mb | 3,647 mb | 3,231 mb | 550 mb |
| 2027-03-31 | 5,191 mb | 4,736 mb | 4,095 mb | 715 mb |

In the base March 2027 bridge, the 4,736 mb cumulative net supply loss is absorbed by 1,256 mb of foregone counterfactual stock builds, 483 mb of emergency releases, 532 mb of commercial/other stock draw, 1,751 mb of demand reduction, and a 715 mb residual. The shares are provisional scenario accounting, not causal estimates.

## Source Breadcrumbs

- EIA February 2026 frozen STEO workbook: https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
- EIA July 2026 STEO workbook and global-oil discussion: https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx and https://www.eia.gov/outlooks/steo/report/global_oil.php
- IEA July OMR: https://www.iea.org/reports/oil-market-report-july-2026
- IEA June adjustment commentary: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
- IEA 21 July oil-market statement: https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
- IMF PortWatch methodology: https://portwatch.imf.org/pages/data-and-methodology

## Validation

- `.venv/bin/python scripts/build_m8q_5_current_traffic_oil_scenarios.py`: wrote 369 rows and validated unique IDs, expected input anchors, output schema, source fields, and all nine horizon bridges.
- Each horizon's market-clearing components sum to net global supply loss within 0.001 million barrels.
- `low_supply > base > high_supply` for cumulative net supply loss at all horizons.
- No chart file, sibling input dataset, issue location/status, price forecast, or dependency was changed by this task.
- 2026-08-03: Root integration review accepted the low/base/high model as a provisional, explicitly low-fidelity scenario input. The physical and market-clearing frames remain separate, the nine horizon identities close within 0.001 million barrels, and the traffic-to-oil mapping is appropriately bounded rather than mechanically inferred from vessel calls.
