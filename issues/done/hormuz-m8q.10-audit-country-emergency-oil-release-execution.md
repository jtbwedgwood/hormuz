---
id: "hormuz-m8q.10"
title: "Audit country execution of March-July emergency oil releases"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "stocks"
  - "country-ledger"
  - "execution-audit"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-04T20:15:00Z"
updated_at: "2026-08-04T21:35:00Z"
---

# Audit country execution of March-July emergency oil releases

## Description

Separate the IEA's 19 March provisional 426 million barrel contribution table from barrels actually delivered through 21 July. Build a country-level execution audit that distinguishes public stocks, obligated-industry stocks, exchange contracts, physical stock declines, and the Canada/Mexico production component.

## Acceptance Criteria

- The ledger reproduces the IEA provisional country allocation and its 280 million barrel public-stock, 119 million barrel obligated-industry, and 28 million barrel production split.
- U.S. rows distinguish exchange announcements and awards from weekly EIA SPR stock declines, and compare the frozen February STEO July stock forecast with the latest July observation.
- Japan rows distinguish national stocks, private obligated stocks, producer-country joint stocks, planned site releases, and receiver-confirmed monthly stock changes.
- Material European contributors use the latest Eurostat emergency-stock observations without treating a net stock decline as a complete measure of gross program delivery.
- Country execution that is not directly observable is shown as a bounded or top-down allocation inference, never as an official observation.
- Country base estimates reconcile exactly to the IEA statement that around 290 million barrels had been released by 21 July, while the reconciliation method and simultaneous-range caveat remain explicit.

## Work Notes

- 2026-08-04: Claimed for the expanded historical accounting. The core methodological distinction is between (1) oil authorized or made available, (2) contracts awarded, (3) obligation relief, (4) reported tank-level decline, and (5) the IEA's top-down estimate of oil actually released. Only the fifth is a complete collective-action total as of 21 July.
- 2026-08-04: Primary starting sources are the IEA 19 March provisional contribution table and the IEA Executive Director's 21 July statement. National implementation checks use EIA weekly U.S. SPR data and February STEO, U.S. DOE award/delivery notices, Japan METI dated site schedules and monthly reserve statements, and Eurostat dataset `nrg_stk_oilm`.
- 2026-08-04: Built `data/derived/hormuz_m8q_10_emergency_release_execution.csv` with 82 rows and 24 fields. The ledger contains all 30 provisional country contributions, the IEA's rounded 280 million barrel public-stock / 119 million obligated-industry / 28 million production / 426 million headline summaries, national implementation milestones, physical stock observations, and a mutually exclusive country decomposition of the IEA's rounded 290 million barrel actual-release estimate.
- 2026-08-04: The 19 March rounded country entries sum to 426.2 million barrels. Removing the Canada and Mexico production contributions (23.6 and 3.9 million) leaves a 398.7 million barrel stock-release envelope. The IEA's rounded channel totals sum to 427 million against the 426 million headline, a source-rounding issue. Canada/Mexico production is not counted in the 21 July 290 million barrel stock-release reconciliation.
- 2026-08-04: U.S. EIA weekly SPR stocks were 415.441 million barrels on 27 February, 311.447 million on 17 July, and 307.650 million on 24 July. The observed 27-February-to-24-July tank draw is 107.791 million barrels. Aligning to the IEA's 21 July statement gives 103.994-107.791 million barrels, with a four-of-seven-day interpolation of 106.163714 million as the base. This corrects an earlier three-of-seven-day interpolation in exploratory work.
- 2026-08-04: The frozen February STEO forecast a 423.861 million barrel U.S. SPR at July end, 8.420 million above the 27 February weekly level. The 24 July observation was already 116.211 million below that counterfactual. A deliberately low-fidelity July-end nowcast is 107.791-115.385 million barrels drawn from 27 February, base 111.588, implying a 303.853 million barrel stock and a 120.008 million barrel gap from the February forecast.
- 2026-08-04: U.S. DOE implementation notices separately identify 45.2 million barrels awarded on 20 March, 8.5 million on 10 April, 26.0 million on 17 April, and 53.3 million on 11 May; DOE said more than 10 million had been delivered by 17 April and about 35 million by 11 May. These are milestones, not additive to the physical tank draw. Exchange barrels have contractual return obligations and are therefore temporary supply support.
- 2026-08-04: Japan's official product-equivalent stocks fell from February to April by 35.79 million barrels in national stock, 12.89 million in private obligated stock, and 10.06 million in producer-country joint stock: 58.746825 million barrels total. METI's two later national-crude schedules were 8.5 and 5.8 million kl, or 89.944283 million barrels together. The reconciliation therefore uses a 58.746825 observed floor, 79.8 initial IEA allocation as base, and 89.944283 later-schedule sensitivity as high. The high is not a simultaneous IEA-allocation estimate.
- 2026-08-04: Eurostat emergency-stock net changes from February through May, converted at a generic 7.33 bbl/tonne, yield positive observed floors of 2.695534 million barrels for Germany and 12.086825 million for Italy; France and Spain emergency-stock levels rose, so their observed floors are zero. A zero floor is not proof of zero gross release because replenishment, transfers, and reclassification can mask delivery. Italy's collective-action attribution is capped at its 10 million barrel IEA allocation.
- 2026-08-04: The country base reconciliation to the IEA's **around** 290 million barrels as of 21 July is: U.S. 106.163714; Japan 79.8; Italy 10.0; South Korea 15.477809; Germany 13.414101; France 10.043378; United Kingdom 9.630636; Spain 7.979670; Türkiye 8.048460; other IEA stock contributors 29.442231 million barrels. After fixing the U.S., Japan, and Italy, the remaining 94.036286 million is allocated at a common 68.7902602% of provisional stock contributions. Those remaining country values are low-to-medium-confidence inference, not reported national execution.
- 2026-08-04: Marginal country bounds are included, but must not be summed into a global low/high range: U.S. 103.994-107.791; Japan 58.746825-89.944283; Italy 10.0-12.086825; South Korea 0-22.5; Germany 2.695534-19.5; France 0-14.6; UK 0-14.0; Spain 0-11.6; Türkiye 0-11.7; other members 0-42.8 million barrels. The exact 290.000 closure is presentational discipline around the IEA's rounded aggregate, not false precision about each country.
- 2026-08-04: Regeneration first queries the official EIA and Eurostat APIs and falls back to embedded official observations extracted on 4 August when an endpoint is throttled or unavailable. Validation passed: 82 unique row IDs, 24 columns, compilation, exact source-summary values, reconciliation within CSV rounding (`289.999999`), and `git diff --check`.
- 2026-08-04: This audit supersedes the coarse country execution split in m8q.8 for the emergency-release slice only. It does not supersede m8q.8 demand/stock context or m8q.7 non-Gulf production estimates.
