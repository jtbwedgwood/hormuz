---
id: "hormuz-a4d.1"
title: "Ingest the August 2026 IEA Oil Market Report"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-a4d"
labels:
  - "iea"
  - "omr"
  - "inventories"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-a4d.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T00:00:00Z"
---

# Ingest the August 2026 IEA Oil Market Report

## Description

Every IEA-sourced number in the blog draft currently comes from the July OMR or earlier, and
the project's 298 mb stock-draw comparator is a **composite of different OMR vintages** whose
preliminary months moved by tens of mb (March 85 -> 129, April 117 -> 74, May 143 -> 73).
The August OMR is the first vintage that can give a **single same-vintage March-July series**,
which is the single highest-value refresh in this epic: it directly moves the 298 mb observed
draw and therefore the 308 mb residual, which is the draft's entire "What's Happening with
the Gap?" section.

Pull from the August 2026 OMR:

1. Monthly global stock change, March through July, **on the August vintage**, replacing the
   cross-vintage composite. Record OECD/non-OECD and government/industry splits where public.
2. Oil-on-water by month, March-July, to firm up the currently ±35 mb May bound and to test
   whether the June +117 mb was refill or storage.
3. July Hormuz oil flow and total Gulf export rate, so the July re-closure can be quantified
   in barrels rather than only in PortWatch ship calls.
4. Any revision to the March-May 2.7 mb/d Hormuz flow estimate and to the alternative-route
   (bypass) export rate, currently pinned at an early-April 7.2 mb/d figure carried forward.
5. Q2/Q3 demand and supply levels for the interagency comparison, and any newly public
   revised **monthly March demand** (previously subscriber-only, which is what forced the
   300-495 mb IEA-draw sensitivity range).
6. Days of cover / net import cover table update beyond the April table.

## Acceptance Criteria

- A same-vintage August monthly table exists for March-July stock change and oil on water.
- The 298 mb composite is either replaced by a single-vintage figure or explicitly retained
  with a documented reason.
- Restated residual (EIA implied draw minus IEA observed) for both March-June and March-July,
  with the delta versus 308.171 mb stated.
- Updated `data/derived/` artifact and a note in this file's Work Notes on what moved.

## Dependency Notes

- Parent: `hormuz-a4d`
- Blocks: `hormuz-a4d.6` - Rebuild the absorption bridge on the August vintage

## Work Notes

- July-vintage baseline to beat: March -129, April -117, May -73, June +21 mb; composite -298 mb.
- Oil-on-water July vintage: March -117, April +53, May unknown (±35), June +117 mb.
- Source: https://www.iea.org/reports/oil-market-report-august-2026
- 2026-08-18: Claimed for August-vintage ingestion. Scope is confined to public IEA OMR evidence and OMR-derived artifacts; STEO inputs and scripts remain owned by `hormuz-a4d.2`.
- 2026-08-18: Extracted the 12 August public release into
  `data/derived/hormuz_a4d_1_august_omr_stocks.csv` and
  `data/derived/hormuz_a4d_1_august_omr_evidence.csv`, reproducibly built by
  `scripts/build_a4d_1_august_omr.py`. The source URL returned HTTP 200 on 18 August and
  every output row carries the primary IEA citation.
- 2026-08-18: The key same-vintage result is a **410 mb global observed draw in
  March-July** and a **69 mb July draw**, hence an exact **341 mb March-June draw** on the
  August vintage. This replaces the mixed-vintage 298 mb comparator for cumulative
  accounting: observed draw rises by 43 mb. July's 69 mb total draw and 6 mb onshore draw
  imply a **63 mb oil-on-water draw** (`-69 - (-6) = -63`), consistent with the IEA's
  statement that the July decline was almost entirely oil on water.
- 2026-08-18: The public release does **not** disclose August-vintage March-June monthly
  stock or oil-on-water cells. Those tables are part of the subscription product. The
  March-July output therefore has explicit nulls for those four months and exact public
  August-vintage aggregate rows; it does not carry earlier-vintage monthly figures forward
  under an August label. This means the old May +/-35 mb oil-on-water uncertainty cannot be
  resolved from public August material.
- 2026-08-18: Gulf production rose to 23.9 mb/d in July, still 8.3 mb/d below pre-war;
  total regional exports **including bypass routes** averaged 15.0 mb/d, down 2.1 mb/d
  month on month, with loadings falling from a 20 mb/d early-July peak to about 12 mb/d
  later in the month. The monthly change implies 17.1 mb/d for June on the August vintage,
  a +1.0 mb/d revision to July OMR's 16.1 mb/d. Because IEA publishes only the combined
  export figure here, it neither revises the 2.7 mb/d March-May Strait-only estimate nor
  separates a new bypass rate from the carried 7.2 mb/d early-April figure.
- 2026-08-18: Other public August anchors captured in the evidence table: July global
  supply 101.5 mb/d (+2.4 mb/d month on month); July refinery runs 80.9 mb/d; 2Q/3Q demand
  contractions of 4.9/2.8 mb/d year on year; a 1.8 mb/d forecast 3Q deficit; and a roughly
  0.55 mb/d cut to second-half demand versus July. Public highlights do not publish Q2/Q3
  demand and supply **levels**, revised March demand, a government/industry monthly stock
  split, or a newer days/net-import-cover table. These are recorded as source limitations,
  not estimated values.
- 2026-08-18: Joined the OMR observations to `a4d.2`'s August-STEO rows in
  `data/derived/hormuz_m8q_1_monthly_oil_balance.csv`. August EIA implies draws of
  **525.786 mb for March-June** and **540.013 mb for March-July**. Subtracting IEA's
  same-vintage observed draws gives residuals of **184.786 mb** and **130.013 mb**,
  respectively, in `data/derived/hormuz_a4d_1_august_omr_residuals.csv`. The like-for-like
  March-June residual is **123.385 mb lower** than 308.171 mb; the requested March-July
  comparison is 178.158 mb lower but also extends the window by a month.
- 2026-08-18: Verification passed using the repository `.venv`: the build writes 7 stock
  rows, 19 flow/demand/supply evidence rows and 2 residual rows; `py_compile` passes; the
  stock artifact contains all five March-July month keys; July total equals onshore plus
  oil-on-water; both cumulative identities and both expected residual values assert. No
  package or `requirements.txt` change was needed.
- 2026-08-18: Acceptance disposition: the critical 298 mb composite is replaced by the
  exact 341 mb August-vintage March-June aggregate, and the March-July aggregate is 410 mb.
  A March-July monthly-shaped table exists, but its March-June cells are intentionally null
  because the public release does not disclose them. Obtaining those monthly values or a
  days-of-cover update would require licensed subscriber tables; this limitation does not
  affect the exact cumulative residuals used by the downstream bridge.
