---
id: "hormuz-m8q.13"
title: "Explain Middle East, Europe, and Africa oil-demand reduction mechanisms"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "demand"
  - "middle-east"
  - "europe"
  - "africa"
  - "policy"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "codex-subagent"
created_at: "2026-08-04T22:45:00Z"
updated_at: "2026-08-05T00:20:00Z"
---

# Explain Middle East, Europe, and Africa oil-demand reduction mechanisms

## Description

Build plausible sector, shortage, switching, and policy explanations for the 173.5 million barrel Middle East, 35.1 million Africa, and 29.7 million Europe oil-consumption revisions, with secondary attention to the smaller Eurasia and Latin America gaps. Focus on countries and sectors large enough to matter.

## Acceptance Criteria

- Establish approximate pre-shock oil-use structure by sector/product for the largest material countries or subregions.
- Investigate refinery/feedstock outages, domestic product scarcity, aviation/mobility interruption, power-sector fuel switching, rationing, conservation policy, price response, and macro/activity losses.
- Identify dated explicit policies and attributed analyst explanations.
- Provide low/base/high scenario allocations of each regional demand gap across switching, conservation/efficiency, shortage/activity reduction, forecast revision, and residual.
- Explain why North American consumption revised upward and whether this supports substitution or geographic activity-shifting hypotheses.
- Record source links, confidence, caveats, and all potential overlaps.

## Work Notes

- 2026-08-04: Opened for the expanded demand-mechanism investigation. The Middle East gap is unusually large and may reflect domestic supply/refinery disruption rather than voluntary conservation; the analysis must not equate all lower consumption with welfare-neutral efficiency.
- 2026-08-05: Completed an exact-closing, machine-readable scenario ledger at `data/derived/hormuz_m8q_13_non_asia_demand_mechanisms.csv`; regenerate with `scripts/build_m8q_13_non_asia_demand_mechanisms.py`. It contains 131 rows: three mutually exclusive scenario allocations for each of six regions, six pre-shock structure rows, and five policy/country/counterexample anchors. The script imports the regional totals directly from m8q.8 and validates every scenario to within one barrel-equivalent of its absolute regional total.

### Accounting boundary

- The object being explained is the **July 2026 EIA STEO revision against the frozen February 2026 forecast**, accumulated for March-July. March-June is historical/estimated; **July remains forecast**, so these are not five months of measured final consumption and cannot support precise causal claims.
- Positive numbers are consumption below the February counterfactual: Middle East **173.496 million bbl**, Africa **35.100**, Europe **29.701**, Eurasia **9.433**, and Central/South America **8.359**. North America instead revised **upward by 16.633 million bbl**. Together these six regions contribute a net **239.455 million bbl** of the global demand bridge.
- Scenario rows are explanatory allocations, not observations or independent additions. Each low/base/high view reassigns the same fixed regional number. The scenario names are `scarcity_dominant`, `base`, and `behavior_switching_high`; they are not statistical confidence intervals.
- "Demand reduction" includes involuntary product non-availability, grounded flights, refinery/feedstock interruption, lost economic activity, voluntary conservation, price response, switching, and ordinary forecast error. Treating all of it as clean-energy substitution would be substantively wrong.

### Base allocation (million barrels, March-July)

- **Middle East — 173.496:** forced refinery/feedstock/LPG scarcity **65.0**; aviation/security mobility loss **38.0**; trade/tourism/logistics and macro loss **30.0**; autonomous price response **12.0**; explicit conservation policy **10.0**; rapid oil switching **4.0**; forecast/unallocated **14.496**. This is a scarcity-and-activity story, not chiefly renewables. IEA reported widespread flight cancellations and LPG disruption in March, about 5 mb/d lower global refinery activity year-on-year in April, and Middle East export refineries still not fully restarted in July. World Bank reported near-zero Gulf growth and sharp Iraq/Kuwait/Qatar slowdowns, with Oman and Saudi relatively cushioned by non-Hormuz ports/pipelines. Counterargument: no public source measures the 65/38/30 split, and gasoline/residual/"other" product use is large enough that multiple pathways overlap.
- **Africa — 35.100:** forced transport-fuel/import scarcity **20.0**; trade/logistics/macro loss **5.0**; LPG/kerosene affordability and fuel stacking **3.5**; explicit conservation **2.5**; price response **2.0**; electrification/other switching **1.0**; residual **1.100**. Kpler's modeled initial East/Southern Africa demand loss was about 260 kb/d, falling to at least 150 kb/d April-July, with diesel the largest product; AfDB/ECA emphasized oil and refined-product import dependence. Egypt supplies the clearest dated policy evidence: 9pm shop closures, reduced lighting and remote work, later reported to reduce load and traffic. Counterargument: South Africa initially reported no immediate physical shortage and used fiscal relief, so the continent cannot be described as uniformly rationed.
- **Europe — 29.701:** aviation/jet constraint **10.0**; policy conservation **4.0**; price response **4.0**; macro/industrial/trade loss **3.0**; road-freight/product scarcity **2.0**; biofuel/electrification/other switching **1.5**; residual **5.201**. The Commission's dated actions were voluntary fuel-saving guidance (31 March), aviation slot/fuel flexibility (8 May), and a savings catalogue (13 May). Its later 15-20 Mtoe figure is annual technical potential, not realized March-July savings, and is deliberately not converted to barrels here. On 18 May the Commission still reported no aggregate EU fuel shortage and identified jet fuel as the main concern; this is why road scarcity receives little weight.
- **Eurasia — 9.433:** refinery/product constraint **4.5**; macro/trade/logistics **1.3**; price response **0.8**; aviation **0.5**; explicit conservation **0.5**; switching **0.2**; residual **1.633**. EIA assigns **9.065 million bbl** of the regional gap to Russia. IEA reported Russian refinery curtailment and affected domestic deliveries, but this is principally an overlapping Russia-Ukraine-war mechanism, not clean Hormuz attribution.
- **Central/South America — 8.359:** transport-price response **1.5**; macro/trade/logistics **1.2**; switching **0.8**; policy **0.7**; aviation **0.7**; localized scarcity **0.5**; residual **2.959**. EIA's Brazil suballocation (**9.577 million bbl**) exceeds the whole-region gap because the rest of the region offsets it by about **1.218 million bbl**. That internal reversal and sparse realized-volume evidence justify the large residual.
- **North America — 16.633 upward revision:** fiscal price shielding/tax relief **6.0**; U.S. product mix/seasonality **3.0**; Canada/Mexico baseline revision **3.0**; energy/export activity **2.0**; residual **2.633**. Canada suspended federal gasoline excise (10 cents/litre) and diesel/aviation excise (4 cents/litre) from 20 April; IMF says subsidies, caps and rebates made transport demand sticky. EIA product detail resists a simple driving story: the U.S. revision includes gasoline **+3.342 million bbl** and residual fuel **+5.672**, but distillate **-13.488** and jet **-3.908**, with total U.S. consumption only **+5.561** after other products. Canada contributes **+10.138** and Mexico **+0.937** million bbl to the region's upward revision.

### Pre-shock structure and material geographies

- OPEC's 2024 baseline puts Middle East demand at **8.854 mb/d**, led by Saudi Arabia **3.386**, Iran **1.859**, UAE **1.017**, Iraq **0.977**, Kuwait **0.468**, and Qatar **0.380**. Africa was **4.649 mb/d**, led by Egypt **0.885**, South Africa **0.632**, Nigeria **0.483**, and Algeria **0.467**. These annual baselines constrain magnitudes but do not identify causal March-July reductions.
- Africa's baseline was unusually transport-fuel-heavy: distillates **1.867 mb/d** and gasoline **1.208**. Eurostat reports road transport at **73%** of EU transport energy and aviation **13%**, while OPEC puts OECD Europe kerosene demand at **1.531 mb/d**. Latin America consumed **6.750 mb/d**, led by Brazil at **3.451**. Russia consumed **3.982 mb/d** versus **1.258** in other Eurasia.

### Scenario sensitivity and interpretation

- Middle East scarcity-dominant versus behavior/switching-high assigns forced refinery/feedstock scarcity **70 vs 55 million bbl**, explicit policy **5 vs 18**, switching **2 vs 7**, with the balance moving across aviation, macro, price response and residual. The base is the preferred narrative because the contemporaneous evidence is much stronger for physical and activity disruption than for rapid structural switching.
- Africa assigns forced transport/import scarcity **22 vs 17 million bbl** and switching **0.5 vs 2.5** across the outer cases. Europe assigns aviation **12 vs 8**, explicit policy **2 vs 6**, and switching **0.5 vs 3**. The smaller Eurasia and Latin America allocations deliberately retain meaningful forecast/model residuals.
- For North America the same three scenario slots are interpreted as more or less **policy shielding**, not more or less demand reduction. All allocations explain an upward revision and carry `allocation_sign_in_global_bridge = -1` so downstream code can net them correctly.
- Evidence quality is medium for baseline structure and dated policies, medium/low for matching mechanisms to regional totals, and low for exact barrel allocation. Avoid presenting component values without "scenario estimate" or equivalent language.

### Primary source breadcrumbs

- IEA Oil Market Reports: [March](https://www.iea.org/reports/oil-market-report-march-2026), [May](https://www.iea.org/reports/oil-market-report-may-2026), [July](https://www.iea.org/reports/oil-market-report-july-2026).
- [World Bank MENA June regional highlights](https://thedocs.worldbank.org/en/doc/2b672b3b0415d6b66c45b66579db4ef5-0050012026/related/GEP-Jun-2026-Regional-Highlights-MNA.pdf); [IMF oil-market assessment](https://www.imf.org/en/blogs/articles/2026/07/15/the-oil-market-absorbed-the-war-shock-but-buffers-are-running-low); [IMF fiscal-policy assessment](https://www.imf.org/en/blogs/articles/2026/06/18/the-energy-shock-is-testing-government-budgets).
- [OPEC Annual Statistical Bulletin 2025](https://www.opec.org/assets/assetdb/asb-2025.pdf); [Eurostat EU oil-use structure](https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/43212.pdf); [Eurostat transport energy](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251128-1).
- [Kpler Africa demand-loss analysis](https://www.kpler.com/blog/next-in-line-for-demand-losses-africa-transportation-fuels); [AfDB/ECA Africa assessment](https://www.afdb.org/en/news-and-events/press-releases/crisis-middle-east-could-cost-africa-02-percent-economic-growth-2026-92485); [Egypt measures](https://sis.gov.eg/en/media-center/news/pm-announces-fresh-energy-rationing-measures-amid-regional-crisis/); [South Africa statement](https://www.gov.za/news/media-statements/mineral-and-petroleum-resources-fuel-supply-and-prices-10-mar-2026).
- EU measures: [31 March](https://energy.ec.europa.eu/news/commission-calls-eu-countries-coordinate-measures-ensure-oil-security-supply-amid-middle-east-energy-2026-03-31_en), [8 May](https://transport.ec.europa.eu/news-events/news/commission-publishes-guidance-support-eu-transport-sector-affected-middle-east-crisis-2026-05-08_en), [13 May](https://energy.ec.europa.eu/news/commission-provides-eu-countries-practical-examples-address-energy-crisis-2026-05-13_en), [18 May](https://energy.ec.europa.eu/news/eu-continues-monitor-oil-market-situation-and-prepares-coordinated-response-address-jet-fuel-supply-2026-05-18_en); [Canada fuel-tax suspension](https://www.canada.ca/en/department-finance/news/2026/04/temporarily-suspending-the-federal-fuel-excise-tax.html).
