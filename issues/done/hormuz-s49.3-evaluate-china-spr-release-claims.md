---
id: "hormuz-s49.3"
title: "Evaluate China SPR release claims"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-s49"
labels:
  - "china"
  - "energy-security"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:52Z"
updated_at: "2026-07-06T18:23:16Z"
---

# Evaluate China SPR release claims

## Description

Investigate claims that China is releasing large SPR volumes using customs data, satellite tank estimates, refinery runs, crude imports, commercial inventories, and market reporting.

## Acceptance Criteria

Conclusion assigns confidence to China SPR release magnitude and explains alternative interpretations.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Cleared blocker: `hormuz-f6r.2` - Analyze China exposure and substitution behavior. Upstream is now done and supports the same core reading: China adjustment is observable through import timing, refinery-run cuts, product-export controls, and opaque commercial/operational inventory behavior, but public data do not isolate a large government SPR draw.
- Unblocked: `hormuz-s49.1` - Inventory reserve and stockpile data sources
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Started preliminary research despite formal dependencies on `hormuz-f6r.2` and `hormuz-s49.1`. This pass is separating direct evidence, indirect proxies, and alternative explanations for reported China SPR releases.
- 2026-07-06 evidence pass:
  - High-level read: I did not find direct official confirmation that China is making a large draw on its government SPR. The strongest evidence points to very large overall crude inventories, plus some drawdown of commercial / operational stockpiles and lower refinery runs during the Iran/Hormuz shock.
  - Direct evidence:
    - EIA estimates China added an average of 1.1 million barrels/day to strategic oil inventories in 2025, reaching nearly 1.4 billion barrels by Dec. 2025; EIA also says preliminary government data indicate China continued building inventories in 2026 before the Iran conflict. Source: https://www.eia.gov/todayinenergy/detail.php?id=67504
    - IEA says Chinese crude stocks built by 111 million barrels in 2025 and were 30% above 2019 levels; its Aug. 2025 OMR said Chinese crude stocks rose by 900 kb/d in 2Q25. Sources: https://www.iea.org/commentaries/as-oil-market-surplus-keeps-rising-something-s-got-to-give and https://www.iea.org/reports/oil-market-report-august-2025
    - Columbia CGEP / Erica Downs says China’s crude imports hit a record 11.6 mb/d in 2025 and that stock building likely continued into 2026. It attributes 83% of the 2025 import increase to stockpiling. Source: https://www.energypolicy.columbia.edu/where-china-gets-its-oil-crude-imports-in-2025-reveal-stockpiling-and-changing-fortunes-of-certain-suppliers-including-those-sanctioned/
  - Official proxies:
    - NBS December 2024: crude imports were 553.42 million tons in 2024, down 1.9% y/y, while crude processing was 708.43 million tons, down 1.6% y/y. Source: https://www.stats.gov.cn/english/PressRelease/202501/t20250124_1958444.html
    - NBS June 2025: crude processing was 62.24 million tons, up 8.5% y/y, and Jan-Jun processing was 361.61 million tons, up 1.6% y/y. Source: https://www.stats.gov.cn/english/PressRelease/202508/t20250815_1960812.html
    - Reuters (via TradingView) on June 2025 customs data: imports were 49.89 million tons (12.14 mb/d), up 7.1% m/m and 7.4% y/y, with higher refinery operations and more imports from Saudi Arabia and Iran. Source: https://www.tradingview.com/news/reuters.com%2C2025%3Anewsml_L4N3T80KV%3A0-china-s-june-crude-imports-climb-after-imports-rise-from-saudi-arabia-iran/
    - JODI is useful as a monthly cross-check, but its latest public update on 25 June 2026 only reaches April 2026 data. Source: https://www.jodidata.org/oil/
  - Market / commercial-stock evidence:
    - Bloomberg via Energy Connects reported on 10 June 2026 that China had started tapping commercial crude reserves to offset the Iran-war shock, with draws expected to average about 1 mb/d and almost 25 million barrels already drawn by 7 June, citing Vortexa, Kpler, Energy Aspects, and Kayrros. Source: https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
    - The same Bloomberg piece says China’s strategic reserves are opaque and that exact SPR utilization remains unclear; it also says Beijing had continued adding to its SPR during the war. Same URL as above.
    - The Straits Times’ Bloomberg reprint explicitly says the commercial volumes are separate from the strategic petroleum reserve, which remains untouched. Source: https://www.straitstimes.com/asia/china-allows-state-oil-firms-to-tap-reserves-as-middle-east-war-drags
    - Kayrros reported a more than 60 million barrel draw in Chinese above-ground crude inventories between 9 Jan and 8 Feb 2025. Strong stock-movement evidence, but not proof of SPR draw versus commercial draw. Source: https://www.kayrros.com/blog/anatomy-of-a-fall/
  - Alternative explanations to keep separate:
    - Lower imports and lower refinery runs can create the appearance of a reserve draw without any formal SPR release. Bloomberg/Energy Connects says China was prioritizing lower refinery use and fuel export limits, while IEA/EIA frame China’s stock builds as barrels removed from the global market. Sources: Energy Connects Bloomberg piece, EIA, IEA.
    - Sanctions and relabeling matter: Columbia CGEP says China imported at least 2.6 mb/d of sanctioned crudes in 2025 and that part of the import mix shift reflects relabeling, especially via Malaysia/Indonesia. Source: Columbia CGEP link above.
    - Floating storage matters: IEA’s Apr. 2026 OMR says floating storage of crude and oil products in the Middle East rose by 100 million barrels when Hormuz flows were choked off. Some apparent stress can be absorbed offshore before onshore inventories move. Source: https://www.iea.org/reports/oil-market-report-april-2026
    - Bonded storage matters: EIA notes Iran reportedly holds crude oil in bonded storage in China, but current levels are unknown. That means “China stocks” can mix commercial, strategic, and third-party barrels. Source: EIA link above.
  - Working conclusion for the issue: treat any claim that China is “releasing large SPR volumes” as low confidence unless it distinguishes government-held SPR from commercial / operational inventories and shows a balance-sheet bridge from customs + runs + exports to an actual reserve draw.

- 2026-07-06 evidence matrix pass, access date 2026-07-06:
  - Government SPR: still not directly observed. EIA estimates China added an average of 1.1 mb/d to strategic oil inventories in 2025, reaching nearly 1.4 billion barrels by Dec. 2025, and says preliminary government data indicate China continued building inventories in 2026. The same EIA article estimates commercial crude inventories in China at about 1.0 billion barrels as of Dec. 2025. This cuts against a broad claim that Beijing was forced into a large government SPR draw.
  - Commercial / operational stock draw: strongest near-term explanation. Bloomberg via Energy Connects says refiners relied on commercial inventories rather than fresh imports, with draws expected to average about 1 mb/d and roughly 25 million barrels already drawn by 7 June 2026; it also says the exact amount taken from state stockpiles remains unclear. Kayrros earlier reported a >60 million barrel draw in Chinese above-ground crude inventories in Feb. 2025, but that is still not proof of government SPR use.
  - Apparent stock balance: the baseline before the shock was already heavy. IEA says Chinese crude stocks built by 111 million barrels in 2025 and were about 30% above 2019 levels; EIA says global and Chinese inventories were still building in 2026. That makes short-run absorption plausible without invoking a large SPR release.
  - Floating / bonded storage: important alternative explanation. IEA says oil on water swelled by 248 million barrels in 2025, with 72% of that sanctioned oil, which means some apparent market tightness can remain offshore. EIA also notes Iran reportedly holds crude oil in bonded storage in China, with unknown levels, so not all observable crude tied to China is Chinese-owned or SPR-owned.
  - Import cuts: China has used imports as a flex variable. NBS shows 2024 crude imports fell 1.9% y/y while crude processing fell 1.6% y/y; Reuters/TradingView reported that June 2025 crude imports rebounded after refiners increased operations and Saudi/Iran inflows rose, but Reuters/TradingView also reported that May 2026 seaborne crude imports slumped to the lowest level in almost 10 years as the Iran war pushed economics and flows around. Net: import behavior is consistent with adjustment, not proof of SPR release.
  - Refinery-run changes: official Chinese stats show crude processing rose 8.5% y/y in June 2025 and 8.9% y/y in July 2025, while Reuters reported higher operations tied to stronger June imports. This is a cleaner explanation for short-term balance changes than assuming SPR draw.
  - Fuel-export controls: important because they can preserve domestic supply without touching the government SPR. Reuters/TradingView reported May 2026 refined-oil exports fell 23.6% y/y, curbed by fuel export controls, while June 2025 refined-product exports were 5.34 million tons, down only 0.6% y/y but the highest monthly total since June 2024. That is consistent with policy-managed internal allocation, not necessarily reserve release.
  - Provisional conclusion: the claim “China is releasing a ton of its SPR” is not well supported. Best current read is that China had large pre-existing inventories and is adjusting the system through commercial/operational draws, import timing, refinery run changes, and product-export controls. A limited strategic draw is possible, but the public evidence does not justify a large-confidence SPR claim.
  - Exact upstream evidence still needed from `hormuz-f6r.2`: country-level substitution and destination mapping for the barrels China did not import, including whether lost Saudi/Iran/Russia barrels were replaced by other suppliers, whether Malaysia reflected transshipment rather than true origin change, and whether any observed draw was from government SPR versus commercial tanks. The missing bridge is customs-by-origin plus tanker/AIS destination data plus refinery throughput and product-export quotas in one reconciled balance sheet.
  - 2026-07-06 cleanup status: moved to `blocked` because the evidence pass is useful but cannot meet the acceptance criteria without `hormuz-f6r.2`.
  - Source breadcrumbs used in this pass:
    - https://www.eia.gov/todayinenergy/detail.php?id=67504
    - https://www.iea.org/commentaries/as-oil-market-surplus-keeps-rising-something-s-got-to-give
    - https://www.iea.org/reports/oil-market-report-august-2025
    - https://www.iea.org/reports/oil-market-report-february-2026
    - https://www.iea.org/reports/oil-market-report-april-2026
    - https://www.energypolicy.columbia.edu/where-china-gets-its-oil-crude-imports-in-2025-reveal-stockpiling-and-changing-fortunes-of-certain-suppliers-including-those-sanctioned/
    - https://www.stats.gov.cn/english/PressRelease/202501/t20250124_1958444.html
    - https://www.stats.gov.cn/english/PressRelease/202508/t20250815_1960812.html
    - https://www.stats.gov.cn/english/PressRelease/202508/t20250821_1960857.html
    - https://www.tradingview.com/news/reuters.com%2C2025%3Anewsml_L4N3TF0S2%3A0-china-s-crude-oil-imports-from-russia-tick-down-in-june-malaysia-imports-surge/
    - https://www.tradingview.com/news/reuters.com%2C2025%3Anewsml_L4N3TF0H9%3A0-china-s-refined-oil-exports-dip-0-6-in-june-but-hit-12-month-high/
    - https://www.tradingview.com/news/reuters.com%2C2026%3Anewsml_L4N42Q0IY%3A0-china-s-may-refined-oil-exports-drop-on-export-curbs-lng-imports-rebound/
    - https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
    - https://www.kayrros.com/blog/anatomy-of-a-fall/
    - https://www.jodidata.org/oil/

- 2026-07-06 final synthesis after `hormuz-f6r.2` cleared, access date 2026-07-06:
  - Acceptance criterion resolved: public evidence does not support a high-confidence claim that China is releasing a large government SPR volume. Best estimate for confirmed government SPR release magnitude is 0 barrels publicly confirmed; confidence in a large government-SPR release is low (about 20/100). Confidence that some limited government-SPR or underground-to-commercial transfer could be occurring is low-to-medium (about 35/100) because Kpler/Bloomberg explicitly cannot rule it out, but public sources do not provide an ownership bridge or magnitude.
  - Most defensible magnitude claim: secondary market reporting supports commercial/operational crude-stock draws near 1 mb/d during the spring/summer 2026 shock, with Energy Aspects/Kayrros estimating about 25 million barrels drawn in the month to 2026-06-07. Confidence in this commercial/operational draw channel is high (about 85/100). This should not be described as a government SPR release.
  - Government SPR versus commercial stocks: EIA's public estimate intentionally treats China's government-held and commercial inventories together as "strategic oil inventories" because China directed NOCs to hold emergency oil in commercial stockpiles. EIA separately estimates about 360 million barrels government-held and about 1.0 billion barrels commercial crude inventories as of Dec. 2025. Therefore "China has 1.4 billion barrels of strategic inventories" is not equivalent to "China has 1.4 billion barrels in a government SPR."
  - Official/agency evidence against a large SPR claim: EIA says China added about 1.1 mb/d to strategic oil inventories in 2025 and preliminary data indicated continued inventory builds before the Iran conflict. IEA's April 2026 OMR says China added 40 million barrels of crude to tanks in March 2026 even as global stocks were falling. IEA's June 2026 OMR says crude imports into China and Japan fell sharply and refinery crude runs in China and other regions were down materially in 2Q26, supporting run cuts/import timing as adjustment channels.
  - Upstream `hormuz-f6r.2` interpretation: China had large Hormuz-linked crude exposure but also large buffers. CGEP/Erica Downs estimates 45-50% of China's crude imports transit Hormuz and notes 1.39 billion barrels of oil in China storage as of 2026-03-02, plus Iranian barrels in floating and bonded storage. That upstream evidence supports "buffer plus substitution/demand adjustment," not a clean SPR draw.
  - Alternative explanations to keep separate in the blog:
    - Commercial/operational inventories: supported by Bloomberg/Energy Connects, Straits Times/Bloomberg, Vortexa, Kpler, Energy Aspects, Kayrros; not official Chinese inventory data.
    - Bonded and floating storage: Iranian barrels in bonded storage at Dalian/Zhoushan and floating storage in Asia may be usable by Chinese refiners without being Chinese government SPR.
    - Import timing and origin relabeling: GAC data miss sanctioned Iranian barrels; Malaysia/Indonesia/Iraq/Oman/UAE labels may include relabeled oil, so customs-origin shifts are not clean substitution evidence.
    - Refinery runs: NBS reports crude processing down 5.8% y/y in April 2026 and down 9.1% y/y in May 2026; IEA reports large China/Asia run cuts. This directly reduces crude needs.
    - Product-export controls: Reuters/Bloomberg/CGEP reporting says China restricted refined-product exports to preserve domestic supply; this rebalances internal product markets without proving SPR use.
  - Blog-safe wording: "China appears to have cushioned the Hormuz shock mainly by drawing commercial/operational stocks, cutting refinery runs, timing imports, using bonded/floating sanctioned barrels, and restricting refined-product exports. A limited opaque SPR contribution is possible, but public evidence does not support the stronger claim that Beijing has released a large government SPR volume."
  - Remaining caveats: China does not publish a clean SPR series; satellite/tanker estimates observe tanks and flows, not legal ownership; EIA's "strategic" definition for China deliberately differs from the U.S. SPR definition; secondary reports may use "reserves" loosely; and exact stock movements after June 2026 remain subject to revisions in tanker/satellite datasets.
  - Source breadcrumbs added/verified in final pass:
    - EIA Today in Energy, 2026-05-12: https://www.eia.gov/todayinenergy/detail.php?id=67504
    - EIA Global Energy Security Data methodology: https://www.eia.gov/outlooks/steo/report/energysecurity/article.php
    - IEA Oil Market Report April 2026: https://www.iea.org/reports/oil-market-report-april-2026
    - IEA Oil Market Report June 2026: https://www.iea.org/reports/oil-market-report-june-2026
    - IEA Middle East and Global Energy Markets topic page: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
    - JODI oil highlights, April 2026 China crude imports: https://www.jodidata.org/
    - NBS Energy Production in April 2026: https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html
    - NBS Energy Production in May 2026: https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html
    - CGEP/Erica Downs on China energy security and Hormuz exposure: https://www.energypolicy.columbia.edu/implications-of-the-conflict-in-the-middle-east-for-chinas-energy-security/
    - CGEP/Erica Downs on 2025 China crude imports and stockpiling: https://www.energypolicy.columbia.edu/where-china-gets-its-oil-crude-imports-in-2025-reveal-stockpiling-and-changing-fortunes-of-certain-suppliers-including-those-sanctioned/
    - CGEP/Palacios and Downs on China refining/petrochemical adjustment: https://www.energypolicy.columbia.edu/disruptions-in-the-middle-east-reinforce-chinas-aim-for-greater-self-sufficiency-in-refining-and-petrochemicals/
    - Bloomberg via Energy Connects on commercial stockpiles, 2026-06-10: https://www.energyconnects.com/news/oil/2026/june/china-taps-commercial-oil-stockpiles-to-help-weather-gulf-shock/
    - Bloomberg via Straits Times on commercial reserves versus SPR: https://www.straitstimes.com/asia/china-allows-state-oil-firms-to-tap-reserves-as-middle-east-war-drags
