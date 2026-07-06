---
id: "hormuz-kmz.2"
title: "Map bypass routes and non-Hormuz export capacity"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "infrastructure"
  - "routes"
  - "supply"
blocked_by:
  - "hormuz-fyp.1"
blocks:
  - "hormuz-kmz.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:33Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Map bypass routes and non-Hormuz export capacity

## Description

Quantify pipelines, alternate ports, domestic storage, and route options that can bypass Hormuz, including Saudi East-West, UAE ADCOP/Fujairah, Iraq/Turkey constraints, and gas/LNG limitations.

## Acceptance Criteria

Capacity table states nameplate vs usable capacity, current utilization, product compatibility, and constraints.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocks: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted

## Work Notes

- Research snapshot as of 2026-07-05.
- Source hierarchy used here: official operator/government/EIA/IEA first; Reuters/trade press only for current outage or contract-status notes.
- Nameplate and usable capacity are not the same thing. Where the public record does not give a clean spare-capacity number, the usable figure below is an inference from public throughput, routing constraints, and operator statements.
- Gas/LNG is the key practical limit: there is no true alternate export route for Qatari LNG, and UAE LNG mostly shares the same Strait exposure except for small deliveries into Kuwait.

| route/infrastructure | owner/country | products_supported | nameplate_capacity | usable_capacity_estimate | current_utilization_or_constraint | can_bypass_hormuz | source | confidence | notes |
|---|---|---|---|---|---|---|---|---|---|
| Saudi East-West crude pipeline (Petroline) to Yanbu / Red Sea export system | Saudi Arabia / Saudi Aramco | crude oil, condensate | 7.0 mb/d max (temporarily expanded from 5.0 mb/d) | ~5-7 mb/d physical bypass capacity; near-term spare is tighter because the line already hit max in Q1 2026 | Aramco said East-West reached 7.0 mb/d in Q1 2026; Saudi also pushed more crude over the line in 2024 to avoid Bab el-Mandeb disruption | Yes | [EIA - Hormuz chokepoint](https://www.eia.gov/todayinenergy/detail.php?id=65504); [Aramco Q1 2026 results](https://www.aramco.com/en/news-media/news/2026/aramco-announces-first-quarter-2026-results); [IEA - Hormuz](https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz) | High | This is the main crude bypass. The usable figure is an inference, not a published spare-slot number. |
| Saudi Abqaiq-Yanbu NGL pipeline | Saudi Arabia / Saudi Aramco | NGL, LPG-range liquids, mixed light liquids | 290 kb/d | ~290 kb/d gross route capacity | Parallel to Petroline; useful for NGL/LPG routing, not a substitute for crude export capacity | Yes, for NGL/LPG only | [EIA - Hormuz chokepoint](https://www.eia.gov/todayinenergy/detail.php?id=4430) | Medium | Relevant because a Hormuz shock hits product mix, not just crude. This does not replace crude bypass capacity. |
| ADCOP / Habshan-Fujairah pipeline and Fujairah export terminal | UAE / ADNOC | crude oil, condensate | 1.5 mb/d nameplate; IEA reports current capacity close to 1.8 mb/d | ~0.7 mb/d additional room beyond ~1.1 mb/d of current UAE crude moved this way | Active route; IEA says the UAE exports about 1.1 mb/d via Fujairah and has around 700 kb/d of extra room in a closure scenario | Yes | [ADNOC who we are](https://www.adnoc.ae/en/adnoc-pipelines/about-us/who-we-are); [IEA - Hormuz](https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz); [EIA - Hormuz chokepoint](https://www.eia.gov/todayinenergy/detail.php?id=65504) | High | Best public UAE bypass option. The 1.5 -> 1.8 mb/d gap is from IEA/EIA current-capacity reporting. |
| Iraq-Turkey pipeline (Kirkuk-Ceyhan) and Ceyhan export port | Iraq / Turkey / KRG-linked flows | crude oil | 1.5-1.6 mb/d nameplate depending on source | ~0.25-0.4 mb/d practical today for northern Iraqi crude | Reuters reported a restart on 2026-03-18 at an initial 250 kb/d; Turkey is resisting extension of the current deal as it nears July 2026 expiry, and security/political disputes still cap flows | Yes, but only for northern Iraqi crude | [EIA - Iraq brief](https://www.eia.gov/international/content/analysis/countries_long/Iraq/Iraq_2025.pdf); [Reuters Connect - Iraq resumes oil exports via Turkiye's Ceyhan port](https://www.reutersconnect.com/item/iraq-resumes-oil-exports-via-turkiyeas-ceyhan-port/dGFnOnJldXRlcnMuY29tLDIwMjY6bmV3c21sX01UMUFOQURMMDAwVUNWWUZZ); [Turkish Minute / Reuters summary](https://www.turkishminute.com/2026/06/16/turkey-opposes-extension-of-iraq-oil-pipeline-deal-under-current-terms-report/) | Medium | This is not a Gulf-wide bypass. It only helps northern Iraq; southern Iraqi exports still depend on Hormuz. |
| Ras Markaz crude storage + Duqm Liquid Export Terminal + OQ8 refinery | Oman / OQ / OTTCO | crude oil, refined products, LPG, sulfur, pet coke | 26.7 million bbl crude storage at Ras Markaz; 3.7 million bbl finished-product storage at Duqm; OQ8 refinery 230 kb/d | Useful as Oman-only non-Hormuz storage/export optionality; no public sustained throughput number that makes it a regional Hormuz substitute | OTTCO says Ras Markaz has handled >176 million bbl since 2023 and Duqm export terminal >21 million bbl via 560 vessels; this is real capacity, but it is mostly storage/handling rather than a giant spare export artery | Yes, for Omani volumes; limited as a regional bypass | [OTTCO Ras Markaz](https://www.ottco.om/terminals/ras-markaz); [OTTCO Duqm Liquid Export Terminal](https://www.ottco.om/terminals/duqm-liquid-export-terminal); [OQ growth projects](https://oq.com/en/our-business/growth-projects); [OQ / Vopak Duqm JV](https://oq.com/en/news-and-media/newsroom/20251023-ottco-and-royal-vopak-sign-strategic-agreement-to-establish-a-joint-venture) | Medium | Important for Omani crude/products and storage optionality. Not a replacement for Saudi/UAE bypass scale. |
| Qatar LNG export system (Ras Laffan / North Field) | Qatar / QatarEnergy | LNG | 126 MTPA planned capacity after expansion phase; QatarEnergy says current LNG capacity is 77 MTPA before expansion | 0 practical bypass capacity for Hormuz closure | IEA says there are no alternative routes to bring Qatari/UAE LNG to market; EIA said the March 2026 closure affected over 10 Bcf/d of LNG supply, mostly from Ras Laffan | No | [QatarEnergy LNG page](https://www.qatarenergy.qa/en/whoweare/Pages/WhatIsLNG.aspx); [IEA - Hormuz](https://www.iea.org/topics/the-middle-east-and-global-energy-markets); [EIA - LNG prices rise amid Hormuz closure](https://www.eia.gov/todayinenergy/detail.php?id=67604) | High | This is the clearest "no practical bypass" case. LNG cargoes need the Strait; there is no piped alternative to the global market. |
| Kuwait / Bahrain export systems | Kuwait / Bahrain | crude oil, refined products | 0 meaningful bypass capacity | 0 | IEA says Kuwait, Qatar and Bahrain rely on the Strait for the vast majority of oil exports; no operational bypass pipeline exists | No | [IEA - Hormuz](https://www.iea.org/topics/the-middle-east-and-global-energy-markets) | High | Keep this as a constraint row rather than a route row. These states can use storage or demand adjustment, but not a true alternate export corridor. |

Bottom line:

- Saudi and UAE together are the only serious crude bypasses. Public estimates of available bypass capacity cluster around 3.5-5.5 mb/d from IEA and about 2.6 mb/d from EIA, but both sources stress that the logistics are not fully tested at scale.
- Qatar LNG has no practical bypass. That is a hard constraint, not a modeling assumption.
- Oman is useful as an Omani export/staging node south of Hormuz, but it does not replace the Saudi/UAE crude bypass in system terms.
- Iraq-Turkey is a partial northern-Iraq escape valve, not a Gulf-system substitute.

### Completion Note

- 2026-07-06: Acceptance criteria met for current project stage. The capacity table separates nameplate from usable capacity, product compatibility, current constraints, bypass feasibility, sources, and confidence. Future work can refine utilization, but the route map is sufficient for `hormuz-kmz.3` sensitivity modeling.
