---
id: "hormuz-m8q.1"
title: "Build February-July 2026 monthly oil balance and counterfactual panel"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "iea"
  - "eia"
  - "monthly-balance"
blocked_by: []
blocks:
  - "hormuz-m8q.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-03T22:57:25Z"
updated_at: "2026-08-03T23:13:57Z"
---

# Build February-July 2026 monthly oil balance and counterfactual panel

## Description

Extract and normalize the February-July 2026 IEA OMR and EIA STEO evidence needed to measure monthly and cumulative realized oil-supply disruption. Preserve source vintages, actual/preliminary/forecast status, and the June partial reopening.

## Acceptance Criteria

- A long-form derived CSV records observation month, publication vintage, source, status, metric, geography, value, unit, definition, confidence, and citation.
- Metrics cover global supply, demand, stock change, affected Gulf supply or shut-ins, refinery runs, and available Hormuz/export/bypass anchors.
- The frozen February pre-war counterfactual is distinguishable from later revised forecasts.
- July values are included where reasonably estimated or forecast, with explicit labels.
- A concise issue-note handoff identifies disagreements and values suitable for cumulative accounting.

## Work Notes

- 2026-08-03: Started as part of the first `hormuz-m8q` parallel pass. Proposed output: `data/derived/hormuz_m8q_1_monthly_oil_balance.csv`. Do not edit the traffic dataset or the separate response-channel evidence table owned by sibling tasks.
- 2026-08-03: Built `data/derived/hormuz_m8q_1_monthly_oil_balance.csv` with 155 rows and 17 fields. `scripts/build_m8q_1_monthly_oil_balance.py` downloads the six official EIA STEO archive workbooks, extracts the world rows from Tables 3c and 3e without third-party packages, derives same-vintage supply-minus-consumption balances, adds official IEA headline observations, validates IDs/schema/months/citations, and writes the CSV. No package or `requirements.txt` change was needed.
- 2026-08-03: **Latest-data convention:** cumulative publication charts may run through **2026-07-31**, but must label the endpoint `July 2026 forecast (EIA July STEO, forecast completed 2026-07-01)`. June is the latest month with preliminary IEA supply, stock, Gulf export, and Gulf production observations. There is no July IEA monthly actual in the 10 July OMR; July supply, demand, and implied stock change in this panel are EIA forecasts.
- 2026-08-03: **Status convention:** in each STEO vintage, months before the publication month are labeled `preliminary_estimate`; the publication month and later months are `forecast`. EIA itself groups estimates and forecasts in shaded cells and notes that the break is approximate. IEA rows preserve finer labels such as `revised_preliminary_estimate`, `point_in_time_estimate`, and `period_average_estimate`. Values should never be selected merely by last non-null row: choose the desired vintage and status explicitly.

### Frozen February counterfactual versus July STEO vintage

The following values come directly from the February and July EIA archive workbooks. Supply and consumption are petroleum and other liquid fuels. `Delta` is July-vintage value minus the frozen 10 February forecast, in mb/d.

| Month | Feb forecast supply | Jul-vintage supply | Supply delta | Feb forecast demand | Jul-vintage demand | Demand delta | Jul implied stock change |
|---|---:|---:|---:|---:|---:|---:|---:|
| Feb | 106.814 | 108.695 | +1.882 | 104.475 | 104.279 | -0.195 | +4.416 |
| Mar | 107.182 | 97.382 | -9.800 | 103.286 | 101.982 | -1.304 | -4.600 |
| Apr | 107.482 | 94.901 | -12.581 | 104.089 | 99.910 | -4.179 | -5.009 |
| May | 107.604 | 93.478 | -14.127 | 104.293 | 99.764 | -4.529 | -6.287 |
| Jun | 108.203 | 97.460 | -10.744 | 105.842 | 101.407 | -4.434 | -3.948 |
| Jul | 108.357 | 99.232 | -9.125 | 105.675 | 101.574 | -4.101 | -2.342 |

- 2026-08-03: On this EIA basis, cumulative March-June supply was **1,441.5 million barrels below** the frozen February monthly forecast; demand was **439.2 million barrels below** forecast. The same-vintage implied balance moved from a counterfactual **396.1 million-barrel build** to a **606.2 million-barrel draw**, a 1,002.2 million-barrel deterioration. Extending through July adds a forecast month: March-July supply is **1,724.4 million barrels below** the frozen forecast, demand is **566.4 million barrels below**, and the balance deteriorates by **1,158.0 million barrels** (from a 479.2 mb build to a 678.8 mb draw). Identity: supply shortfall minus demand shortfall equals balance deterioration. These are forecast-vintage differences, not a uniquely identified causal decomposition.
- 2026-08-03: Independent IEA anchors broadly corroborate the physical profile. Its latest reported supply levels are 97.0 mb/d in March, 95.1 in April, 94.5 in May, and 98.8 in June. Its loss measures are 10.1 mb/d versus February in March, 12.8 in April, 13.6 in May, then 9.4 in June after the partial reopening. Applying those rates to calendar days gives about 1.40 billion barrels of March-June supply loss, close to the EIA frozen-forecast result but not definitionally identical.
- 2026-08-03: **Do not merge unlike outage measures.** EIA July estimates Middle East **crude** shut-ins of 11.2 mb/d in May and 8.3 mb/d in June. IEA reports broader **total-oil** global/pre-war losses of 13.6 and 9.4 mb/d and Gulf production 11.4 mb/d below pre-war in June. Keep crude shut-ins, Gulf total-oil loss, and world total-oil/liquids shortfall as separate metrics.
- 2026-08-03: **Stock-series disagreement is large and analytically useful.** Latest available IEA observed-inventory estimates sum to a 298 mb draw over March-June (-129, -117, -73, +21 mb), whereas the July STEO supply-minus-consumption balance implies a 606 mb draw. IEA also revised May from -143 mb in its June OMR to -73 mb in July. The global bridge must state whether it uses observed/visible inventory coverage or a model-implied total balance and carry the gap as coverage/statistical residual; it must not average the two.
- 2026-08-03: **June relaxation is explicit.** IEA reports June global supply +4.1 mb/d to 98.8, Gulf production +3.5 mb/d, and Gulf exports +6.5 mb/d to 16.1. Exports rose faster than production because stored/floating barrels were released; June oil on water rose 117 mb while onshore inventories still fell 96 mb. This is why the scenario history should preserve June rather than extend the March-May closure regime mechanically.
- 2026-08-03: IEA June commentary gives the best route-period anchor: Hormuz oil flow averaged 2.7 mb/d in March-May versus roughly 20 mb/d pre-war. It also reports early-June Saudi exports via Yanbu above 5 mb/d and UAE total exports at 4.3 mb/d versus 1.9 mb/d in March. These are period/point estimates, not full monthly cargo balances; the CSV labels them accordingly.

### Source breadcrumbs

- EIA STEO archive index and workbooks (release dates 10 Feb, 10 Mar, 7 Apr, 12 May, 9 Jun, 7 Jul): https://www.eia.gov/outlooks/steo/outlook.php and `https://www.eia.gov/outlooks/steo/archives/{feb26|mar26|apr26|may26|jun26|jul26}_base.xlsx`
- EIA July global-oil narrative, including May/June Middle East crude shut-ins and 2Q/3Q inventory-balance estimates: https://www.eia.gov/outlooks/steo/report/global_oil.php
- IEA OMR February-July 2026: https://www.iea.org/reports/oil-market-report-february-2026 ; https://www.iea.org/reports/oil-market-report-march-2026 ; https://www.iea.org/reports/oil-market-report-april-2026 ; https://www.iea.org/reports/oil-market-report-may-2026 ; https://www.iea.org/reports/oil-market-report-june-2026 ; https://www.iea.org/reports/oil-market-report-july-2026
- IEA June adjustment commentary and Kpler-based route/export chart notes: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
