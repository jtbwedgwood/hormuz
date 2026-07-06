---
id: "hormuz-s49.4"
title: "Assess LNG and gas storage buffering"
type: "task"
status: "blocked"
priority: "P2"
parent: "hormuz-s49"
labels:
  - "energy-security"
  - "gas-storage"
  - "lng"
  - "spr"
  - "stockpiles"
blocked_by:
  - "hormuz-f6r.3"
blocks:
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:54Z"
updated_at: "2026-07-06T08:40:00Z"
---

# Assess LNG and gas storage buffering

## Description

Estimate how LNG importers and gas storage levels cushion reduced Gulf LNG supply, including Japan/Korea/China/Europe seasonal context.

## Acceptance Criteria

Storage coverage and drawdown capacity are translated into days/months of demand where possible.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Blocked by: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Unblocked: `hormuz-s49.1` - Inventory reserve and stockpile data sources
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Started preliminary research despite formal dependencies on `hormuz-f6r.3` and `hormuz-s49.1`. Gathered public storage/days-of-cover hooks and caveats for exposed LNG/gas importers.
- Buffer definition to use later: `days of demand ~= working gas volume / average daily consumption`; for LNG systems, use usable terminal/tank inventory, not nameplate regasification throughput. Withdrawal/send-out capacity is a rate limit, not stock. For underground gas storage, use working gas volume, not total geological capacity.
- Europe: GIE’s AGSI/ALSI platforms are the best public daily source. GIE says AGSI/ALSI provide daily inventory reporting for underground gas storages and large-scale LNG terminals, cover 100% of EU27 underground storage and 100% of EU27 large-scale LNG terminals, and publish operational data in open format. Current GIE homepage snapshot on 2026-07-05 06:00 CEST shows EU storage at 565.62 TWh and 50.03% full. GIE also says storage levels are reported daily and that data can lag or be corrected, with the platform doing a first daily publish around 19:30 and a second processing run at 23:00; weekend data can arrive late and retroactive updates are possible. Sources: https://www.gie.eu/agsi-and-alsi-transparency-platforms/ ; https://www.gie.eu/transparency/databases/storage-database/ ; https://www.gie.eu/ ; https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_II_018.pdf (accessed 2026-07-06).
- Europe seasonal context: GIE says underground storage matters for winter flexibility and has cited storage covering up to 60% of daily peak demand in EU Member States in a winter-security context. A 2022 GIE release said 95% filling at the start of winter could cover about 28% of EU annual gas consumption. Use this as narrative context, but not as a proxy for current 2026 stock. Source: https://www.gie.eu/press/gas-infrastructure-a-pillar-of-resilience-for-winter-energy-security/ ; https://www.gie.eu/press/eus-underground-gas-storage-is-ready-for-winter/ (accessed 2026-07-06).
- Japan: IEA says Japan has no underground gas storage, has 37 operational LNG receiving terminals, and total LNG storage capacity of over 18 mcm, equivalent to around 12 bcm of gas storage and around 36 days of domestic natural gas. METI separately said on 2026-03-03 that Japan has LNG stock to cover national consumption for approximately three weeks and can share LNG between utilities; METI also says the LNG survey was discontinued in April 2022, so public stock visibility is weak. Useful interpretation: Japan’s buffer is commercial LNG tank inventory, not seasonal underground storage. Sources: https://www.iea.org/articles/japan-natural-gas-security-policy ; https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html ; https://www.meti.go.jp/english/statistics/tyo/sekiyuso/index.html (accessed 2026-07-06).
- Korea: IEA says Korea has no underground gas storage and stores gas exclusively as LNG in above-ground tanks; the five LNG terminals operated by KOGAS have 74 LNG storage tanks and 6.56 bcm of storage capacity. The same IEA page says Korea’s Urban Gas Business Act obligates KOGAS to hold two reserve layers: mandatory inventory volumes equal to 7 days and preventive reserve volumes equal to 30 days of average daily domestic sales over the last 24 months, i.e. 37 days in total on that basis. KOGAS also describes LNG tanks explicitly as a buffer that stores LNG in low-demand seasons and supplies winter demand. Sources: https://www.iea.org/articles/korea-natural-gas-security-policy ; https://www.kogas.or.kr/site/eng/1040303000000 ; https://www.kogas.or.kr/site/eng/1030903020000 (accessed 2026-07-06).
- China: public coverage is better on demand and CNPC storage than on a unified daily inventory dashboard. Official Chinese reporting says 2024 natural-gas consumption reached up to 425 bcm. CNPC’s 2024 annual report says 23 gas storage facilities were operational by end-2024, with 18.43 bcm total gas injection in 2024 and 22.6 bcm cumulative peak-shaving capacity. That 22.6 bcm is about 5.3% of 425 bcm, or roughly 19 days of average 2024 national consumption if treated as a pure volume upper bound; practical usable coverage will be lower because peak-shaving capacity is not the same as instantly drawable stock. Sources: https://english.www.gov.cn/news/202407/23/content_WS669fa738c6d0868f4e8e963c.html ; https://www.cnpc.com.cn/en/GSF/common_index.shtml ; https://www.cnpc.com.cn/en/2024enbyfgrme/202508/9ecba8819b384e93af04806bb1bf1c4d/files/034812bc78584f07ac303e5a147046cd.pdf (accessed 2026-07-06).
- India: public data are strong on consumption and infrastructure, weak on storage. PPAC publishes current natural-gas consumption tables monthly in MMSCM and MoPNG highlights the national pipeline buildout, but I did not find a public national storage inventory comparable to AGSI/ALSI or Korea’s KOGAS pages. IEA says India’s LNG imports will need to more than double to about 65 bcm/year by 2030, which is useful context for why storage-buffer math matters, but the country-level buffer estimate will likely need to be a modeled proxy rather than a direct published stock series. Sources: https://ppac.gov.in/natural-gas/consumption ; https://mopng.gov.in/en/pdc/investible-projects/oil-amp-gas-infrastructure/natural-gas-pipelines ; https://www.iea.org/news/indias-natural-gas-demand-set-for-60-rise-by-2030-supported-by-upcoming-global-lng-supply-wave (accessed 2026-07-06).
- Public vs paid: the IEA country pages and GIE transparency pages are usable public sources. IEA’s Natural Gas Information data product is subscription/licensed and contains the detailed annual balances, stock levels, and trade-by-origin data that would make the eventual country-day calculations cleaner; use the public pages for narrative and the paid dataset only if we need a rigorous denominator table. Source: https://www.iea.org/data-and-statistics/data-product/natural-gas-information (accessed 2026-07-06).
- Open question for the next pass: whether to normalize buffer to average annual demand, winter peak demand, or firm sales. Japan and Korea reserve rules are defined against different demand bases, so the final writeup will need one common denominator plus a note on local reserve definitions.
- 2026-07-06 update: the task is not fully complete because `hormuz-f6r.3` still blocks the Asia adjustment pass and India still lacks a public national gas-storage stock series. I pushed the public-source table as far as possible below.
- 2026-07-06 cleanup status: moved to `blocked` because the public-source table is partial and final Asia adjustment depends on `hormuz-f6r.3`.

### Table-ready buffer estimate

| Region | Buffer metric | Stock / capacity basis | Demand denominator | Days of average demand | Reporting cadence / lag | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Europe (underground storage) | EU27 underground gas storage working gas | Observed stock | EU natural gas inland demand of 13,093,256 TJ in 2025 (= 3,637.0 TWh/yr) | 56.7 days (`565.62 TWh / 9.97 TWh/day`) | Daily inventory reporting; GIE says first publish around 19:30 and a second processing run around 23:00, with possible weekend lag and retroactive corrections | High | This is the cleanest public buffer series. Use working gas volume, not geological capacity. Source URLs: https://www.gie.eu/agsi-and-alsi-transparency-platforms/ ; https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Natural_gas_supply_statistics ; https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_II_018.pdf (accessed 2026-07-06). |
| Japan | LNG tank inventory / total LNG storage capacity | Policy-reported stock and capacity ceiling | National LNG consumption | ~21 days current policy statement; ~36 days capacity ceiling | Public LNG survey was discontinued in April 2022, so there is no regular public stock series | Medium | METI said on 2026-03-03 that Japan has LNG stock to cover national consumption for approximately three weeks. IEA’s country note still gives 37 operational receiving terminals with >18 mcm (~12 bcm) storage capacity, roughly 36 days of domestic natural gas. This is LNG tank inventory, not underground storage. Sources: https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html ; https://www.iea.org/articles/japan-natural-gas-security-policy ; https://www.meti.go.jp/english/statistics/tyo/sekiyuso/index.html (accessed 2026-07-06). |
| Korea | LNG tank inventory / statutory reserve | Observed reserve rule + LNG tank capacity | Average daily domestic sales over the last 24 months | 37 days statutory reserve (7 mandatory + 30 preventive) | No public daily stock series in the cited sources; policy analysis is the public hook | High on rule, medium on contemporaneous fill | Korea has no underground gas storage and stores gas as LNG in above-ground tanks. IEA says KOGAS terminals have 74 tanks and 6.56 bcm of storage capacity. The legal stockholding rule is defined directly as 7 days plus 30 days of average daily domestic sales. Sources: https://www.iea.org/articles/korea-natural-gas-security-policy ; https://www.kogas.or.kr/site/eng/1040303000000 (accessed 2026-07-06). |
| China | Gas storage facilities / peak-shaving capacity | Capacity proxy, not a clean observed stock series | 2024 national gas consumption up to 425 bcm | ~19.4 days upper-bound equivalent (`22.6 bcm / 425 bcm * 365`) | Annual corporate disclosure; no unified daily public inventory dashboard found | Low-medium | CNPC said 23 storage facilities were operational by end-2024, with 18.43 bcm total gas injection in 2024 and 22.6 bcm cumulative peak-shaving capacity. That 22.6 bcm is best read as an upper bound, not instantly drawable stock, so real coverage is lower than 19 days. Sources: https://english.www.gov.cn/news/202407/23/content_WS669fa738c6d0868f4e8e963c.html ; https://www.cnpc.com.cn/en/2024enbyfgrme/202508/9ecba8819b384e93af04806bb1bf1c4d/files/034812bc78584f07ac303e5a147046cd.pdf (accessed 2026-07-06). |
| India | LNG regasification capacity, not national storage stock | Capacity proxy only | PPAC monthly national gas consumption in MMSCM; public national storage inventory not found | Not defensible from public sources without modeled terminal-tank assumptions | PPAC is monthly on consumption; public storage inventory series is absent | Low | India’s public data are strong on consumption and pipeline buildout, but I did not find a national gas-storage inventory comparable to GIE or KOGAS. PNGRB says India has around 170 MMSCMD of LNG regasification capacity, which is a flow constraint, not a stock buffer. Any days-of-cover estimate for India has to be modeled from terminal-level tank inventories, operating practices, and contract flexibility. Sources: https://ppac.gov.in/natural-gas/consumption ; https://pngrb.gov.in/pdf/CaseStudies/20251224_CSComm_CGD.pdf ; https://mopng.gov.in/en/pdc/investible-projects/oil-amp-gas-infrastructure/natural-gas-pipelines (accessed 2026-07-06). |

### Source breadcrumbs

- GIE AGSI/ALSI daily inventory and coverage notes: https://www.gie.eu/agsi-and-alsi-transparency-platforms/ ; https://www.gie.eu/transparency/databases/storage-database/ ; https://www.gie.eu/transparency-platform/GIE_API_documentation_v007.pdf
- Europe demand denominator: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Natural_gas_supply_statistics
- Japan LNG stock and policy: https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html ; https://www.iea.org/articles/japan-natural-gas-security-policy ; https://www.meti.go.jp/english/statistics/tyo/sekiyuso/index.html
- Korea LNG storage and reserve rule: https://www.iea.org/articles/korea-natural-gas-security-policy ; https://www.kogas.or.kr/site/eng/1040303000000 ; https://www.kogas.or.kr/site/eng/1030903020000
- China storage and consumption: https://english.www.gov.cn/news/202407/23/content_WS669fa738c6d0868f4e8e963c.html ; https://www.cnpc.com.cn/en/2024enbyfgrme/202508/9ecba8819b384e93af04806bb1bf1c4d/files/034812bc78584f07ac303e5a147046cd.pdf
- India consumption and regasification capacity: https://ppac.gov.in/natural-gas/consumption ; https://pngrb.gov.in/pdf/CaseStudies/20251224_CSComm_CGD.pdf ; https://mopng.gov.in/en/pdc/investible-projects/oil-amp-gas-infrastructure/natural-gas-pipelines
