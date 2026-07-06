---
id: "hormuz-kmz.4"
title: "Investigate non-obvious disrupted products"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "non-energy"
  - "supply"
blocked_by:
  - "hormuz-fyp.1"
  - "hormuz-fyp.5"
blocks:
  - "hormuz-kmz.7"
  - "hormuz-s49.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:36Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Investigate non-obvious disrupted products

## Description

Look beyond oil/LNG/fertilizer for meaningful Hormuz-linked trade: petrochemical feedstocks, polymers, sulfur, metals, food, containerized goods, spare parts, or shipping services.

## Acceptance Criteria

Each candidate product is classified as material, minor, or not worth pursuing, with evidence and estimated scale.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Blocks: `hormuz-kmz.7` - Produce product disruption master table
- Blocks: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.

### Source-backed classification pass

Method:

- Favor primary/official sources and only use trade press or blog sources for framing where the official source is unavailable.
- Classify as `material` when Hormuz exposure is large enough to plausibly move a global market or a major regional market.
- Classify as `minor` when the channel is real but either second-order, geographically narrow, or hard to isolate as a separate market.
- Classify as `not worth pursuing` when the Hormuz linkage is too diffuse to justify a standalone line of inquiry for the blog.

Key evidence collected:

- IEA says the Strait is the primary export route for oil and natural gas from Gulf producers, around 25% of world seaborne oil trade transited the Strait in 2025, and around 80% of oil and oil products crossing it went to Asia. The same IEA page says over 110 bcm of LNG passed through in 2025, with about 93% of Qatar’s and 96% of the UAE’s LNG exports transiting the Strait. It also says about half of global seaborne sulphur trade moves through Hormuz and about 5 million tonnes of aluminum are shipped through it each year. Source: [IEA Strait of Hormuz topic page](https://www.iea.org/topics/the-middle-east-and-global-energy-markets).
- IEA’s March 2026 Oil Market Report says plunging LPG and naphtha supplies are forcing petrochemical plants to curb polymer production, and LPG use in cooking and heating is at risk. Source: [IEA Oil Market Report, March 2026](https://www.iea.org/reports/oil-market-report-march-2026).
- IEA’s LPG commentary says 30% of all seaborne LPG exports transited Hormuz in 2025, volumes fell from about 1.5 mb/d in 2025 to 0.3 mb/d in March 2026, and India lost more than half of its LPG imports in the first two months of the conflict. Source: [IEA LPG / cooking fuel commentary](https://www.iea.org/commentaries/energy-crisis-threatens-world-s-most-vulnerable-as-cooking-fuel-shortages-grow).
- World Bank says the Gulf region is a major source of fertilizers, aluminum, and many industrial inputs; it also flags shipping-through-Hormuz as the main variable for the shock’s duration. Source: [World Bank commodity markets blog](https://blogs.worldbank.org/en/developmenttalk/five-questions-on-how-the-war-in-the-middle-east-is-affecting-commodity-markets).
- UNCTAD says bunker fuel costs more than doubled, war-risk premiums surged, tanker freight rates jumped, and containers were affected by congestion and repositioning. Source: [UNCTAD cascading logistics disruptions](https://unctad.org/system/files/non-official-document/myem_tlb_12th_session_p4_tokuda_en.pdf).
- QatarEnergy says surplus LPG, condensates, sulfur, and naphtha are exported; its 2024 review also notes export/import facilities for refined products at the terminal. Source: [QatarEnergy annual review 2024 search result](https://www.qatarenergy.qa/en/MediaCenter/Publications/%E2%80%8BQatarEnergy%20Annual%20Review%202024.pdf) and [QatarEnergy news detail snippet](https://www.qatarenergy.qa/en/MediaCenter/Pages/newsdetails.aspx?ItemId=3897).
- ADNOC says Shah gas produces 4.2 million tons of sulfur per year and about 5% of global sulfur production, and ADNOC trading has expanded into LPG, naphtha, sulphur, and carbon. Source: [ADNOC Sour Gas](https://www.adnoc.ae/en/adnoc-sour-gas) and [ADNOC trading](https://www.adnoc.ae/en/adnoc-trading).
- EGA says it sold 2.74 million tonnes of primary cast metal in 2024 and supplies 50+ countries; Alba says it sold 1.61 million tonnes of metal in 2024, with 1.16 million tonnes of value-added product sales. Source: [EGA homepage](https://www.ega.ae/en) and [Alba annual report 2024](https://www.albasmelter.com/uploads/Alba_Annual_Report_2024_1.pdf).
- DP World says Jebel Ali handled 15.5 million TEU in 2024 and JAFZA logged $190 billion in trade over the last 12 months. Source: [DP World Jebel Ali throughput](https://www.dpworld.com/en/news/dp-world-records-highest-cargo-volumes-at-jebel-ali-port-since-2015) and [JAFZA 40th anniversary release](https://www.dpworld.com/en/news/jafza-turns-40-with-record-190bn-in-trade).
- FAO says import dependency exceeds 90% in some Gulf states, and the Council statement says Gulf countries rely on imports for 70 to 90% of staple food supply. Source: [FAO regional trade/nutrition note](https://www.fao.org/neareast/news/details/strengthening-the-link-between-trade-and-nutrition-in-the-arab-region/en) and [FAO Council opening statement](https://www.fao.org/director-general/speeches/details/180th-session-of-the-council--implications-for-world-food-security-and-agriculture-arising-from-disruptions-of-supply-chains-in-the-gulf-region--including-the-closure-of-key-maritime-routes--opening-statement/en).

| candidate product/service | classification | why_it_matters | approximate_scale | exposed_exporters_or_ports | likely_data_source | source | confidence | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sulphur | material | Half of seaborne sulphur trade moves through Hormuz, and sulfuric acid is a key input into fertilizer, refining, and several critical minerals chains. | Roughly 50% of global seaborne sulphur trade; ADNOC alone says 4.2 Mt/yr capacity and about 5% of global production. | UAE: ADNOC Sour Gas / Shah; QatarEnergy / Mesaieed; Saudi Gulf refining systems. | IEA trade share; company annual reviews; UN Comtrade HS 2503. | [IEA](https://www.iea.org/topics/the-middle-east-and-global-energy-markets); [ADNOC Sour Gas](https://www.adnoc.ae/en/adnoc-sour-gas); [QatarEnergy review snippet](https://www.qatarenergy.qa/en/MediaCenter/Publications/%E2%80%8BQatarEnergy%20Annual%20Review%202024.pdf) | high | One of the best non-obvious leads. Strong blog material if framed as an overlooked industrial input. |
| Aluminum | material | Hormuz is a real export lane for Gulf primary aluminum, which feeds construction, transport, packaging, and power systems globally. | IEA says about 5 Mt/yr of aluminum is shipped through the Strait; World Bank pegs the Gulf at about 8% of global supply. | Bahrain: Alba; UAE: EGA; Saudi and Qatari Gulf smelter/export chains. | IEA/World Bank; producer annual reports; UN Comtrade HS 7601. | [IEA](https://www.iea.org/topics/the-middle-east-and-global-energy-markets); [World Bank](https://blogs.worldbank.org/en/developmenttalk/five-questions-on-how-the-war-in-the-middle-east-is-affecting-commodity-markets); [EGA](https://www.ega.ae/en); [Alba](https://www.albasmelter.com/uploads/Alba_Annual_Report_2024_1.pdf) | high | Strong and visualizable. Worth keeping. |
| Petrochemicals / plastics | material | The clearest mechanism is feedstock scarcity: lower LPG and naphtha availability is already forcing polymer plants to cut output. | No clean single global Hormuz volume, but the affected Gulf petrochemical complex is very large; SABIC’s petrochemicals revenue was SAR 129.5 bn in 2024 and it operates across 44 countries in 2025. | SABIC sites in Saudi Arabia; ADNOC downstream / Borouge-linked flows in UAE; Qatar downstream complexes. | IEA OMR; company segment reports; UN Comtrade HS 29/39. | [IEA OMR](https://www.iea.org/reports/oil-market-report-march-2026); [SABIC business segment](https://www.sabic.com/en/investors/performance-financial-highlights/annual-report); [SABIC report](https://www.sabic.com/en/reports/integrated-report-2024/business-performance/business-segment-performance) | medium-high | This is a material knock-on channel, but the exact volume is harder to isolate than sulfur/aluminum. |
| LPG / NGL feedstocks / naphtha | material | This is a major cooking-fuel and petrochemical-feedstock shock, not just an energy price move. | IEA says 30% of seaborne LPG exports transited Hormuz in 2025; volumes fell from about 1.5 mb/d to 0.3 mb/d in March 2026; India lost more than half its LPG imports in early conflict months. | QatarEnergy / Ras Laffan and Mesaieed; UAE ADNOC; Saudi export/refinery systems. | IEA commentaries; company annual reviews; UN Comtrade HS 2711. | [IEA LPG commentary](https://www.iea.org/commentaries/energy-crisis-threatens-world-s-most-vulnerable-as-cooking-fuel-shortages-grow); [IEA OMR](https://www.iea.org/reports/oil-market-report-march-2026); [QatarEnergy review snippet](https://www.qatarenergy.qa/en/MediaCenter/Publications/%E2%80%8BQatarEnergy%20Annual%20Review%202024.pdf); [ADNOC refining](https://www.adnoc.ae/en/news-and-media/press-releases/2020/adnoc-invests-usd-3-and-a-half-bn-to-upgrade-ruwais-refining-capabilities-and-maximize-value-for-uae) | high | Probably the single strongest non-obvious market after sulfur/aluminum. |
| Containerized inputs / spare parts | minor | The shock shows up as lead times, inventory imbalances, and freight costs rather than a distinct commodity market. | Jebel Ali handled 15.5m TEU in 2024 and JAFZA did $190bn in trade, but only a subset is Hormuz-exposed and the affected product mix is diffuse. | Jebel Ali / JAFZA; Khalifa Port; Sohar / Salalah / regional distribution hubs. | Port throughput; customs data; UN Comtrade partner-country mirrors. | [UNCTAD logistics note](https://unctad.org/system/files/non-official-document/myem_tlb_12th_session_p4_tokuda_en.pdf); [DP World Jebel Ali](https://www.dpworld.com/en/news/dp-world-records-highest-cargo-volumes-at-jebel-ali-port-since-2015); [JAFZA trade](https://www.dpworld.com/en/news/jafza-turns-40-with-record-190bn-in-trade) | medium | Important operationally, but not clean enough for a standalone market estimate yet. |
| Metals other than aluminum | not worth pursuing | The linkage is mostly indirect price/input-cost transmission, not a clean Hormuz-specific trade lane. | World Bank says base metals prices may rise, but it does not identify a large discrete Hormuz-locked flow comparable to aluminum or sulfur. | Diffuse; mostly downstream refineries/mines worldwide rather than a chokepoint export lane. | LME / World Bank price series; national customs. | [World Bank commodity markets blog](https://blogs.worldbank.org/en/developmenttalk/five-questions-on-how-the-war-in-the-middle-east-is-affecting-commodity-markets); [IEA sulfuric acid note](https://www.iea.org/topics/the-middle-east-and-global-energy-markets) | medium | Keep only as a pricing spillover unless a sharper flow emerges. |
| Food / agri imports into the Gulf | minor | Gulf import dependence is real, but the market impact is mostly regional and heavily buffered by inventories, rerouting, and substitute suppliers. | FAO says import dependency exceeds 90% in some Gulf states; FAO also says Gulf countries rely on imports for 70-90% of staple food supply. | Gulf import ports and distributors; supplier bases in Turkey, India, Oman, the US, and Europe. | FAO; WITS / UN Comtrade; national food-security agencies. | [FAO note](https://www.fao.org/neareast/news/details/strengthening-the-link-between-trade-and-nutrition-in-the-arab-region/en); [FAO Council statement](https://www.fao.org/director-general/speeches/details/180th-session-of-the-council--implications-for-world-food-security-and-agriculture-arising-from-disruptions-of-supply-chains-in-the-gulf-region--including-the-closure-of-key-maritime-routes--opening-statement/en); [WITS Qatar food imports](https://wits.worldbank.org/CountryProfile/en/Country/QAT/Year/LTST/TradeFlow/Import/Partner/by-country/Product/16-24_FoodProd) | medium | Worth a brief mention for Gulf cost-of-living, not as a global market pillar. |
| Shipping services (freight, bunker, war risk insurance) | material | This is the broad multiplier: it affects every Hormuz-linked flow and several non-energy routes too. | UNCTAD says bunker fuel costs more than doubled, war-risk premiums surged, tanker freight rates jumped, and containers were affected by congestion and repositioning. | All Hormuz-bound tankers and container services; especially Asia-facing routes. | UNCTAD / Clarksons; Drewry; marine insurance market notices. | [UNCTAD logistics note](https://unctad.org/system/files/non-official-document/myem_tlb_12th_session_p4_tokuda_en.pdf); [UNCTAD Hormuz press material](https://unctad.org/system/files/press-material/ma26003_strait-of-hormuz-disruptions_en.pdf) | high | Not a product, but too important to omit because it amplifies the entire shock. |

Open question:

- If this needs to become a blog section, the best high-signal subset is probably `sulphur + aluminum + LPG/naphtha + shipping services`, with petrochemicals as the mechanism story and food/containerized goods as secondary spillovers.

### Completion Note

- 2026-07-06: Acceptance criteria met. Candidate products/services are classified as material, minor, or not worth pursuing, with evidence and approximate scale. The best publication-grade non-obvious leads are sulphur, aluminium, LPG/naphtha feedstocks, petrochemicals as mechanism, and shipping services as amplifier.
