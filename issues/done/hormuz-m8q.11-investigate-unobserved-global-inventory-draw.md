---
id: "hormuz-m8q.11"
title: "Investigate the unobserved global oil-inventory draw"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "stocks"
  - "residual"
  - "analyst-evidence"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "codex"
created_at: "2026-08-04T22:45:00Z"
updated_at: "2026-08-05T00:12:00Z"
---

# Investigate the unobserved global oil-inventory draw

## Description

Investigate the roughly 308 million barrel March-June difference between the EIA global balance's implied draw and the IEA observed-stock estimate. Search official statements, national data, trade press, tanker/storage analysis, and attributed analyst commentary for plausible locations and mechanisms, including non-IEA commercial stocks, China commercial or government stocks, oil on water, bonded storage, timing, and balance-model error.

## Acceptance Criteria

- Reconcile the U.S. commercial-stock draw with the IEA emergency-release headline and identify what is or is not already in IEA observed stocks.
- Produce a candidate allocation range for material mechanisms/geographies that sums to the residual, while labeling it as scenario accounting rather than observation.
- Include attributed competing analyst views and reasons each could be right or wrong.
- Distinguish physical tank draw, oil-on-water changes, statistical discrepancy, forecast revision, commercial stock, and government reserve.
- Record direct source links, dates, quotations only within copyright limits, confidence, and double-counting cautions.

## Work Notes

- 2026-08-04: Opened for the expanded residual investigation. The 308 million barrels is a difference between unlike coverage systems, not automatically a hidden physical draw. Candidate stories must first test coverage and timing before assigning it to China or other opaque stocks.
- 2026-08-04: Added `scripts/build_m8q_11_inventory_residual_scenarios.py` and generated `data/derived/hormuz_m8q_11_inventory_residual_scenarios.csv`. The ledger combines official methodology and observed anchors with three exact-closing sensitivity cases. It deliberately labels every allocation as scenario accounting rather than observation.

### Bottom line

The apparent **308.171 million barrel “missing draw” is real as arithmetic but not as an observed physical category**. It is the difference between:

- **606.171 million barrels** of March-June inventory draw implied by the project's EIA February-versus-July supply-and-demand balance; and
- **298 million barrels** in a project composite of IEA monthly observed-stock headlines.

The first is a model residual; the second is a bottom-up but preliminary observed-stock estimate. The IEA itself says that exact supply-demand-stock balance cannot be achieved because of reporting lags, and its `miscellaneous-to-balance` item combines non-reported stocks, floating storage/oil in transit, and errors in supply, demand, and stock estimates. This is almost a direct description of the 308 million barrel problem. Source: [IEA OMR glossary and methodology](https://www.iea.org/articles/oil-market-report-glossary), especially “Data Sources,” “Stocks,” and the preliminary-stock discussion.

The preferred interpretation is therefore a **mixed physical-plus-measurement residual**, not “China secretly released 308 million barrels” and not “the IEA missed 308 million barrels of tanks.” The base scenario assigns **115 million barrels** to genuinely physical draws outside the IEA observed perimeter and **193.171 million** to oil-on-water/cargo timing, preliminary-vintage differences, and supply-demand model error. The 115/193 split is a scenario, not an estimate.

### Resolution of the U.S. commercial-stock question

The U.S. commercial draw is **not** part of the IEA's “around 290 million barrels actually released” collective-action headline. That headline describes barrels released under the emergency program—government reserves and, in some countries, obligated-industry arrangements. Ordinary commercial inventory movement is outside that program.

The commercial draw **is**, however, inside IEA observed global stocks. The IEA methodology says:

- industry stocks are primary stocks owned by companies and traders, including industry stocks held to meet emergency obligations;
- its U.S. preliminary stock estimates use EIA Weekly and Monthly Petroleum Status Reports; and
- all reported stocks are generally primary stocks in refineries, terminals, pipelines and incoming vessels, whether government- or industry-owned.

Through the matched March-June endpoint used here, weekly EIA data show:

| U.S. component | March-June draw, million barrels | Where it belongs |
|---|---:|---|
| SPR | 89.786 | IEA observed stocks **and** collective-action delivery to the extent executed under that program |
| Total commercial petroleum excluding SPR | 67.317 | IEA observed stocks, but **not** the collective-action headline absent a specific obligation-relief action |
| **Combined** | **157.103** | Subset of global observed stocks |

The previously quoted **50.187 million barrel** commercial draw runs through 24 July. It is smaller because U.S. commercial stocks rebuilt somewhat in July. It is the wrong endpoint for the March-June 308.171 million barrel residual.

The combined March-June U.S. draw is about **52.7% of the project's 298 million barrel IEA composite**. IEA standardization and week-versus-month endpoints will make the exact IEA U.S. contribution differ slightly, but the central conclusion is robust: **the commercial draw explains why emergency-release totals and total inventory movement differ; it does not explain the 308 million barrel residual because it is already in the observed-stock denominator.**

Primary sources:

- [EIA weekly SPR](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1)
- [EIA weekly total commercial petroleum excluding SPR](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1)
- [IEA OMR methodology](https://www.iea.org/articles/oil-market-report-glossary)
- [IEA 21 July statement on roughly 290 million barrels released](https://www.iea.org/news/iea-executive-director-statement-on-oil-markets)

### A newly identified problem: 298 million barrels is not a single-vintage IEA total

The project constructed 298 million barrels from March -129, April -117, May -73 and June +21 million barrels. Those are the latest explicit monthly figures readily available in the public report summaries, but they are **not contemporaneous estimates from one OMR vintage**. The preliminary numbers changed sharply:

| Month | First public estimate | Later public estimate | Revision evidence |
|---|---:|---:|---|
| March | -85 million barrels in April OMR | -129 million in May OMR | 44 million more draw |
| April | -117 million in May OMR | -74 million in June OMR | 43 million less draw |
| May | -143 million in June OMR | -73 million in July OMR | 70 million less draw |
| June | +21 million in July OMR | not yet revised publicly | oil on water +117 outweighed onshore draw near 96 |

Sources: [April OMR](https://www.iea.org/reports/oil-market-report-april-2026), [May OMR](https://www.iea.org/reports/oil-market-report-may-2026), [June OMR](https://www.iea.org/reports/oil-market-report-june-2026), and [July OMR](https://www.iea.org/reports/oil-market-report-july-2026).

This means the residual should not be reported to the nearest million barrels without a strong warning. A June-vintage reading of the IEA's rounded 3.8 mb/d average draw since the war began implies a through-May cumulative draw in roughly the mid-340-million-barrel range before June's 21 million barrel build, rather than the mixed-vintage 298 million. The public summaries do not expose enough revised monthly detail to build a clean July-vintage March-June series. A 35 million barrel “preliminary vintage/cutoff” allowance is retained in every scenario, but that is judgment, not a formal error band.

### What is observable outside the United States

#### China: competing stories, with evidence for both

**Story A: Beijing mostly protected the SPR and forced the adjustment through lower refinery runs and commercial stocks.** This currently has the strongest direct support.

- On 10 April, reporting based on people familiar with the decision said Beijing authorized state refiners to use commercial reserves separate from the SPR. Energy Aspects suggested capacity to use about 1 mb/d in April-June and FGE estimated as much as 1 mb/d in April, but neither was an observed delivered total. [Straits Times/Bloomberg](https://www.straitstimes.com/asia/china-allows-state-oil-firms-to-tap-reserves-as-middle-east-war-drags)
- Kpler's Muyu Xu found observable China stocks near a record **1.24 billion barrels and up about 25 million** since the war by 13 May, directly contradicting a large visible early draw. Kpler said the May deficit not yet visible in data could mean either underground-stock use **or further downward refinery-run revisions**, especially in China. [Kpler, 13 May](https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2)
- Energy Aspects/Kayrros later estimated almost **25 million barrels drawn between May and 7 June**, and Vortexa, Kpler and Energy Aspects expected about **1 mb/d** of commercial draws going forward. [Bloomberg/Energy Connects, 10 June](https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/)
- The IEA later reported a **40 million barrel March build** and **41 million barrel June draw**. Those visible months net to only a 1 million barrel draw, with April-May unresolved in the public summary. [IEA July OMR](https://www.iea.org/reports/oil-market-report-july-2026)
- Kpler said in June that China refinery intake remained 2.6 mb/d below pre-war levels while onshore inventories were “largely untouched.” [Kpler, 17 June](https://www.kpler.com/blog/returning-persian-gulf-barrels-risk-a-short-term-supply-glut)

**Story B: underground government or NOC stocks quietly replenished visible commercial tanks.** This is possible, but not measurable from public evidence.

- Kpler analyst Sumit Ritolia said underground reserves might have been used to replenish observable tanks and that SPR use could not be completely ruled out; the same report said Kpler thought Beijing had continued adding to SPR during the war. These statements are compatible if gross underground withdrawals and simultaneous replenishment occurred, but they do not identify a net government draw. [Bloomberg/Energy Connects](https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/)
- U.S. Energy Secretary Chris Wright said China was releasing “some” reserves, while Kpler and satellite evidence emphasized commercial use and continuing SPR additions. Wright might have access to intelligence unavailable publicly, but his statement did not distinguish commercial from government stocks or provide a volume. It is treated as suggestive, not an observation.
- EIA estimates China entered the war with nearly **1.4 billion barrels** of broadly defined strategic inventory: about **360 million government-held** and **1 billion commercial**. EIA explicitly combines the two because NOC commercial stocks can perform a strategic function. The scale makes a hidden draw physically possible but says nothing about whether it occurred. [EIA, 21 April](https://www.eia.gov/todayinenergy/detail.php?id=67504)

The scenario range assigns **0/20/75 million barrels** to a *net additional* China underground/government draw not already visible. The 75-million high case averages 0.62 mb/d over March-June, below the analyst 1 mb/d commercial-use capacity. The base 20 is intentionally cautious. None of these is a finding.

#### Other Asia and non-OECD inventories

Country evidence confirms that large physical draws occurred, but most visible amounts should already be in the IEA observed total:

- Kpler estimated Japan drew **more than 70 million barrels** by 13 May; this is OECD-visible and therefore part of the observed denominator.
- Kpler estimated South Korea's visible wartime draw at **7 million barrels**, while noting that unreported SPR activity or refinery cuts could mask the true position.
- Kpler estimated India declined from **107 million barrels at end-February to 91 million in mid-May**, including SPR, commercial and refinery tanks. It separately identified about 3 million barrels from SPR sites. [Economic Times quoting Kpler](https://m.economictimes.com/markets/commodities/news/indias-crude-oil-stocks-drop-15-amid-iran-conflict-raising-supply-concerns/amp_articleshow/131105689.cms)
- Kpler later estimated **78 million barrels** of ex-China Asia-Pacific draw over March-May. This overlaps Japan, Korea, India and other country rows; it is a regional cross-check, not an additional amount. [Kpler, 17 June](https://www.kpler.com/blog/returning-persian-gulf-barrels-risk-a-short-term-supply-glut)
- Singapore official product stocks fell near a 13-year low, reaching about **34.4 million barrels** in the week before 17 June, then recovered to 35.3 million. This is strong mechanism evidence for regional commercial-product use but insufficient here for a clean pre-war cumulative barrel estimate. [Enterprise Singapore data reported by Reuters](https://energynews.oedigital.com/fuel-oil/2026/06/18/singapores-oil-product-stockpiles-recover-but-hover-at-a-13year-low)

Because the IEA has no formal non-OECD submission system and uses government, company, consultancy and journalistic sources with highly variable lags, some India/Asia/Africa/Latin America/producer storage will be missed or held unchanged. But directly observed Kpler country draws cannot simply be added to the 308 million residual: the IEA uses those same kinds of sources.

The scenario range assigns **30/70/110 million barrels** to *net other-non-OECD primary-stock draws outside the IEA visible perimeter*. This is a global coverage allowance, not a country estimate.

### Oil on water, storage perimeter, and statistical discrepancy

Oil on water is not omitted wholesale. It is part of the IEA observed global series:

- Kpler estimated oil on water fell **135 million barrels** from pre-war levels by late March, recovered to about 1.27 billion in early May, and stood near 1.235 billion on 13 May.
- The IEA estimated oil on water **rose 117 million barrels in June**, more than offsetting an approximately 96 million barrel onshore draw, producing the 21 million barrel global build.

The correct residual mechanism is therefore not “oil on water,” but **differences in AIS visibility, loading/discharge timing, sanctioned or dark fleet coverage, and geographic classification of in-transit versus landed stocks**. The scenarios allow 20/35/40 million barrels for this measurement/timing channel.

The IEA stock perimeter also excludes tertiary/end-user stocks and power-station stocks. Independent storage can be proprietary and difficult to collect. Physical draws from retail, end users, power stations and unreported downstream facilities could therefore support actual consumption without appearing in primary-stock observations. The scenarios allocate 10/25/35 million barrels to this channel.

Finally, Kpler's central interpretation of its own missing May balance is highly relevant: an implied deficit not visible in stocks points to **either underground draws or additional downward revisions to refinery runs**, particularly in China. The latter means demand was lower than modeled, not that hidden tanks were drained. This is why the base case leaves **123.171 million barrels** in EIA supply/demand/taxonomy error, and the measurement-heavy case leaves 213.171 million there.

### Exact-closing scenario accounting

All figures are million barrels and every column closes to 308.171. “Low” and “high” describe the amount assigned to unobserved physical draw, not statistical confidence bounds.

| Candidate mechanism | Low hidden-physical | Base mixed | High hidden-physical | Evidentiary status |
|---|---:|---:|---:|---|
| China underground government/NOC net draw not visible elsewhere | 0.000 | 20.000 | 75.000 | Possible; no public net measurement |
| Other non-OECD unreported primary-stock draw | 30.000 | 70.000 | 110.000 | Plausible coverage gap; country total unknown |
| Secondary/tertiary stocks excluded from primary-stock perimeter | 10.000 | 25.000 | 35.000 | Definitionally omitted; flow unmeasured |
| Oil-on-water and cargo timing/measurement error | 20.000 | 35.000 | 40.000 | Observed series exists but is volatile and revision-prone |
| IEA preliminary-vintage, standardization and cutoff mismatch | 35.000 | 35.000 | 35.000 | Directly demonstrated by large month revisions |
| EIA supply/demand forecast, taxonomy and balance error | 213.171 | 123.171 | 13.171 | Closing model allocation |
| **Total** | **308.171** | **308.171** | **308.171** | Exact arithmetic only |
| **Memo: genuinely hidden physical draw** | **40.000** | **115.000** | **220.000** | Sum of first three rows |

The high-hidden-physical case requires the EIA balance to be almost right and the IEA visible-stock perimeter to have missed 220 million physical barrels in four months. That is possible given opaque non-OECD storage, but it conflicts with the large observed-data revisions and China evidence showing tanks initially built. It is a stress case, not the preferred story.

The measurement-heavy case is also deliberately extreme: only 40 million hidden physical barrels and 268.171 million of measurement/model discrepancy. It is supported by the size of IEA preliminary revisions and Kpler's warning that refinery runs may need further downward revision, but it may understate real draws across non-OECD commercial and end-user systems.

The base mixed case is the best publication narrative at present:

> The EIA global balance implies about 606 million barrels were drawn from inventories in March-June, while a composite of public IEA observed-stock estimates identifies about 298 million. The roughly 308 million barrel difference should not be read as a secret reserve release. A defensible illustrative split assigns perhaps 115 million barrels to physical draws outside the visible primary-stock perimeter—including a small possible China underground component—and about 193 million to preliminary-data revisions, cargo timing, and errors in modeled supply or consumption. The true split is not observable, and analysts disagree most sharply about whether China used underground reserves or simply cut refinery runs more than balance models yet capture.

### Double-counting rules

1. The IEA 290 million collective release and the IEA observed-stock draw are different measures. Do not subtract 290 from 298 and call the balance “commercial stocks.”
2. U.S. March-June commercial stocks are already inside the observed-stock total; the 67.317 million draw cannot be assigned to the 308.171 residual.
3. U.S. SPR is in both observed stocks and collective-action execution. It must appear only once in any physical inventory pie.
4. Visible China, Japan, Korea, India, Singapore, or regional Kpler estimates are generally candidate suballocations/cross-checks of IEA observed stocks, not additions to them.
5. Regional ex-China Asia overlaps country rows.
6. Oil on water is already in the IEA observed total. Only measurement/timing differences around it belong in the residual scenario.
7. China commercial authorization, analyst draw capacity and government statements are not delivery observations.
8. The scenario totals partition 308.171. Their memo subtotals and anchor rows are non-additive.

### Validation

- Generated a 42-row, 16-field ledger with unique row IDs.
- Verified all three scenario allocations sum exactly to 308.171 million barrels.
- Verified U.S. March-June component arithmetic: 89.786 SPR + 67.317 commercial = 157.103 million barrels.
- Script compiles and regenerates with the repository `.venv`; no added dependencies.
