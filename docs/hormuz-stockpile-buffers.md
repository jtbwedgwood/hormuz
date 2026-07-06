# Hormuz Stockpile Buffers

Last updated: 2026-07-06.

## Bottom Line

Stockpiles buy time, but they do not make the Hormuz shock disappear. The best current result is a ranked buffer story: oil reserves can bridge specific residual flow gaps, Japan is the cleanest public case, China should not be described as a confirmed large SPR draw, gas/LNG buffers are much less comparable than oil reserves, and fertilizer/chemical inventories are mostly too opaque for global days-of-cover claims.

For the blog post, the cleanest framing is:

- Oil reserves are real but policy-gated. IEA/OECD releases and national reserves can bridge residual gaps, but announced allocations, exchanges, private obligations, and actual stock draws are not the same thing.
- China SPR claims are low confidence. Public evidence supports commercial/operational stock draws and broad inventory optionality, not a large confirmed government-SPR release.
- LNG/gas buffers are heterogeneous. Europe has the best daily public stock series; Japan and Korea have useful LNG tank/rule buffers; China is only a capacity proxy; India is mostly rationing and replacement cargoes rather than visible storage.
- Fertilizer and chemical buffers are the weak link. India supports seasonal fertilizer stock proxies, but global sulfur, ammonia, petrochemical, and LPG-feedstock days-of-cover claims are not public enough.

## Coolest Results

| Result | Why It Matters | Best Current Number | Confidence |
|---|---|---:|---|
| Japan is the cleanest reserve bridge. | It links high exposure, named replacement routes, reserve releases, and limited demand destruction. | Base residual inventory bridge: about 199.5 days on the modeled reserve-draw leg. | High. |
| China is not a confirmed SPR release story. | This prevents a tempting but unsupported headline. | Publicly confirmed large government SPR release: effectively 0; commercial/operational draw proxy: about 25 days at 1.0 mb/d. | Medium-low for duration; high for "not proven SPR." |
| Europe has the cleanest gas stock dashboard. | GIE gives daily public working-gas storage, unlike most LNG importers. | 565.62 TWh, about 56.7 days of average 2025 EU gas demand. | High. |
| Korea has a clear LNG reserve rule but weaker live visibility. | The rule is public, actual contemporaneous fill is less visible. | 37 days on the legal domestic-sales basis. | Medium. |
| India gas/LPG is a rationing story, not a storage story. | The policy response is more observable than stock duration. | No defensible public national storage-days estimate; official gas affected-supply denominator was 47.4 MMSCMD. | Medium-high for policy; low for storage. |
| Fertilizer buffers are country-specific. | Food-chain claims need care. | India seasonal proxies: urea 41 days, DAP 67 days, MOP 123 days, NPKS 113 days. | Medium to medium-low. |

## Consolidated Buffer Table

The main output is `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`. It has 21 rows and should be used as a scenario table, not a live reserve tracker.

| Importer / Region | Product / Channel | Buffer Metric | Base Buffer Days | Confidence |
|---|---|---|---:|---|
| United States | Crude oil and petroleum liquids | IEA allocation / SPR exchange bridge | 492.0 | Medium-high |
| Europe and Mediterranean | Crude oil and refined products | Approximate EU share of IEA release | 400.0 | Medium |
| Japan | Crude oil and condensate | Public/private reserve release bridge | 199.5 | High |
| South Korea | Crude oil and condensate | IEA release allocation bridge | 56.3 | Medium-low |
| India | Crude oil and condensate | Phase-I strategic reserve proxy | 156.4 | Medium |
| China | Crude oil and condensate | Commercial/operational crude stock draw proxy | 25.0 | Medium-low |
| Europe | Gas / LNG-linked gas market | Underground gas storage working gas | 56.7 | High |
| Japan | LNG | LNG tank inventory / capacity ceiling | 21.0 | Medium |
| South Korea | LNG and condensate-linked gas | LNG statutory reserve rule | 37.0 | Medium |
| China | Natural gas / LNG | Gas storage peak-shaving capacity proxy | 19.4 | Low-medium |
| Singapore | LNG / gas | LNG terminal tank capacity ceiling | 15.6 | Low-medium |
| Thailand | LNG | LNG emergency-exercise scenario coverage | 36.0 | Medium for scenario, low for current stock |
| India | Urea fertilizer | Seasonal stock divided by average seasonal sales | 41.0 | Medium |
| India | DAP / phosphate fertilizer | Seasonal stock divided by average seasonal sales | 67.0 | Medium |
| India | MOP / potash fertilizer | Seasonal stock divided by average seasonal sales | 123.0 | Medium-low for Hormuz relevance |
| India | NPKS fertilizer | Seasonal stock divided by average seasonal sales | 113.0 | Medium-low |

Rows for India gas/LPG, global urea, global sulfur, and petrochemical/LPG/naphtha feedstocks are intentionally qualitative or blank in the day-count fields. Public evidence supports exposure and policy response, but not a reliable global stock-duration calculation.

## How To Read The Days

Use the days in three different ways, depending on the row.

| Row Type | What The Days Mean | Main Caveat |
|---|---|---|
| Oil reserve rows | Public stock/release anchor divided by modeled low/base/high inventory-draw need. | This is a residual bridge calculation, not proof that all reserves can be released instantly. |
| Europe gas storage | Observed working gas divided by average daily demand. | Average-demand days overstate winter or peak-demand coverage. |
| Japan/Korea LNG | Policy-reported LNG stock, tank capacity, or statutory reserve rule. | Public live inventory visibility is limited. |
| China gas | Peak-shaving capacity equivalent. | Capacity is not the same as usable current stock. |
| India fertilizer | Seasonal stock divided by average seasonal sales proxy. | Fertilizer demand is seasonal and product-specific. |
| Qualitative rows | No defensible public day count. | Do not invent precision from exposure alone. |

## China SPR Read

The China result deserves special treatment because it is the easiest place to overclaim.

Public evidence supports:

- commercial or operational crude stock draws;
- large aggregate crude inventories and prior stockbuilding;
- refinery-run cuts and product-export controls;
- import timing changes;
- bonded Iranian barrels and floating storage as alternative interpretations.

Public evidence does not support:

- a large confirmed government-SPR release volume;
- a clean separation of government SPR, commercial tanks, bonded storage, and floating barrels;
- a precise public day-count for China's official SPR response.

The best blog wording is: "China appears to be using commercial and operational stock flexibility, not a publicly confirmed large SPR release."

## Oil Versus Gas Versus Fertilizer

Oil is the easiest product to make comparable across countries because strategic reserves and IEA release allocations are public enough for bridge math. The catch is that these rows measure how long a reserve can support a modeled residual draw, not how long a country can replace all Hormuz imports.

Gas/LNG is harder. Europe has a transparent underground storage system and daily reporting. Japan and Korea mostly store gas as LNG in above-ground tanks and policy systems. China has capacity disclosures but not a unified public daily inventory dashboard. India has clear rationing and affected-supply data, but no public national gas storage ledger comparable to GIE.

Fertilizer and chemicals are harder still. India is good enough for seasonal fertilizer proxy rows. Global sulfur, ammonia, petrochemical, LPG, and naphtha feedstock inventories are not public enough for rigorous days-of-cover calculations.

## What We Know Versus What We Are Modeling

| Claim Type | Status |
|---|---|
| U.S./IEA/OECD/Japan/Korea reserve response | Strong for announced allocations, official stock frameworks, and public reserve-policy notes; medium for actual net draw timing. |
| China large government-SPR release | Low confidence; unsupported as a public claim. |
| China commercial/operational stock draw | Supported by market reporting, but ownership and exact state/commercial split remain opaque. |
| Europe gas storage days | Strong for public daily stock and average-demand denominator. |
| Japan/Korea LNG days | Medium. Policy/capacity anchors are public; live tank inventory is less transparent. |
| India gas/LPG storage duration | Not defensible from public sources; use policy rationing and replacement evidence instead. |
| Fertilizer/chemical global buffers | Mostly qualitative. India seasonal fertilizer proxies are usable; global stock ledgers are not. |

## Blog Wording

Use:

- "Reserves buy time for residual gaps; they do not erase the shock."
- "Japan is the cleanest public reserve-bridge example."
- "China's government SPR draw is not proven; the better-supported story is commercial/operational stock flexibility."
- "Gas and fertilizer day counts are not directly comparable to oil reserve days."

Avoid:

- "The world has X days of Hormuz cover."
- "China released a ton of SPR."
- Treating capacity as current usable stock.
- Charting oil, gas, and fertilizer days on one axis without a caveat about denominators.

## Files

- Epic: `issues/done/hormuz-s49-rq4-assess-strategic-stockpiles-and-reserve-releases.md`
- Source inventory: `issues/done/hormuz-s49.1-inventory-reserve-and-stockpile-data-sources.md`
- OECD/U.S. reserve response: `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv`
- China SPR evidence matrix: `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv`
- LNG/gas buffer table: `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv`
- Fertilizer/chemical buffer table: `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv`
- Consolidated buffer table: `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`

## Key Sources

- IEA collective oil stock release announcement: https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict
- IEA member-country release contributions: https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
- EIA U.S. petroleum stocks and SPR context: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1 and https://www.eia.gov/todayinenergy/detail.php?id=67625
- EIA China crude inventory analysis: https://www.eia.gov/todayinenergy/detail.php?id=67504
- IEA Oil Market Reports: https://www.iea.org/reports/oil-market-report-april-2026 and https://www.iea.org/reports/oil-market-report-june-2026
- METI Japan reserve and LNG statements: https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html and https://www.meti.go.jp/english/press/2026/0515_003.html
- GIE gas storage transparency: https://www.gie.eu/ and https://www.gie.eu/agsi-and-alsi-transparency-platforms/
- Eurostat natural gas and emergency oil stock statistics: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Natural_gas_supply_statistics and https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Emergency_oil_stocks_statistics
- IEA Japan and Korea natural gas security policy: https://www.iea.org/articles/japan-natural-gas-security-policy and https://www.iea.org/articles/korea-natural-gas-security-policy
- KOGAS LNG terminal/storage pages: https://www.kogas.or.kr/site/eng/1040303000000
- India PIB / PPAC energy and SPR sources: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2238525&lang=1&reg=3 and https://ppac.gov.in/faqs
- FAO and World Bank fertilizer disruption context: https://www.fao.org/newsroom/detail/fao-chief-economist-warns-of-severe-global-food-security-risks-from-disruption-to-strait-of-hormuz-trade-corridor/en and https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten-
