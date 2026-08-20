---
id: "hormuz-r3v.5"
title: "Separate the Hormuz effect from ordinary forecast revision"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "counterfactual"
  - "attribution"
  - "method"
blocked_by: []
blocks: []
children: []
owner: "codex-subagent"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-05T16:50:00Z"
---

# Separate the Hormuz effect from ordinary forecast revision

## Description

This is the deepest structural weakness in the historical accounting. Every headline number
derives from "frozen February 2026 STEO versus July 2026 STEO." That difference captures
**everything that changed EIA's mind since February**, of which Hormuz is only one part. It
also contains:

- ordinary demand and supply marks that would have happened with no closure at all;
- taxonomy, seasonal-adjustment and product-reclassification changes between vintages;
- unrelated events, most clearly the Russia-Ukraine refinery damage that puts Russian supply
  39.11 mb below the February path and accounts for nearly all of the Eurasian demand gap.

The current documents flag this qualitatively but never size it, so the 566.36 mb demand
slice silently credits ordinary revision to the war. The r3v.1 ledger makes a first attempt
by carrying the residual-stories "structural trend and ordinary revision" share across to the
March-June frame, giving **87.8 mb**, and classing it T4. That is almost certainly a floor.

## Acceptance Criteria

- An empirical baseline for ordinary STEO revision magnitude: distribution of five-month-ahead
  supply and demand revisions across recent non-crisis STEO vintage pairs, so a "normal"
  revision band exists to compare against.
- A decomposition of the February-to-July revision into Hormuz-plausible versus
  would-have-happened-anyway, at least at region level, with the method stated.
- Explicit removal or separate labelling of clearly non-Hormuz components, Russia being the
  clearest case.
- A revised headline that distinguishes "global supply was 1.44 bn bbl below the February
  path" from "Hormuz caused X bn bbl of supply loss," with X carrying a range.
- Propagation into the r3v.1 tier tally, since a larger ordinary-revision term moves barrels
  from T3 into T4.

## Notes

A clean causal counterfactual is not achievable with public data and should not be promised.
The realistic goal is a defensible band plus an honest statement that the headline is a
revision comparison, not a causal estimate. The alternative — continuing to present a vintage
difference as if it were a Hormuz effect — is the single most criticizable claim in the
project.

## Source Leads

- EIA STEO archive for non-crisis vintage pairs: https://www.eia.gov/outlooks/steo/archives/
- Existing vintage comparison: `data/derived/hormuz_m8q_1_monthly_oil_balance.csv`
- Non-Gulf supply detail incl. Russia: `data/derived/hormuz_m8q_7_nongulf_supply_ledger.csv`

## Work Notes

- 2026-08-05: Claimed for parallel work. Construct empirical non-crisis five-vintage-month
  revision distributions for supply and demand, remove named non-Hormuz components where
  possible, and produce a causal-attribution band rather than a point estimate.
- 2026-08-05: Added `scripts/build_r3v_5_ordinary_steo_revision_baseline.py` and
  `data/derived/hormuz_r3v_5_ordinary_steo_revision_baseline.csv`. The build downloads the
  February and July EIA STEO archive workbooks for 2017-19, 2023-26 and reproduces both the
  March-June matched frame and the March-July headline frame. It stores all raw vintage-pair
  revisions, three reference distributions, region diagnostics, Russia removal, preferred
  causal-plausible bands, conservative sensitivities, and one r3v.1 propagation row.

### Sign convention and reference sample

Every revision is **February vintage minus July vintage** for the same monthly supply or
demand values, multiplied by days in month. Positive therefore means that the July vintage
put supply or consumption below the February path. This is exactly the convention used by
the existing 2026 accounting.

The primary `ordinary plus background news` reference sample is 2017, 2018, 2019, 2023,
2024 and 2025. Pandemic years 2020-21 and the invasion-onset year 2022 are deliberately
excluded. The retained years are not event-free: they contain weather, OPEC decisions,
sanctions and ordinary macro/data news. Accordingly, the empirical band is a scale benchmark,
not a formal no-Hormuz counterfactual or confidence interval. Separate pre-COVID 2017-19 and
post-COVID 2023-25 subsets are included in the CSV as sensitivity checks.

### Preferred attribution method

Russia is removed from both the 2026 target and every reference-year world total before the
ordinary-revision adjustment. This avoids subtracting the 2026 Russia component once by name
and again through a world baseline that contains Russia. The preferred range subtracts the
signed p10-to-p90 world-ex-Russia reference distribution from the 2026 world-ex-Russia
revision. The full observed reference-year min/max is retained as a deliberately conservative
sensitivity. A band endpoint can exceed the observed net global revision: that occurs when
the reference distribution implies that ordinary revision would have raised supply or demand,
partly offsetting rather than causing the observed downward 2026 mark.

This is a bounded causal-plausibility exercise, not an identified treatment effect. In
particular, the ordinary revision process may itself change during a shock, six reference
years are too few to estimate tails precisely, and revisions can include taxonomy changes.

### Results: distinguish revision-path facts from Hormuz-plausible effects

| Frame | Quantity | Frozen-February minus July vintage | Named Russia component | 2026 ex-Russia revision | Preferred Hormuz-plausible band | Full historical-envelope sensitivity |
|---|---|---:|---:|---:|---:|---:|
| March-June | Supply | 1,441.5 mb | 27.4 mb | 1,414.1 mb | **1,309.2-1,467.7 mb** | 1,258.6-1,472.1 mb |
| March-June | Demand | 439.2 mb | 6.4 mb | 432.8 mb | **325.1-497.2 mb** | 312.9-527.9 mb |
| March-July | Supply | 1,724.4 mb | 39.1 mb | 1,685.3 mb | **1,538.7-1,742.1 mb** | 1,505.6-1,756.0 mb |
| March-July | Demand | 566.4 mb | 9.1 mb | 557.3 mb | **449.5-634.9 mb** | 439.0-671.3 mb |

The revised wording should therefore be: **global oil supply was 1.441 bn bbl below the
frozen February path in March-June (1.724 bn bbl in March-July); a defensible empirical
Hormuz-plausible range is about 1.31-1.47 bn bbl through June and 1.54-1.74 bn bbl through
July.** Do not call the vintage differences themselves causal estimates.

The result is robust in scale. Before Russia removal, the six March-July reference-year
global supply revisions ranged from -50.7 to +178.1 mb and demand from -129.5 to +122.9 mb.
The 2026 revisions are 1,724.4 and 566.4 mb: supply is 9.7 times the largest prior downward
revision, and demand 4.6 times the largest prior downward revision. Ordinary revision is
material for honest uncertainty, but cannot plausibly explain most of the 2026 gap.

### Regional demand diagnostic

| Region | 2026 March-July revision | Reference p10-p90 | Reference min-max |
|---|---:|---:|---:|
| North America | -16.6 mb | -31.2 to 66.1 | -37.6 to 74.5 |
| Central and South America | 8.4 mb | -25.9 to 12.9 | -36.1 to 14.5 |
| Europe | 29.7 mb | -25.4 to 19.9 | -32.5 to 26.8 |
| Eurasia | 9.4 mb | -24.1 to 8.9 | -33.1 to 11.4 |
| Middle East | **173.5 mb** | -19.2 to 5.5 | -24.5 to 6.3 |
| Africa | 35.1 mb | -6.3 to 20.7 | -8.8 to 28.7 |
| Asia and Oceania | **326.9 mb** | -40.8 to 45.1 | -46.7 to 90.3 |

Asia/Oceania and the Middle East contribute 500.4 mb of the 566.4 mb global demand revision
and are radically outside every reference-year result. This is the strongest region-level
evidence that most of the demand mark is shock-related. North America and Central/South
America are ordinary-sized. Europe's and Africa's gaps are only modestly beyond the historical
envelope. Eurasia is ordinary-sized, and Russia supplies 9.1 of its 9.4 mb downward revision;
it should remain separately labelled as non-Hormuz rather than used as closure evidence.

Regional non-OPEC supply rows are also retained for diagnosis but are not addable to world
supply and cannot capture OPEC country effects. The global supply series is the controlling
causal-band input.

### r3v.1 propagation handoff

The CSV row `r3v1-march-june-demand-t4-revision-allowance` equals **114.113 mb**: the
positive 6.382 mb Russia demand revision plus the **107.732 mb p90 absolute** March-June
world-ex-Russia ordinary revision. This is an uncertainty reserve, not a point estimate of
barrels proven unrelated to Hormuz. It should replace, not supplement, the earlier 87.802 mb
structural/ordinary T4 demand slice in r3v.1. Holding the March-June market bridge fixed and
rescaling the other three speculative demand mechanisms proportionally would move 26.311 mb
from T3 to T4: T3 becomes approximately **466.0 mb (32.3%)** and T4 **422.3 mb (29.3%)**;
T1 and T2 remain 157.1 and 396.1 mb. The parent synthesis owner will perform that integration
to avoid concurrent edits.

### Named non-Hormuz evidence and source caveats

- The same EIA vintage pair puts Russian oil supply 27.4 mb below the February path through
  June and 39.1 mb below it through July. IEA's July OMR explicitly reported that intensified
  Ukrainian attacks on Russian refinery and export infrastructure affected crude runs,
  exports and domestic deliveries. This supports separate labelling, but the EIA Russia row
  is still a revision rather than a strike-by-strike causal estimate.
  Source: https://www.iea.org/reports/oil-market-report-july-2026
- Reuters reported IEA's estimate that May Russian crude output was 8.7 mb/d, about 10% below
  target amid the attacks. This is corroborating analyst/news context, not an additive barrel
  row. Source: https://uk.marketscreener.com/news/ukrainian-attacks-push-russian-oil-output-10-below-target-in-may-iea-says-ce7f5cdcdd81f527
- Primary input workbooks are the official EIA STEO archives, linked row by row in the CSV:
  https://www.eia.gov/outlooks/steo/archives/

### Verification

- `.venv/bin/python scripts/build_r3v_5_ordinary_steo_revision_baseline.py` wrote 417 rows.
- `.venv/bin/python -m py_compile scripts/build_r3v_5_ordinary_steo_revision_baseline.py`
  passed.
- The build checks duplicate row IDs. All raw source rows carry geography, taxonomy, both
  vintage URLs, sign convention, confidence, causal warning and double-counting rule.
