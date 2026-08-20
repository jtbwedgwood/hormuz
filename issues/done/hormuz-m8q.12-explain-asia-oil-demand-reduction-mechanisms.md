---
id: "hormuz-m8q.12"
title: "Explain Asian oil-demand reduction mechanisms"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-m8q"
labels:
  - "oil"
  - "demand"
  - "asia"
  - "policy"
  - "fuel-switching"
blocked_by: []
blocks:
  - "hormuz-m8q.4"
children: []
owner: "codex-subagent"
created_at: "2026-08-04T22:45:00Z"
updated_at: "2026-08-04T23:35:00Z"
---

# Explain Asian oil-demand reduction mechanisms

## Description

Build plausible sector and behavioral explanations for the 326.9 million barrel Asia/Oceania oil-consumption revision, focusing on China, India, Japan, South Korea, and the residual Asian group. Start from pre-shock oil use by sector and product, then assess what could physically switch fuels within months, what represents reduced activity or unmet consumption, and what was driven by explicit policy versus decentralized behavior.

## Acceptance Criteria

- Establish approximate pre-shock sector/product oil-use structures for material countries using primary data where possible.
- Separate power generation, transport, aviation, petrochemicals, industry, buildings, and refinery/feedstock effects.
- Identify dated policies and distinguish them from price response, shortage/rationing, macro weakness, and autonomous conservation.
- Provide low/base/high scenario allocations of each measured country demand gap across switching, efficiency/conservation, activity loss/shortage, structural trend or forecast revision, and residual.
- Keep EV/renewable structural displacement already embedded in the February forecast separate from incremental post-shock response.
- Record news/analyst disagreements, sources, assumptions, and explicit non-additivity warnings.

## Work Notes

- 2026-08-04: Opened for hypothesis-building after the exact regional demand bridge was completed. Fast oil-to-electricity switching is likely limited in China because oil has a small power-generation role; transport, aviation, petrochemicals, refinery constraints, and activity effects require separate treatment.
- 2026-08-04: Added `scripts/build_m8q_12_asia_demand_mechanism_scenarios.py` and generated `data/derived/hormuz_m8q_12_asia_demand_mechanism_scenarios.csv` with 66 rows. The ledger contains two alternative, non-additive views: a six-channel physical/behavioral mechanism allocation and a four-channel policy-versus-decentralized overlay. Every low/base/high column closes exactly to six decimals for China, India, Japan, the bounded Korea suballocation, the remaining Asia/Oceania residual, and the fixed 326.900353 million-barrel regional total.

### Scope and strongest conclusion

The **326.900 million barrels** is the July EIA STEO's March-July Asia/Oceania consumption revision against the frozen February STEO. March-June are preliminary; July is forecast. It is not an observed, causal estimate of oil voluntarily conserved because of Hormuz.

The most defensible regional story is:

> Asia did not replace hundreds of millions of barrels of oil with new renewable electricity in five months. Oil contributes almost nothing to Chinese and Indian power generation and only small shares in Japan and Korea. The fast adjustment occurred mainly through lower refinery and petrochemical throughput, especially naphtha; reduced aviation and industrial activity; expensive or unavailable product suppressing use; export restrictions preserving domestic supply; and decentralized price response. EVs, LNG/electric trucks, public transport and existing electrification made road demand more elastic, but most installed technology and baseline adoption were already in the February forecast.

The IEA's May report says petrochemicals and aviation were the most affected sectors, while its June report says end-user deliveries and Asian refinery runs were each down by roughly 5 mb/d year on year in 2Q26. These two statements support substantial final-demand and feedstock effects but do not identify country barrels. S&P Global's naphtha work provides the clearest physical mechanism: before the war, 1.2 mb/d crossed Hormuz, supplying 60-70% of Asian import needs; March Middle East shipments fell below one-fifth of February; Asian crackers cut rates or declared force majeure.

### Preferred regional mechanism scenario

The base case is deliberately low-fidelity. It is an allocation of the measured revision, not a claim that these values were observed independently.

| Mechanism | Low-switching case | Base case | High-switching case |
|---|---:|---:|---:|
| Incremental switching/electrification beyond February path | 15.730 | **39.633** | 74.334 |
| Voluntary conservation/efficiency | 33.083 | **52.563** | 63.973 |
| Forced shortage, refinery and feedstock constraints | 127.431 | **100.652** | 76.135 |
| Activity loss and macro feedback | 65.493 | **59.849** | 49.717 |
| Structural trend and ordinary forecast revision | 68.819 | **57.036** | 46.395 |
| Unresolved | 16.345 | **17.168** | 16.345 |
| **Asia/Oceania total** | **326.900** | **326.900** | **326.900** |

The scenario labels describe the interpretation, not statistical confidence limits. The low case puts only 4.8% of the region gap in switching; the base puts 12.1%; the high puts 22.7%. The base therefore rejects both extremes: neither "renewables solved it" nor "all of it was forced shortage" fits the evidence.

### Policy versus decentralized response

The preferred alternative overlay assigns the same 326.900 million barrels as follows:

| Attribution | Base estimate | Regional share | Interpretation |
|---|---:|---:|---|
| Explicit direct demand-restraint policy | **32.494m** | 9.9% | Telework, travel reduction, public transport/carpooling, conservation campaigns and purchase controls |
| Decentralized market/household response | **89.688m** | 27.4% | Price response and autonomous switching using already-installed equipment |
| Forced supply/industrial constraint | **113.567m** | 34.7% | Unavailable feedstocks/products, rationing, curtailed refinery/cracker/aviation activity |
| Structural, non-causal forecast revision and unknown | **91.151m** | 27.9% | Pre-existing trends, normal revisions and what cannot be identified |

This overlay is **not additive** to the six-mechanism table. It answers a different question. Direct policy is probably smaller in China, India, Japan and Korea than in Southeast Asia because these governments frequently used price controls, subsidies, tax cuts, stock releases and export restrictions to preserve supply and mute consumer incentives. Direct restraint was much more visible across Southeast Asia: the IEA records teleworking, shortened work weeks, travel reduction, public-transport promotion, fuel purchase controls and rationing across multiple countries by 7 May.

### China: 119.992 million barrels

Pre-shock structure and feasibility:

- China consumed 16.2 mb/d of refined petroleum products in 2023. EIA attributes already-slowing gasoline and diesel growth in 2024 to NEVs, high-speed rail, LNG/electric heavy trucks and weak property activity. EVs were already 48% of new vehicle sales in 2024.
- Petroleum generated only **0.1%** of Chinese electricity in 2023. Therefore additional wind and solar mainly displace coal or gas; they cannot directly explain a material oil slice over March-July.
- The likely short-run margins are gasoline and diesel mileage, aviation, petrochemical feedstock, refinery exports and inventories. Electric/LNG fleets make transport more able to switch mileage quickly, but new vehicle sales over five months turn over only a small fraction of the fleet.

Current evidence:

- NBS data imply crude-processing shortfalls of roughly 24.7m barrels in April, 39.4m in May and 80.8m in June versus a year earlier. These are not additive to end-use demand.
- S&P Global reported gasoline and gasoil sales about 10% lower year on year in late May, citing high prices and substitution; CERA expected a 1.4 mb/d 2Q oil-demand decline. State-refinery utilization was a 74-month low in May.
- Kpler argues the reduced crude availability was handled mainly through steeper refinery-run cuts while inventories continued to build in March and April. Reuters analyst Clyde Russell likewise cautioned that April's lower runs reflected export restrictions, not necessarily weak domestic final demand.
- The NDRC capped the March and April gasoline/diesel price increases below formula levels and instructed refiners to ensure supply. This likely **preserved** demand relative to full pass-through, so the gap cannot simply be called voluntary price response.

Preferred 119.992m allocation: **24.0 switching/electrification, 24.0 conservation, 36.0 forced refinery/feedstock constraint, 18.0 activity loss, 12.0 structural/forecast revision, and 6.0 unresolved**. The low/high switching range is 9.6-42.0m. A 24m base switching estimate averages 157 kb/d over 153 days, which is plausible as accelerated use of the existing EV/LNG-truck/high-speed-rail system; it is not attributed to newly built renewable capacity.

Reasons the 24m switching estimate may be too high: much of the structural displacement was already forecast; fuel-price controls muted the signal; the fleet cannot turn over quickly. Reasons it may be too low: gasoline/gasoil sales were down 10%, high oil prices altered utilization immediately, and electric/LNG alternatives were already deployed at scale.

### India: 41.141 million barrels

Pre-shock structure and feasibility:

- India consumed about 5.5 mb/d in 2024. Diesel and gasoline accounted for 42.9% and 16.1% of refinery product output respectively, while LPG, naphtha, jet fuel and bitumen are material non-road uses.
- Petroleum is 29% of primary energy but **less than 1% of power generation**. The electric grid, mostly coal plus renewables, could support induction cooking or EVs, but new renewable generation is not a direct substitute for most oil use.
- India had already reached national E20 gasoline blending in 2025. The proposed E85/E100 vehicles and higher future blends are strategically important but could not materially change the March-July fleet/fuel pool. Counting all E20 ethanol as a crisis response would be wrong.

Current evidence:

- PPAC data show that aggregate product consumption was down 6.5% year on year in May and 3.1% in June. The mix matters: May gasoline was down only 3.4% while diesel was up 1.6%; June gasoline and diesel were up 7.4% and 6.2%. By contrast, LPG was down 20% year on year in May and 14% in June, naphtha down 29% and 42%, and bitumen down 39% in May and 18% in June.
- This product pattern suggests the EIA gap is primarily **lower-than-expected growth plus LPG/naphtha/construction weakness**, not a 41m literal contraction in ordinary road fuel.
- FGE expected 2026 gasoline growth of 3.5-3.7%, slightly below its earlier 4%; ICRA cut gasoline growth from 5-6% to 3-4% and diesel from 2-3% growth to flat or contraction. Truckers reported longer waits for return loads as manufacturing slowed.
- Government policy often worked against conservation: the 29 March package cut petrol/diesel excise by Rs10/litre and imposed diesel/ATF export levies; public OMCs later absorbed about Rs5bn/day to protect consumers. Four mid-May pump-price hikes still left gasoline 7.8% and diesel 8.6% higher. A June retail-purchase control targeted bulk-customer arbitrage and hoarding, explicitly not general rationing.
- Prime Minister Modi did explicitly ask households to use public transport, carpool and skip international travel. This is real policy evidence, but no realized oil-savings estimate exists.

Preferred 41.141m allocation: **3.29 switching, 4.11 conservation, 7.41 forced shortage/feedstock, 10.29 activity loss, 13.17 ordinary growth/forecast revision, and 2.88 unresolved**. The relatively large revision bucket reflects continued year-on-year gasoline/diesel growth. The most credible actual destruction is in LPG, naphtha, bitumen and lost freight/industrial activity.

### Japan: 19.522 million barrels

Pre-shock structure and feasibility:

- Petroleum supplied 38% of Japanese primary energy in 2021 but only **3% of electricity**. Japan's oil use had already declined by more than 1.1 mb/d from 2013 to 2022 because of demographics, efficiency, nuclear restarts and weaker petrochemicals; these trends were already forecast.
- Japan's exposure was logistical and petrochemical: 94% of 2025 crude imports came from the Middle East and 93% passed Hormuz. Daiwa estimates more than 80% of naphtha supply is Middle East-linked once refinery feedstock is included.

Current evidence:

- April crude imports fell 65.7% year on year and domestic product sales fell 11.3%. Naphtha sales fell 35.6%, versus gasoline down 2.6%; that is much stronger evidence for forced petrochemical/feedstock contraction than household driving conservation.
- Daiwa estimates naphtha prices rose 83% from the start of 2026 and a tail-risk 50% supply cut could reduce real GDP 0.43%, mainly through chemicals.
- Japan released stocks and sourced alternative crude/naphtha. Refinery utilization subsequently recovered above 70%. This means the import collapse is not the same as final-demand destruction.
- METI subsidized gasoline, diesel, kerosene, heavy oil and jet fuel from 19 March, limiting consumer price pass-through. The policy makes large voluntary-conservation claims less likely.

Preferred 19.522m allocation: **1.56 switching, 2.34 conservation, 8.78 forced refinery/naphtha constraint, 2.93 activity loss, 2.93 trend/revision, and 0.98 unresolved**. The central story is petrochemical/feedstock loss, not rapid renewable substitution.

### South Korea: 7.65-61.20 million barrels, 30.60m base

Korea remains a candidate suballocation of the 146.246m Asia residual because EIA does not publish a separate country row in the STEO table used here.

- Road transport is about one-third of Korean oil demand, while naphtha is unusually important because Korea is a major petrochemical and refined-product exporter. Oil-fired power is small; rapid electricity-sector switching is not the main barrel mechanism.
- Kpler estimates Korean refinery runs fell nearly 1 mb/d in both April and May to roughly 2 mb/d, with another 300 kb/d inventory draw needed to sustain runs. The refinery-run loss is much larger than the 0.2 mb/d base demand-gap inference because it includes exports and stock movement.
- Korean petrochemical producers cut cracker rates and declared force majeure. More than 60% of crude and 50% of naphtha had passed Hormuz before the war.
- Seoul capped gasoline/product prices and instructed refiners to divert naphtha exports to domestic use; it also secured 24m UAE barrels and alternative supplies. These measures preserve domestic use and shift the likely gap toward petrochemicals/exports rather than motorists.

Preferred base allocation within 30.60m: **1.53 switching, 2.45 conservation, 13.77 forced refinery/feedstock constraint, 5.51 activity loss, 5.81 trend/revision, and 1.53 unresolved**. Even the base is less certain than the country totals above.

### Other Asia/Oceania: 115.646 million barrels in the base case

This bucket is heterogeneous and mechanically equals 146.246m less the Korea scenario. It includes Southeast Asia, Taiwan, Australia/New Zealand and other economies, so no single story should be presented as region-wide fact.

- Before the crisis, 60% of Southeast Asian crude imports came from the Middle East and 45% of product supply was Middle-East-linked after indirect refinery/feedstock trade.
- The IEA documents unusually explicit demand restraint by 7 May: telework and reduced travel in Cambodia, Laos, Malaysia, Myanmar, the Philippines and Thailand; public transport/carpooling in Indonesia, Singapore and Thailand; shorter school/work weeks; even-odd plates; purchase controls and fuel rationing.
- Many of the same governments also used subsidies, tax cuts and price caps, which offset the price signal. Some increased biofuel blending, but rapid scale-up was constrained by fuel standards, vehicle compatibility and agricultural feedstock.
- Regional petrochemical cuts are well evidenced: naphtha-fed crackers in Northeast and Southeast Asia reduced rates, while soaring input costs suppressed plastics demand. Aviation also fell below normal, according to IEA.
- Switching power generation from gas to coal or hydro helped the broader energy balance in Thailand and the Philippines but is not generally an oil-demand saving and should not be placed in the oil pie.

Preferred base allocation of 115.646m: **9.25 switching, 19.66 conservation, 34.69 forced shortage/feedstock, 23.13 activity loss, 23.13 forecast/structural revision, and 5.78 unresolved**. Explicit policy gets a larger base share here (20%) than in China, India, Japan or Korea because policy measures were broader and more coercive.

### Source disagreements and adjudication

1. **Weak demand versus forced runs:** S&P describes China's weak product demand and substitution; Kpler and analyst Clyde Russell emphasize feedstock constraints, export restrictions and continued inventory builds. Both can be true: domestic gasoline/diesel were buffered by product stocks and export cuts while refinery and petrochemical throughput contracted. The base splits China across switching/conservation (40%), forced constraints (30%), activity (15%) and non-causal/revision (15%).
2. **India shortage versus secure supply:** transporters described local diesel scarcity and idled trucks, while the government repeatedly stated there was no national shortage. The June control order says bulk-customer arbitrage caused localized outlet problems. This supports localized forced disruption, not nationwide road-fuel rationing.
3. **Import/refinery loss versus final demand:** Japan and Korea import and run cuts were far larger than their modeled domestic demand gaps because imports also serve exports and stocks. Therefore import/run numbers are mechanism evidence only.
4. **EV/renewable acceleration:** analysts credibly argue high oil prices increased EV interest and use of LNG/electric trucks. But sales, capacity and generation cannot be converted into crisis barrels without fleet, mileage, charging and February-counterfactual data. The scenario publishes a range instead of a false point estimate.

### Publication-ready synthesis

> Our base case assigns the 326.9 million-barrel Asia/Oceania demand revision to about 39.6 million barrels of incremental switching/electrification, 52.6 million of voluntary conservation, 100.7 million of forced refinery/feedstock and product constraints, 59.8 million of lost economic activity, 57.0 million of structural or ordinary forecast revision, and 17.2 million unresolved. An alternative policy lens attributes only about 32.5 million barrels directly to government restraint, versus 89.7 million of decentralized response and 113.6 million forced by supply or industrial constraints. These numbers are disciplined scenarios that close the accounting gap, not measured causal estimates.

### Double-counting and interpretation rules

- Do not add the mechanism allocation to the policy overlay; both allocate the same barrels.
- Do not add China refinery-run shortfalls, Japan/Korea import losses, cracker outages or product-specific declines to country demand gaps.
- Do not add Korea to the fixed 146.246m residual; subtract it to define "Other Asia/Oceania."
- Do not count pre-existing EV fleets, E20 ethanol, nuclear restarts, renewable capacity or structural efficiency as an incremental crisis response unless measured against the February path.
- Do not call power-sector coal/gas switching an oil saving when oil-fired generation was not displaced.
- Do not equate forecast revisions, import declines, refinery inputs and final consumption.

### Source breadcrumbs, accessed 4 August 2026

- EIA February and July STEO workbooks: https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx ; https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx
- IEA May and June OMR: https://www.iea.org/reports/oil-market-report-may-2026 ; https://www.iea.org/reports/oil-market-report-june-2026
- IEA Southeast Asia Energy Outlook 2026 policy table: https://www.iea.org/reports/southeast-asia-energy-outlook-2026/southeast-asia-s-energy-challenges-and-emerging-opportunities
- IEA State of Energy Policy 2026: https://www.iea.org/reports/state-of-energy-policy-2026/executive-summary
- EIA country briefs for China, India and Japan: https://www.eia.gov/international/content/analysis/countries_long/China/ ; https://www.eia.gov/international/content/analysis/countries_long/India/ ; https://www.eia.gov/international/content/analysis/countries_long/Japan/
- China refinery/product analysis: https://www.spglobal.com/energy/en/news-research/latest-news/shipping/052926-china-may-extend-refining-run-cuts-in-june-amid-tight-supply-low-demand
- Kpler Asian refinery and stock analysis: https://www.kpler.com/blog/drawing-down-how-the-market-is-absorbing-the-hormuz-shock-2
- China March price-control explanation: https://en.ndrc.gov.cn/news/mediarusources/202506/t20250626_1404387.html
- India official 13 and 29 March measures and 12 June control: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2239794&lang=1&reg=3 ; https://www.pib.gov.in/PressReleasePage.aspx?PRID=2246647&lang=1&reg=1 ; https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=289939
- India PPAC June product data and analyst demand outlook: https://www.marketscreener.com/news/india-s-june-fuel-consumption-slips-3-7-from-previous-month-ce7f5edbdf8df721 ; https://www.marketscreener.com/news/india-s-fuel-demand-outlook-hit-by-price-hikes-slowing-industrial-activity-ce7f5ddfdb8ff52c
- India fuel-switching/reporting context: https://apnews.com/article/ethanol-fuel-iran-war-india-southeast-asia-33b5a9d9aac68e4143c66a24dd4451fc
- Japan April product data: https://www.sahmcapital.com/news/content/update-1-japans-april-oil-imports-fall-nearly-66-yy-as-iran-war-disrupts-supply-2026-05-29
- Daiwa Japan naphtha analysis: https://www.dir.co.jp/english/research/report/analysis/20260707_025886.html
- Japan METI energy support: https://www.enecho.meti.go.jp/category/gekihen_lp/
- Korea supply/refining evidence: https://www.spglobal.com/energy/en/news-research/latest-news/refined-products/040826-south-korean-govt-secures-110-mil-barrels-of-crude-for-april-may-amid-hormuz-disruptions ; https://apnews.com/article/south-korea-oil-tanker-iran-hormuz-03228f42ac32c0bfce3bab744a77d199
- S&P Asia naphtha/petrochemical report: https://www.spglobal.com/energy/en/news-research/special-reports/chemicals/emerging-stronger-apic-2026/asia-petrochemicals-face-middle-east-war-challenges

### Validation

- Regenerated 66 rows with the repository `.venv`; no new dependency required.
- Verified unique row IDs and uniform 22-column CSV structure.
- Verified both accounting views close exactly to six decimals for every geography in all three scenarios.
- Verified China + India + Japan + bounded Korea + adjusted Other Asia/Oceania equals 326.900353 million barrels in every scenario.
- Script compilation, manifest parsing/uniqueness and `git diff --check` pass.
