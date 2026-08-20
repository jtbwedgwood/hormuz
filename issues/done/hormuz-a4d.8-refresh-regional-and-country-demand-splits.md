---
id: "hormuz-a4d.8"
title: "Refresh regional and country demand revision splits on the August vintage"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-a4d"
labels:
  - "demand"
  - "regional"
  - "blog"
blocked_by:
  - "hormuz-a4d.2"
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T14:45:00-06:00"
---

# Refresh regional and country demand revision splits on the August vintage

## Description

The draft's entire "Impacts by Country/Region" section, plus its planned demand-reduction-by-
locality figure, rests on the regional EIA demand revisions in
`docs/hormuz-inventory-and-demand-residual-stories.md`. Those are **March-July, July vintage**,
while the draft's headline demand number (439 mb) is **March-June**. The draft already
rescales one of them by hand — the Middle East's ~135 mb is the 173.5 mb March-July figure
scaled to March-June — which is exactly the kind of silent frame-mixing worth removing.

1. Recompute regional revisions on the August vintage for both frames: Asia/Oceania
   (326.900 mb March-July), Middle East (173.496), Africa (35.100), Europe (29.701),
   Eurasia (9.433), Central/South America (8.359), North America (**+16.633**, the
   counterexample the draft's US section relies on), gross 582.989 / net 566.356 mb.
2. Recompute country revisions: China (119.992), India (41.141), Japan (19.522), Korea
   (provisional 30.60, a bounded suballocation rather than an EIA observation), Other
   Asia/Oceania (115.646).
3. Re-derive the prewar-demand denominators so the draft's "12.5% of prewar regional oil
   demand" style percentages are consistent (Middle East prewar ~8.85 mb/d; India ~5.5 mb/d).
4. Restate the mechanism cross-walk: explicit government restraint 8.6%, decentralized
   response/rapid switching 20.2%, forced supply/refinery/activity constraint 51.2%,
   structural/unknown 20.0%. Confirm these shares survive the new totals — this is the
   sharpest finding available to the demand section and the draft currently omits it.
5. Refresh the China mechanism evidence: crude-processing shortfalls (25 / 39 / 81 mb y/y in
   April/May/June), refinery runs, product export controls, and any July/August NBS release.
   The draft's China section promises "little on-the-ground impact (speculate about why)" and
   this is the material that answers it.
6. Regenerate `hormuz_m8q_12_asia_demand_mechanism_scenarios.csv` and
   `hormuz_m8q_13_non_asia_demand_mechanisms.csv`.

## Acceptance Criteria

- Regional and country revisions restated on the August vintage, with the frame (March-June
  vs March-July) labelled on every number.
- Mechanism-class shares recomputed and confirmed to close exactly.
- A single table the blog's regional figure can be built from without further rescaling.

## Dependency Notes

- Parent: `hormuz-a4d`
- Blocked by: `hormuz-a4d.2` - the August STEO is the input

## Work Notes

- 2026-08-18: Claimed for the August STEO refresh. Scope is the February-vs-August
  regional/country demand bridge on matched March-June and March-July frames,
  mechanism allocations, China evidence, publication-ready figure data, and validation.

- 2026-08-18: Added `scripts/build_a4d_8_august_demand_splits.py`. It downloads the
  frozen February and August STEO workbooks, extracts Table 3e, and regenerates the two
  requested mechanism artifacts plus the new one-table figure input
  `data/derived/hormuz_a4d_8_demand_splits_blog_table.csv`. The manifest now points all
  three artifacts to this builder. No dependencies changed and no a4d.6 bridge or prose
  files were edited.
- 2026-08-18: August demand revision (million barrels; positive means below the frozen
  path): March-June world **440.436**; Asia/Oceania **273.527**, Middle East **115.923**,
  Africa **26.540**, Europe **29.335**, Eurasia **6.442**, offset by North America
  **-6.850** and Central/South America **-4.480**. March-July world **570.336**;
  Asia/Oceania **346.066**, Middle East **150.415**, Africa **35.075**, Europe **33.472**,
  Eurasia **9.138**, North America **2.037**, offset by Central/South America **-5.867**.
  Thus the old North American counterexample changes sign on the August March-July frame.
- 2026-08-18: Named Asia revisions are March-June / March-July: China
  **104.058 / 136.440**, India **52.476 / 64.897**, Japan **18.815 / 21.964** mb.
  Korea remains a low-confidence **0.05/0.20/0.40 mb/d** suballocation, yielding a base
  **24.4 / 30.6** mb; Other Asia/Oceania is the exact base residual at
  **73.778 / 92.166** mb. Korea is never represented as an EIA observation.
- 2026-08-18: Denominators are explicit. Frozen-February period-average demand and the
  gap share are carried for every EIA geography. Separate OPEC 2024 prewar anchors put
  Middle East demand at **8.854 mb/d** and India at approximately **5.5 mb/d**; their
  August gap shares are **10.73% / 11.10%** (March-June / March-July) and
  **7.82% / 7.71%**, respectively. This replaces the draft's silent rescaling.
- 2026-08-18: The old July-vintage global mechanism shares do not survive numerically.
  On the August March-July gross downward denominator of **576.203 mb**, the exact-closing
  base cross-walk is **46.017 mb (8.0%)** explicit restraint, **120.039 mb (20.8%)**
  decentralized response/switching, **286.233 mb (49.7%)** forced supply/refinery/activity
  constraint, and **123.914 mb (21.5%)** structural/revision/unknown. Central/South
  America's **-5.867 mb** offset reaches the **570.336 mb** world net. March-June shares
  are **8.1% / 20.9% / 49.6% / 21.4%**. The substantive finding survives: explicit
  restraint is under one-tenth, decentralized response about one-fifth, and forced
  constraint about half; these remain scenarios rather than causal estimates.
- 2026-08-18: Refreshed China evidence retains official NBS crude-processing shortfalls
  of **24.664 / 39.420 / 80.777 mb-equivalent** year over year in April/May/June and the
  existing customs reconstruction of **35.226 mb-equivalent** of broad refined products
  retained domestically through export suppression. Runs are not final demand, and export
  curbs preserve domestic availability rather than create supply. The NBS release calendar
  scheduled July national-economy data for 17 August, but no official English or Chinese
  July energy-production release was located by the 18 August cutoff, so July runs were
  not imputed.
- 2026-08-18: Validation passed under `.venv`: builder compiles and reruns; all three CSVs
  parse; 60 Asia rows, 144 non-Asia rows, and 55 blog rows have unique IDs; every
  low/base/high geography allocation closes within CSV precision; all non-Asia scenarios
  close to their absolute regional gaps; mechanism classes close exactly to gross downward
  regions; regional gross plus signed offsets matches the independent world row on both
  frames; manifest dataset IDs remain unique. Acceptance criteria met.
