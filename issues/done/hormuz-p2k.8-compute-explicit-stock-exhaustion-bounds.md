---
id: "hormuz-p2k.8"
title: "Compute explicit stock exhaustion bounds instead of declining to divide"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-p2k"
labels:
  - "oil"
  - "stocks"
  - "spr"
  - "durability"
blocked_by: []
blocks: []
children: []
owner: "codex-p2k-stock-bounds"
created_at: "2026-08-06T00:00:00Z"
updated_at: "2026-08-06T19:45:00Z"
---

# Compute explicit stock exhaustion bounds instead of declining to divide

## Description

`docs/hormuz-shock-absorption-durability.md` and
`data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv` record the U.S. SPR at
**304.809 mb on 31 July 2026** and a July draw rate of **0.596 mb/d**, then record
`headroom_days_at_current_rate: unknown` and decline to divide, on the correct but
unhelpful grounds that days-to-zero is not days-to-binding-floor.

This is an over-refusal. Days-to-zero is a legitimate and clearly labelled **upper bound**,
and withholding it leaves the durability epic without its single most concrete output. The
correct fix is to publish bounds with explicit labels, not to publish nothing.

### Arithmetic currently missing

- U.S. SPR at the July rate: 304.809 / 0.596 = **511 days**, about 24 December 2027.
- U.S. SPR at the March-June rate of 0.736 mb/d (89.786 mb over 122 days): **414 days**,
  about 18 September 2027.
- IEA government stocks: the reported >1,000 mb lower bound against a ~2.2 mb/d collective
  release pace (290 mb over the 132 days from 11 March to 21 July) gives roughly **455 days**.

Each is an upper bound because real floors bind earlier. Stating that is the point.

### Floors are more computable than currently claimed

- **The 90-day obligation is a published IEA rule.** Members must hold 90 days of net
  imports. With public net-import data this yields a computed floor rather than an unknowable
  one. The complication is that the obligation is met by government *plus* obligated
  industry stocks, so the government-only floor requires the stock-category split; that is a
  harder problem than currently stated, but not an unknowable one.
- **The U.S. SPR level appears to be at a multi-decade low.** 304.809 mb is below the
  post-2022-drawdown trough of roughly 346 mb, which would make it the lowest since about
  the mid-1980s. This should be verified against the full EIA weekly history and stated if
  it holds; it is a striking and checkable fact currently absent from the analysis.
- **Rate capacity degrades before volume exhausts.** DOE's 4.4 mb/d nominal maximum applies
  at high inventory; cavern pressure falls as volume falls. Any public DOE or GAO material on
  the rate-versus-inventory relationship should be used, and its absence stated explicitly if
  it cannot be found.

## Acceptance Criteria

- Days-to-zero published for the U.S. SPR and the IEA government aggregate, at more than one
  observed draw rate, each labelled **upper bound**.
- A computed or explicitly bounded 90-day-obligation floor, with the government versus
  obligated-industry split handled or its absence stated.
- Verification of whether 304.809 mb is a multi-decade U.S. SPR low.
- `headroom_days_at_current_rate` populated in the balance sheet with bounds rather than
  `unknown`, retaining a separate field for the binding-floor estimate.
- A one-sentence publishable claim of the form "the U.S. SPR cannot sustain the current draw
  rate beyond roughly N months even on the most permissive assumption."

## Notes

The principle to carry forward: **a clearly labelled bound is more useful than a refusal.**
Where a floor genuinely is not public, say so and still publish the bound that is computable.

## Source Leads

- EIA weekly SPR series, full history: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
- DOE SPR quick facts and drawdown capability: https://www.energy.gov/ceser/spr-quick-facts
- IEA oil security and the 90-day obligation: https://www.iea.org/topics/oil-security
- `data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv`

## Work Notes

- 2026-08-06: Claimed for a standalone, reproducible bounds audit. Shared p2k.1 files will
  be left to the coordinating agent; this task will supply exact integration fields and rows.
- 2026-08-06: Built `scripts/build_p2k_8_stock_exhaustion_bounds.py`, producing the
  12-row, 28-field `data/derived/hormuz_p2k_8_stock_exhaustion_bounds.csv`; registered it
  once in `data/manifest.csv`.

### Explicit exhaustion arithmetic

- The 31 July U.S. SPR level is **304.809 mb**. At the exact 26 June-31 July endpoint
  draw of 20.846 mb over 35 days (**0.5956 mb/d**), physical zero is **511.768 days**
  away, or **16.81 months**, around **24 December 2027**. This is the requested
  most-permissive upper bound; an operational or policy floor binds no later than that.
- At the project March-June calendar-accounting rate, 89.786 mb over 122 days
  (**0.735951 mb/d**), physical zero is **414.170 days**, or **13.61 months**, around
  **18 September 2027**. The literal 27 February-26 June weekly-endpoint interval is 119
  elapsed days; its **0.754504 mb/d** rate produces **403.986 days**, around 7 September.
  Both are published so the accounting convention is not mistaken for an observation.
- Publishable sentence: **The U.S. SPR cannot sustain the latest 0.596 mb/d draw beyond
  roughly 17 months even if every last barrel were usable; real operational and policy
  limits can only shorten that window.**
- For IEA members, 1,000 mb divided by the 11 March-21 July collective pace of 290/132
  (**2.19697 mb/d**) is **455.172 days**; at the IEA-reported May flow of 2.5 mb/d it is
  **400 days**. However, the IEA level is *greater than* 1,000 mb, and the flow includes
  government plus obligated-industry stocks. Therefore 400/455 are lower bounds on a
  hypothetical days-to-zero calculation, **not strict upper bounds on the actual aggregate
  zero date**. Days to country-specific binding floors may still be much shorter. The issue's
  original claim that 455 is itself an upper bound is directionally useful but mathematically
  false given a lower-bound numerator.

### Floors and release-rate evidence

- The freely accessible IEA April 2026 table reports aggregate IEA net importers at **136
  days** of prior-year net imports: **78 industry + 58 public**. Against the 90-day rule,
  industry cover leaves a minimum aggregate public contribution of max(0, 90-78) = **12
  days** and at most **46 public-stock days** above the aggregate obligation. National law,
  location and non-fungibility reduce freely usable headroom, so the public headroom bound
  is **0-46 days**, not automatically 46.
- The same IEA table classifies the **United States as a net exporter**. Consequently the
  IEA 90-day rule creates a **zero-barrel U.S. SPR statutory floor**. DOE's 411 mb = 125
  days statement uses crude net imports and is not the IEA all-petroleum calculation. The
  decision-relevant U.S. floor remains operational/political, not statutory.
- GAO-26-106918 provides the missing public rate-versus-inventory evidence. As of December
  2025, DOE estimated **2.700 mb/d effective draw capability versus 4.415 mb/d design**
  (61%); more than one quarter of the 413 mb snapshot was unavailable because of construction
  and cavern outages. Bayou Choctaw and West Hackberry together held 139 mb but had only
  1.200 mb/d effective capability versus 1.815 mb/d design, with low cavern inventory
  explicitly cited. DOE separately says 4.4 mb/d can last up to 90 days and then declines.
  No current numeric curve from total inventory to draw rate was found.
- Full EIA weekly history verifies that 304.809 mb was the **lowest level since 18 February
  1983**, when stocks were 303.746 mb; the following week was 305.348 mb. The correct
  headline is lowest in more than 43 years, not merely since the mid-1980s.

### Primary sources

- EIA weekly SPR history: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
- DOE Quick Facts: https://www.energy.gov/hgeo/opr/spr-quick-facts
- DOE FAQ: https://www.energy.gov/hgeo/opr/spr-faqs
- GAO-26-106918: https://files.gao.gov/reports/GAO-26-106918/index.html
- IEA stock methodology/table: https://www.iea.org/data-and-statistics/data-tools/oil-stocks-of-iea-countries
- IEA April table API: https://api.iea.org/netimports/monthly?year=2026&month=04
- IEA July release/remaining-stock statement: https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
- IEA May 2.5 mb/d release pace: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock

### Integration and validation

- Sent the coordinating agent exact p2k.1 integration values and the crucial IEA bound
  caveat before touching shared balance-sheet or reader-facing files.
- After receiving the coordinating agent's explicit clearance, updated and regenerated
  `scripts/build_p2k_1_absorption_buffer_balance_sheet.py` / its CSV, updated
  `docs/hormuz-shock-absorption-durability.md`, and recorded the handoff in p2k.1's issue.
  `memo-us-spr-current.headroom_days_at_current_rate` is now a **0-511.767965 day**
  days-to-binding-floor interval whose upper endpoint is labelled physical zero; the IEA
  memo carries both the 400/455-day arithmetic and its lower-bound-numerator caveat.
- Builder regenerates in `.venv`, compiles, emits uniform rows and unique row IDs, asserts
  the 512/414/455-day arithmetic and 12/46-day IEA floor calculation, and passes
  `git diff --check`. No price forecast or price inference appears.
