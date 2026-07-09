# Hormuz Global Energy Shock Accounting

Last updated: 2026-07-07.

## Bottom Line

The public evidence supports an accounting frame, not a closed world balance sheet. Oil has the largest gross barrel shock, but public replacement rows mix genuinely new supply, bypassed flows, redirected cargoes, reserve draws, and poorer buyers being priced out. LNG is cleaner physically because Qatar/UAE cargoes have no practical bypass; LPG is important but much less observable.

## Concise Balance Table

| Product | Gross Loss, Base | Replacement / Redirection | Inventory Draw | Demand Reduction | Residual / Read | Confidence |
|---|---:|---|---|---|---|---|
| oil and petroleum liquids | 15.06 mb/d flow-equivalent | 5.15 mb/d sum of quantified major-importer bridge rows; mostly diverted/reallocated cargoes, not proven new output | 6.3 mb/d global oil-stock draw check; 2.60 mb/d sum of quantified importer inventory bridge rows | 1.48 mb/d sum of quantified major-importer demand-response rows | 5.83 mb/d using importer inventory rows; 2.13 mb/d if substituting the global stock-draw check; Oil clears through a mix of route preservation, reserve/commercial stock draw, demand response, and cargo redirection. Public data do not isolate genuinely new non-Hormuz production from redirected cargoes. | medium |
| LNG | 0.30 bcm/d flow-equivalent | 0.05 bcm/d Asia aggregate replacement/spot supply proxy | 0.07 bcm/d Asia aggregate storage draw proxy | 0.15 bcm/d Asia aggregate fuel switching or curtailment proxy | 0.03 bcm/d; LNG is the cleanest hard-loss row: the modeled base loss is close to the whole Qatar/UAE flow, and clearing depends mainly on scarce flexible cargoes, storage, and demand curtailment. | medium_high |
| LPG / NGL feedstocks | 1.2 mb/d flow-equivalent | 0.18 mb/d India-visible replacement proxy | 0.06 mb/d India-visible inventory/operational draw proxy | 0.18 mb/d India-visible rationing or demand-management proxy | 0.78 mb/d not allocated by public global evidence; LPG/NGL clearing is under-observed. India gives a visible rationing and replacement case, but global displacement among household fuel, petrochemicals, and poorer importers remains mostly opaque. | medium_low |

## Blog-Ready Caveat

These rows should not be summed across countries or products. The importer adjustment rows are scenario bridges, not cargo-by-cargo world accounting: a barrel counted as Japan's replacement supply may be a cargo diverted from another buyer, and the global oil-stock draw overlaps with country inventory-draw assumptions.

## Double-Counting Risks

- oil and petroleum liquids: High. F6R importer rows are scenario allocations and overlap with the global stock-draw check; replacement supply may be another buyer's displaced consumption.
- LNG: Medium. The Asia aggregate row overlaps with China/Japan/Korea qualitative LNG rows; do not add those country rows to this aggregate.
- LPG / NGL feedstocks: High. LPG may be included in petroleum liquids/product aggregates and overlaps with petrochemical feedstock rows; India-visible adjustment is not a global total.

## Sources

- EIA, Strait of Hormuz oil chokepoint route data: https://www.eia.gov/todayinenergy/detail.php?id=65504
- EIA, Hormuz LNG route data: https://www.eia.gov/todayinenergy/detail.php?id=65584
- IEA, Strait of Hormuz factsheet: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- IEA, Middle East and global energy markets: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- Local inputs: `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`, `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, and `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`.

## Files

- Accounting table: `data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv`
- Builder script: `scripts/build_ccx_global_energy_accounting.py`
