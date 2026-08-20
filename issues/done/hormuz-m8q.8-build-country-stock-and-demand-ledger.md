---
id: "hormuz-m8q.8"
title: "Build country-level stock and demand ledger through July 2026"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "stocks"
  - "demand"
  - "country-ledger"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-04T18:45:00Z"
updated_at: "2026-08-04T19:15:00Z"
---

# Build country-level stock and demand ledger through July 2026

## Description

Build the detailed historical stock and demand components needed to explain the March-July oil balance country by country. Separate government releases, obligated-industry relief, commercial inventory change, demand revisions, refinery-run cuts, and structural electrification context.

## Acceptance Criteria

- The U.S. ledger compares the frozen February STEO stock path with weekly actual SPR, commercial crude, and total commercial petroleum stocks through the latest July observation.
- The IEA collective action separates the 19 March provisional country allocation from the 290 million barrels reported delivered through 21 July and from a July-end nowcast.
- China stock rows preserve ownership ambiguity and do not label commercial or operational stocks as government SPR.
- Country and regional demand reductions are calculated monthly against the frozen February 2026 forecast, with March-June preliminary and July forecast statuses explicit.
- Fuel switching, EVs, and renewables are converted into barrels only where an incremental 2026 oil displacement can be defended; structural context already embedded in the February forecast is not added again.
- Each row has low/base/high values where appropriate, source/date/status/confidence, a method, and a double-counting rule.

## Work Notes

- 2026-08-04: Claimed for the historical-accounting expansion. Prior breadcrumbs are `hormuz-m8q.1`, `hormuz-m8q.3`, `hormuz-s49.2`, `hormuz-s49.3`, `hormuz-f6r.2`, and `hormuz-f6r.5`; all are being treated as inputs to refresh rather than final country accounting.
- 2026-08-04: Added `scripts/build_m8q_8_country_stocks_demand_ledger.py` and generated `data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv` with 181 rows and 21 fields. The builder downloads the archived February and July STEO workbooks, parses XLSX XML with the standard library, refreshes three EIA weekly U.S. stock series, and appends sourced national-policy/mechanism rows. No new Python dependency is required.
- 2026-08-04: The exact frozen-February-versus-July STEO demand bridge for March-July is **566.356 million barrels**. The seven region components close to the world total within 0.000004 mb from CSV rounding: Asia/Oceania 326.900 mb, Middle East 173.496 mb, Africa 35.100 mb, Europe 29.701 mb, Eurasia 9.433 mb, Central/South America 8.359 mb, and North America -16.633 mb. March-June are preliminary in the July vintage; July is forecast. This is a forecast revision, not proof that every barrel was causal Hormuz demand destruction.
- 2026-08-04: Named country demand suballocations are China 119.992 mb, India 41.141 mb, Japan 19.522 mb, Brazil 9.577 mb, Russia 9.065 mb, United States -5.561 mb, Canada -10.138 mb, and Mexico -0.937 mb. The Asia/Oceania residual excluding China, India, and Japan is 146.246 mb. South Korea is kept as a low-confidence candidate suballocation of that residual: 7.65/30.60/61.20 mb low/base/high, derived from the earlier 0.05/0.20/0.40 mb/d bounded inference. It is not additive to the residual.
- 2026-08-04: U.S. weekly stocks now run through **24 July**, released 29 July. SPR fell from 415.441 mb on 27 February to 307.650 mb on 24 July, an observed draw of 107.791 mb. The frozen February STEO instead projected a 6.950 mb March-July build; the preferred change-versus-change swing is 114.741 mb. The actual 24 July level is 116.211 mb below the February STEO July-end level, a slightly different endpoint comparison that also contains the February baseline mismatch.
- 2026-08-04: U.S. total commercial crude and petroleum products excluding SPR fell 50.187 mb from 27 February to 24 July, versus a frozen February forecast build of 59.755 mb. The additive change swing is therefore 109.942 mb. Commercial crude alone fell 34.771 mb versus a forecast build of 18.113 mb, but is a memo subset and must never be added to total commercial stocks. SPR plus total commercial stocks delivered 157.978 mb of observed draw; adding 66.705 mb of foregone forecast builds produces a 224.683 mb U.S. stock-path swing.
- 2026-08-04: IEA accounting distinguishes three facts: 400 mb announced on 11 March; a provisional 19 March country table totaling 426 mb (280 public stocks, 119 obligated-industry stocks, and 28 production, subject to rounding); and **290 mb actually delivered in aggregate through 21 July**. The public source does not provide an executed country table. The ledger therefore records plans separately and publishes a deliberately low-confidence country imputation constrained to sum to 290 mb in every case. Only the U.S. portion is directly observed at high frequency. A separate 290/315/330 mb July-end nowcast is an alternative cutoff, not additional supply.
- 2026-08-04: Provisional material country/region plans retained for narrative are U.S. 172.2 mb public stocks; Japan 79.8 mb (54.0 public, 25.8 obligated industry); South Korea 22.5 mb with unresolved split; EU approximately 80 mb; other IEA members 71.5 mb arithmetic residual. The imputed 21 July base split is U.S. 103.994 mb, Japan 61.8 mb, South Korea 15 mb, EU 60 mb, and other members 49.206 mb. Apart from the U.S., these are allocation estimates, not official delivery claims.
- 2026-08-04: China remains ownership-opaque. IEA reported a 40 mb tank build in March and 41 mb draw in June, only a 1 mb net draw across those two known months; April, May, and July ownership-resolved changes are missing. No separately quantified large government-SPR release is supported. EIA's broad estimates of roughly 360 mb government-held and about 1 bn barrels of commercial crude at end-2025 explain why a commercial/operational cushion is plausible without proving government use.
- 2026-08-04: NBS run-cut evidence is quantified but kept nested within the China demand/import/stock bridge. April processing of 54.65 Mt (-5.8% y/y) implies a 24.66 mb crude-throughput shortfall at 7.33 bbl/t; May 53.72 Mt (-9.1%) implies 39.42 mb; June 51.24 Mt (-17.7%) implies 80.78 mb. These are refinery-throughput comparisons, not additive end-use demand destruction.
- 2026-08-04: The ledger explicitly refuses a standalone China renewables/EV barrel slice. Useful facts are recorded in native units: EVs were 48% of new vehicle sales in 2024; China added 356 GW non-hydro renewable capacity in 2024; renewables were 55% of installed generation capacity; in June 2026 NEV output rose 29.4% y/y and solar generation rose 14.2%, while wind fell 5.6% and thermal generation rose 0.5%. The frozen February oil forecast already incorporated structural adoption, installed electric capacity is not oil displacement, and China uses little oil-fired power. IEA's policy tracker likewise has no de-duplicated realized oil-savings volume. These mechanisms stay inside the measured demand gap or residual.
- 2026-08-04: Primary source breadcrumbs, accessed 4 August 2026:
  - EIA February STEO workbook: https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
  - EIA July STEO workbook: https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx
  - EIA weekly SPR: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
  - EIA weekly commercial crude: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCESTUS1
  - EIA weekly total commercial petroleum excluding SPR: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1
  - IEA 11 March collective action: https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict
  - IEA 19 March provisional contributions: https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
  - IEA 21 July delivery statement: https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
  - IEA July OMR: https://www.iea.org/reports/oil-market-report-july-2026
  - EIA China stocks: https://www.eia.gov/todayinenergy/detail.php?id=67504
  - EIA China country analysis: https://www.eia.gov/international/content/analysis/countries_long/China/
  - NBS April, May, and June releases: https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html ; https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html ; https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html
  - IEA policy response tracker: https://www.iea.org/data-and-statistics/data-tools/2026-energy-crisis-policy-response-tracker
- 2026-08-04: Validation passed with `.venv/bin/python`: 181 unique row IDs; 21 uniform columns; exact regional demand closure; imputed IEA country delivery rows sum to 290 mb in low/base/high; script compiles; regeneration succeeds; `data/manifest.csv` parses with one m8q.8 registration; `git diff --check` passes.
