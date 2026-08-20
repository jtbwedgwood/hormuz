---
id: "hormuz-m8q.6"
title: "Build country-level Gulf physical oil ledger for March-July 2026"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "gulf"
  - "physical-ledger"
  - "2026-actuals"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-04T00:00:00Z"
updated_at: "2026-08-04T08:00:00Z"
---

# Build country-level Gulf physical oil ledger for March-July 2026

## Description

Construct a country-by-country, month-by-month physical ledger of Gulf oil affected by the Hormuz shock. Quantify counterfactual production/export availability, actual or preliminary production and exports, Hormuz transit, non-Hormuz rerouting, storage accumulation or draw, and shut-in or otherwise unavailable supply for Saudi Arabia, UAE, Iraq, Kuwait, Qatar, Iran, and material Oman/Bahrain volumes.

## Acceptance Criteria

- Report March-July cumulative million barrels, with monthly `mb/d` rates retained for audit.
- Separate measured, reported, calculated, and bounded/inferred values and preserve publication vintage.
- Give named-route rerouting estimates for Saudi East-West/Petroline, UAE Habshan-Fujairah, Iraq-Turkey/Ceyhan, and any other material route.
- Preserve the June relaxation and do not infer loaded oil volumes mechanically from vessel-call counts.
- Reconcile country estimates to IEA Gulf/global production and export anchors with an explicit residual.
- Store the ledger in a machine-readable derived dataset, generate it reproducibly, register it in the manifest, and record citation breadcrumbs and double-counting limits here.

## Work Notes

- 2026-08-04: Claimed as a new historical-accounting workstream under `hormuz-m8q`. This ledger is deliberately narrower than the global market-clearing bridge: it follows physical Gulf barrels before reserve releases, demand response, and non-Gulf replacement supply are added.
- 2026-08-04: Created `data/derived/hormuz_m8q_6_gulf_physical_oil_ledger.csv` (102 data rows, 24 fields) and reproducible builder `scripts/build_m8q_6_gulf_physical_oil_ledger.py`; registered the dataset in `data/manifest.csv`.

### Core country result: EIA crude shut-ins through 30 June

EIA's July STEO Table 1 is the strongest public country-level historical source found. It reports February production and March-June estimated closure-related crude shut-ins. Multiplying monthly rates by calendar days gives **1,183.49 million barrels of crude shut in during March-June**:

| country | Feb production (mb/d) | March-June crude shut-in (million bbl) | share |
|---|---:|---:|---:|
| Saudi Arabia | 10.500 | 359.80 | 30.4% |
| Iraq | 4.400 | 358.83 | 30.3% |
| Kuwait | 2.560 | 215.83 | 18.2% |
| UAE | 3.600 | 121.20 | 10.2% |
| Qatar | 0.557 | 57.95 | 4.9% |
| Iran | 3.390 | 52.51 | 4.4% |
| Bahrain | 0.193 | 17.37 | 1.5% |
| **Total** | **25.200** | **1,183.49** | **100%** |

Monthly EIA crude shut-ins were 8.89 mb/d in March, 10.40 in April, 11.20 in May, and 8.29 in June. This cleanly preserves the June relaxation. The implied actual crude-production levels are stored separately; they are not additional ledger contributions.

### Broader total-oil cross-check

- IEA's public total-oil taxonomy is broader than the EIA country crude table. Public anchors are at least 10 mb/d curtailed in March, 14.4 mb/d below pre-war levels in April, more than 14 mb/d shut in around the May report, and 11.4 mb/d below pre-war levels in June.
- A rough calendar integration of those mixed-status anchors is **1,518 million barrels for March-June**. This is not an official monthly IEA series: March and May are point-in-time lower bounds. It is included as a cross-check so condensates and NGLs are not silently omitted.
- IEA independently reported cumulative Middle East producer total-oil losses above **1.3 billion barrels as of 22 June**, consistent in order of magnitude with the broader reconstruction.
- Therefore the defensible historical statement is: **1.183 billion barrels of country-resolved crude shut-ins through June; about 1.5 billion barrels on a broader total-oil basis, with lower confidence.**

### Route reconstruction and physical reconciliation

- IEA reports March-May Hormuz oil flow averaging 2.7 mb/d versus roughly 20 mb/d pre-war. June total Gulf exports were 16.1 mb/d including bypass routes. The ledger infers 8.9 mb/d June Hormuz flow as 16.1 less a 7.2 mb/d alternative-route working estimate; this is not derived from ship calls.
- Gross missing Hormuz flow integrates to **1,924.6 million barrels** over March-June.
- Gross modeled non-Hormuz route exports integrate to **825.7 million barrels**, of which **362.1 million barrels** are incremental to a 3.8 mb/d pre-war alternative-route baseline. A reasonable public-source sensitivity is **300-430 million barrels**.
- Incremental route estimate by component: Saudi East-West/Petroline to Yanbu **319.5 million barrels**; UAE Habshan-Fujairah **76.1 million**; Iraq-Turkiye/Ceyhan **26.25 million**; other-route residual (including Jask/Syria and baseline uncertainty) **-59.75 million**. The negative residual means the named Saudi/UAE/Iraq gains more than explain the aggregate increase from the working pre-war route baseline; it is not evidence of negative physical flow.
- The route arithmetic is: 1,924.6 gross missing Hormuz barrels - 362.1 incremental bypass = **1,562.5 million barrels of route-implied disruption**. EIA country crude shut-ins explain 1,183.49 million; the remaining **379.01 million barrels** is an explicit non-crude/taxonomy/storage/domestic-use/timing residual. This residual must not be presented as a measured product loss.
- March Gulf storage accumulated about **120 million barrels** (+100 floating crude/products, +20 onshore crude), demonstrating why missing transit was not immediately identical to production loss. A low-confidence June timing inference records about **60 million barrels** released from Gulf storage: exports rose 6.5 mb/d while production rose only 3.5 mb/d, and IEA explicitly attributes much of the crude/condensate wave to onshore/floating draws.

### Route-specific evidence and limits

- Saudi Arabia: IEA says Yanbu exports rose from 2 mb/d pre-war to more than 5 mb/d in early June. Aramco separately reports the East-West pipeline reached its 7 mb/d maximum capacity in Q1. The ledger uses a March ramp and a conservative 5 mb/d April-June flow; these are calibrated estimates, not monthly cargo observations.
- UAE: IEA gives the Habshan-Fujairah pipeline 1.8 mb/d capability and says UAE total exports rose from 1.9 mb/d in March to 4.3 mb/d in early June. Dark/STS activity along Oman is treated as Hormuz flow, not pipeline bypass. The 42 million-barrel Mandous complex is a flexibility/capacity fact, not an observed draw volume.
- Iraq: North Oil Company reported 250 kb/d through Ceyhan beginning 18 March. The ledger uses 0.113 mb/d for March (14 days at 250 kb/d) and 0.25 mb/d April-June. This is small relative to Iraq's southern-export loss.
- Kuwait, Qatar and Bahrain have no material public operational bypass route. Iran's Jask terminal is kept inside an aggregate residual because no credible public March-June throughput series was found.
- Oman is not included in the EIA closure-related country shut-in table because its export terminals lie outside Hormuz. It remains relevant as a coastline/STS geography, not as a lost Gulf-producer supply row.

### July cutoff

- As of 2026-08-04, the latest country-resolved official estimate is **June 2026**. EIA explicitly says it publishes only aggregate disruptions for future months and gives a 5.427 mb/d 3Q26 forecast. That forecast predates renewed hostilities on 7-8 July and is not a July actual.
- The dataset contains a July coverage flag and the official 3Q aggregate as forecast context, but excludes it from historical cumulative totals. Assigning July shut-ins to countries would be false precision until the August STEO/OMR or another credible country source is published.

### Source Breadcrumbs

- EIA July 2026 STEO, Table 1 country crude shut-ins and aggregate future forecast: https://www.eia.gov/outlooks/steo/archives/jul26.pdf
- IEA March OMR, at least 10 mb/d Gulf total-oil curtailment including 8 mb/d crude and 2 mb/d condensates/NGLs: https://www.iea.org/reports/oil-market-report-march-2026
- IEA April OMR, Hormuz 3.8 mb/d in early April and alternative routes 7.2 mb/d versus less than 4 pre-war; Gulf storage changes: https://www.iea.org/reports/oil-market-report-april-2026
- IEA May OMR, April affected-Gulf loss and cumulative/response anchors: https://www.iea.org/reports/oil-market-report-may-2026
- IEA July OMR, June reopening, 16.1 mb/d Gulf exports, 11.4 mb/d Gulf production loss, and stock timing: https://www.iea.org/reports/oil-market-report-july-2026
- IEA 22 June adjustment commentary, cumulative losses, routes, Yanbu/UAE exports and Kpler chart definitions: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
- Saudi Aramco Q1 2026, East-West maximum capacity reached: https://www.aramco.com/en/news-media/news/2026/aramco-announces-first-quarter-2026-results
- Iraq/Ceyhan 250 kb/d restart reported by North Oil Company, 18 March: https://www.thenationalnews.com/business/energy/2026/03/18/iraq-to-resume-oil-exports-via-turkeys-ceyhan-port-amid-regional-tensions/

### Validation and completion

- Regenerated the CSV from the repository-local `.venv`, compiled the builder, verified 102 rows and 24 fields, checked that seven country cumulative rows sum exactly to 1,183.49 million barrels, and ran `git diff --check` successfully.
- Acceptance criteria are met for the latest public historical cutoff. July remains explicitly unavailable rather than being backfilled with the future-scenario model.
