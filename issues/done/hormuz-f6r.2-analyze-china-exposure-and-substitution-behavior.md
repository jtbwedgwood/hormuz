---
id: "hormuz-f6r.2"
title: "Analyze China exposure and substitution behavior"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "china"
  - "importers"
  - "imports"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-f6r.5"
  - "hormuz-s49.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:43Z"
updated_at: "2026-07-06T19:20:00Z"
---

# Analyze China exposure and substitution behavior

## Description

Estimate China's exposure to Hormuz crude, LNG, LPG, petrochemicals, and fertilizers, then examine substitution via Russia, domestic inventories, demand reduction, refinery runs, or SPR/commercial draws.

## Acceptance Criteria

China section separates observed data from inference and flags opaque inventory assumptions.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Cleared/stale blocker: `hormuz-f6r.1` - Build importer exposure matrix. The full matrix can refine volumes later, but public China behavior analysis no longer depends on it.
- Cleared dependency: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Blocks: `hormuz-s49.3` - Evaluate China SPR release claims

## Work Notes

- 2026-07-06: Claimed for preliminary China exposure/substitution analysis. `hormuz-f6r.1` remains the formal matrix dependency, but country research can proceed using completed KMZ tables and will be reconciled after the matrix lands.
- 2026-07-06: Completed best public-source pass and wrote `data/derived/hormuz_f6r_2_china_adjustment_matrix.csv`. Acceptance criteria are substantially met for a China section because the output separates observed data from inference and explicitly flags opaque inventory assumptions. Removed stale blocker on `hormuz-f6r.1`; the full importer matrix can later refine volumes, but the China behavioral assessment is usable now.

### Synthesis for Blog Draft

- Core China crude exposure is large but not a simple "shortage" story. CGEP/Erica Downs summarizes GAC 2025 data as 42% of China's crude imports from Saudi Arabia, Iraq, UAE, Oman, Kuwait, and Qatar, plus Kpler's 1.38 mb/d estimate for Iranian crude that mostly does not appear as Iran in GAC data. CGEP's useful public shorthand is that 45-50% of China's crude imports transit Hormuz. Access date: 2026-07-06. Source: https://www.energypolicy.columbia.edu/implications-of-the-conflict-in-the-middle-east-for-chinas-energy-security/
- Official and agency data show adjustment through lower imports/runs and inventory behavior, not a proven large government-SPR release. JODI's April 2026 highlight reports China crude imports at 9.39 mb/d, down 2.4 mb/d. NBS reports crude processing down 5.8% y/y in April 2026 and down 9.1% y/y in May 2026. IEA's April 2026 OMR says China added 40 mb of crude to tanks in March even as global observed stocks fell and Asian importing-country stocks dropped. Access date: 2026-07-06. Sources: https://www.jodidata.org/ ; https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html ; https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html ; https://www.iea.org/reports/oil-market-report-april-2026
- The SPR claim remains ambiguous. The `hormuz-s49.3` notes and `data/derived/hormuz_s49_3_china_spr_evidence_matrix.csv` point away from a confident claim that China is "releasing a ton of SPR." Best read: China is using a mix of commercial/operational stocks, import timing, bonded/floating Iranian barrels, lower refinery runs, and product-export controls. Government SPR use is possible, but public data do not isolate ownership or release volumes. Access date: 2026-07-06. Sources: `issues/blocked/hormuz-s49.3-evaluate-china-spr-release-claims.md`; https://www.eia.gov/todayinenergy/detail.php?id=67504 ; https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
- LNG exposure is cleaner than substitution. CGEP summarizes China as importing 31% of its LNG from the Middle East in 2025, with Qatar at 28%. The practical adjustment is mostly demand reduction, fuel switching, and reluctance to pay high spot prices; Russia/Central Asia pipeline supply is constrained in the near term. This is observed exposure plus inferred behavior, not a measured LNG replacement-volume estimate. Access date: 2026-07-06. Source: https://www.energypolicy.columbia.edu/implications-of-the-conflict-in-the-middle-east-for-chinas-energy-security/
- LPG/petrochemicals are a plausible high-impact channel but weak on China-specific public flow data. IEA/KMZ tables support the global claim that about 30% of seaborne LPG exports move via Hormuz, and IEA says early demand cuts are concentrated in naphtha, LPG, and jet fuel. For China, the defensible conclusion is likely petrochemical/feedstock run cuts and demand destruction, not a quantified replacement-supplier story yet. Access date: 2026-07-06. Sources: https://www.iea.org/reports/oil-market-report-april-2026 ; `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`
- Fertilizer and chemical exposure should be treated as indirect for China unless `f6r.1` finds destination volumes. KMZ/s49.5 establish strong global Hormuz exposure for sulfur, urea, ammonia, and MAP/DAP, but current public notes do not support a China-specific substitution estimate. Use as a price/input-cost and industrial-feedstock channel, not as a hard China volume claim. Access date: 2026-07-06. Sources: `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv`; https://www.iea.org/topics/the-middle-east-and-global-energy-markets

### Observed vs Inferred Channels

- Observed: China had large 2025 crude/LNG exposure to Hormuz-linked Middle East suppliers; China crude imports fell sharply in JODI April 2026; NBS April/May 2026 crude processing fell; IEA reported China adding crude to tanks in March 2026.
- Observed via secondary market reporting: commercial/operational crude stock draws and refined-product export curbs. Label these as Reuters/Bloomberg/market-analytics evidence, not official Chinese inventory data.
- Inferred: exact replacement barrels from Russia, bypassed Saudi/UAE crude, relabeled Iranian barrels, and floating/bonded storage allocation.
- Inferred and low confidence: China-specific LPG/petrochemical/fertilizer substitution volumes.
- Opaque: government SPR versus commercial/operational storage. Public sources do not provide a clean ownership bridge.

### Source Breadcrumbs

- CGEP China energy security Q&A, accessed 2026-07-06: https://www.energypolicy.columbia.edu/implications-of-the-conflict-in-the-middle-east-for-chinas-energy-security/
- IEA Oil Market Report April 2026, accessed 2026-07-06: https://www.iea.org/reports/oil-market-report-april-2026
- JODI homepage/highlights, accessed 2026-07-06: https://www.jodidata.org/
- NBS Energy Production in April 2026, accessed 2026-07-06: https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html
- NBS Energy Production in May 2026, accessed 2026-07-06: https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html
- EIA China Country Analysis Brief PDF, accessed 2026-07-06: https://www.eia.gov/international/content/analysis/countries_long/China/pdf/China-2025.pdf
- EIA Today in Energy on China crude inventories, accessed 2026-07-06: https://www.eia.gov/todayinenergy/detail.php?id=67504
- Bloomberg via Energy Connects on China commercial crude stockpiles, accessed 2026-07-06: https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
