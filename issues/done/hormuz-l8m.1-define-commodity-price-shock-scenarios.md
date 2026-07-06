---
id: "hormuz-l8m.1"
title: "Define commodity price shock scenarios"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "prices"
  - "scenarios"
  - "us-business"
blocked_by:
  - "hormuz-fyp.1"
  - "hormuz-fyp.2"
  - "hormuz-fyp.3"
  - "hormuz-fyp.6"
  - "hormuz-kmz.6"
blocks:
  - "hormuz-4j7.3"
  - "hormuz-l8m.2"
  - "hormuz-l8m.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:58Z"
updated_at: "2026-07-06T17:20:00Z"
---

# Define commodity price shock scenarios

## Description

Build low/base/high price scenarios for oil, refined products, natural gas/LNG, electricity, fertilizer, freight, and insurance using observed market moves and historical analogues.

## Acceptance Criteria

Scenario inputs include dates, prices, deltas from baseline, sources, and rationale for persistence assumptions.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.2` - Build canonical disruption chronology
- Blocked by: `hormuz-fyp.3` - Define baseline periods and scenario taxonomy
- Blocked by: `hormuz-fyp.6` - Inventory market price series and units
- Blocked by: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Blocks: `hormuz-4j7.3` - Collect historical supply, price, inventory, and demand data
- Blocks: `hormuz-l8m.2` - Estimate added cost to US businesses by sector
- Blocks: `hormuz-l8m.3` - Estimate US power-price implications for data centers

## Work Notes

- 2026-07-06T16:00Z: Claimed for scenario construction. Use `docs/foundation-chronology-and-scenarios.md` as the governing event/scenario taxonomy and `docs/foundation-data-inventory.md` for preferred price series. `hormuz-kmz.6` is still in progress, so any supply-removal inputs here remain provisional.
- 2026-07-06T16:25Z: First-pass price-scenario frame for downstream RQ5 tasks. Treat this as provisional until `hormuz-kmz.6` reconciles disrupted volumes and until the next EIA STEO release, scheduled 2026-07-07, is checked.
- 2026-07-06T17:20Z: Final handoff after `hormuz-kmz.6` and `hormuz-kmz.7` completion. The scenario inputs now carry dates, price levels, deltas from the pre-shock baseline, source links, and persistence assumptions in one place. Handoff vector for `hormuz-l8m.2` and `hormuz-l8m.3`: low = Brent $75-$85/b with gasoline +$0.40-$0.70/gal, diesel +$0.70-$1.00/gal, jet +$0.75-$1.10/gal, Henry Hub roughly flat to +$0.25/MMBtu, fertilizer +10%-20%, and AWRP 0.3%-0.8% hull; base = EIA June path with Brent about $105/b near term easing to $89/b by 4Q26, gasoline +$1.00/gal, diesel +$1.34/gal, jet +$1.42/gal, Henry Hub near the EIA path, fertilizer +25%-35%, and AWRP 0.8%-1.5%; high = Brent $120-$150/b, gasoline +$1.25-$1.75/gal, diesel +$1.75-$2.50/gal, jet +$1.75-$2.75/gal, Henry Hub +$0.75-$1.50/MMBtu regional sensitivity, fertilizer +50%-60%, and AWRP 2%-5%+. Persistence assumptions remain aligned to the scenario taxonomy: low eases into 4Q26, base stays elevated through 2026 and into early 2027, and high persists through 4Q26 under renewed disruption risk.

### Scenario Anchors

Use `2026-01-01` to `2026-02-27` spot/futures averages as the near-term pre-shock counterfactual where daily data are available. Where the source only provides monthly/forecast comparisons, use EIA February 2026 STEO as the pre-conflict counterfactual and state that explicitly.

| Scenario | Operational state | Persistence assumption | Price-shock use in RQ5 |
|---|---|---|---|
| L8M-low: fragile reopening keeps improving | Traffic/flows recover through 3Q26; attacks and mine risk fade enough for insurers to reprice lower, but not to normal immediately. | Elevated prices through summer, easing into 4Q26. | Use for "AI cost barely moves" lower bound: oil/products remain above February but below the April/May shock; Henry Hub remains near current EIA path. |
| L8M-base: EIA June STEO central case | Strait remains effectively closed/limited near term, shipments resume in 3Q26, and pre-conflict traffic does not return until early 2027. | Brent elevated in June/July, easing in 4Q26 and 2027 as production restarts and inventories rebuild. | Main scenario for sector-cost table because it is public, official, internally consistent, and already embeds demand destruction/inventory draw assumptions. |
| L8M-high: reopening stalls or reverses | Renewed attacks, route-control dispute, or insurance refusal pushes traffic back toward partial/de facto closure. | High prices persist into 4Q26; freight and war-risk premia remain binding; demand destruction grows. | Stress case for tail-risk bars/bands. Keep labeled speculative unless confirmed by post-July market data or upstream supply work. |

### Quantitative Inputs To Carry Forward

| Commodity/channel | Pre-shock or baseline | Current/central observed or forecast | Scenario-ready low/base/high input | Source and confidence |
|---|---:|---:|---:|---|
| Brent crude | EIA says Brent averaged $71/b in February 2026; project baseline should compute Jan-Feb daily average from EIA/FRED. | EIA June STEO: Brent averaged $117/b in April, $107/b in May, forecast about $105/b in June and July, $89/b by 4Q26, $95/b 2026 annual, $79/b 2027. | Low: $75-$85/b through 2H26. Base: EIA June path, roughly $105/b near term and $89/b 4Q26. High: $120-$150/b while traffic/insurance fails. | EIA STEO global oil markets, released 2026-06-09, accessed 2026-07-06: https://www.eia.gov/outlooks/steo/report/global_oil.php. Confidence high for EIA forecast assumption, medium for realized path. |
| Global liquid fuels balance | February STEO expected demand growth; June STEO says inventories now meet demand because Middle East production was shut in. | EIA estimates 11.3 mb/d May Middle East crude shut-ins, 6.3 mb/d average global inventory draw in 2Q26, and OECD inventories falling toward lows not seen since 2003. | Feed high scenario from duration of inventory draw, not just spot Brent. Use `inventory_draw_mbpd * duration_days` as a persistence metric. | Same EIA STEO global oil page. Confidence high for EIA stated assumptions; upstream reconciliation still blocked by `hormuz-kmz.6`. |
| U.S. gasoline wholesale | EIA February STEO is counterfactual. | EIA June STEO forecasts 2026 wholesale gasoline at $2.98/gal, almost $1.00/gal above February STEO; retail gasoline $3.90/gal in 2026. | Low: +$0.40-$0.70/gal wholesale vs February. Base: +$1.00/gal. High: +$1.25-$1.75/gal if cracks stay wide. | EIA STEO petroleum products, released 2026-06-09, accessed 2026-07-06: https://www.eia.gov/outlooks/steo/report/petro_prod.php. Confidence high. |
| U.S. diesel wholesale | EIA February STEO counterfactual. | EIA forecasts 2026 diesel wholesale $3.40/gal, +$1.34/gal vs February; retail diesel $4.87/gal. Diesel margins rise because Europe/Asia seek replacements for volumes previously supplied through Hormuz. | Low: +$0.70-$1.00/gal. Base: +$1.34/gal. High: +$1.75-$2.50/gal, especially for logistics/manufacturing stress. | EIA STEO petroleum products. Confidence high for central forecast. |
| U.S. jet fuel wholesale | EIA February STEO counterfactual. | EIA forecasts 2026 jet fuel wholesale $3.37/gal, +$1.42/gal vs February. | Low: +$0.75-$1.10/gal. Base: +$1.42/gal. High: +$1.75-$2.75/gal. | EIA STEO petroleum products. Confidence high. |
| Henry Hub gas | 2025 annual $3.53/MMBtu; EIA January/February pre-conflict forecasts should be retrieved for exact counterfactual. | May 2026 averaged $2.94/MMBtu; EIA expects about $3.34/MMBtu in 2H26 and $3.60/MMBtu for 2026 because associated gas supply limits upward pressure despite LNG/export demand. | Low/base: use EIA path, with small U.S. gas shock. High: +$0.75-$1.50/MMBtu regional sensitivity if LNG pull, weather, or pipeline constraints bind. | EIA STEO natural gas, released 2026-06-09, accessed 2026-07-06: https://www.eia.gov/outlooks/steo/report/natgas.php. Confidence high for Henry Hub central path; medium for regional basis. |
| U.S. electricity | Use EIA regional retail/wholesale power data plus ISO hub data; baseline from Jan-Feb 2026 or 2025 seasonal average. | EIA June STEO says gas keeps about 40% U.S. generation share in 2026/2027; summer generation +3% vs 2025, mainly weather-driven and met by solar/wind growth. | Pass through via heat-rate rule: `power_delta_$/MWh = gas_delta_$/MMBtu * marginal_heat_rate_MMBtu_per_MWh * gas_on_margin_share`. Send to `hormuz-l8m.3`. | EIA STEO overview/natural gas/electricity tables. Confidence medium until ISO-region work is done. |
| Fertilizer | World Bank Pink Sheet/CMO pre-shock monthly data; compute Dec 2025 and Jan-Feb 2026 baselines by product. | World Bank 2026 materials: fertilizer prices surged in 1Q26 due to Hormuz disruption, with later monthly easing; June 2026 commodity update says fertilizer index fell 21.8% in June after earlier spike. | Low: +10%-20% vs Jan-Feb. Base: +25%-35% 2026 average for fertilizer index. High: urea-heavy +50%-60% if Gulf nitrogen exports remain constrained. | World Bank Commodity Markets/Pink Sheet, accessed 2026-07-06: https://www.worldbank.org/en/research/commodity-markets; April 2026 CMO. Confidence high for monthly public series, medium for product-specific persistence. |
| Aluminium/metals | World Bank/LME baseline from 2025 or Jan-Feb 2026. | World Bank April 2026 CMO/blog notes metals and minerals up in 1Q26, with aluminium especially exposed to Middle East supply concerns. | Low: 0%-10%; base: +15%-25% for aluminium-sensitive manufacturing; high: +30%+ if Gulf smelter/export disruption persists. | World Bank Commodity Markets Outlook/Pink Sheet. Confidence medium for Hormuz attribution; use as secondary channel. |
| Freight/war-risk insurance | Pre-crisis additional war-risk premium roughly 0.1%-0.15% of hull value in cited market reports; exact benchmark should be validated with broker data if available. | S&P Global reported some successful Hormuz tanker transits around 0.8% AWRP after no-claims bonus on 2026-03-30; Lloyd's List reported high-risk quotes up to 10% of hull value on 2026-03-11, with safer voyages much lower. | Low: 0.3%-0.8% hull per voyage. Base: 0.8%-1.5%. High: 2%-5%+; reserve 10% for extreme individual vessels, not average scenario. | S&P Global shipping note, 2026-03-30, accessed 2026-07-06: https://www.spglobal.com/energy/en/news-research/latest-news/shipping/033026-war-risk-insurance-cost-off-highs-but-still-elevated-in-persian-gulf; Lloyd's List, 2026-03-11: https://www.lloydslist.com/LL1156586/Gulf-war-risk-premiums-topping-double-digit-millions-of-dollars-per-trip. Confidence medium because commercial quote definitions vary. |

### Modeling Rules For Downstream Tasks

- Keep observed market data, EIA forecast assumptions, and speculative tail scenarios in separate columns. Do not average them together.
- For U.S. business costs, express shocks as both absolute input deltas (`$/gal`, `$/MMBtu`, `$/MWh`, `$/mt`) and percentage deltas versus the counterfactual; sector models can then multiply by physical energy use or input-output shares.
- For AI/data centers, the oil shock mostly matters through diesel backup fuel, construction/materials, and macro inflation; the direct operating channel is electricity, and EIA's current central case implies only a modest U.S. Henry Hub shock.
- For freight/insurance, convert ship-level premia to landed cost only after vessel/cargo assumptions are explicit: `insurance_cost_per_bbl = hull_value * AWRP / cargo_barrels`; for a $100 million VLCC with 2 million barrels, 1% AWRP is about $0.50/bbl before other freight/delay costs.
- Current live-market caveat: news on 2026-07-06 reports Brent/WTI nearer the low-$70s as reopening/OPEC+ news improved sentiment, but EIA's June STEO remains the central documented scenario until the 2026-07-07 STEO is checked. Use live prices only as sensitivity/current-state annotation.

## Completion Note

- 2026-07-06: Acceptance criteria met. Scenario inputs include dates, prices, baseline deltas, sources, and persistence assumptions, with the final handoff tied to the reconciled market-balance work from `hormuz-kmz.6` and the product disruption master table in `hormuz-kmz.7`.
