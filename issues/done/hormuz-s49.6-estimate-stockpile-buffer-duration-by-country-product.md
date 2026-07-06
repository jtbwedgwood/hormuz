---
id: "hormuz-s49.6"
title: "Estimate stockpile buffer duration by country/product"
type: "task"
priority: "P1"
parent: "hormuz-s49"
labels:
  - "buffer"
  - "energy-security"
  - "modeling"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-4j7.3"
  - "hormuz-ccx.2"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:57Z"
status: "done"
updated_at: "2026-07-06T19:35:00Z"
---

# Estimate stockpile buffer duration by country/product

## Description

Convert inventory and disrupted-flow estimates into days of cover under low/base/high disruption scenarios.

## Acceptance Criteria

Buffer table states assumptions, replenishment limits, demand seasonality, and confidence levels.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Unblocked: `hormuz-fyp.2` - Build canonical disruption chronology
- Unblocked: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Unblocked: `hormuz-s49.2` - Quantify OECD and US reserve response
- Cleared blocker: `hormuz-s49.3` - Evaluate China SPR release claims
- Cleared blocker: `hormuz-s49.4` - Assess LNG and gas storage buffering
- Unblocked: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-ccx.2` - Develop blog narrative outline

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.
- 2026-07-06: Reviewed the current repo evidence from `hormuz-s49.2`, `hormuz-s49.3`, `hormuz-s49.4`, `hormuz-s49.5`, the kmz derived tables, and the foundation manifest/docs.
- Earlier blocked-pass decision, superseded by the final consolidation below: do **not** close this issue yet. At that point the repo had enough fragments to sketch coverage, but not enough to publish a consolidated conservative buffer table that satisfied the acceptance criteria for all requested regions and products.
- What is currently supportable from the notes:
  - Oil / OECD / US / Japan / Korea / Europe: reserve and release snapshots exist, but the repo does not yet assemble a single common demand denominator or replenishment-limit framework across all regions. The U.S., Japan, and Korea figures in `hormuz-s49.2` are especially useful, but they are not yet normalized into one comparative days-of-cover table.
  - China SPR / commercial crude: `hormuz-s49.3` supports a low-confidence distinction between opaque strategic stocks and visible commercial drawdown, which is not enough to assign a conservative buffer duration for government SPR alone.
  - LNG / gas: `hormuz-s49.4` provides useful partial coverage, including Europe daily storage, Japan ~3 weeks, Korea 37 days on the reserve-rule basis, China a ~19-day upper-bound proxy, and India only a modeled proxy. Europe still needs the same denominator treatment as the others before the table can be called complete.
  - Fertilizer / chemicals: `hormuz-s49.5` gives a defensible India case study and a qualitative global claim that fertilizers lack coordinated strategic reserves, but the broader country/product table is still incomplete and petrochemicals remain qualitative only.
- Precise blocker:
  - The repo currently lacks one consolidated buffer table that harmonizes demand seasonality, replenishment limits, and confidence levels across the requested oil, gas/LNG, China crude, and fertilizer/chemical rows.
  - The open sibling tasks are still the source of truth for the missing pieces: `hormuz-s49.2` for OECD/US/Japan/Korea/Europe oil reserves, `hormuz-s49.3` for China SPR uncertainty, `hormuz-s49.4` for LNG/gas denominators, and `hormuz-s49.5` for fertilizer/chemicals.
- Superseded: those inputs have now been reconciled into the final consolidated table described below, with mixed bases preserved as caveats rather than hidden.
- 2026-07-06 cleanup status: moved to `blocked`. Removed stale `hormuz-l8m.3` block because RQ5 completed that sensitivity table with stockpile buffering recorded as a caveat rather than a blocker.
- 2026-07-06 final pass: `hormuz-s49.3` and `hormuz-s49.4` are now done in local issue state, so the stale blockers are cleared. Claimed the task, cleared `blocked_by`, and consolidated the S49, KMZ, FYP, and F6R local outputs into `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`.

### Final Output

| Output | Path | Status |
|---|---|---|
| Consolidated stockpile buffer duration table | `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv` | complete |
| Manifest registration | `data/manifest.csv` | complete |

### Method

- Scope: major importer/product rows where local public-source work supported either numeric stock duration, numeric release-duration math, or an explicit qualitative/proxy classification.
- Scenario convention:
  - For oil rows, low/base/high durations divide the public stock/release anchor by `hormuz_f6r_5` low/base/high inventory-draw flow-equivalent assumptions. This answers "how long the reserve bridge can sustain the modeled inventory-draw leg," not "how long the country can ignore the whole Hormuz shock."
  - For gas/LNG rows, use the strongest public storage denominator available. Europe, Japan, Korea, China, Singapore, and Thailand are mostly average-demand or scenario-affected-supply proxies, not harmonized Hormuz-loss denominators.
  - For India gas/LPG, global fertilizer, sulfur, and petrochemical rows, no defensible public stock-duration series exists, so the table leaves duration cells blank and marks qualitative/proxy coverage explicitly.
  - For India fertilizer rows, use the S49.5 seasonal stock divided by reported season-to-date sales proxy. These are not low/base/high Hormuz disruption days because fertilizer demand is strongly seasonal.
- Calculation checks:
  - U.S. oil: 172.2 mb IEA allocation / 0.20, 0.35, 0.60 mb/d inventory-draw assumptions = 861.0, 492.0, 287.0 days.
  - Japan crude: 79.8 mb / 0.25, 0.40, 0.55 mb/d = 319.2, 199.5, 145.1 days.
  - South Korea crude: 22.5 mb / 0.20, 0.40, 0.70 mb/d = 112.5, 56.3, 32.1 days.
  - India crude proxy: 5.33 MMT Phase-I SPR converted at 7.33 bbl/tonne, about 39.1 mb, / 0.10, 0.25, 0.40 mb/d = 391.0, 156.4, 97.8 days.
  - China crude proxy: reported 25 mb commercial/operational draw / 0.50, 1.00, 1.80 mb/d = 50.0, 25.0, 13.9 days.

### Final Synthesis

- The strongest stockpile-buffer result is not "the world has plenty of reserves"; it is "reserves buy time only for specific residual flow gaps." Japan is the cleanest case because public evidence ties large crude exposure, named replacement routes, reserve releases, and limited demand destruction into one bridge story.
- U.S. and Europe oil reserve rows look large in days because direct modeled inventory-draw needs are small relative to IEA release allocations. Those rows should be framed as price/global-market stabilizers, not as evidence that U.S./EU physical import exposure is the binding constraint.
- South Korea has meaningful oil and LNG buffers on paper, but public drawdown visibility is weaker than Japan's.
- China should not be written as "China is releasing a ton of SPR." The table uses only a reported commercial/operational draw proxy for duration. Broad EIA inventory estimates are cited as optionality, not converted into a government SPR day count.
- Gas/LNG buffers are much less comparable than oil reserves. Europe has the best daily public stock series; Japan and Korea have meaningful LNG tank/rule buffers but weak real-time public visibility; China is a capacity proxy; India is mostly rationing and cargo replacement rather than storage.
- Fertilizer and chemical buffers are the weakest for global numeric claims. India supports seasonal urea/DAP/MOP/NPKS proxy days, but FAO/IFA evidence supports the broader claim that fertilizers lack coordinated strategic reserves and that sulfur/petrochemical inventory days should remain qualitative.

### Source Breadcrumbs

- Local derived inputs:
  - `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv`
  - `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv`
  - `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv`
  - `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv`
  - `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv`
  - `data/derived/hormuz_f6r_5_replacement_demand_response.csv`
  - `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`
  - `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`
- Local issue anchors:
  - `issues/done/hormuz-s49.1-inventory-reserve-and-stockpile-data-sources.md`
  - `issues/done/hormuz-s49.2-quantify-oecd-and-us-reserve-response.md`
  - `issues/done/hormuz-s49.3-evaluate-china-spr-release-claims.md`
  - `issues/done/hormuz-s49.4-assess-lng-and-gas-storage-buffering.md`
  - `issues/done/hormuz-s49.5-assess-fertilizer-and-chemical-inventory-buffers.md`
  - `issues/done/hormuz-f6r.2-analyze-china-exposure-and-substitution-behavior.md`
  - `issues/done/hormuz-f6r.3-analyze-japan-korea-india-and-southeast-asia-adjustment.md`
  - `issues/done/hormuz-f6r.5-quantify-replacement-supply-and-demand-destruction.md`
- External source anchors are embedded per row in `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`, including IEA collective release notices, EIA SPR/China inventory analysis, METI Japan reserve/LNG statements, GIE/Eurostat gas storage denominators, KOGAS/IEA Korea gas security pages, India PIB/PPAC releases, FAO/IFA fertilizer sources, and IEA/World Bank petrochemical/fertilizer context.

### Validation

- 2026-07-06: Validated with repo-local Python:
  - `.venv/bin/python` parsed `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv` as 21 rows and 19 columns.
  - Required fields were populated.
  - Formula checks passed for the six numeric oil/commercial-draw rows.
  - `data/manifest.csv` parsed and includes `hormuz_s49_6_stockpile_buffer_duration`.

### Remaining Caveats

- The table is suitable for RQ4 and downstream historical-comparison scaffolding, but it is not a live operational reserve tracker.
- Oil rows mix announced allocations, policy-gated releases, and total reserve snapshots; the row notes state which anchor is used.
- Gas/LNG and fertilizer rows use heterogeneous denominators by necessity. Do not chart them as if all day counts are the same metric without a prominent caveat.
- Proprietary cargo-flow, tank-level, or commercial inventory data could materially improve China, LPG/petrochemical, sulfur, and country-level fertilizer duration estimates.
- 2026-07-06 F6R follow-up: upstream China and LNG/gas adjustment tasks are now done, and this issue is back in `in-progress`. Remaining work is synthesis, not external unblock: reconcile S49 oil, China, LNG/gas, fertilizer/chemical, and F6R replacement/demand-response rows into one conservative buffer-duration table.
