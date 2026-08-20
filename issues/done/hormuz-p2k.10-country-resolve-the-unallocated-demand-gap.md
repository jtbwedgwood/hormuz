---
id: "hormuz-p2k.10"
title: "Country-resolve the unallocated 56% of the demand gap"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "demand"
  - "country-detail"
  - "middle-east"
blocked_by: []
blocks:
  - "hormuz-p2k.3"
children: []
owner: "codex-root"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T23:00:00Z"
---

# Country-resolve the unallocated 56% of the demand gap

## Description

The March-July demand gap of 566.4 mb is only partially country-resolved, and the
unresolved portion is exactly where the most consequential human and economic stories are.

| Geography | mb | Fidelity |
|---|---:|---|
| China | 120.0 | EIA STEO country row |
| India | 41.1 | EIA STEO country row |
| Japan | 19.5 | EIA STEO country row |
| Brazil | 9.6 | EIA STEO country row |
| Russia | 9.1 | EIA STEO country row |
| **Middle East** | **173.5** | **regional total, no country split** |
| **Asia/Oceania excl. China, India, Japan** | **146.2** | **regional total, no country split** |
| Africa | 35.1 | regional total, no country split |
| South Korea | 30.6 | low-confidence imputation nested inside residual Asia |

**About 320 mb, or 56% of the demand gap, has no country resolution.** The named countries
are largely tier-2 industrial stories: refinery runs, petrochemical feedstock, naphtha. The
unresolved regions are where the tier-3 candidates live — Southeast Asian rationing, Middle
East product scarcity, African import and foreign-exchange constraints.

This blocks `hormuz-p2k.3`, which cannot build a credible mechanism-by-country cost tier
matrix while more than half the barrels sit in two undifferentiated regional buckets.

## Two scale mismatches to fix while doing this

1. **Period.** These figures are March-**July** (566.4 mb) while the absorption bridge is
   March-**June** (439.2 mb). Any country table published alongside the bridge must be
   restated on the matched frame or clearly labelled.
2. **Forecast contamination.** China's 120.0 mb includes **29.05 mb of July forecast**; the
   March-June figure is **90.94 mb**. The same correction is needed for every country row
   before they are compared with observed March-June evidence.

## Acceptance Criteria

- A March-June country demand table for as many countries as public data supports, with
  explicit fidelity labels distinguishing EIA country rows, JODI-derived estimates, national
  statistics and project imputations.
- Middle East decomposed at least between Saudi Arabia, Iran, UAE, Iraq, Kuwait and Qatar, or
  an explicit statement of why it cannot be, given that this is the second-largest single
  bucket in the entire demand gap.
- Residual Asia/Oceania decomposed to at least South Korea, Taiwan, Singapore, Indonesia,
  Thailand, Vietnam, Malaysia and Australia, or the same explicit statement.
- South Korea's 30.6 mb either upgraded to an observation or retained as an imputation with
  its nesting inside residual Asia made unmissable, so it is never added twice.
- All country rows restated on the matched March-June frame with July forecast removed.

## Notes

JODI-Oil is the most likely route to country-level non-OECD demand, with the caveat that its
publication lag reached only April 2026 as of the last project check, and that submission
completeness varies sharply by country. Where JODI is unavailable, national statistical
offices and refinery-run data are the fallback, with the standing caution from `p2k.4` that
refinery runs are not final consumption.

## Source Leads

- `data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv`
- JODI-Oil: https://www.jodidata.org/oil/
- EIA STEO country tables in the February and July workbooks
- IEA Oil Market Report regional demand commentary, March-July 2026

## Work Notes

- 2026-08-06: Claimed by the parent agent. The country table will use the EIA February-to-July
  vintage difference only where an actual STEO country series exists; JODI apparent-demand
  changes and national refinery/product indicators will be kept as allocation evidence rather
  than silently substituted for the EIA counterfactual. All closing allocations will use the
  March-June regional totals and retain nested/imputed flags.
- 2026-08-06: Completed `data/derived/hormuz_p2k_10_country_demand_resolution.csv`
  (39 rows) with reproducible builder
  `scripts/build_p2k_10_country_demand_resolution.py`. The corrected March-June denominator is
  439.228 mb worldwide. The exact STEO rows are 134.865 mb for the Middle East, 256.089 mb for
  Asia/Oceania, 90.943 mb for China, 33.540 mb for India and 16.231 mb for Japan. This leaves
  115.375 mb in Asia/Oceania after China, India and Japan, of which the existing South Korea
  imputation is 24.400 mb and explicitly nested rather than additive.
- 2026-08-06: Public STEO does not supply the required Gulf or residual-Asia country series.
  The ledger therefore closes those regional denominators using neutral 2024 EIA petroleum-
  consumption shares, plainly labelled low-fidelity project allocations. That produces, among
  others, Saudi Arabia 52.394 mb, Iran 28.427 mb, Iraq 15.310 mb, UAE 12.669 mb; and—after
  South Korea—Indonesia 14.527 mb, Singapore 13.232 mb, Thailand 12.250 mb, Australia 10.223
  mb and Taiwan 7.777 mb. These are pressure-location scaffolds, not observations.
- 2026-08-06: JODI March-May year-on-year apparent-product demand is retained only as a
  non-additive cross-check because it uses a different counterfactual and has uneven stock and
  submission coverage. It supports a material South Korean contraction but does not upgrade
  the 24.400 mb frozen-February-path estimate into an observation. Builder checks enforce
  world-to-region closure, allocation closure, South Korea nesting and unique row IDs.
