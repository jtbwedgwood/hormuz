---
id: "hormuz-r3v.1"
title: "Build the confidence-tiered absorption ledger and waist-node Sankey"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "uncertainty"
  - "figure"
  - "synthesis"
blocked_by: []
blocks:
  - "hormuz-r3v.2"
  - "hormuz-r3v.4"
  - "hormuz-r3v.5"
children: []
owner: "claude"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T23:59:00Z"
---

# Build the confidence-tiered absorption ledger and waist-node Sankey

## Description

Answer the question the existing accounting does not answer directly: of all the oil shut in
by the Hormuz closure, how much do we actually know the fate of, and how much is honestly
unknown? Deliver one diagram that shows rerouting and market clearing together without
double counting.

## Acceptance Criteria

- Every market-clearing barrel carries an evidence tier; tiers total to the net supply loss. **Met.**
- The unknown bucket is a stated number. **Met: base 422.3 mb (29.3%), with a 116.9-527.8 mb model/vintage sensitivity (8.1%-36.6%).**
- The unreconciled plug is a sibling of the other absorption slices. **Met.**
- One non-double-counting diagram. **Met via the waist-node design.**

## Work Notes

- 2026-08-05: Added `scripts/build_r3v_1_confidence_tiered_absorption.py`, producing
  `data/derived/hormuz_r3v_1_confidence_tiered_ledger.csv`,
  `figures/fig-r3v-hormuz-absorption-sankey.svg` and its figure-data CSV. Wrote
  `docs/hormuz-what-happened-to-the-barrels.md`.

### Result

On the matched March-June 2026 frame, against the 1,441.477 mb net global supply loss:

| Tier | Meaning | mb | Share |
|---|---|---:|---:|
| T1 | Directly observed | 156.24 | 10.8% |
| T2 | Reasonably assumed | 396.08 | 27.5% |
| T3 | Educated guess | 466.87 | 32.4% |
| T4 | Unknown | 422.28 | 29.3% |

T4 is the 308.171 mb balance plug plus a 114.113 mb empirical allowance for Russia and
ordinary forecast revision inside the demand gap.

- 2026-08-05 r3v.4 propagation (later superseded for the fixed demand-unknown term by the
  r3v.5 integration below): Added low/base/high columns to the ledger. The
  unreconciled plug is now 2.760/308.171/413.700 mb, based on the public IEA/EIA/OPEC and
  observed-stock vintage envelope. Total T4 is 90.562/395.973/501.502 mb. The existing
  Sankey remains base-case geometry but labels the 3-414 mb plug range. This is an
  epistemic sensitivity, not a confidence interval or estimate of hidden tanks.

- 2026-08-05 r3v.2/r3v.5 propagation: Split the exact-window Austria, Belgium and Finland
  observations out of the mixed rest-of-world inventory row. Their signed total is a
  0.859 mb build, so strict T1 falls slightly rather than rising; Japan's 72.136 mb derived
  late-June estimate remains a provisional cross-check outside T1. Replaced the old
  proportional 87.8 mb demand-unknown slice with r3v.5's 114.113 mb empirical uncertainty
  allowance. With the r3v.4 residual range, total T4 is now 116.873/422.284/527.813 mb.

- 2026-08-06 r3v.7 correction: Retired the invalid 2.760-413.700 mb cross-scope agency
  range. Holding EIA's 606.171 mb implied draw fixed and varying only the public IEA
  observed-stock vintage gives a current **238.171/308.171/347.571 mb** plug sensitivity.
  Total T4 is therefore **352.284/422.284/461.684 mb**. Base geometry and tier shares do
  not change; the ledger and Sankey annotations now use the observed-vintage range.

### Design decisions worth preserving

- **Waist node.** The Sankey runs missing transit → net global supply loss → absorption.
  Bypass and non-Gulf production are terminal off-ramps *upstream* of the waist; demand and
  stocks are *downstream*. Because they sit on opposite sides, nothing double counts, which
  is what previously forced the analysis into two separate framings.
- **The plug is not a stock category.** EIA's 606.171 mb implied draw is split into the
  298.000 mb observed composite and the 308.171 mb residual, presented as siblings. Filing
  the residual under inventory draw implies it is a kind of stock movement; it is not, and
  the IEA's own miscellaneous-to-balance definition says as much.
- **Model error is no longer booked twice.** Previously the implied draw absorbed all balance
  error, and the m8q.11 scenario then assigned a further ~123 mb of the residual to EIA
  balance error. The top-level split removes the duplication.
- **Demand response is bounded, not identified.** The T4 allowance comes from the r3v.5
  ordinary-revision benchmark; only the remaining three shock-response stories retain the
  relative shares from the earlier scenario work.
- **T1 is deliberately conservative.** Japan's strong 72.136 mb provisional cross-check is
  not a directly reported June tank volume, and the large Czech June break fails a continuity
  screen. Exact observed builds remain negative rather than being converted to zero.

### Verification

The build script asserts, and the run passes: Frame A components sum to the 1,924.6 mb
denominator; Frame B slices sum to the 1,441.477 mb waist; observed draw plus residual equals
the implied draw; the four demand mechanisms sum to the demand gap; and the four tier totals
sum to the waist. SVG text extents were checked programmatically against the canvas under
pessimistic font metrics; no overflow. Note that `qlmanage` previews crop this figure to a
square and are not a reliable check on it.

### p2k.12 oil-on-water boundary propagation

- 2026-08-06: Added three non-additive memos: 316/351/386 mb onshore-accessible draw,
  220.171/255.171/290.171 mb apparent unmatched-boundary residual, and zero valid same-bound
  closure. The additive 298 mb observed draw, 308.171 mb plug, tier totals and Sankey are
  intentionally unchanged.
