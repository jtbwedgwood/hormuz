---
id: "hormuz-a4d.2"
title: "Ingest the August 2026 EIA STEO and re-run the February-vintage revision path"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-a4d"
labels:
  - "eia"
  - "steo"
  - "balance"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-a4d.6"
  - "hormuz-a4d.8"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T13:10:00-06:00"
---

# Ingest the August 2026 EIA STEO and re-run the February-vintage revision path

## Description

The draft's four headline numbers (1,441 mb supply shortfall, 439 mb demand reduction,
396 mb foregone build, 57 mb non-Gulf supply gain) are all **frozen-February-STEO versus
July-STEO** comparisons. Two things change with the August workbook:

- **July stops being a forecast.** The current docs exclude July from the headline precisely
  because EIA's July supply figure was a forecast completed on 1 July, before the 7-8 July
  escalation. With August actuals/estimates, the natural blog frame becomes **March-July**,
  which is also the frame the regional demand splits already use.
- Every March-June monthly value is revisable, so the "matched March-June frame" numbers
  themselves move.

Re-run `scripts/`-side comparisons with `aug26_base.xlsx` in place of `jul26_base.xlsx`,
holding `feb26_base.xlsx` frozen:

1. Global supply revision, March-June and March-July. (July vintage: 1,441.48 mb / 1,724.36 mb.)
2. Global consumption revision, same frames. (July vintage: 439.23 mb / 566.36 mb.)
3. Expected-stock-build revision. (July vintage: 396.08 mb / 479.23 mb.) Also restate the
   February monthly build expectation the draft quotes as "2.4 to 3.9 mb/d."
4. Implied inventory draw. (July vintage: 606.17 mb / 678.78 mb.)
5. Country supply revisions: US, Brazil, Russia, Guyana, Mexico, Argentina, Canada, Malaysia,
   India, Norway, Oman. The draft quotes US +65, Brazil +32, Russia -27 on the March-June
   frame and the docs carry +77.98 / +35.48 / -39.11 on March-July; keep the two frames
   clearly separated so the blog does not mix them.
6. Gulf country crude shut-ins through July, extending the existing Saudi/Iraq/Kuwait/UAE/
   Qatar/Iran/Bahrain table (July vintage total 1,183.49 mb through June).
7. Whether EIA's forward assumptions changed (the current baseline assumes gradual resumption
   in 3Q26 and no pre-conflict traffic until early 2027). This underwrites the unwritten
   "What Will Happen if the Closure Persists?" section.

## Acceptance Criteria

- August-vintage values for all four headline components on both the March-June and
  March-July frames, with deltas versus the July vintage.
- Restated route bridge: missing Hormuz transit - incremental bypass - non-Gulf supply =
  supply shortfall + residual, on the August vintage.
- A recommendation on whether the blog should switch its primary frame to March-July.
- `hormuz_m8q_1_monthly_oil_balance.csv` and `hormuz_m8q_7_nongulf_supply_ledger.csv`
  regenerated or explicitly superseded.

## Dependency Notes

- Parent: `hormuz-a4d`
- Blocks: `hormuz-a4d.6`, `hormuz-a4d.8`

## Work Notes

- 2026-08-18: Claimed for the August STEO refresh. Scope is the EIA workbook,
  February-vintage comparisons, STEO-facing derived artifacts, and documented
  validation; OMR-specific artifacts remain with `hormuz-a4d.1`.

- Workbook: https://www.eia.gov/outlooks/steo/archives/aug26_base.xlsx
- Frozen baseline stays https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx
- The 1,309-1,468 mb "Hormuz-plausible" band from `hormuz-r3v.5` is a function of the
  target vintage; it must be recomputed, not carried over.

- 2026-08-18: Regenerated
  `data/derived/hormuz_m8q_1_monthly_oil_balance.csv` with the 11 August STEO
  (forecast completed 6 August) and expanded the EIA panel through August.
  Regenerated `data/derived/hormuz_m8q_7_nongulf_supply_ledger.csv` against the
  frozen February workbook; July is now a preliminary estimate, not a forecast.
- 2026-08-18: Added the dedicated reproducible audit
  `scripts/build_a4d_2_august_steo_comparison.py` ->
  `data/derived/hormuz_a4d_2_august_steo_comparison.csv` and registered it in
  `data/manifest.csv`. The artifact contains explicit vintage, frame, status,
  source-locator, method, confidence, and caveat fields.
- August headline identity (million barrels; August value, then delta versus July
  vintage): March-June supply shortfall **1,362.300 (-79.177)**, consumption
  reduction **440.436 (+1.208)**, foregone expected build **396.078 (0.000)**,
  and implied draw **525.786 (-80.385)**. March-July: **1,589.576 (-134.788)**,
  **570.336 (+3.980)**, **479.227 (0.000)**, and **540.013 (-138.768)**.
  Both identities close below 0.000001 mb. The frozen-February March-June
  monthly implied-build range remains **2.362-3.897 mb/d**, supporting the
  rounded draft language "2.4 to 3.9 mb/d."
- Named August-minus-February supply revisions are published for both frames in
  the audit. March-June / March-July standouts (million barrels) are US
  **+70.058 / +83.798**, Brazil **+40.816 / +44.545**, and Russia
  **-27.425 / -39.114**. The artifact also includes Guyana, Mexico, Argentina,
  Canada, Malaysia, India, Norway, and Oman, plus each delta versus the July
  vintage. The complete non-Middle-East regional net plus Oman is **+79.308 mb**
  through June.
- Restated matched March-June route bridge (million barrels): **1,924.600 gross
  missing Hormuz transit - 362.100 incremental bypass - 79.308 non-Middle-East
  plus Oman supply = 1,362.300 global supply shortfall + 120.892 residual**.
  The residual remains explicitly a route/taxonomy/timing diagnostic. A
  March-July route bridge is not fabricated because the existing public route
  reconstruction has no period-matched July route-flow estimate.
- August STEO Table 1 changes the historical country presentation to a
  March-May average plus June and July estimates. Displayed country cumulative
  crude shut-ins through July (million barrels): Kuwait **195.75**, UAE
  **133.40**, Iran **30.62**, Iraq **393.00**, Qatar **64.85**, Bahrain
  **19.57**, Saudi Arabia **370.67**. EIA's published total-row integration is
  **1,318.26 mb**, but the displayed countries sum to **1,207.86 mb** because
  the March-May total is 10.05 mb/d while displayed countries sum to 8.85 mb/d.
  The unexplained **110.40 mb** discrepancy is preserved as a reconciliation
  row rather than allocated to a country.
- Forward assumptions changed materially: EIA assumes severe Hormuz constraints
  through August, slow flow increases starting in September, and aggregate crude
  shut-ins of **6.573 mb/d in 3Q26, 4.200 in 4Q26, and 1.637 in 1Q27**. Most
  production/trade returns near pre-conflict patterns in early 2027, but about
  **0.6 mb/d** remains disrupted through end-2027. Source: August STEO overview
  and Global Oil Markets/Table 1, https://www.eia.gov/outlooks/steo/archives/aug26.pdf
- Recommendation: switch the blog's primary historical frame to
  **March-July** because July is now a past-month estimate and captures the
  renewed July escalation; keep March-June as a sensitivity and the route-bridge
  frame. Continue calling all international past-month values preliminary
  estimates, not final observations.
- Recomputed the `hormuz-r3v.5` preferred supply-effect band on matched
  **February-August** pairs for 2017-19 and 2023-25 rather than carrying forward
  the February-July distribution. The result is **1,220.45-1,418.75 mb** for
  March-June and **1,388.68-1,647.21 mb** for March-July; these remain bounded
  plausibility ranges, not identified causal effects.
- Validation: all three builders compile under `.venv`; regenerated CSVs parse
  cleanly; row IDs are unique; both headline identities, the route bridge, and
  the published Gulf total were asserted in code. No dependencies changed.
