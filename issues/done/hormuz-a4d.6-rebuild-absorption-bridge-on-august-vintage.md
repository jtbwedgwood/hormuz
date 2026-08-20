---
id: "hormuz-a4d.6"
title: "Rebuild the absorption bridge, Sankey and confidence tiers on the August vintage"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-a4d"
labels:
  - "accounting"
  - "sankey"
  - "uncertainty"
  - "blog"
blocked_by:
  - "hormuz-a4d.1"
  - "hormuz-a4d.2"
  - "hormuz-a4d.5"
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T22:00:00Z"
---

# Rebuild the absorption bridge, Sankey and confidence tiers on the August vintage

## Description

This is the consolidation step. Once `.1`, `.2` and `.5` land, re-run
`scripts/build_r3v_1_confidence_tiered_absorption.py` and the dependent artifacts so the
draft's central arithmetic — and the Sankey the draft reserves a slot for — are internally
consistent on one vintage.

1. Restate the market-clearing bridge on the August vintage. July-vintage March-June baseline:
   1,441.5 mb = 439.2 lower consumption + 396.1 foregone build + 298.0 observed draw +
   308.2 residual. Produce the March-July version too.
2. Recompute the confidence tiers. July vintage: T1 directly observed 156.2 mb (10.8%),
   T2 396.1 (27.5%), T3 466.9 (32.4%), T4 unknown 422.3 (29.3%), with a 117-528 mb
   model/vintage range on T4. If a same-vintage IEA series from `.1` narrows the residual,
   the T4 range narrows with it — that is the most publishable outcome of this epic.
3. Rebuild `figures/fig-r3v-hormuz-absorption-sankey.svg` and its data CSV, preserving the
   waist-node structure so rerouting (upstream) and market clearing (downstream) are not
   double counted.
4. Recompute the interagency Q2 decomposition (July vintage: 2.110 mb/d gap = 1.254 demand +
   0.856 supply; 295 mb -> 103 mb residual for April-June) and extend to Q3 if the August
   OMR permits.
5. Re-benchmark the residual's daily rate against the historical interagency range
   (July vintage: 2.526 mb/d against a documented 0.30-1.30 mb/d range, and against 1998 H1's
   1.799 mb/d). If the August vintage brings it inside the historical range, the draft's
   "outside the usual range for inter-agency disagreement" sentence must change.

## Acceptance Criteria

- One arithmetically closing bridge on a single vintage, for both frames.
- Regenerated Sankey figure and `hormuz_r3v_1_confidence_tiered_ledger.csv`.
- Explicit statement of how much the residual and the T4 "we don't know" share moved.
- `docs/hormuz-what-happened-to-the-barrels.md` updated, including its cutoff line.

## Dependency Notes

- Parent: `hormuz-a4d`
- Blocked by: `hormuz-a4d.1`, `hormuz-a4d.2`, `hormuz-a4d.5`

## Work Notes

- 2026-08-18: Claimed after `.1`, `.2`, and `.5` completed. Scope is the August-vintage
  absorption bridge, confidence tiers, Sankey/data, interagency and historical residual
  comparisons, and the cutoff-consistent central draft. Demand-specific `.8` artifacts are
  out of scope. The public-OMR access limits and EIA Gulf-country/total discrepancy will be
  carried through rather than imputed away.
- 2026-08-18: Rebuilt `scripts/build_r3v_1_confidence_tiered_absorption.py` around the
  completed August handoffs. It now writes a dedicated 23-row consolidation artifact,
  `data/derived/hormuz_a4d_6_august_absorption_bridge.csv`, plus both-frame confidence tiers
  and the regenerated Sankey/data. No package or `requirements.txt` change was needed.
- 2026-08-18: Both market-clearing identities close exactly at six decimals. March-June:
  **1,362.300139 = 440.436262 lower consumption + 396.077697 foregone build + 341.000000
  observed draw + 184.786180 residual** mb. March-July: **1,589.576253 = 570.335875 +
  479.227481 + 410.000000 + 130.012897 mb**. March-July is the primary historical frame;
  March-June remains the route/Sankey frame because public July route data are insufficient.
- 2026-08-18: Confidence tiers now use the public same-vintage IEA aggregate as T1 rather
  than the old mixed-vintage stock composite. March-June tiers are T1 **341.000**, T2
  **396.078**, T3 **440.436**, T4 **184.786** mb. March-July tiers are T1 **410.000**, T2
  **479.227**, T3 **570.336**, T4 **130.013** mb. Against the task's July-vintage comparable
  T4 headline of 422.3 mb / 29.3%, like-for-like T4 falls **237.5 mb and 15.7 percentage
  points** to 184.8 mb / 13.6%; the primary frame is 130.0 mb / 8.2%.
- 2026-08-18: Retired the 117-528 mb cross-model/vintage range rather than falsely calling
  it August-vintage uncertainty. The public August OMR does not expose Q2/Q3 supply and
  demand levels, so a new matched interagency decomposition is not recoverable. The July
  Q2 result (2.110 mb/d = 1.254 demand + 0.856 supply) remains in the bridge artifact only
  as a clearly labelled historical reference; August Q2 and Q3 rows are explicit nulls.
- 2026-08-18: Re-benchmarked the plug: March-June is **1.515 mb/d**, above the documented
  0.30-1.30 mb/d annual interagency range but below 1998 H1's 1.799 mb/d; March-July is
  **0.850 mb/d**, inside the annual range. The central doc now explicitly retires the claim
  that the primary-frame residual is outside the usual range.
- 2026-08-18: Preserved EIA's **110.4 mb** published Gulf-total-minus-displayed-country-row
  discrepancy as an unallocated, non-additive reconciliation row. Preserved the August OMR
  subscriber-table limitation: no fabricated March-June monthly stock/OOW cells, Q2/Q3
  agency levels, or July route decomposition.
- 2026-08-18: Updated `docs/hormuz-what-happened-to-the-barrels.md` through the 11 August
  STEO / 12 August OMR cutoff, `data/manifest.csv`, and `figures/README.md`. Did not edit
  a4d.8 demand-specific artifacts; coordinated with its owner after their August regional
  splits landed.
- 2026-08-18: Validation passed in `.venv`: builder compilation and execution, exact
  six-decimal market and route identities, four-tier sums for both frames, unique row IDs,
  CSV parsing, manifest-ID uniqueness, SVG XML parsing, and visual render inspection via a
  native 1800x920 PNG. The Sankey labels, shares and footer fit without clipping.
