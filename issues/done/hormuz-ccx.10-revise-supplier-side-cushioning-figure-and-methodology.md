---
id: "hormuz-ccx.10"
title: "Revise supplier-side cushioning figure and methodology"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-ccx"
labels:
  - "figures"
  - "supply"
  - "research"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "codex"
created_at: "2026-07-14T00:00:00Z"
updated_at: "2026-07-14T23:00:00Z"
---

# Revise supplier-side cushioning figure and methodology

## Description

Rebuild the supplier-side cushioning figure around pooled oil and LNG supplier totals from the two baseline Sankeys, and document the recoverability estimates, confidence, storage-versus-shut-in logic, and bypass projects under development.

## Acceptance Criteria

- Figure has only oil and LNG sections and reconciles supplier baselines to the simplified Sankeys.
- Filled bars represent recoverable exports; shaded remainders represent unrecoverable exports.
- Figure is stripped of methodological caveats beyond a short public source line.
- Companion document explains every estimate, confidence, storage/delayed-export limits, production implications, and relevant projects under development.
- Figure remains reproducible from a machine-readable companion CSV.

## Work Notes

- 2026-07-14: Claimed for a second research and design pass. Delegated evidence audits for Saudi/UAE oil, other oil suppliers, and Qatar/UAE LNG; main agent owns accounting, synthesis, figure generation, and visual QA.
- 2026-07-14: Figure denominators will be the 2024 EIA/Vortexa origin totals already used by the Sankeys. Pooled oil totals are crude/condensate plus the Sankey's indicative refined-products/LPG allocation. "Recoverable" means a baseline export flow that can still reach the world market during a sustained effective Hormuz closure through an operational non-Hormuz route; storage without an export route delays a shut-in but does not count as recoverable flow.
- 2026-07-14: Non-Saudi/UAE oil audit recommendation: Iraq `~0.30 of 3.70 mb/d` recoverable (medium confidence); Kuwait `~0.00 of 2.18 mb/d` (high); Qatar `~0.00 of 1.45 mb/d` (high); Iran `~0.05 of 2.40 mb/d` (low); residual Other `~0.00 of 0.353 mb/d` (low/medium). Exact pooled denominators reconcile to the oil Sankey CSV.
- 2026-07-14: Iraq's estimate combines about 250 kb/d actually sent from northern fields to Ceyhan with roughly 50 kb/d of demonstrated fuel-oil trucking and re-export via Syria. The larger 500-650 kt/month Syrian fuel-oil arrangements and 50 kb/d planned crude trucking are upside, not yet demonstrated sustained throughput. These substitute at the national export level but do not physically reroute Basra crude; southern Iraq still lacks a working connection to the Mediterranean routes.
- 2026-07-14: Iran's Jask route should be valued from observed cargoes, not its 1 mb/d nameplate. One 2 million barrel cargo loaded in March and another loading was reported/observed in May, implying only about 40-50 kb/d averaged over the closure period. Jask is operational at cargo scale but not demonstrated as a sustained high-throughput bypass.
- 2026-07-14: Storage is a timing buffer, not recoverable route capacity. Current EIA/IEA evidence says Gulf tanks filled quickly and forced upstream/refinery cuts. Qatar's public condensate system was designed for about eight days of storage at a 500 kb/d peak rate; Iraq's last public southern-storage figure was about 10 million barrels, roughly three days of its 2024 Hormuz crude baseline. Kuwait and Iran have substantial tankage, but public gross capacity does not reveal empty working space.
- 2026-07-14: Development watch: Iraq began the 2.5 mb/d Basra-Haditha pipeline in May 2026, but completion depends on future budget allocations and downstream links to Syria/Turkiye/Jordan also need work. Iraq's national Kirkuk-Ceyhan rehabilitation was in final inspection with up to 600 kb/d discussed. Kuwait is discussing links/expansions with Saudi Arabia and the UAE but has published no route, capacity, commitment, or timeline. No committed non-Hormuz oil route was found for Qatar. Iran's Jask is an attempted reactivation of existing infrastructure, not a new project.
- 2026-07-14: Saudi/UAE oil audit. Saudi Arabia reconciles to `5.477690 + 1.300000 = 6.777690 mb/d`, or `~6.8 mb/d`, in the oil Sankey. Recommended recoverable amount is `~4.0 mb/d` (medium confidence), the midpoint of the IEA's `3-5 mb/d` estimate of spare East-West Pipeline capacity as of early 2026. Aramco subsequently demonstrated the physical upper end by ramping the line to `7.0 mb/d` in Q1 2026; its Q1 presentation says about `2 mb/d` of that system feeds west-coast refineries, leaving about `5 mb/d` of gross crude export capacity. The estimate counts incremental capacity against the former Hormuz flow, not all barrels already using the Red Sea route. It credits no separate Abqaiq-Yanbu NGL bypass because the IEA says that `0.3 mb/d` line is fully utilised. The numerator is therefore best read as reroutable crude within a pooled crude/products denominator; public evidence does not support a separate incremental recovery credit for the Sankey's `1.3 mb/d` indicative Saudi products/LPG allocation.
- 2026-07-14: UAE oil reconciles to `1.890093 + 1.500000 = 3.390093 mb/d`, or `~3.4 mb/d`. Recommended recoverable amount is `~0.7 mb/d` (medium-high confidence): IEA reports ADCOP/Fujairah current capacity near `1.8 mb/d` and normal domestic-crude exports on the route around `1.1 mb/d`, leaving up to `0.7 mb/d` incremental room in a closure. ADNOC's own 2026 offering document gives the original/design rating as about `1.5 mb/d`; the difference from the reported `1.8 mb/d` is an operational uprating, so the extra-room estimate should retain a tilde. ADCOP transports crude, not refined products/LPG, and the public record does not quantify an incremental non-Hormuz products route from Ruwais/Jebel Dhanna; no products recovery is added to the numerator.
- 2026-07-14: Storage is timing optionality, not sustainable flow capacity. Aramco reports using domestic and international storage during Q1 2026 but does not publish an auditable barrel total; its balance sheet shows inventories rising from `$18.811bn` at end-2025 to `$25.017bn` at 2026-03-31, which is value rather than physical barrels and cannot be converted cleanly because it covers crude, products, chemicals, and international operations. The UAE has the `42 million barrel` Mandous underground crude-storage complex near Fujairah, outside Hormuz, plus an `8 million barrel` Fujairah export-terminal figure in the Abu Dhabi government prospectus; avoid adding these because the facilities may overlap and represent capacity, not empty space. Mandous can ship pre-positioned crude during a closure and later refill, but cannot support a permanent flow above pipeline-connected production. IEA's July OMR confirms the mechanism: June Gulf exports rose `6.5 mb/d`, while production rose only `3.5 mb/d`, aided by drawdown of onshore and floating inventories that had filled during the closure. Crude/products physically stored during a short closure can be exported later; once accessible tanks and floating storage fill, ongoing output must be curtailed. This is consistent with IEA/EIA estimates of substantial Saudi and UAE crude production cuts during the closure.
- 2026-07-14: Development pipeline. The UAE's new West-East Pipeline is genuinely under construction and expected online in `2027`; the Abu Dhabi Media Office says it will double ADNOC's export capacity through Fujairah. Do not include it in current recoverability. Saudi Arabia has no comparably committed new bypass in the reviewed primary record. Reuters reported on 2026-07-07 that Saudi Arabia was in preliminary discussions about adding up to `2 mb/d` of East-West capacity, potentially including neighboring barrels, but there was no final investment decision, specification, or completion date; describe it as under consideration, not active capacity.
- 2026-07-14: LNG audit. Qatar and UAE are both `~0` sustained recoverability under a strict closure because neither has an operational non-Hormuz route to the world LNG market. Qatar's public 1.46 million m3 gross Ras Laffan tankage is about 31 Bcf gas-equivalent, or a 3.3-day gross ceiling at the figure baseline; usable headroom is smaller. No defensible UAE LNG tank total was found. North Field and Ruwais expansions remain Hormuz-exposed; Dolphin is regional pipeline gas; Golden Pass is a U.S.-gas corporate portfolio hedge, not recovery of Qatar production.
- 2026-07-14: Completed `figures/fig-ccx-supplier-side-cushioning.svg`, its reproducible evidence CSV and builder, plus `docs/hormuz-supplier-side-cushioning.md`. Accounting tests reconcile every baseline to the Sankey input rows, the nine recoverable/unrecoverable pairs sum exactly, the pooled oil denominator is 20.26 mb/d, and only Qatar/UAE appear in the LNG section. SVG passed `xmllint` and `git diff --check`; a 1440x820 Chrome render was visually inspected for clipping, overlap, label fit, and source/footer placement.
- 2026-07-14: LNG audit recommendation: Qatar `~0 of 9.3 Bcf/d` and UAE `~0 of 0.70 Bcf/d` recoverable during a sustained effective closure, both high confidence. These are 2024 EIA/Vortexa Hormuz-flow denominators, and the IEA states that there are no alternative routes to bring Qatari or UAE LNG volumes to market. The zeroes are route-capacity estimates, not claims that stored LNG disappears or that no ship can ever make a risky transit through a partial closure.
- 2026-07-14: Qatar's publicly documented common Ras Laffan LNG tankage is `1.46 million m3` gross (`8 x 140,000 m3 + 4 x 85,000 m3`). Using the EIA/DOE approximation that LNG occupies about 1/600 of its gaseous volume gives about `30.9 Bcf` gas-equivalent, or a gross ceiling of about `3.3 days` at the 2024 `9.3 Bcf/d` baseline. Confidence is medium because the tank disclosure is from 2015 and gross tankage overstates incremental usable space. No defensible public Das Island LNG tank-volume figure was found; the IEA instead provides strong qualitative evidence that UAE output was significantly curtailed as spare tank capacity dwindled, while ADNOC Gas describes some volumes as deferred through inventory management.
- 2026-07-14: LNG already in available tanks can be exported after Hormuz reopens; once tanks fill, liquefaction/feedgas must be curtailed or shut in, and unliquefied gas is not a deferred cargo. No active Qatar/UAE LNG bypass project was found. The existing Dolphin pipeline is separate, near-fully-contracted pipeline gas and cannot be credited to the LNG baseline; Ruwais LNG and Qatar's North Field expansions remain inside Hormuz. Golden Pass supplies US gas and is a QatarEnergy portfolio hedge, not recovery of Qatari national LNG. Separately, 2026 attacks damaged two Qatari trains representing `12.8 mtpa` or `17%` of capacity for an official estimated `3-5 years`; document this current physical-capacity loss without mixing it into the route-only figure estimate.

## Source Breadcrumbs

- EIA/Vortexa oil Sankey inputs: https://www.eia.gov/todayinenergy/detail.php?id=65504 and linked figure workbooks.
- EIA/Vortexa LNG Sankey inputs: https://www.eia.gov/todayinenergy/detail.php?id=65584 and linked figure workbook.
- IEA Hormuz factsheet: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- IEA Middle East market page: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- IEA current Gulf bypass/export evidence (June 2026): https://www.iea.org/commentaries/how-global-oil-supplies-have-readjusted-to-help-fill-the-huge-gap-left-by-the-strait-of-hormuz-shock
- IEA country supply series, February-June 2026: https://www.iea.org/data-and-statistics/charts/oil-producer-supply-by-gulf-countries-february-2026-june-2026
- EIA April 2026 storage/shut-in assessment: https://www.eia.gov/pressroom/releases/press586.php
- Iraq operational Ceyhan and Syrian fuel-oil routes: https://www.thenationalnews.com/business/energy/2026/04/02/iraq-begins-fuel-oil-exports-through-syria-amid-hormuz-disruption/ and https://www.hydrocarbonprocessing.com/news/2026/06/iraq-to-export-crude-naphtha-through-syria-after-hormuz-shock/
- Iraq Basra-Haditha project and budget-dependent schedule: https://www.thenationalnews.com/business/energy/2026/05/01/iraq-starts-work-on-basra-haditha-pipeline-for-crude-exports/
- Iran Jask observed restart evidence: https://apnews.com/article/24c4b439d2c6a5b571fea90e4d1227d8 and https://www.iranintl.com/en/202605293657
- Kuwait no-bypass outcome and preliminary pipeline discussions: https://www.thenationalnews.com/business/energy/2026/06/19/kuwait-to-ramp-up-oil-output-to-two-million-bpd-within-a-week-as-strait-of-hormuz-reopens/
- Qatar condensate storage design evidence: https://www.qatarenergylng.qa/Portals/0/DNNGalleryPro/uploads/2024/3/19/ThePioneer-September-October08.pdf
- IEA Strait factsheet, including `3-5 mb/d` Saudi spare capacity, `0.7 mb/d` UAE extra room, and fully used Saudi NGL line: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- Aramco Q1 2026 results, including achieved `7.0 mb/d` East-West throughput and storage use: https://www.aramco.com/en/news-media/news/2026/aramco-announces-first-quarter-2026-results
- Aramco Q1 2026 presentation, including `~2 mb/d` to west-coast refineries: https://www.aramco.com/-/media/publications/corporate-reports/reports-and-presentations/2026/q1/saudi-aramco-q1-2026-webcast-presentation-english.pdf
- Aramco Q1 2026 interim report, including inventory balance-sheet values: https://www.aramco.com/-/media/publications/corporate-reports/reports-and-presentations/2026/q1/saudi-aramco-q1-2026-interim-report-english.pdf
- Saudi Ministry of Energy confirmation that East-West pumping capacity returned to `7.0 mb/d` after April damage: https://www.spa.gov.sa/en/N2557744
- ADNOC 2026 offering document, including original/design ADCOP capacity near `1.5 mb/d`: https://adnoc.ae/-/media/adnoc-v2/sub-brands/adnoc-murban/files/2026/adnoc-sukuk-programme-2026-update---base-offering-memorandum.ashx
- Abu Dhabi government prospectus, including `8 million barrels` of Fujairah export-terminal storage: https://addof.gov.ae/Publications/abudhabigov/Emirate_of_Abu_Dhabi_Base_Prospectus.pdf
- IEA July 2026 OMR, including Gulf export/production rebound and inventory drawdown: https://www.iea.org/reports/oil-market-report-july-2026
- Abu Dhabi Media Office on the new West-East Pipeline, under construction and due in 2027: https://www.mediaoffice.abudhabi/en/crown-prince-news/khaled-bin-mohamed-bin-zayed-chairs-meeting-of-executive-committee-of-adnoc-board-of-directors-may-2026/
- Reuters relay on Saudi preliminary discussions to add up to `2 mb/d` of East-West capacity; no FID or timeline: https://www.sahmcapital.com/news/content/%D8%AD%D8%B5%D8%B1%D9%8A-%D9%85%D8%B5%D8%A7%D8%AF%D8%B1-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%AA%D8%AF%D8%B1%D8%B3-%D8%B2%D9%8A%D8%A7%D8%AF%D8%A9-%D8%B3%D8%B9%D8%A9-%D8%AE%D8%B7-%D8%A3%D9%86%D8%A7%D8%A8%D9%8A%D8%A8-%D8%A7%D9%84%D9%86%D9%81%D8%B7-%D8%A5%D9%84%D9%89-%D8%A7%D9%84%D8%A8%D8%AD%D8%B1-%D8%A7%D9%84%D8%A3%D8%AD%D9%85%D8%B1-2026-07-07
- QatarEnergy LNG common Ras Laffan tank capacities and boil-off recovery: https://www.qatarenergylng.qa/english/Media/News/Article/ArticleID/232/QATARGAS%20LOADS%205000TH%20LNG%20CARGO%20FROM%20COMMON%20LNG%20STORAGE%20AND%20LOADING%20ASSET%20IN%20RAS%20LAFFAN
- EIA LNG volume conversion (`~600:1` gas to liquid): https://www.eia.gov/kids/energy-sources/natural-gas/
- ADNOC Gas Q1 2026 statement on tank/inventory management and deferred volumes: https://www.adnocgas.ae/en/news-and-media/press-releases/2026/q1-2026-results
- Qatar News Agency report of QatarEnergy's `12.8 mtpa`, `17%`, `3-5 year` damaged-capacity estimate: https://qna.org.qa/en/news/news-details?date=19%2F03%2F2026&id=minister-of-state-for-energy-affairs-iranian-attacks-disrupted-17-percent-of-gas-export-capacity
- Dolphin Energy operational and contracted volumes: https://www.dolphinenergy.com/en-US/Operations/ and https://www.dolphinenergy.com/en-US/Marketing-and-Distribution/
- ADNOC Ruwais LNG capacity and 2028 commercial-start timeline: https://www.adnoc.ae/en/news-and-media/press-releases/2026/adnoc-signs-15-year-sales-and-purchase-agreement-with-inpex-for-ruwais-lng-project/
- EIA Golden Pass ownership, capacity, and train-start timeline: https://www.eia.gov/todayinenergy/detail.php?id=67564
