---
id: "hormuz-m8q.9"
title: "Audit historical March-July global oil accounting bridge"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "accounting-audit"
  - "historical"
  - "double-counting"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "codex"
created_at: "2026-08-04T18:43:08Z"
updated_at: "2026-08-04T18:58:17Z"
---

# Audit historical March-July global oil accounting bridge

## Description

Independently audit and synthesize the completed Gulf physical, non-Gulf supply, stock, and demand ledgers into a two-stage historical accounting identity. Prevent route preservation, production, inventories, demand, and foregone counterfactual stock builds from being counted twice. Preserve the difference between country-resolved March-June estimates and July forecast/nowcast values.

## Acceptance Criteria

- Define separate physical-supply and market-clearing identities with explicit signs, boundaries, and units.
- Reconcile EIA forecast-vintage global totals to IEA observed-stock evidence without averaging unlike concepts.
- Give low/base/high historical attribution values and exact residuals that close to the selected denominator.
- Identify unsupported causal attributions, taxonomy mismatches, data-status problems, and every material overlap among route, supply, stock, and demand rows.
- Produce a machine-readable audit bridge, register it in the manifest, and provide a publication-ready detailed outline with exact arithmetic and warnings.

## Work Notes

- 2026-08-04: Claimed for an independent accounting audit. Inputs are `hormuz-m8q.1`, `.3`, `.6`, `.7`, and `.8` when available. This task will not edit the `.4` integration documents or figures.
- 2026-08-04: Added `scripts/build_m8q_9_historical_bridge_audit.py` and generated `data/derived/hormuz_m8q_9_historical_bridge_audit.csv` with 81 rows. The audit also incorporates the more detailed `.10` emergency-release execution audit that became available during reconciliation. Registered the output in `data/manifest.csv`.

### Audit conclusion: use two stages, not one all-purpose pie

The publication must present two successive identities:

1. **Physical route/supply diagnostic, through 30 June:** start with missing Hormuz transit; subtract incremental Gulf bypass and the net supply revision outside the affected Gulf; carry a route/taxonomy/timing residual; the outcome is the net global supply shortfall. This explains what happened before oil reached the global balance.
2. **Global market clearing, through 30 June or with a separately labelled July forecast extension:** the net global supply shortfall equals lower consumption plus a counterfactual stock build that did not happen plus an implied actual inventory draw. Emergency releases, national stock draws, and country demand rows are suballocations of those three buckets, not additional top-level slices.

This separation is mandatory. Gulf rerouting and non-Gulf production are already embodied in the measured global supply outcome. Government stocks are already inside global stock movement. A chart that adds rerouting, non-Gulf production, SPR, commercial stocks, foregone stock builds, and demand reduction against the same global-supply denominator will double count.

### Recommended historical headline and cutoff language

> Between 1 March and 30 June 2026, global oil supply was roughly **1.40-1.44 billion barrels below pre-war expectations**, using the latest IEA total-oil estimates and the EIA's frozen-February-versus-July petroleum-liquids comparison. Extending the EIA comparison through 31 July raises the shortfall to **1.724 billion barrels**, but July is a forecast completed on 1 July, not a country-resolved historical observation.

The 1.40-1.44 billion barrel June range is not a statistical confidence interval. Its low endpoint is the rough IEA integration (10.1, 12.8, 13.6, and 9.4 mb/d in March-June, or about 1.401 billion barrels); its high endpoint is the consistent EIA forecast-vintage calculation (1.441 billion barrels). The modest gap is an inter-source/taxonomy check. Do not use the broader 1.518 billion barrel affected-Gulf loss as the world net shortfall; it is upstream of offsetting supply elsewhere.

### Stage A: matched-cutoff physical bridge, March-June

The base route diagnostic closes as follows, in million barrels:

| component | low-bypass case | base | high-bypass case | accounting treatment |
|---|---:|---:|---:|---|
| Gross Hormuz flow missing versus 20 mb/d pre-war | 1,924.600 | 1,924.600 | 1,924.600 | Starting route-exposure denominator |
| Incremental non-Hormuz Gulf exports | 300.000 | 362.100 | 430.000 | Subtract; uncertain calibrated route estimate |
| Net non-Middle-East production revision | 54.382 | 54.382 | 54.382 | Subtract; EIA revision, not proven causal response |
| Oman production revision | 2.514 | 2.514 | 2.514 | Subtract; outside-Hormuz terminals |
| Net global supply shortfall | 1,441.477 | 1,441.477 | 1,441.477 | EIA outcome passed to Stage B |
| Route/taxonomy/timing residual | 126.227 | 64.127 | -3.773 | Exact closing residual |

The cases vary only the 300/362.1/430 million barrel bypass range. They are attribution cases, not statistical confidence bounds. The high-bypass case's small negative residual shows that the upper bypass estimate nearly over-explains the route-to-supply bridge once net outside-Gulf production is included.

The boundary is deliberately described as a **diagnostic**, not a clean physical identity. Missing exports, production, Gulf storage, domestic Gulf use, and the EIA/IEA product taxonomies differ. The residual is where those mismatches belong; it must not be assigned to a favored mechanism.

#### Route detail behind the 362.1 million barrel base estimate

- Saudi East-West/Petroline to Yanbu: **319.5 million incremental barrels** above a 2 mb/d working pre-war baseline; calibrated to a March ramp and about 5 mb/d in April-June.
- UAE Habshan-Fujairah: **76.1 million incremental barrels** above a 1.1 mb/d baseline.
- Iraq-Turkiye/Ceyhan: **26.253 million incremental barrels**, using 250 kb/d beginning 18 March.
- Other routes/baseline calibration: **-59.753 million barrels**.

The last negative item is not negative oil flow. It is evidence that the named Saudi/UAE/Iraq estimates sum to more than the aggregate route increase implied by the working 3.8 mb/d pre-war bypass baseline. Therefore 319.5, 76.1, and 26.253 cannot be presented as three independently measured cargo totals. They close only with the negative calibration residual.

#### Parallel upstream cross-check: do not add to the route bridge

EIA's country table estimates **1,183.49 million barrels of crude shut in** during March-June: Saudi Arabia 359.80, Iraq 358.83, Kuwait 215.83, UAE 121.20, Qatar 57.95, Iran 52.51, and Bahrain 17.37 million barrels. IEA's broader but rough total-oil integration is **1,518 million barrels** for affected Gulf producers. Crude is a subset of total oil, and neither measure is additive to missing transit or the global shortfall.

On the IEA total-oil boundary, affected-Gulf losses of roughly 1.518 billion barrels minus an inferred 117.3 million barrel outside-Gulf/taxonomy offset yield the 1.401 billion barrel world loss. The EIA country ledger directly identifies 56.896 million barrels of net March-June production cushion outside the Hormuz-dependent Gulf (54.382 outside the EIA Middle East region plus 2.514 in Oman); the remaining roughly 60 million barrels is cross-source geography/taxonomy and other-supply residual, not a country estimate.

#### Material non-Gulf country revisions through June

Named positive production revisions versus the frozen February EIA path total **127.703 million barrels**, partly offset by **61.916 million barrels** of named negative revisions. Material positive rows are United States +65.006, Brazil +31.746, China +7.133, Guyana +3.371, Mexico +3.179, Argentina +2.551, Oman +2.514, Azerbaijan +1.215, and Kazakhstan +1.154 million barrels. Material negative rows are Russia -27.422, Malaysia -7.443, India -7.118, Norway -7.096, Canada -1.351, and Indonesia -1.309 million barrels.

These are forecast-vintage revisions, not controlled estimates of production caused by Hormuz. The IEA's reported 3.5 mb/d increase in Atlantic-to-East-of-Suez exports cannot be added: it mixes higher production, U.S. SPR and industry-stock draw, and redirection of existing cargoes. Canada's 23.6 million barrel provisional production commitment also cannot be treated as delivery; EIA instead shows Canadian supply below the frozen forecast.

### Stage B: exact global market-clearing identities

Through June, the EIA identity is:

> **1,441.477 million barrels lower supply = 439.228 lower consumption + 396.078 expected stock build that did not occur + 606.171 implied inventory draw.**

With July's explicitly forecast extension:

> **1,724.364 million barrels lower supply = 566.356 lower consumption + 479.227 expected stock build that did not occur + 678.781 implied inventory draw.**

Thus the March-July forecast-vintage shares are 32.84% lower consumption, 27.79% foregone build, and 39.36% implied inventory draw. A foregone build is a counterfactual balance contribution, not oil physically released from a tank.

### Stock reconciliation and country detail

IEA's observed-stock estimates show a **298 million barrel draw in March-June** (-129, -117, -73, +21 million barrels by month). EIA's supply-minus-demand balance implies **606.171 million barrels** over the same period. The **308.171 million barrel gap** is an inventory-coverage/model/statistical residual. Do not average the two series and do not describe the gap as hidden SPR.

IEA reported around **290 million barrels actually released through 21 July**. That is a suballocation of global inventory movement, not 290 million barrels to add on top of the 678.781 million barrel implied draw. For a 31 July endpoint only, the project uses 290/315/330 million barrels as low/base/high release cases. The corresponding residual non-emergency/unobserved/balancing draws are 388.781/363.781/348.781 million barrels, so each case closes exactly to 678.781. Only 290 is an official reported aggregate; 315 and 330 are nowcasts.

The more detailed `.10` execution audit fits the following base country allocation exactly to the rounded 290 million barrel aggregate: United States 106.164, Japan 79.800, Italy 10.000, South Korea 15.478, Germany 13.414, France 10.043, United Kingdom 9.631, Spain 7.980, Turkiye 8.048, and other IEA stock contributors 29.442 million barrels. These are not all observations:

- U.S.: 103.994-107.791 million barrel physical SPR decline brackets the 21 July cutoff; base interpolation is 106.164.
- Japan: 58.747 million barrel receiver-confirmed floor; 79.8 base capped at its provisional plan; 89.944 later-schedule sensitivity.
- Italy: 12.087 million barrel February-May net emergency-stock decline supports at least the 10 million barrel plan, but gross program delivery is capped at 10 in the base allocation.
- South Korea, Germany, France, UK, Spain, Turkiye, and the other-member group are partly or mostly top-down pro-rata allocations after the better-observed U.S./Japan/Italy rows. Their low/high values are marginal country bounds and must not be summed into a simultaneous global range.

The provisional 19 March table is not delivery. Its reported rounded composition of 280 million public stocks, 119 million obligated-industry stocks, and 28 million production sums to 427 while the table total is stated as 426. The exact stock-contribution entries sum to about 398.7 million barrels, and Canada/Mexico production commitments are separate. Preserve the rounding/classification discrepancy.

#### U.S. counterfactual statement suitable for publication

> From 27 February through 24 July, the U.S. SPR fell **107.791 million barrels**, although the frozen February STEO had projected a **6.950 million barrel build** over March-July. Total U.S. commercial crude and products excluding the SPR fell another **50.187 million barrels**, versus a projected **59.755 million barrel build**. Actual government plus commercial stocks therefore supplied **157.978 million barrels**, and the combined actual-draw-plus-foregone-build swing was **224.683 million barrels**.

The SPR draw is already within the IEA collective release; commercial crude is inside total commercial petroleum stocks; and both are within global inventory accounting. The 24 July endpoint also differs from the IEA's 21 July aggregate cutoff.

China's public stock evidence is much weaker. IEA reports a 40 million barrel tank build in March and a 41 million barrel draw in June, only a 1 million barrel net draw across the two known months. April, May, and July ownership-resolved changes are missing. There is no public basis for a separately quantified large government-SPR slice; commercial/operational use is more plausible, but hidden government use cannot be measured as zero.

### Demand decomposition through July forecast

The 566.356 million barrel global consumption gap decomposes exactly by EIA region: Asia/Oceania 326.900, Middle East 173.496, Africa 35.100, Europe 29.701, Eurasia 9.433, Central/South America 8.359, and North America **-16.633** million barrels. North America's negative value means consumption was above the frozen path and offset some reductions elsewhere.

Within those regions, named country suballocations are China 119.992, India 41.141, Japan 19.522, Brazil 9.577, Russia 9.065, United States -5.561, Canada -10.138, and Mexico -0.937 million barrels. The Asia/Oceania residual after China, India, and Japan is 146.246 million barrels. A provisional South Korea estimate of 7.65/30.60/61.20 million barrels is only a candidate suballocation of that residual, not an extra slice.

The forecast revisions are not pure causal demand destruction. They include shortages, refinery and petrochemical constraints, price effects, conservation, macroeconomic revisions, weather, and structural trends. China's April, May, and June refinery-throughput shortfalls of roughly 24.66, 39.42, and 80.78 million barrel crude-equivalent are mechanism evidence nested inside its demand/import/stock bridge, not additional end-use reductions.

No standalone renewable/EV contribution is defensible. China's 48% EV share of 2024 new-vehicle sales, 356 GW of 2024 wind/solar additions, 55% renewable share of installed generating capacity, and June 2026 solar/NEV growth are useful context, but they do not isolate incremental post-February oil displacement. Much of the structural trend was already embedded in the frozen February forecast, installed electric capacity is not generation, and China uses little oil-fired power. Any realized switching remains inside the 119.992 million barrel China demand revision or the residual unless new counterfactual oil-use evidence emerges.

### Publication warnings and unsupported claims

1. Do not write "Hormuz caused 1.724 billion barrels of lost supply" without qualification. It is a global EIA forecast revision and July is forecast.
2. Do not present July country Gulf shut-ins or route flows as observed. The last country-resolved public estimate is June; the July EIA 3Q aggregate predates the 7-8 July escalation.
3. Do not add crude shut-ins, total-oil Gulf losses, missing Hormuz flow, or route-implied disruption. They are alternative boundaries.
4. Do not add gross bypass exports and incremental bypass. Incremental is the difference from baseline.
5. Do not add Atlantic export redirection to production, SPR, or commercial draw.
6. Do not add emergency releases to total/global inventory draw. They are a subcomponent.
7. Do not label obligated-industry relief as government SPR or an announcement as delivered oil.
8. Do not call every national stock decline a program release; replenishment, exchanges, reclassification, and ordinary commercial movements can occur simultaneously.
9. Do not add U.S. stock-path swings to global foregone build and actual draw; the swing crosses both buckets.
10. Do not sum region and nested country demand rows, Korea and the residual Asia row, or China refinery-run proxies and China consumption.
11. Do not convert renewable capacity, EV sales shares, or policy counts into oil barrels without an incremental post-February counterfactual.
12. Always retain the physical residual and the stock coverage/model residual. Low/base/high attribution cases are not confidence intervals.

### Validation

- Regenerated 81 audit rows from the completed upstream ledgers with the repository `.venv`.
- Verified the route diagnostic closes in all three bypass cases.
- Verified the EIA market-clearing identities close to floating-point precision through June and through July.
- Verified emergency-release plus other-stock residual closes to the EIA implied draw in all three July-end cases.
- Verified the seven demand regions close to the global demand gap and the `.10` country emergency base estimates close to 290 million barrels.
- Script compilation, CSV parsing, unique row IDs, manifest uniqueness, and `git diff --check` pass.
