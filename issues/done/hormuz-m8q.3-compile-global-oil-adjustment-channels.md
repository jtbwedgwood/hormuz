---
id: "hormuz-m8q.3"
title: "Compile global oil adjustment channels and durability evidence"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "stocks"
  - "demand"
  - "supply-response"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-03T22:57:25Z"
updated_at: "2026-08-03T23:13:57Z"
---

# Compile global oil adjustment channels and durability evidence

## Description

Assemble observed or bounded evidence for the non-transit channels needed by the cumulative global oil accounting: initial surplus, Gulf bypass, incremental non-Gulf supply, emergency and commercial stock draw, demand reduction or fuel switching, and residual. Record durability constraints for future scenarios without forecasting prices.

## Acceptance Criteria

- A derived evidence table separates observed values, announcements, forecast estimates, and analyst inferences.
- Strategic/government stocks, obligated industry stocks, commercial stocks, China commercial/operational estimates, and oil on water are not conflated.
- Non-Gulf production growth is separated from redirection of existing exports.
- Demand reduction is benchmarked to the February pre-war outlook where possible and flags overlap with refinery-run cuts.
- Each channel has an as-of date, low/base/high or explicit uncertainty, durability constraint, source URL, and double-counting note.
- The issue handoff recommends which categories are fit for a cumulative pie and which should remain residual or narrative.

## Work Notes

- 2026-08-03: Started as part of the first `hormuz-m8q` parallel pass. Proposed output: `data/derived/hormuz_m8q_3_global_adjustment_evidence.csv`. Do not edit the monthly balance or PortWatch outputs owned by sibling tasks.
- 2026-08-03: Created `data/derived/hormuz_m8q_3_global_adjustment_evidence.csv` with 40 evidence rows and 21 fields. It covers the prewar surplus and stock cushion; Gulf bypass and limited-transit preservation; incremental non-Gulf production versus trade redirection; announced, provisional, observed, and remaining IEA emergency stocks; total/onshore/oil-on-water stock movements; China stock ownership ambiguity; demand reduction, refinery runs, fuel-switching policy evidence; and the required residual.
- 2026-08-03: The `cumulative_march_july_use` field is the integration router for the requested chart ending 2026-07-31:
  - `direct_cumulative_stock_input_through_2026-07-31_estimate` is the provisional emergency-release input. It is 290/315/330 million barrels low/base/high: 290 mb was reported released through 21 July; the base carries the observed May release rate of 2.5 mb/d through the final ten days; the high allows modest acceleration but stays below the announced envelope. This is explicitly a project inference and must be replaced if an official July-end execution update appears.
  - `june_monthly_physical_input`, `june_monthly_net_stock_input`, `may_monthly_demand_level`, and the related `needs_*_reconciliation`/`q2_anchor_*` rows are anchors for the sibling monthly balance, not standalone cumulative slices.
  - `july_proxy_not_primary` applies EIA's 2.2 mb/d 3Q inventory-draw forecast uniformly to July (-68.2 mb). It is deliberately low confidence because the STEO was completed on 1 July, assumes improving Strait traffic, and predates the 7-8 July escalation. Show it as forecast-hatched if used at all.
  - `context_only` rows are stock levels, capacity, annual forecasts, mixed trade-flow evidence, or mechanisms. They must not be mechanically integrated over March-July.
- 2026-08-03: Primary accounting conclusions and pie guidance:
  - **Fit for a cumulative slice after reconciliation:** actual emergency/strategic release; net observed stock change separated into government versus non-government only where ownership is complete; demand reduction versus the frozen February monthly forecast; incremental non-Gulf production versus that same forecast; Gulf route preservation relative to the frozen physical-flow counterfactual; residual.
  - **Not a standalone slice:** the 3.7 mb/d prewar surplus. It is a prewar balance condition, partly embodied in the stocks that entered the crisis, not a recurring postwar supply flow. The 477 mb 2025 stock build and 8.2 bn barrel opening stock level are context, not post-28-February offsets.
  - **Not additive as reported:** Atlantic Basin exports up 3.5 mb/d. IEA says this combines higher production, trade redirection, and stock draw; only a monthly production delta versus the frozen forecast belongs in incremental supply.
  - **Not additive as reported:** refinery-run cuts. They are a transmission mechanism from crude scarcity to product supply/end-user demand and overlap measured demand reduction.
  - **No separate renewables/fuel-switching slice yet:** IEA documents measures across nearly 80 countries but does not publish a de-duplicated realized global oil-displacement number. Keep these inside demand reduction or residual unless incremental 2026 oil savings can be measured.
  - **Always publish residual:** it should absorb statistical discrepancies, timing, revisions, unobserved stocks, and incomplete ownership splits rather than being back-allocated to preferred narratives.
- 2026-08-03: Stock ledger findings:
  - IEA announced 400 mb on 11 March. Its 19 March provisional country table summed to 426 mb: 280 mb public stocks, 119 mb obligated industry stocks, and 28 mb production increases. Those categories are not interchangeable and the 426 mb plan is not an observed draw.
  - IEA reported a 2.5 mb/d collective-action delivery rate in May, 290 mb cumulatively released by 21 July, and more than 1 bn barrels of government-controlled emergency stocks still held. The remaining gross stock is not all operationally or legally releasable.
  - July OMR revised the stock picture materially. June global observed stocks built 21 mb because oil on water rose 117 mb while onshore tanks drew about 96 mb. OECD government releases were 44 mb in June. The components must not be added to the +21 mb net total.
  - The June OMR's preliminary March-May average global draw of 3.8 mb/d is retained as a source-vintage marker, not the preferred cumulative total, because later monthly figures revised materially (for example the July OMR reports a 73 mb May OECD decline while the June OMR's 143 mb figure covered global observed stocks).
- 2026-08-03: China conclusion strengthened with latest official/agency evidence. China added 40 mb of crude to tanks in March, then led the June non-OECD draw with a 41 mb decline. IEA reported by 21 July that crude imports were nearly 50% below prewar levels. EIA's prewar estimate separates roughly 360 mb government-held from roughly 1 bn barrels of commercial crude in December 2025, even though EIA's broader China "strategic" definition includes commercial inventories. The public evidence therefore supports a large commercial/operational cushion and June draw, but not a separately quantified large government-SPR release.
- 2026-08-03: Demand findings. February IEA forecast 2026 demand growth of +0.85 mb/d; July projected -1.0 mb/d, a 1.85 mb/d downward annual revision. July OMR estimated 2Q demand down 4.8 mb/d year on year and May demand at 97.9 mb/d, down 5.3 mb/d year on year. EIA independently forecast 2026 consumption down 1.2 mb/d. None of those annual/year-on-year figures is the requested March-July gap versus the frozen February monthly forecast; the sibling balance must perform that monthly conversion.
- 2026-08-03: Route/supply findings. IEA reported early-April alternative-route Gulf exports at 7.2 mb/d versus less than 4 mb/d prewar; Saudi Yanbu exports above 5 mb/d in early June versus 2 mb/d prewar; and June total Gulf exports at 16.1 mb/d versus a 24 mb/d prewar average. The June 6.5 mb/d export rebound exceeded the 3.5 mb/d Gulf production rebound because it also released floating/onshore stocks. IEA's 21 July qualitative update said Gulf exports had slipped below late-June highs but remained above early-March to mid-June levels, so the refreshed tanker series should set the current-traffic scenario rather than assuming June's 16.1 mb/d is durable.
- 2026-08-03: Non-Gulf supply findings. The best public incremental-production anchor is IEA's statement that 2026 Americas supply growth was revised up by more than 0.6 mb/d since the start of the year, to 1.5 mb/d. This still needs a country/month February-vintage reconciliation. By contrast, the 3.5 mb/d rise in Atlantic Basin exports and the US May record of 13.1 mb/d are mixed production/redirection/stock signals and belong in narrative or destination-flow work, not directly in the pie.
- 2026-08-03: Primary official/source breadcrumbs (accessed 2026-08-03):
  - IEA OMR February 2026: https://www.iea.org/reports/oil-market-report-february-2026
  - IEA OMR March 2026: https://www.iea.org/reports/oil-market-report-march-2026
  - IEA OMR April 2026: https://www.iea.org/reports/oil-market-report-april-2026
  - IEA OMR May 2026: https://www.iea.org/reports/oil-market-report-may-2026
  - IEA OMR June 2026: https://www.iea.org/reports/oil-market-report-june-2026
  - IEA OMR July 2026: https://www.iea.org/reports/oil-market-report-july-2026
  - IEA June adjustment commentary: https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
  - IEA 11 March action: https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict
  - IEA 19 March provisional contribution table: https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
  - IEA 21 July market statement: https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
  - IEA policy response tracker: https://www.iea.org/data-and-statistics/data-tools/2026-energy-crisis-policy-response-tracker
  - EIA July 2026 STEO global oil market: https://www.eia.gov/outlooks/steo/report/global_oil.php
  - EIA China/US/Japan strategic inventory methodology and estimates: https://www.eia.gov/todayinenergy/detail.php?id=67504
- 2026-08-03: Validation passed with repository `.venv`: Python `csv.DictReader` parsed 40 unique evidence IDs across 12 channel labels and 21 columns with no ragged rows or missing required provenance/method fields. `data/manifest.csv` also parses cleanly and contains exactly one registration for the dataset. `git diff --check` passes for the files owned by this task.
