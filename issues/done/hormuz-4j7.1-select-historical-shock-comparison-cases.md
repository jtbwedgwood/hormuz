---
id: "hormuz-4j7.1"
title: "Select historical shock comparison cases"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-4j7"
labels:
  - "case-selection"
  - "comparisons"
  - "history"
blocked_by:
  - "hormuz-fyp.1"
blocks:
  - "hormuz-4j7.2"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:07Z"
updated_at: "2026-07-06T00:30:00-07:00"
---

# Select historical shock comparison cases

## Description

Choose the comparison set and justify inclusion/exclusion across oil embargoes, wars, strikes, infrastructure attacks, sanctions, and logistics shocks.

## Acceptance Criteria

Case list includes event dates, affected supply, duration, market context, and why the analogue matters.

## Dependency Notes

- Parent: `hormuz-4j7` - RQ6: Compare with historical energy and shipping shocks
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocks: `hormuz-4j7.2` - Define normalized comparison metrics

## Work Notes

- 2026-07-06: Claimed from `issues/open/tasks/`, reviewed completed source-quality rubric `hormuz-fyp.1`, and selected a comparison set for `hormuz-4j7.2` normalized metrics. Source standard used here: official/primary and institutional sources first; confidence reflects source quality plus comparability to a Strait of Hormuz shock.

### Recommended Comparison Set

| Case | Event dates / duration | Affected supply | Market context | Why the analogue matters | Confidence |
|---|---:|---:|---|---|---|
| Suez Crisis | Nov. 1956-Mar. 1957, about 4 months; IEA disruption window `Nov. 1956-March 1957` | IEA gross peak supply loss: 2.0 mb/d | Early postwar oil trade; Europe still heavily route-dependent; alternative pipeline/long-route options limited but oil market was much smaller than today | Best historical "strategic chokepoint closed by state/military action" case, but less comparable on scale and modern LNG/products | Medium |
| Six-Day War / Suez closure shock | June-Aug. 1967 acute oil disruption; canal remained closed June 1967-June 1975 | IEA gross peak supply loss: 2.0 mb/d | Route shock became long-lived logistics adaptation rather than a persistent equivalent physical supply loss | Useful for separating "route closure duration" from "actual barrels unavailable"; informs rerouting, tanker-size, and freight adaptation | Medium |
| Arab-Israeli War and Arab oil embargo | Oct. 1973-Mar. 1974, about 5 months | IEA gross peak supply loss: 4.3 mb/d; Fed History says OAPEC cuts nearly quadrupled oil from $2.90/bbl pre-embargo to $11.65/bbl in Jan. 1974 | Tight macro backdrop: high industrial capacity use, dollar devaluation, diminished U.S. domestic spare capacity; importing countries imposed conservation/efficiency policies | Canonical consumer-country vulnerability shock; best analogue for demand restraint, policy response, and macro inflation/stagflation narratives | High |
| Iranian Revolution | Nov. 1978-Apr. 1979 acute disruption; production impairment persisted beyond initial event | IEA gross peak supply loss: 5.6 mb/d; EIA says average Iranian crude output fell 3.9 mb/d over 1978-1981, with nearly 90% of Iranian output lost in Jan. 1979 | Strong global demand and speculative/precautionary stockbuilding; Fed History says oil prices more than doubled from Apr. 1979 to Apr. 1980 | Best producer-regime-collapse analogue for long recovery and for distinguishing gross loss from offsetting OPEC supply | High |
| Outbreak of Iran-Iraq War | Oct. 1980-Jan. 1981 acute disruption | IEA gross peak supply loss: 4.1 mb/d | Two major Gulf producers at war soon after the 1979 shock; direct regional war risk with eventual spillover into shipping | Most geographically relevant Gulf war supply-loss analogue before the Tanker War; useful for regional infrastructure and export-terminal vulnerability | High for supply loss; Medium for market context |
| Tanker War / Persian Gulf shipping attacks | Escalated 1984-1988 within the Iran-Iraq War; U.S. escort/reflagging phase mainly 1987-1988 | Not cleanly measured as daily supply removed; Naval History and Heritage Command describes rare tanker sinkings despite repeated attacks; Strauss Center notes 239 petroleum tankers attacked and 55 sunk/constructive total loss | Shipping risk/insurance and convoy problem more than sustained global supply removal; Strait remained open | Best analogue for "traffic continues under fire" rather than full closure; useful for insurance, escorts, dark fleet behavior, and vessel-count metrics | Medium |
| Iraqi invasion of Kuwait / Gulf War | Aug. 2, 1990-Jan. 1991 acute disruption; Kuwaiti recovery took years | IEA/EIA gross peak loss: about 4.3 mb/d combined Iraq/Kuwait; EIA says nearly all Kuwaiti and Iraqi output went offline immediately | IEA first collective action; large military conflict but with available offsetting supply and stocks | Best modern war + large producer outage analogue with official stock response and visible recovery path after infrastructure sabotage | High |
| Venezuelan oil strike | Dec. 2002-Mar. 2003, about 3 months | IEA gross peak supply loss: 2.6 mb/d | Non-Middle-East producer disruption overlapped with Iraq war and Nigerian strikes; market had multiple simultaneous disruptions | Useful non-war, non-Gulf political/labor benchmark; helps avoid overfitting every shock to Middle East military dynamics | High |
| Iraq war / overlapping 2003 disruptions | Mar.-Dec. 2003 for Iraq war disruption; overlapping with Venezuelan strike and Nigerian strikes | IEA gross peak supply loss: 2.3 mb/d for war in Iraq | IEA notes early 2003 disruptions overlapped, making attribution hard | Secondary in core set because it tests "compound shocks" and attribution, but less clean than 1990 or 1979 | Medium |
| Hurricanes Katrina/Rita | Sept. 2005 acute U.S. Gulf production/refining/logistics disruption | IEA gross peak supply loss: 1.5 mb/d; IEA collective action occurred after offshore rigs, pipelines, and refineries were damaged | Rich-country refining/product logistics shock, not a geopolitical export chokepoint | Useful control case for product-market/refining constraints and emergency stock releases; less relevant to Hormuz geopolitics | Medium |
| Libya civil war | Feb. 2011-rest of 2011 expected disruption; IEA collective action announced June 23, 2011 | IEA gross peak supply loss: 1.6 mb/d; IEA estimated 132 million barrels of light sweet crude removed by end-May 2011 | Tight light-sweet crude market during post-2008 recovery; IEA released 60 million barrels to bridge to OPEC increases | Best grade-specific disruption analogue: small global share, outsized price/product effects due to crude quality and refinery fit | High |
| Abqaiq-Khurais attack | Sept. 14, 2019; severe outage lasted days to weeks, with full restoration targeted by end-Sept. | EIA/CRS report temporary disruption of 5.7 mb/d, about 5% of global supply; Abqaiq capacity about 7 mb/d | High inventories and rapid Saudi repair/storage response muted duration despite record daily outage | Best infrastructure-attack analogue; use to show why peak barrels alone exaggerate impact if duration and inventories are favorable | High |
| Ever Given / Suez obstruction | Mar. 23-29, 2021; UNCTAD describes a seven-day Suez blockage | No clean oil supply loss; affected flow was canal capacity and containerized trade, including a 21,000+ TEU container vessel blocking the route | Pandemic-era supply chains and container freight were already strained; short, accidental obstruction rather than military closure | Best modern "high-frequency vessel tracker sees near-zero transits" analogue where supply is delayed, not destroyed | High for duration/route facts; Low as oil-supply analogue |
| Russia invasion of Ukraine / sanctions and buyer strike | Feb. 24, 2022 onward; acute market shock from Mar.-Apr. 2022, then long sanctions rerouting | IEA estimated from Apr. 2022 that 3 mb/d of Russian oil output could be shut in; Russia exported about 5 mb/d crude and 2.85 mb/d products pre-shock; IEA 2022 collective actions totaled 182.7 million barrels | Pre-existing tightness after COVID recovery; sanctions, self-sanctioning, freight/insurance, and redirection rather than simple field shutdown | Best analogue for sanctions, tanker rerouting, buyer substitution, and strategic stock releases at scale | High for market response; Medium for physical supply loss |

### Recommended Core Set for Analysis

- Use as primary comparators: `1973-74 Arab oil embargo`, `1978-79 Iranian Revolution`, `1980 Iran-Iraq War outbreak`, `1990 Iraq/Kuwait`, `2011 Libya`, `2019 Abqaiq-Khurais`, and `2022 Russia/Ukraine sanctions`.
- Use as route/shipping comparators: `1956 Suez`, `1967-75 Suez closure`, `1984-88 Tanker War`, and `2021 Ever Given/Suez`.
- Use as control/secondary comparators: `2002-03 Venezuela strike`, `2003 Iraq/Nigeria/Venezuela compound shock`, and `2005 Katrina/Rita`.

Rationale: the primary set covers the cleanest official daily supply-loss cases and the most policy-relevant modern shocks. The route/shipping set should not be merged mechanically with supply-loss cases; those cases measure freight delay, war-risk premia, vessel throughput, and rerouting rather than barrels permanently removed. The control set is useful for robustness checks and for showing when price effects came from grades/refining/logistics rather than only crude supply volume.

### Excluded or Secondary Cases

- COVID-19 demand collapse, 2020: exclude from main "supply shock" comparison; keep only as macro context for inventories, spare capacity, and demand destruction methods.
- 1979-1981 second oil shock and 1980 Iran-Iraq war as a combined episode: avoid double-counting in the core table. Treat Iranian Revolution and Iran-Iraq outbreak as separate acute events, then optionally show a combined "1978-81 Gulf instability" sensitivity.
- Iraqi oil export suspension, June-July 2001: IEA lists 2.1 mb/d gross peak loss, but duration and market importance are narrower; use only if the metrics task needs a sanctions/export-policy mini-case.
- Red Sea/Houthi shipping disruptions, 2023-2025: useful modern shipping-risk comparison, but outside the historical oil-supply core unless another task supplies verified transit, freight, and insurance data.
- Fukushima/Japan LNG demand shock, 2011: not an oil supply disruption; potentially useful for LNG substitution and demand pull, but outside this task.

### Open Data Gaps for `hormuz-4j7.2` / `hormuz-4j7.3`

- Need a consistent denominator for each event: global liquids production, seaborne oil trade, and regional export capacity at event date. IEA peak-loss figures are comparable for gross supply loss, but not normalized.
- Need duration metric choices: peak-loss days, days above 1 mb/d loss, cumulative barrels lost, and recovery-to-90%-of-baseline. Some cases have clean official windows; Tanker War, sanctions, and long Suez closure do not.
- Need price series conventions: nominal vs real Brent/WTI/Arabian Light; pre-1980 benchmark selection is nontrivial.
- Need inventory/spare-capacity context: IEA stock releases are well documented, but OPEC spare capacity and commercial inventory coverage must be assembled consistently.
- Need product/LNG extension: Suez and Hormuz comparisons should include LNG, LPG, refined products, and petrochemical feedstocks where data exist; most historical oil-shock tables do not.

### Source Breadcrumbs

- IEA, `IEA Response System for Oil Supply Emergencies`, 2012, accessed 2026-07-06. Key table: major world oil supply disruptions with dates and gross peak supply losses; key policy notes: IEA response criteria and stockdraw tools. https://energy.gov/sites/prod/files/2013/09/f3/IEA%20Response%20System%20for%20Oil%20Supply%20Emergencies%202012.pdf
- EIA, `Effects of crude oil supply disruptions: how long can they last?`, 2011-03-23, accessed 2026-07-06. Used for Iranian Revolution, Iraq/Kuwait, Venezuela duration/recovery notes and offsetting supply framing. https://www.eia.gov/todayinenergy/detail.php?id=730
- IEA, `Oil security and emergency response`, accessed 2026-07-06. Used for IEA 90-day stock obligation, collective-action history, and assessment criteria. https://www.iea.org/about/oil-security-and-emergency-response
- U.S. Department of State, Office of the Historian, `Oil Embargo, 1973-1974`, accessed 2026-07-06. Used for embargo target countries, production cuts, price/macro/policy context. https://history.state.gov/milestones/1969-1976/oil-embargo
- Federal Reserve History, `Oil Shock of 1973-74`, accessed 2026-07-06. Used for dates, price move, macro context, and U.S. spare-capacity context. https://www.federalreservehistory.org/essays/oil-shock-of-1973-74
- Federal Reserve History, `Oil Shock of 1978-79`, accessed 2026-07-06. Used for Iranian Revolution output loss, demand/hoarding context, price doubling, and inflation context. https://www.federalreservehistory.org/essays/oil-shock-of-1978-79
- EIA, `Saudi Arabia crude oil production outage affects global crude oil markets`, 2019-09-16, accessed 2026-07-06. Used for Abqaiq/Khurais facility capacity and immediate outage facts. https://www.eia.gov/todayinenergy/detail.php?id=41413
- CRS via EveryCRSReport, `Attacks on Saudi Oil Facilities: Effects and Responses`, 2019-10-01, accessed 2026-07-06. Used for Abqaiq 5.7 mb/d outage and share of global supply. https://www.everycrsreport.com/files/20191001_IN11173_7532e63c088a7570f3182f0c7b5ff3767678164c.html
- IEA, `IEA makes 60 million barrels of oil available to market to offset Libyan disruption`, 2011-06-23, accessed 2026-07-06. Used for Libya cumulative loss, expected duration, and stock-release rationale. https://www.iea.org/news/iea-makes-60-million-barrels-of-oil-available-to-market-to-offset-libyan-disruption
- IEA, `Oil Market Report - March 2022`, 2022-03-16, accessed 2026-07-06. Used for Russian oil shut-in risk, spare-capacity context, and sanctions/buyer-strike framing. https://www.iea.org/reports/oil-market-report-march-2022
- IEA, `IEA Governing Board concludes 2022 collective actions`, 2023-06-30, accessed 2026-07-06. Used for 182.7 million barrel total 2022 emergency stock release. https://www.iea.org/news/iea-governing-board-concludes-2022-collective-actions
- EIA, `World Oil Transit Chokepoints`, accessed 2026-07-06. Used for chokepoint framing and Suez/Hormuz rerouting logic. https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints
- EIA, `The Suez Canal and SUMED Pipeline are critical chokepoints for oil and natural gas trade`, 2019-07-23, accessed 2026-07-06. Used for Suez/SUMED modern bypass logic. https://www.eia.gov/todayinenergy/detail.php?id=40152
- IEA, `Suez Canal - Factsheet`, accessed 2026-07-06. Used for modern Suez oil/LNG flow and rerouting context. https://iea.blob.core.windows.net/assets/0a3c8da7-43ad-4511-a0ff-932fd8d0825a/SuezCanal-Factsheet.pdf
- U.S. Naval History and Heritage Command, `H-018-1: The Tanker War`, accessed 2026-07-06. Used for Tanker War shipping-risk framing and tanker resilience. https://www.history.navy.mil/about-us/leadership/director/directors-corner/h-grams/h-gram-018/h-018-1.html
- Strauss Center, `Strait of Hormuz: Tanker War`, accessed 2026-07-06. Used for tanker attack counts and petroleum-tanker loss-rate framing; institutional secondary source. https://www.strausscenter.org/strait-of-hormuz-tanker-war/
- UNCTAD resilient maritime logistics case study, `Port of Port Said, Egypt`, accessed 2026-07-06. Used for 2021 Ever Given/Suez one-week operational obstruction and 21,000+ TEU fact. https://resilientmaritimelogistics.unctad.org/guidebook/case-study-3-port-port-said-egypt
