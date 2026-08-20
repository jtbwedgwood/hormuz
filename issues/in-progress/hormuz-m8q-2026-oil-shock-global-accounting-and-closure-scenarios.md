---
id: "hormuz-m8q"
title: "2026 oil shock: realized supply loss, global accounting, and closure scenarios"
type: "epic"
status: "in_progress"
priority: "P0"
parent: null
labels:
  - "oil"
  - "2026-actuals"
  - "global-balance"
  - "scenarios"
  - "synthesis"
blocked_by: []
blocks:
  - "hormuz-ccx.2"
  - "hormuz-ccx.4"
  - "hormuz-ccx.5"
children:
  - "hormuz-m8q.1"
  - "hormuz-m8q.2"
  - "hormuz-m8q.3"
  - "hormuz-m8q.4"
  - "hormuz-m8q.5"
  - "hormuz-m8q.6"
  - "hormuz-m8q.7"
  - "hormuz-m8q.8"
  - "hormuz-m8q.9"
  - "hormuz-m8q.10"
  - "hormuz-m8q.11"
  - "hormuz-m8q.12"
  - "hormuz-m8q.13"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-03T22:40:09Z"
updated_at: "2026-08-05T00:30:00Z"
---

# 2026 oil shock: realized supply loss, global accounting, and closure scenarios

## Description

Reframe the core Hormuz research around oil and the observed 2026 shock:

1. Estimate how much the post-2026-02-28 disruption reduced global oil supply in each month for which actual or preliminary data exist.
2. Reconcile how the world absorbed the resulting gap through continued or rerouted Gulf flows, higher non-Gulf supply, the pre-war surplus, strategic and commercial stock draws, demand reduction or fuel switching, and an explicit residual.
3. Build low-fidelity but auditable oil-supply scenarios for specified closure durations, testing how long each mitigation channel can persist. Do not forecast oil prices.

Use 2026 actuals and contemporaneous estimates wherever available. Older data may define structural capacity or historical context, but 2024 route volumes must not stand in for realized 2026 supply losses.

## Scope Decisions

- Primary unit: million barrels per day (`mb/d`), with cumulative million barrels for multi-month totals.
- Primary commodity scope: IEA/EIA total oil or petroleum liquids so the global supply-demand-stock identity can close. Also report crude/condensate separately where sources permit. Exclude LNG, fertilizer, aluminium, and other non-oil products. Keep LPG/NGL/refined-product components only when they are part of a source's total-oil definition, and label the taxonomy to prevent double counting.
- Observed window: February 2026 pre-war baseline through the latest month with usable actual or preliminary observations. Preserve preliminary-versus-final status and source-vintage dates.
- Counterfactual: the February 2026 IEA/EIA outlook, frozen before the 2026-02-28 shock, supplemented by seasonal monthly actuals where a simple February level would mislead. Show sensitivity to counterfactual choice.
- Closure must be an operational transit assumption, not a binary label. Scenarios should specify permitted Hormuz flow, bypass flow, production constraints, and start/end dates.
- No Brent or product-price forecast. Price may be discussed only as a causal mechanism behind observed demand response, not as a projected output.

## Why This Is Feasible

This is a reasonable research path if the output is presented as a bounded reconstruction rather than a uniquely identified causal estimate. The public IEA record already supplies monthly anchors for Gulf and global production, Hormuz and bypass flows, inventories, emergency releases, refinery runs, and demand. EIA STEO vintages provide an independent pre-war counterfactual and current monthly balance.

The hard part is attribution. A missing Hormuz transit barrel is not necessarily a lost global-supply barrel; it may be rerouted, stored in the Gulf, shipped later, or replaced elsewhere. Similarly, refinery-run cuts are often a mechanism behind lower crude demand, not an additional supply offset. The analysis must therefore publish both an accounting identity and an uncertainty residual.

## Required Accounting Frames

### A. Physical disruption panel

Keep these monthly quantities separate:

- pre-war Hormuz and total Gulf exports;
- actual Hormuz transit;
- actual Gulf bypass and other non-Hormuz exports;
- affected Gulf production versus the frozen counterfactual;
- oil accumulated in Gulf onshore or floating storage;
- production shut in or lost to infrastructure damage;
- global oil supply versus counterfactual.

This panel answers "what happened to the at-risk Gulf barrels?"

### B. Global market-clearing bridge

For each month and cumulatively, reconcile the counterfactual Gulf supply loss with:

- Gulf route preservation or rerouting already captured in actual Gulf supply;
- pre-existing global surplus or excess stocks entering the crisis;
- incremental non-Gulf production versus the February counterfactual;
- net strategic/government stock draw versus counterfactual;
- net commercial and other observed stock draw versus counterfactual;
- demand reduction versus the February counterfactual, including clearly evidenced fuel switching;
- statistical, timing, and unobserved residual.

Do not count diverted cargoes as new global supply. Do not count an announced stock allocation as an observed draw. Do not add refinery-run cuts to end-user demand reduction without checking overlap.

The requested pie chart is acceptable for cumulative shares only after this bridge closes. The primary audit figure should be a waterfall or Sankey because it makes the identity and residual clearer; the pie can be the simplified publication view.

## Current Repository Inventory

| Existing asset | What can be reused | Limitation for this epic |
|---|---|---|
| `docs/hormuz-supplier-side-cushioning.md` and `scripts/build_ccx_supplier_side_cushioning.py` | Best current structural treatment of Saudi, UAE, Iraq, and Iran bypass routes; includes early-2026 demonstrated flows and route durability. | Denominators are largely 2024 EIA/Vortexa baselines; it is not a monthly global balance. |
| `data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv` and `docs/hormuz-global-energy-shock-accounting.md` | Existing accounting vocabulary and double-counting warnings. | Oil gross loss is a modeled 15.06 mb/d based on older exposure/scenario inputs; importer bridge rows are judgments and overlap with the global stock draw. This should be superseded, not merely relabeled. |
| `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv` | Exposure, bypass, and inventory-draw sensitivity scaffold. | Core oil row uses a 2024 20.26 mb/d baseline and modeled low/base/high values, not monthly 2026 observed supply. |
| `data/derived/hormuz_f6r_5_replacement_demand_response.csv` and `docs/hormuz-importer-adjustment.md` | Country mechanism hypotheses, especially Japan procurement/reserves, India substitution, and China run cuts. | Numeric bridge values are scenario allocations, not cargo or national-balance observations; they cannot be summed globally. |
| `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv` | Strong starting ledger for the IEA 400 mb action, regional allocations, U.S. withdrawals, Japan, Korea, and the distinction between public and obligated stocks. | Needs actual monthly execution through the latest date and separation from total observed inventory movement. |
| `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv` and `data/derived/hormuz_f6r_2_china_adjustment_matrix.csv` | Strong qualitative conclusion: commercial/operational draw and run cuts are supported; a large government-SPR draw is not. Includes April-May NBS evidence. | No public ownership-resolved stock series; needs later 2026 imports, runs, exports, and tank estimates. |
| `data/external/portwatch/hormuz_daily_chokepoint.csv` and `data/derived/hormuz_2y7_public_daily_tracker.csv` | Daily transit severity and reopening chronology through 2026-06-28. | Vessel calls/capacity are not loaded oil volumes, direction, or production. Refresh and use only as corroboration. |
| `data/derived/hormuz_4j7_3_current_hormuz_metric_slice.csv` | Source map for total-oil, crude, stock, and response claims. | The current headline row explicitly lacks a de-duplicated observed low/base/high disruption range. |
| `data/manifest.csv` | Relevant source inventory already includes IEA OMR/stocks, JODI, EIA stock series, China NBS/GACC, PortWatch, and project outputs. | Monthly 2026 OMR/STEO vintages and extracted values are mostly links or prose, not versioned raw/derived time series. |

## Data To Collect Or Normalize

### P0: needed to answer the three questions

1. **IEA OMR monthly evidence table, February-latest.** Extract supply, demand, Gulf/Hormuz/bypass flows, refinery runs, observed stock changes, government-stock changes, and explicit revisions from the February, March, April, May, June, July, and subsequent OMR releases. Store source vintage, observation month, status, definition, and citation for every value.
2. **EIA STEO vintage panel.** Preserve the February 2026 pre-war forecast and each post-shock vintage. Extract monthly global production, consumption, and stock change plus Middle East shut-ins where available. This is both an independent check and a transparent counterfactual-revision approach.
3. **Observed Gulf supply/export panel.** Saudi Arabia, Iraq, UAE, Kuwait, Iran, Qatar, Bahrain/Neutral Zone where material: production, total exports, Hormuz flow, bypass flow, onshore/floating storage change, and infrastructure outages. Prioritize IEA figures/commentary, EIA, JODI, OPEC secondary-source series, and national company/agency releases; use licensed Kpler/Vortexa only if access and publication terms allow.
4. **Global inventory ledger.** Separate IEA/OECD government stocks, obligated industry stocks, ordinary commercial stocks, non-OECD visible stocks, China estimates, and oil on water. Record announcements, availability, and actual draws as different fields.
5. **Demand counterfactual and observed response.** Build monthly global and regional demand deltas versus the frozen February forecast. Decompose only where evidence supports it: refinery/feedstock constraints, aviation, petrochemicals/naphtha, road fuel conservation, macroeconomic activity, shortages/rationing, and fuel switching. Treat renewable or electrification effects as a named bucket only if incremental 2026 displacement versus counterfactual is measurable; otherwise include them in demand reduction or residual.
6. **Latest transit chronology.** Refresh PortWatch and reconcile major reopening/reclosure dates with IEA/EIA flow estimates. Traffic data validate timing; they do not set cargo volumes.

### P1: improves attribution and durability

- country monthly imports by origin and refinery throughput for China, India, Japan, and South Korea;
- actual IEA emergency-release schedules and remaining usable emergency stocks by country;
- U.S. weekly SPR and commercial-stock series, plus analogous public series where available;
- non-Gulf incremental output/export response from the United States, Brazil, Guyana, Canada, Kazakhstan, Venezuela, Russia, and relevant refiners;
- policy-level demand-conservation measures from the IEA tracker and national agencies, paired with observed consumption rather than announcement counts;
- capacity, maintenance, crude-quality, port, tanker, and insurance constraints needed to turn theoretical supply into durable delivered supply.

## Proposed Work Plan

1. **Lock definitions and frozen counterfactual.** Write the total-oil taxonomy, monthly accounting equations, treatment of revisions, and scenario start dates before collecting more figures.
2. **Build a revision-aware monthly source table.** Normalize IEA OMR and EIA STEO February-latest into one long-form dataset with `observation_month`, `publication_vintage`, `actual_or_forecast`, `metric`, `value`, `unit`, `geography`, `definition`, `confidence`, and `source_url`.
3. **Estimate realized disruption.** Produce monthly gross route disruption, Gulf production loss, and net global supply loss with low/base/high uncertainty bands. Show why these three measures differ.
4. **Close the cumulative global bridge.** Reconcile March-latest in million barrels. Quantify the largest defensible buckets first; leave a visible unknown/residual rather than forcing a complete allocation.
5. **Audit importer mechanisms without summing scenario rows.** Use existing country work as hypotheses, then replace inferred values with actual trade, runs, stocks, and consumption data where available. Give China a range for commercial/operational stocks and leave government SPR separate and opaque.
6. **Model mitigation durability.** For each bucket, estimate current sustainable rate, remaining stock/capacity, ramp or decay rule, binding constraint, and uncertainty. Distinguish one-time stock cushions from renewable flows and reversible demand cuts from structural changes.
7. **Run closure-duration scenarios.** At minimum: effective closure through 2026-09-30, through 2026-12-31, and through 2027-03-31. Because partial reopening occurred in June, label clearly whether each is a no-reopening counterfactual from 2026-02-28 or a renewed-closure scenario from a specified later date. Include transit-severity sensitivities.
8. **Publish the evidence package.** Deliver the monthly data table, accounting waterfall/Sankey, simplified pie, durability table, scenario chart, source notes, and a concise oil-only narrative. Run a citation and arithmetic audit before unblocking blog drafting.

On kickoff, decompose these work packages into child task files and populate `children`; do not reuse completed issue IDs or silently overwrite their outputs.

## Scenario Design

Each scenario should propagate the accounting buckets rather than extrapolating price:

| Mitigation channel | Durability treatment |
|---|---|
| Gulf bypass and limited transit | Constrain by demonstrated throughput, export terminal capacity, existing utilization, crude/product compatibility, security, and maintenance. It is a continuing flow but not infinitely expandable. |
| Non-Gulf incremental supply | Use observed 2026 response first, then field/project ramp limits and decline/maintenance constraints. Separate higher production from redirection of existing exports. |
| Pre-war surplus | Treat as a finite initial cushion already embodied in stocks or lower required production, not a recurring monthly contribution. |
| Government/strategic stocks | Use actual release schedules, maximum feasible release rates, remaining stocks above legal/operational floors, and policy uncertainty. |
| Commercial and oil-on-water stocks | Use observed draw rates initially, then taper as working inventories approach operational minima. Do not assume all Chinese storage is government controlled or available. |
| Demand reduction | Split involuntary shortages and temporary conservation from persistent efficiency, modal or fuel switching, and structural output changes. Allow rebound when supply returns. |
| Refinery adaptation | Credit incremental product supply or crude-demand reduction only once and preserve crude/product timing differences. |
| Unknown/residual | Carry forward explicitly; widen over longer horizons rather than converting uncertainty into a precise point estimate. |

## Acceptance Criteria

- A source-vintage-aware monthly dataset covers February 2026 through the latest usable observation for global supply, demand, stock change, affected Gulf supply/exports, Hormuz/bypass flows, and major response channels.
- The analysis reports and explains at least three distinct measures: missing Hormuz flow, affected Gulf production loss, and net global supply loss.
- A cumulative global accounting bridge closes arithmetically within a published residual and uncertainty range; no importer or product double counting remains.
- Every pie slice is derived from that bridge, has an exact denominator, and can be traced to machine-readable data. A waterfall or Sankey exposes the underlying identity.
- 2024 data are used only for structure or sensitivity where a 2026 observed/counterfactual value is unavailable, and each such use is flagged.
- The stock ledger distinguishes announced availability, actual emergency release, obligated-industry relief, commercial draw, China commercial/operational stock movement, and government SPR.
- Demand reduction is measured against a frozen pre-war forecast and does not treat all refinery-run cuts, fuel switching, or macro weakness as independent additive buckets.
- Closure scenarios through at least 2026-09-30, 2026-12-31, and 2027-03-31 publish assumptions, bucket durability, remaining buffers, uncertainty bands, and failure points; they do not forecast oil prices.
- Outputs are reproducible from repository-local scripts and `.venv`, registered in `data/manifest.csv`, and citation-audited.

## Source Breadcrumbs

- IEA OMR February 2026 pre-war baseline: https://www.iea.org/reports/oil-market-report-february-2026
- IEA OMR March 2026: https://www.iea.org/reports/oil-market-report-march-2026
- IEA OMR April 2026: https://www.iea.org/reports/oil-market-report-april-2026
- IEA OMR May 2026: https://www.iea.org/reports/oil-market-report-may-2026
- IEA OMR June 2026: https://www.iea.org/reports/oil-market-report-june-2026
- IEA OMR July 2026: https://www.iea.org/reports/oil-market-report-july-2026
- IEA June commentary on observed market adjustment: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
- IEA emergency stock release and regional implementation: https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict and https://www.iea.org/news/update-on-iea-collective-action-decision-of-11-march-2026
- EIA July 2026 STEO global oil balance: https://www.eia.gov/outlooks/steo/report/global_oil.php
- IEA policy-response tracker launch: https://www.iea.org/news/iea-launches-tracker-to-monitor-policy-responses-to-energy-market-impacts-of-middle-east-conflict

## Work Notes

- 2026-08-03: Created after auditing the repository against the revised oil-only questions. The repo has strong source breadcrumbs, structural bypass work, reserve-response tables, China caveats, a traffic series, and an initial accounting frame. It does not yet have the required revision-aware monthly 2026 global oil dataset or a closed, non-overlapping accounting identity.
- 2026-08-03: Public IEA anchors demonstrate feasibility. March OMR estimated at least 10 mb/d of Gulf production cuts; April OMR reported March global supply down 10.1 mb/d and alternative-route exports up to 7.2 mb/d; May OMR put April global supply 12.8 mb/d below February and reported March-April stock draws; June OMR reported a 3.8 mb/d average observed stock draw since the war and a 5 mb/d year-on-year 2Q26 demand drop; July OMR reported a 4.1 mb/d June global-supply rebound, continued onshore stock draws, and June demand recovering from its May low. These are starting anchors, not yet a reconciled causal decomposition.
- 2026-08-03: The June IEA commentary is the closest public precursor to the requested pie: it reports average March-May Hormuz flows of 2.7 mb/d versus roughly 20 mb/d pre-war, a 3.7 mb/d pre-war market surplus, 3.8 mb/d average stock draws, 2.5 mb/d IEA emergency supply in May, Saudi and UAE bypass/export responses, Atlantic Basin supply gains, and major demand reductions. The epic must convert these partly overlapping facts into a single cumulative bridge with a residual.
- 2026-08-03: Current closure scenarios require careful labeling because June brought partial reopening and July saw renewed hostilities. A scenario "closed through September" can mean either a counterfactual with no June reopening or a renewed closure from an August start date; results are not comparable unless the start state is explicit.
- 2026-08-03: Claimed the epic and started three parallel child tasks. User direction fixes the first scenario convention: preserve observed history including the June relaxation, make charts cumulative through an explicit latest-data date, and project traffic near the refreshed current level through each future closure horizon. July estimates or forecast values may be used if clearly labeled by vintage and status.
- 2026-08-03: Opened `hormuz-m8q.4` for root-owned integration of the three parallel inputs into cumulative accounting charts and provisional future scenarios.
- 2026-08-03: After the transit refresh completed, opened `hormuz-m8q.5` for a separate provisional supply-scenario model using observed history through July, the refreshed current traffic regime, and mitigation durability constraints.
- 2026-08-03: All four delegated workstreams returned usable outputs. `m8q.1` built the revision-aware monthly balance, `m8q.2` refreshed PortWatch through 2026-07-23 and defined the current traffic regime, `m8q.3` compiled adjustment-channel evidence and durability constraints, and `m8q.5` produced the provisional oil-only closure model. Tasks `.1`, `.2`, `.3`, and `.5` are complete; `.4` remains active for the physical-disruption panel and final audit.
- 2026-08-03: First integrated results: EIA's July vintage places March-July liquids supply 1,724.4 million barrels below the frozen February forecast, reconciled arithmetically as 566.4 mb lower consumption, 479.2 mb of expected stock build that did not occur, and 678.8 mb of implied inventory draw. This is a forecast-vintage global balance revision, not a fully identified Hormuz causal effect. The provisional constant-current-traffic base case yields cumulative net supply losses of 2,534 mb through September, 3,647 mb through December, and 4,736 mb through March 2027, with explicit uncertainty and residuals.
- 2026-08-04: User requested that future scenarios pause as a publication focus until the historical March-July accounting is locked. Opened country-level workstreams `.6` Gulf physical flows and rerouting, `.7` incremental non-Gulf production, and `.8` emergency/commercial stocks plus demand/fuel switching. The target narrative must quantify material countries, dated actions, cumulative million barrels, low/base/high where needed, and an explicit residual. Every country row must be traceable to a source and marked observed, estimated, or speculative; refinery cuts, renewables, imports, and route shifts must not be double counted as independent supply.
- 2026-08-04: Completed the expanded historical package. `.6` reconstructs Gulf country shut-ins and bypass routes, `.7` measures non-Gulf country supply revisions, `.8` builds country stock and demand detail, `.10` audits announced-versus-executed emergency releases, and independent audit `.9` reconciles the physical route diagnostic and the global market-clearing identity. The user-facing synthesis is `docs/hormuz-historical-oil-accounting-march-july-2026.md`. The locked headline is 1.40-1.44 billion barrels of March-June global supply loss relative to prewar expectations; the consistent March-July EIA comparison is 1.724 billion barrels but July is forecast and not yet country-resolved.
- 2026-08-04: Opened `.11`-.13 to investigate the two largest residual mysteries: the gap between EIA implied and IEA observed stock draws, and the mechanisms behind lower oil consumption. These are explicitly hypothesis-building tasks. They must distinguish sourced observation, attributed analyst opinion, project inference, and numerical scenario rather than upgrading speculation into fact.
- 2026-08-05: Completed `.11`-.13 and integrated them into `docs/hormuz-inventory-and-demand-residual-stories.md`. Inventory scenarios partition the 308.171 million barrel diagnostic into 40/115/220 million barrels of candidate hidden physical draw in low/base/high-hidden cases, with the balance assigned to timing, vintage and model discrepancies. Demand scenarios close by country/region and yield a base global policy lens of 50.194 million barrels explicit restraint, 117.488 million decentralized response/switching, 298.767 million forced constraint/activity loss, and 116.540 million structural/revision/unknown across gross downward regions, offset by 16.633 million of higher North American consumption to reach the 566.356 million world gap. These are scenario stories, not causal estimates.
