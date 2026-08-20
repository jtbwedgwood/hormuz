---
id: "hormuz-a4d"
title: "Refresh blog-bearing evidence to the August 2026 vintage"
type: "epic"
status: "done"
priority: "P0"
parent: null
labels:
  - "blog"
  - "refresh"
  - "august-omr"
  - "accounting"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children:
  - "hormuz-a4d.1"
  - "hormuz-a4d.2"
  - "hormuz-a4d.3"
  - "hormuz-a4d.4"
  - "hormuz-a4d.5"
  - "hormuz-a4d.6"
  - "hormuz-a4d.7"
  - "hormuz-a4d.8"
  - "hormuz-a4d.9"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T20:00:00Z"
---

# Refresh blog-bearing evidence to the August 2026 vintage

## Description

The whole repo is built on the **July 2026** IEA OMR and the **July 2026** EIA STEO. The
August OMR (and August STEO) have since published, and the blog draft is being written for a
**mid-August 2026** publication date. This epic refreshes **only the evidence that a claim in
the blog draft actually rests on**. It is explicitly *not* a mandate to re-run every analysis
in `data/derived/`.

Scope discipline: if a number does not appear in, or directly underwrite, a sentence in
`blogpost/` or the draft outline, leave it at its current vintage and say so.

Claims in the draft that depend on a refresh (implicit ones included):

- 1,925 mb missing Hormuz transit; 2.7 mb/d Mar-May and 8.9 mb/d June Hormuz flow
- 300-430 mb incremental bypass; 57 mb net non-Gulf supply gain (US +65, Brazil +32, Russia -27)
- 1,441 mb net supply shortfall and the 1,300-1,500 mb Hormuz-plausible band
- 298 mb observed stock draw (90 US SPR + 67 US commercial + 141 rest-of-world); 351 mb ex-oil-on-water
- 396 mb foregone build (2.4-3.9 mb/d Feb STEO expectation)
- 439 mb demand reduction; 308 mb unexplained residual
- Q2 interagency gap: 1.3 mb/d demand, 0.9 mb/d supply, 295 mb -> 103 mb
- Middle East demand reduction ~135 mb, ~12.5% of prewar regional demand
- "traffic has never come close to prewar levels"; the July re-closure; the current regime
- US SPR draw rate and remaining runway (Impacts/US section)

## Acceptance Criteria

- Every blog-bearing number above is either (a) restated on the August vintage with the
  delta from the July vintage documented, or (b) explicitly confirmed unchanged.
- `docs/hormuz-what-happened-to-the-barrels.md` and
  `docs/hormuz-historical-oil-accounting-march-july-2026.md` carry an August-vintage cutoff line.
- A short delta table (July vintage -> August vintage) exists so the draft can be edited
  by find-and-replace rather than re-reasoned.
- Anything that moved by more than its stated uncertainty band is flagged for narrative
  rewrite, not just number substitution.

## Dependency Notes

- Blocks: `hormuz-ccx.5` - Draft blog post from evidence package

## Work Notes

- 2026-08-18: All nine child tasks completed. The preferred blog frame is now March-July,
  because July is a past-month estimate in the August STEO rather than a July-vintage forecast.
- 2026-08-18: Short headline delta table for draft revision (million barrels unless noted):

  | Claim | July-vintage value | August-vintage value | Draft action |
  |---|---:|---:|---|
  | Global supply shortfall, Mar-Jun | 1,441.48 | 1,362.30 | Replace; retain matched route frame |
  | Global supply shortfall, Mar-Jul | 1,724.36 | 1,589.58 | Use as primary frame |
  | Lower consumption, Mar-Jun | 439.23 | 440.44 | Replace |
  | Lower consumption, Mar-Jul | 566.36 | 570.34 | Use as primary frame |
  | Foregone expected build, Mar-Jun | 396.08 | 396.08 | Confirmed unchanged |
  | EIA implied draw, Mar-Jun | 606.17 | 525.79 | Replace |
  | IEA observed draw, Mar-Jun | 298 mixed-vintage | 341 same-vintage | Replace and rewrite provenance |
  | Unexplained residual, Mar-Jun | 308.17 | 184.79 | Narrative rewrite required |
  | Unexplained residual, Mar-Jul | not comparable | 130.01 | Use with primary frame |
  | Net non-Gulf supply gain, Mar-Jun | 56.90 | 79.31 | Replace |
  | Middle East demand revision, Mar-Jul | 173.50 | 150.41 | Replace; 11.1% of prewar demand |
  | Post-8-Jul traffic, total calls/day | 10.6 | 4.125 | Replace; PortWatch also revised baseline |
  | U.S. SPR endpoint | 304.809 mb (31 Jul) | 298.694 mb (7 Aug) | Replace with date |

- 2026-08-18: Narrative rewrites, not number substitutions, are required for four findings:
  the unknown residual roughly halved; July's re-closure produced a substantial price response;
  PortWatch heavily revised both history and the low-regime estimate; and the sourced chronology
  supports severe nonzero controlled transit after reciprocal escalation, not a causally proven
  "full closure because of U.S. violations."
- 2026-08-18: `docs/hormuz-what-happened-to-the-barrels.md` now carries the active August
  synthesis cutoff. `docs/hormuz-historical-oil-accounting-march-july-2026.md` is explicitly
  labeled as a preserved July-vintage audit document and points readers to the August synthesis.
