---
id: "hormuz-p2k.5"
title: "Quantify remaining foregone-build capacity from the pre-war forward path"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "stocks"
  - "surplus"
  - "durability"
blocked_by: []
blocks:
  - "hormuz-p2k.1"
children: []
owner: "p2k_foregone_build"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-05T23:30:00Z"
---

# Quantify remaining foregone-build capacity from the pre-war forward path

## Description

The 396.08 mb "expected inventory build that did not occur" is about 27.5% of March-June
absorption, and it is the least understood channel because it is not a mechanism at all —
it is the absence of accumulation.

The frozen February 2026 STEO expected an implied global build of **2.4 to 3.9 mb/d** across
March-July (3.897, 3.393, 3.311, 2.362 and 2.682 mb/d respectively, per
`data/derived/hormuz_m8q_4_cumulative_global_oil_accounting.csv`). That is not a seasonal
wiggle. It is a structural surplus: the world was heading into a glut.

### The headline this supports

**The Hormuz shock hit a market that was expecting a substantial surplus, and roughly a
quarter of the absorption was simply that surplus failing to materialize.** The same physical
disruption into a tight market would have been materially more damaging. This is one of the
strongest and most policy-relevant findings available from the existing data.

### The forward question, and the trap in it

The February STEO forecast horizon extends beyond the disruption window, so a pre-war
expected-build path exists for future periods and can be extracted.

**Do not simply sum the remaining forecast builds.** Foregone build is not a buffer that is
drawn down; it only exists as a cushion while the underlying market is in surplus. Once the
market is in deficit there is nothing left to fail to accumulate. The February path is also
stale by construction: its expectation of a late-2026 or 2027 build was conditioned on
earlier periods building too, which did not happen.

The correct question is therefore not "how many forecast build barrels remain" but
"**how much genuine surplus, if any, does the market still have, and under what assumptions**."

## Acceptance Criteria

- Extraction of the frozen February 2026 implied-build path for all remaining forecast
  periods, with the seasonal and structural components distinguished.
- An explicit statement of the seasonal pattern: global stocks typically build in the first
  half during refinery turnarounds and seasonally weaker northern-hemisphere demand, then
  draw in the second half. March-June is normally a building window, so the February forecast
  was ordinary in direction, if not in magnitude.
- A defensible answer to whether any foregone-build cushion remains, with the staleness
  caveat handled rather than ignored.
- Comparison against the July-vintage forward path to see how much surplus EIA still expects
  after the shock.
- A counterfactual sensitivity: how much larger the observed absorption burden would have
  been had the pre-war market been balanced or tight rather than in surplus.

## Source Leads

- EIA STEO February 2026 workbook, full forecast horizon: https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
- EIA STEO July 2026 workbook for the post-shock forward path
- IEA commentary on the pre-war surplus: https://www.iea.org/commentaries/as-oil-market-surplus-keeps-rising-something-s-got-to-give
- `data/derived/hormuz_m8q_4_cumulative_global_oil_accounting.csv`

## Work Notes

### Deliverables and method

- Added `scripts/build_p2k_5_foregone_build_capacity.py` and
  `data/derived/hormuz_p2k_5_foregone_build_capacity.csv` (74 rows). The builder downloads
  the official frozen-February and post-shock July EIA STEO workbooks and extracts world
  petroleum-and-other-liquids production and consumption for every month from January 2026
  through December 2027. Positive production minus consumption is an implied build; it is
  neither observed inventory nor an already-held reserve.
- The seasonal/structural split is deliberately transparent. For each vintage and calendar
  year, `structural_balance_mb_d` is the day-weighted annual mean and
  `seasonal_deviation_mb_d` is the monthly balance less that mean. The two close exactly to
  the monthly balance. This is a descriptive decomposition, not an estimated normal-season
  model.
- Added monthly rows, annual structural summaries, decision-relevant period summaries,
  March-June balanced/tight-market sensitivities and three integration verdict rows. The
  artifact is registered in `data/manifest.csv`.

### Seasonal direction versus structural scale

The useful stylized seasonal prior is that global crude stocks tend to build during
lower-demand/refinery-turnaround windows in the first half and draw as demand strengthens in
the second half. March-June is therefore an ordinary **direction** for a build. This must not
be over-generalized: crude and individual product stocks have different cycles, refinery
maintenance can build crude while drawing products, and fall is also a major turnaround
season. EIA notes that refinery outages are concentrated in the first quarter and fall when
total demand is seasonally low, while its product-market explainer documents different
gasoline and distillate inventory cycles:

- https://www.eia.gov/petroleum/articles/refoutagesindex.php
- https://www.eia.gov/finance/markets/products/balance.php

The February path was not mainly a seasonal wiggle. Its implied balance was positive in all
24 months through December 2027. The day-weighted structural mean was **3.051 mb/d in 2026**
and **2.680 mb/d in 2027**, or 1,113.461 mb and 978.205 mb respectively. Of the **396.078 mb**
March-June expected build, **372.171 mb (94.0%)** is the simple 2026 structural mean times
122 days and only **23.907 mb (6.0%)** is the within-year seasonal deviation. The exact split
depends on the stated decomposition, but the conclusion does not: magnitude, persistence and
all-positive monthly signs identify a structural-surplus forecast.

The independent IEA pre-war narrative supports that reading. In October 2025 it reported a
1.9 mb/d January-September surplus and said the projected 2026 overhang was approaching
4 mb/d, attributing it to OPEC+ and non-OPEC+ supply growth against tepid demand. The IEA and
EIA figures are corroborating context, not additive series:
https://www.iea.org/commentaries/as-oil-market-surplus-keeps-rising-something-s-got-to-give

### What remains in the two forecast paths

| Forecast slice | Frozen February | Post-shock July | Interpretation |
|---|---:|---:|---|
| Jul-Dec 2026 | +539.141 mb (+2.930 mb/d) | +46.883 mb (+0.255 mb/d) | July net hides a continuing Q3 draw. |
| Aug-Dec 2026 | +455.992 mb (+2.980 mb/d) | +119.493 mb (+0.781 mb/d) | Relevant remaining months as of this audit. |
| Aug-Sep 2026 | +163.248 mb (+2.676 mb/d) | **-131.946 mb (-2.163 mb/d)** | July vintage has no near-term foregone-build cushion. |
| Oct-Dec 2026 | +292.743 mb (+3.182 mb/d) | **+251.440 mb (+2.733 mb/d)** | Conditional late-year surplus returns. |
| Calendar 2027 | +978.205 mb (+2.680 mb/d) | **+1,836.441 mb (+5.031 mb/d)** | Large conditional structural surplus, not banked capacity. |

The July 2027 surplus is larger than February's because both sides changed: July forecasts
2027 supply averaging 109.839 mb/d versus February's 108.753, while demand averages
104.808 mb/d versus February's 106.073. Thus the extra 2.351 mb/d surplus is roughly half
higher supply and half lower demand. It is not evidence that 1.836 bn barrels are available
to absorb a continued closure.

### Remaining-cushion verdict

**Credit zero durable foregone-build headroom in the buffer balance sheet.** The historical
396.078 mb is fully spent because it was accumulation that did not happen. Forecast
accumulation is a flow conditional on future supply exceeding demand, not a stock level or a
capacity ceiling.

For scenario work, retain two explicitly conditional sensitivities instead:

1. The July path still requires a 131.946 mb draw in August-September, so there is no
   near-term cushion even in EIA's post-shock forecast.
2. A 251.440 mb Q4 build and 1,836.441 mb 2027 build can reduce the marginal burden **only if**
   the July path's reopening, production recovery and demand assumptions materialize. Under
   continued current-level Strait traffic, the embedded Gulf supply recovery is stale and
   these volumes must not be summed into available headroom. The frozen February path is
   useful as the historical counterfactual but is even staler as a forward forecast.

Integration rows are `verdict-durable-buffer-credit`, `verdict-near-term-july-path` and
`verdict-later-surplus-sensitivities`.

### Balanced/tight pre-war counterfactual

The March-June frozen-February surplus was **396.078 mb**, 27.5% of the 1,441.477 mb physical
supply-path shortfall. Because that passive cushion existed, lower consumption plus actual
implied draws had to absorb 1,045.399 mb. Holding the physical shortfall fixed gives:

| Pre-war balance assumption | Required active absorption | Increase versus frozen-February case |
|---|---:|---:|
| Frozen February: +3.247 mb/d build | 1,045.399 mb | -- |
| Balanced: 0 mb/d | 1,441.477 mb | +396.078 mb (+37.9%) |
| Tight: 1 mb/d expected draw | 1,563.477 mb | +518.078 mb (+49.6%) |
| Tight: 2 mb/d expected draw | 1,685.477 mb | +640.078 mb (+61.2%) |

This sensitivity supports the policy-relevant claim that the same physical disruption would
have demanded much more active stock draw and/or demand reduction in a balanced or tight
market. It does not claim all behavioral and supply responses would otherwise have remained
unchanged.

### Verification

- `.venv/bin/python scripts/build_p2k_5_foregone_build_capacity.py` wrote 74 rows.
- `.venv/bin/python -m py_compile scripts/build_p2k_5_foregone_build_capacity.py` passed.
- Row IDs and manifest dataset IDs are unique. Every monthly row satisfies
  `structural + seasonal = implied balance` within rounding tolerance.
- The directly extracted February March-June build is 396.077697 mb, matching the upstream
  rounded 396.078 mb bridge input.
