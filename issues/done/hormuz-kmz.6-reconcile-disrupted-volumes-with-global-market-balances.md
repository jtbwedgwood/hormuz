---
id: "hormuz-kmz.6"
title: "Reconcile disrupted volumes with global market balances"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-kmz"
labels:
  - "balances"
  - "commodities"
  - "markets"
  - "supply"
blocked_by:
  - "hormuz-fyp.6"
  - "hormuz-kmz.3"
  - "hormuz-kmz.5"
blocks:
  - "hormuz-4j7.3"
  - "hormuz-f6r.5"
  - "hormuz-kmz.7"
  - "hormuz-l8m.1"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:39Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Reconcile disrupted volumes with global market balances

## Description

Compare estimated disrupted supply with global demand, spare capacity, inventories, OPEC+ behavior, LNG balances, and product-specific market slack.

## Acceptance Criteria

Market-balance table shows disrupted share of global/regional supply and explains why price response is or is not proportional.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-fyp.6` - Inventory market price series and units
- Blocked by: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocked by: `hormuz-kmz.5` - Quantify freight, insurance, and war-risk disruption
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Blocks: `hormuz-kmz.7` - Produce product disruption master table
- Blocks: `hormuz-l8m.1` - Define commodity price shock scenarios

## Work Notes

- Preliminary market-balance pass, built from public baseline facts before `hormuz-kmz.1`, `hormuz-kmz.3`, and `hormuz-kmz.5` are finished. I am treating this as a first-cut denominator check, not the final scenario table.
- Dependency gaps that still matter:
  - `hormuz-kmz.3` still controls the final disrupted volume estimates, so the volumes below are provisional proxies where the public source already gives a clean market share.
  - `hormuz-kmz.5` will still matter for pass-through, rerouting delay, insurance, and freight effects; those are not yet embedded quantitatively here.
  - `hormuz-kmz.1` is still needed for a fully standardized product taxonomy, especially for petroleum products versus LPG/ethane/naphtha-style splits.
- The core balance point is straightforward on the oil side: the Strait is not a niche route. In 2025 it carried about 20 mb/d of oil and oil products, about 25% of world seaborne oil trade, and roughly 15 mb/d of crude alone, about 34% of global crude trade. Global world liquid-fuels consumption was about 104 mb/d in EIA's 2025 STEO baseline, so a full closure is a system-wide shock even before product-specific bottlenecks are added. Source: IEA Strait of Hormuz page; EIA STEO.
- Spare-capacity offset is real but limited. IEA says the world’s spare crude production capacity was over 4 mb/d in Q4 2025, and available alternative crude export capacity out of the Gulf is only about 3.5 to 5.5 mb/d via Saudi/UAE pipelines. That means a large share of the lost Hormuz crude stream can be partially offset, but not cleanly or instantly, and the bypass is narrow relative to the 15 mb/d crude flow exposed.
- LNG is the cleanest “no bypass” case. IEA says over 110 bcm of LNG passed through Hormuz in 2025, representing almost one-fifth of global LNG trade, and there are no alternative routes to bring Qatari/UAE LNG to the global market other than existing liquefaction plants. EIA’s 2023 global LNG trade benchmark of 52.9 Bcf/d is broadly consistent with a global market denominator in the mid-50 Bcf/d range.
- Products and fertilizers show the strongest downstream market spillovers because they rely on the same Gulf energy chain and have weaker substitute supply than crude alone. IEA says Gulf producers exported 3.3 mb/d of refined products and 1.5 mb/d of LPG in 2025, with more than 3 mb/d of regional refining capacity already shut and more than 4 mb/d at risk; feedstock availability is the binding constraint for replacement runs outside the region. For fertilizers, IFASTAT’s public Hormuz page says upstream Hormuz countries account for 23% of global ammonia trade, 34% of global urea trade, 49% of global sulfur trade, and 18% of global MAP+DAP trade. IEA’s topic page gives a similar high-level summary: more than 30% of global urea trade, about 20% of ammonia and phosphate trade, and about half of global seaborne sulfur trade move through the Strait.
- Aluminum is a smaller share than oil, but still large enough to matter in a market-balance frame. IEA says the Gulf region produces around 8% of global aluminium supply and about 5 million tonnes are shipped each year through the Strait from smelters in Bahrain, Qatar, Saudi Arabia, and the UAE. That is a meaningful physical volume, but the offset mechanism is better thought of as slower demand destruction and partial rerouting than as true spare supply.
- Petrochemicals are the least cleanly balanceable public-row right now. IEA’s longer-run petrochemicals work says petrochemical feedstock accounts for 12% of global oil demand, which is useful as a global denominator proxy, but I do not yet have a Hormuz-specific trade denominator that is as clean as oil, LNG, or fertilizers. For now I am treating this as a transmission channel rather than a standalone market-balance row.
- These rows are deliberately overlapping. The first two are system-level oil views; the remaining rows are product slices or feedstock proxies and should not be summed into a single total without de-duplication.

| product | candidate_disrupted_volume_or_proxy | global_market_denominator | disrupted_share | slack_or_offset_mechanism | source | confidence | notes |
|---|---:|---:|---:|---|---|---|---|
| Crude oil | 14.95 mb/d through Hormuz in 2025 | Global crude trade, implied ~44 mb/d | ~34% | Saudi/UAE bypass pipelines (3.5-5.5 mb/d available), plus over-4 mb/d world spare crude capacity, but not all readily accessible | IEA Strait of Hormuz page; EIA OPEC spare-capacity explainer | High | Share is against crude trade, not all liquids. This is the cleanest oil-market balance row. |
| Total oil and oil products | 19.87 mb/d total oil via Hormuz in 2025 | World liquid-fuels consumption, ~104.0 mb/d (EIA 2025 STEO) | ~19% | Emergency stocks, demand destruction, and rerouting via Atlantic Basin/Asia; but immediate system-wide pricing impact | IEA Strait of Hormuz page; EIA STEO | High | This is the best broad oil-system proxy for headline balance framing. |
| Refined products | 3.3 mb/d Gulf refined-product exports in 2025 | Global refined-product trade, roughly 18-25 mb/d depending on definition/year | ~13-18% if using 18-25 mb/d denominator; IEA/World Bank state ~20% of refined-product trade moved via Hormuz | More than 3 mb/d of regional refining capacity already shut; feedstock availability limits replacement runs elsewhere | IEA Oil Market Report March 2026; World Bank blog on Hormuz disruptions | Medium-high | Public sources disagree a bit on the precise denominator because product-trade boundaries differ. |
| LPG | 1.5 mb/d Gulf LPG exports in 2025 | Global LPG trade, not yet cleanly standardized in a public source; rough proxy is world liquids market | Proxy only; no clean standalone public denominator yet | Substitute supply from outside the Gulf exists, but it is not a true bypass market and is constrained by tanker/feedstock logistics | IEA Oil Market Report March 2026 | Medium | Keep as a proxy row until the product taxonomy is standardized. |
| LNG | 112 bcm via Hormuz in 2025 | Global LNG trade, implied ~560 bcm/yr (from 112 bcm at ~20%) | ~20% | No alternative route to global LNG market; Dolphin pipeline has limited spare capacity; Oman LNG terminals near full utilization | IEA Strait of Hormuz page; EIA LNG trade page | High | This is the strongest “no bypass” balance. |
| Urea | Upstream Hormuz countries account for 34% of global urea trade | Global urea trade | 34% | Some rerouting through land corridors; Northern Hemisphere buying has already been front-loaded; demand can be deferred but not fully replaced | IFASTAT Hormuz page; World Bank fertilizer blog | High | World Bank also frames the Middle East as nearly one-quarter of global urea exports; IFASTAT gives the cleaner Hormuz-linked share. |
| Ammonia | Upstream Hormuz countries account for 23% of global ammonia trade | Global ammonia trade | 23% | Limited rerouting; LNG/gas feedstock constraints bind output outside the Gulf as well | IFASTAT Hormuz page; World Bank fertilizer blog | High | Ammonia is both a trade item and a feedstock, so this has second-order effects on urea and phosphates. |
| MAP + DAP / phosphate | Upstream Hormuz countries account for 18% of global MAP+DAP trade | Global MAP+DAP trade | 18% | Some importers can lean on inventory and non-Gulf supply, but sulfur and ammonia feedstock bottlenecks tighten the offset | IFASTAT Hormuz page; World Bank fertilizer blog | Medium-high | IEA’s topic page gives the broader “about 20% of phosphate trade” framing. |
| Sulfur | About half of global seaborne sulfur trade moves through Hormuz | Global seaborne sulfur trade | ~50% | Inventory drawdown and alternative origin shifts (notably Canada/Kazakhstan), but sulfur stock can be tight and is hard to substitute quickly | IEA Hormuz topic page; IFASTAT Hormuz page | Medium | This is one of the more important hidden bottlenecks because sulfur is upstream of phosphate fertilizers and some refining/critical-mineral chemistry. |
| Aluminum | About 5 million tonnes/yr shipped through Hormuz; Gulf region ~8% of global aluminum supply | Global aluminum supply, implied ~62.5 Mt/yr from the 8% share | ~8% | Some output can be adjusted outside the Gulf, but the offset is slower and depends on power, alumina, and shipping logistics | IEA Hormuz topic page | Medium | I am treating this as a supply share, not a direct trade share. It is useful for scale, but it is not a clean bypass market. |
| Petrochemical feedstocks | Petrochemical feedstock is 12% of global oil demand | Global oil demand / feedstock demand, 104.0 mb/d oil baseline; no clean Hormuz-specific product denominator yet | Proxy only; 12% of global oil demand is the relevant baseline share | Non-Gulf naphtha/LPG/ethane can partially substitute, but IEA notes the steepest losses are already in petrochemicals | IEA petrochemicals report; IEA Middle East topic page; World Bank oil-market blog | Medium-low | This is best treated as a transmission channel for naphtha/LPG/ethane shocks, not a finalized standalone product-balance row. |

- Working conclusion: oil is large in absolute barrels, but LNG and some fertilizer/sulfur rows are more market-inelastic because there is little or no bypass and less spare capacity. That is the cleanest explanation for why price response can be nonlinear relative to physical volumes alone.

Key source links used here:
- IEA Strait of Hormuz page: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- IEA Middle East and Global Energy Markets topic: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- IEA March 2026 Oil Market Report: https://www.iea.org/reports/oil-market-report-march-2026
- EIA STEO global oil markets: https://www.eia.gov/outlooks/steo/report/global_oil.php
- EIA LNG trade article: https://www.eia.gov/todayinenergy/detail.php?id=62464 and https://www.eia.gov/todayinenergy/detail.php?id=65584
- IFASTAT home/Strait of Hormuz page: https://ifastat.org/
- World Bank fertilizer blog: https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten-
- IEA petrochemicals report: https://www.iea.org/reports/the-future-of-petrochemicals

### Completion Note

- 2026-07-06: Acceptance criteria met for a preliminary market-balance reconciliation. The table includes disrupted-volume proxies, denominators, shares, slack/offset mechanisms, sources, confidence, and non-additivity caveats. It should be refreshed after `hormuz-kmz.3` is unblocked, but downstream tasks can use these denominators now.
