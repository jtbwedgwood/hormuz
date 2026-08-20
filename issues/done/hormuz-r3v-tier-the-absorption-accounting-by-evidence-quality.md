---
id: "hormuz-r3v"
title: "Tier the Hormuz absorption accounting by evidence quality"
type: "epic"
status: "done"
priority: "P0"
parent: ""
labels:
  - "oil"
  - "uncertainty"
  - "synthesis"
  - "review"
blocked_by: []
blocks:
  - "hormuz-ccx.1"
  - "hormuz-ccx.5"
children:
  - "hormuz-r3v.1"
  - "hormuz-r3v.2"
  - "hormuz-r3v.3"
  - "hormuz-r3v.4"
  - "hormuz-r3v.5"
  - "hormuz-r3v.6"
  - "hormuz-r3v.7"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T23:59:00Z"
---

# Tier the Hormuz absorption accounting by evidence quality

## Description

External-review workstream opened after a consultant read of
`hormuz-historical-oil-accounting-march-july-2026.md` and
`hormuz-inventory-and-demand-residual-stories.md`.

The two-stage physical/market-clearing framework and the double-counting discipline in
those documents are sound. The gap is not rigor, it is **framing of uncertainty**. Three
defects motivated this epic:

1. **No tier rollup.** The derived CSVs carry `confidence` and `estimate_type` per row, but
   nothing ever totals barrels by evidence quality. The reader cannot answer "how much of
   this do we actually know?" without reading two documents end to end.
2. **The largest slice is an accounting plug.** EIA's "implied inventory draw" is defined as
   supply minus demand minus expected build, so `arithmetic_residual` is 0.000000 in every
   month of `hormuz_m8q_4_cumulative_global_oil_accounting.csv` by construction. Presenting
   it as a co-equal absorption bucket alongside demand and foregone build obscures that it
   absorbs all balance error. Model error was then effectively booked a second time inside
   the m8q.11 residual scenarios.
3. **No Hormuz counterfactual.** The whole reconstruction rests on frozen-February versus
   July STEO vintages, which capture everything that changed EIA's mind since February, not
   only the closure.

## Acceptance Criteria

- Every barrel in the market-clearing bridge carries an explicit evidence tier, and the
  tiers total to the net global supply loss.
- The size of the honest "we do not know" bucket is stated as a number with a range, not as
  prose caveats.
- The unreconciled balance plug is presented as a sibling of the other absorption slices,
  never as a subcomponent of inventory draw.
- One diagram shows rerouting and market clearing together without double counting.
- The China coordinated-drawdown claim is addressed directly, with the strongest available
  evidence on both sides.

## Work Notes

- 2026-08-05: Opened. `hormuz-r3v.1` is complete and delivers the tiered ledger, the
  waist-node Sankey and `docs/hormuz-what-happened-to-the-barrels.md`. Headline result on
  the matched March-June frame: **T1 observed 157.1 mb (10.9%), T2 reasonably assumed
  396.1 mb (27.5%), T3 educated guess 492.3 mb (34.2%), T4 unknown 396.0 mb (27.5%)**.
- 2026-08-05: The China question resolves consistently with `hormuz-s49.3`. No change to
  that issue's conclusion is warranted; the new document restates it for a general reader
  and adds the definitional trap (EIA reports Chinese government plus NOC-commercial stocks
  together as "strategic inventories") as the most likely source of the stronger public
  claims.
- 2026-08-05: `.2` through `.5` were opened after the initial synthesis. The expectation
  that `.2` would cheaply move substantial barrels into T1 was tested rather than assumed.
- 2026-08-05: Claimed `.2`-.5 after user review. Priority is `.2`, `.4`, and `.5`. The
  price-path work in `.3` is retained only as contextual market evidence; it must not infer
  physical shortage severity mechanically from flat price because news, risk premia,
  expectations, policy, and macro factors can dominate. `.4` explicitly tests rather than
  assumes the document's claim that a roughly 300 mb balance residual over the four-month
  March-June frame is ordinary.
- 2026-08-05: Completed `.3` as a deliberately low-weight price context. Public daily Brent,
  WTI and the Brent-WTI spread are now reproducible through 27 July. No current public
  futures time-spread series was available from the EIA workbook, which ends in April 2024.
  Price is not used to infer the size of the supply loss or 308 mb residual.
- 2026-08-05: Completed `.2`. Exact usable February-June Eurostat observations for Austria,
  Belgium and Finland net to a 0.859 mb build, not the expected large draw. Czechia's 12.7 mb
  apparent draw fails a continuity screen. Japan's 72.136 mb late-June estimate is retained
  as a strong provisional cross-check but not T1 because the endpoint volume is derived from
  days of cover. Korea and most large EU series lack June tank endpoints.
- 2026-08-05: Completed `.4`. The 308.171 mb base discrepancy equals 2.526 mb/d over 122
  days and is exceptional in the bounded historical benchmark: above all six documented
  annual interagency ranges and 1.94 times the largest. Three-agency and observed-vintage
  sensitivity gives a 2.760/308.171/413.700 mb residual range. This is model/vintage
  disagreement, not a range for hidden physical inventory.
- 2026-08-05: Completed `.5`. The preferred empirical March-June Hormuz-plausible band is
  1,309-1,468 mb for supply and 325-497 mb for demand, after removing Russia and applying
  signed p10-p90 ordinary-revision benchmarks from 2017-19 and 2023-25. The 1,441 mb supply
  figure remains the exact revision-path fact, not a causal point estimate.
- 2026-08-05: Propagated all four audits through r3v.1 and the synthesis. Final base tiers
  are T1 156.244 mb (10.8%), T2 396.078 (27.5%), T3 466.871 (32.4%), and T4 422.284
  (29.3%). Total T4 sensitivity is 116.873-527.813 mb. All child tasks are done; epic closed.
- 2026-08-06: Completed follow-up `.6`. The historical literature supports calling the
  308.171 mb item a large, historically legible preliminary-balance discrepancy—not a normal
  four-month residual and not 308.171 mb of measured hidden barrels. The closest cumulative
  precedent found is opposite-sign 1998 H1 (325.7 mb over six months, 1.799 mb/d); same-sign
  2003 episodes were about 1.6-1.7 mb/d versus 2.526 mb/d here. GAO and later methodology
  literature support both data/model error and unreported stocks but cannot identify their
  shares. `data/derived/hormuz_r3v_6_missing_barrels_evidence.csv` records the full search,
  historical comparisons and mechanism ranking.
- 2026-08-06: Reopened `.3` narrowly for the p2k.13 storage discriminator. Public convenience
  histories, checked against CME commentary and the 5 August official bulletin, show WTI
  front-minus-December backwardated on 84/84 March-June observations and Brent on 82/84.
  This is medium-weight evidence against profit-seeking carry storage, not evidence against
  blocked cargo, congestion, sanctions dwell or mechanically required voyage float. Price
  remains contextual and is not used to infer the physical shortage or forecast a path.
- 2026-08-06: Completed `.7`. The earlier 261.36 mb IEA comparator is retired because it
  mixed a quarterly call-on-DoC with chained-vintage monthly OPEC+ crude production rather
  than computing global demand minus total supply. The exact public Q2 EIA-IEA gap is 2.110
  mb/d: 59.4% demand and 40.6% supply. The published supply buckets put essentially all of
  the latter outside DoC crude, so no p2k.7 bypass uplift is warranted. March IEA demand
  remains non-public; the new artifact carries explicit sensitivity instead of a false point.
  The r3v.1 plug range is correspondingly narrowed to 238.171/308.171/347.571 mb using only
  observed-stock vintage sensitivity, and total T4 to 352.284/422.284/461.684 mb.
