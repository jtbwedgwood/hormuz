---
id: "hormuz-f6r.4"
title: "Assess Europe and Mediterranean exposure"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-f6r"
labels:
  - "europe"
  - "importers"
  - "imports"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-f6r.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:46Z"
updated_at: "2026-07-06T11:05:00Z"
---

# Assess Europe and Mediterranean exposure

## Description

Determine whether Europe is materially exposed through crude/products/LNG/fertilizer flows or through global price spillovers rather than direct Hormuz dependence.

## Acceptance Criteria

Exposure is categorized as direct physical, indirect price, or minimal, with supporting trade data.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Former blocker resolved for this issue: `hormuz-f6r.1` - Build importer exposure matrix. The full global importer matrix can still improve country-level precision, but Europe/Mediterranean classification no longer depends on it.
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction

## Work Notes

- 2026-07-06: Claimed for Europe/Mediterranean exposure analysis. `hormuz-f6r.1` remains the formal matrix dependency, but regional direct/indirect exposure classification can proceed in parallel.
- 2026-07-06: Completed regional exposure classification and created `data/derived/hormuz_f6r_4_europe_exposure_matrix.csv`. Access date for all source URLs in this note and CSV: 2026-07-06.

### Bottom Line

Europe is materially exposed to a Hormuz shock, but mostly through prices and global competition for flexible molecules/barrels rather than a simple "Europe loses its Gulf cargoes" story.

- Crude: direct physical exposure is real but moderate at the EU aggregate level. The Council/Eurostat 2025 oil explainer says the EU imported about 435 Mt of crude, Saudi Arabia supplied 6.8%, Iraq 5.8%, and GCC countries about 7% by quantity. Because EIA/IEA show most Hormuz oil/LNG flows go to Asia, the EU-wide headline should be "some direct sour-crude exposure, larger benchmark/product-price exposure."
- Products: refined products, especially jet/diesel, are a medium exposure channel. IEA says Gulf producers exported 3.3 mb/d of refined products and 1.5 mb/d LPG in 2025, while nearly 3 mb/d of regional refining capacity has been shut. The European Commission separately identified jet fuel as the main near-term EU product constraint and urged coordinated measures, maintenance deferral, free product flows, and fuel saving.
- LNG/gas: this is Europe's strongest direct physical channel, but still not Asia-scale. Eurostat says Qatar supplied 8.9% of EU LNG imports by value in 2025; the Commission Q2 2025 gas report gives Qatar 8% of EU LNG in that quarter; ACER says winter 2025/26 Qatar LNG was 7% of EU LNG and 4% of total EU gas imports. ACER's 2026 LNG report says EU LNG imports reached 146 bcm in 2025 and LNG accounted for 47% of EU gas supply, making Europe very exposed to global LNG price competition even when direct Qatari shares are modest.
- Storage: GIE/S49 notes put EU underground gas storage at 565.62 TWh and 50.03% full on 2026-07-05, about 56.7 days of average 2025 demand. This buffers physical scarcity, but it does not buffer the cost of refilling storage in a tighter LNG market. ACER says reaching 80% storage is feasible at current LNG import rates, but reaching 90% would be difficult without additional supply.
- Fertilizer/sulfur: Europe is mostly an indirect price taker. FAO says Hormuz normally carries up to 30% of internationally traded fertilizers and nearly half of global sulfur trade; World Bank says urea prices rose above $850/mt in April 2026, up 80% since February, with the fertilizer index driven higher by Hormuz-linked export disruption. S49.5 found no global strategic fertilizer reserve, so this is a cost and substitution channel rather than a reliable stockpile story.
- Petrochemicals/metals: classify as indirect price with selective direct supply-chain exposure. IEA says petrochemicals have seen the steepest losses because feedstock availability is constrained, and reports 1.5 mb/d Gulf LPG exports plus about 5 Mt/year of Gulf aluminium shipped through Hormuz. Public Europe-specific petrochemical inventory and cargo data remain too thin for a hard direct-volume claim.
- Mediterranean nuance: the EU aggregate hides higher physical exposure for Mediterranean/eastern-Med refineries and Türkiye-like markets that use more Iraqi/Saudi/Gulf grades or products. This pass did not complete a harmonized EMRA/national customs/UN Comtrade country matrix, so the table labels Türkiye/eastern Mediterranean as "direct physical likely, not quantified here" rather than publishing a false precision estimate.

### Table Deliverable

| Output | Path | Status |
|---|---|---|
| Europe/Mediterranean exposure matrix | `data/derived/hormuz_f6r_4_europe_exposure_matrix.csv` | complete |

### Classification Summary

| Region/channel | Classification | Confidence | Evidence anchor |
|---|---|---|---|
| EU crude | Direct physical + indirect price | Medium | Saudi 6.8%, Iraq 5.8%, GCC about 7% of EU crude imports by quantity in 2025; most Hormuz flows still Asia-bound. |
| EU refined products / jet / diesel | Indirect price, localized physical risk | Medium | IEA Gulf product/LPG export and refinery-shutdown figures; Commission jet-fuel warning. |
| EU LNG/gas | Direct physical + indirect price | Medium-high | Qatar 7-9% of EU LNG depending on period/source; LNG 47% of EU gas supply in ACER 2025 report; storage refill cost exposure. |
| UK / northwest non-EU Europe | Indirect price | Medium | Benchmark gas/oil/product exposure; country import matrix not collected here. |
| Türkiye / eastern Mediterranean | Direct physical likely, not quantified | Medium-low | Geography and likely crude slate imply higher physical exposure; needs national customs/EMRA reconciliation before publication. |
| EU fertilizer / sulfur | Mostly indirect price | Medium | FAO/World Bank global fertilizer, sulfur, urea shock evidence; EU product import-origin matrix not completed. |
| EU petrochemicals / aluminium / LPG | Mostly indirect price with selective direct exposure | Medium | IEA LPG, petrochemical, and aluminium Hormuz disruption notes; public inventory/cargo data weak. |
| EU electricity/households | Indirect price | Medium | ACER TTF/storage/LNG competition evidence; country power pass-through not quantified here. |

### Caveats

- Do not sum the rows. Crude, refined products, LPG, petrochemicals, fertilizer, sulfur, and aluminium overlap through feedstock and downstream chains.
- Trade-origin shares are not the same as route certainty. Iraq, Saudi Arabia, and Qatar exposure must be separated by field/terminal and bypass route before making refinery-specific claims.
- Europe is less directly exposed than Asia to missing Hormuz cargoes, but Europe is now a very large LNG spot buyer and therefore remains exposed to the global clearing price.
- Gas storage is a volume buffer, not a price shield. A well-filled storage system can still be expensive to refill.
- Fertilizer and petrochemical inventory data are not good enough for Europe-wide days-of-cover claims without proprietary datasets or more granular national releases.

### Source Breadcrumbs

- Eurostat, "EU imports of energy products decreased again in 2025": https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260325-3
- Council of the EU, "Where does the EU get its oil from?": https://www.consilium.europa.eu/en/infographics/where-does-the-eu-get-its-oil-from/
- European Commission, Q2 2025 gas and electricity market report news: https://energy.ec.europa.eu/news/quarterly-reports-highlight-progress-gas-and-electricity-markets-q2-2025-2026-01-15_en
- European Commission, oil security coordination amid Middle East disruption: https://energy.ec.europa.eu/news/commission-calls-eu-countries-coordinate-measures-ensure-oil-security-supply-amid-middle-east-energy-2026-03-31_en
- European Commission, jet fuel/product supply monitoring: https://energy.ec.europa.eu/news/eu-continues-monitor-oil-market-situation-and-prepares-coordinated-response-address-jet-fuel-supply-2026-05-18_en
- ACER, key developments in European gas wholesale markets winter 2025/26: https://www.acer.europa.eu/key-developments-european-gas-wholesale-markets-winter-2025-2026
- ACER, 2026 LNG monitoring report: https://www.acer.europa.eu/sites/default/files/documents/Publications/ACER-LNG-Monitoring-Report-2026.pdf
- GIE AGSI/ALSI / homepage storage snapshot: https://www.gie.eu/
- EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint": https://www.eia.gov/todayinenergy/detail.php?id=65504
- IEA, "The Middle East and Global Energy Markets": https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- FAO, Hormuz disruption and fertilizer/food security warning: https://www.fao.org/newsroom/detail/fao-chief-economist-warns-of-severe-global-food-security-risks-from-disruption-to-strait-of-hormuz-trade-corridor/en
- World Bank, "Fertilizer prices surge as Strait of Hormuz disruptions tighten supplies": https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten-
- Project source tables used: `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`, `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`, `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv`, `data/derived/hormuz_s49_4_lng_gas_buffer_table.csv`, `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv`.

### Completion Note

- 2026-07-06: Acceptance criteria substantially met. Exposure is categorized by channel as direct physical, indirect price, or limited/minimal, with trade/storage anchors and caveats. Removed stale `hormuz-f6r.1` blocker from this issue because the regional classification no longer depends on the full importer matrix. Downstream `hormuz-f6r.5` still lists this task as a blocker, but that file is outside the requested write scope.
