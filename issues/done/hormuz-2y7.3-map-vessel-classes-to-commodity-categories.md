---
id: "hormuz-2y7.3"
title: "Map vessel classes to commodity categories"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-2y7"
labels:
  - "ais"
  - "classification"
  - "shipping"
  - "tracker"
  - "vessels"
blocked_by:
  - "hormuz-fyp.1"
  - "hormuz-fyp.5"
blocks:
  - "hormuz-2y7.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:24Z"
updated_at: "2026-07-06T15:00:00Z"
---

# Map vessel classes to commodity categories

## Description

Build vessel class and size mapping needed to connect ship counts to cargo exposure: VLCC/Suezmax/Aframax, LNG carriers, LPG, product tankers, bulkers, container ships, naval/support vessels.

## Acceptance Criteria

Mapping includes AIS vessel type caveats, DWT/capacity assumptions, cargo ambiguity, and links to commodity taxonomy.

## Dependency Notes

- Parent: `hormuz-2y7` - RQ1: Build reliable daily Hormuz ship tracker
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Blocks: `hormuz-2y7.4` - Prototype daily transit count pipeline

## Work Notes

- 2026-07-06: Claimed. First-pass vessel-to-commodity mapping delegated to subagent Sagan. Because `hormuz-fyp.5` taxonomy is still in progress, cargo buckets here are provisional and should reconcile later to the foundation taxonomy.
- 2026-07-06: Mapping pass from Sagan. Core rule: AIS vessel type is only a first-pass classifier. For commodity exposure, join AIS to registry fields, dimensions/DWT, draught change, port-call sequence, and cargo/trade data. AIS Message 5 broadly reports ship/cargo type, ETA, draught, and destination; it does not reliably identify commodity. NOAA/MarineCadastre groups AIS into broad buckets such as Cargo, Tanker, Military, Tug Tow, Other. Sources: https://www.navcen.uscg.gov/ais-class-a-static-voyage-message-5, https://coast.noaa.gov/data/marinecadastre/ais/VesselTypeCodes2018.pdf.

### Recommended Daily Count Buckets

1. `crude_condensate_large_tankers`: VLCC + Suezmax; include Aframax only when registry/route supports crude/condensate.
2. `clean_products_tankers`: MR/LR1/LR2/product tankers.
3. `chemical_tankers`: registry chemical/oil-chemical; specific cargo unknown unless matched.
4. `lng_carriers`.
5. `lpg_and_liquefied_gas_carriers`: split later into LPG/ammonia/ethylene if cargo data supports it.
6. `dry_bulk`: sub-bucket only when cargo data supports fertilizer/sulfur/petcoke/grain/ore/coal/steel.
7. `container_general_ro_ro`.
8. `naval_support_service`: exclude from commodity throughput, retain separately for traffic/security context.

### Provisional Vessel Mapping

| Tracker bucket | AIS / registry filter | Size/capacity assumption | Likely Hormuz commodities | Ambiguity / defer logic |
|---|---|---|---|---|
| Crude/condensate VLCC | AIS tanker + crude tanker registry, roughly 200k-320k DWT | EIA: about 1.9-2.2 million barrels crude | Crude oil, condensate | High confidence only with Gulf export port and laden outbound draught. Vessel type cannot distinguish crude vs condensate vs some fuel oil. |
| Crude/condensate Suezmax | AIS tanker + roughly 120k-200k DWT | Roughly 0.8-1.1 million barrels crude by DWT/barrel conversion | Crude oil, condensate | Same as VLCC; may carry dirty petroleum products/fuel oil. |
| Aframax/LR2 ambiguous large tanker | AIS tanker + roughly 80k-120k DWT; LR2 if coated product tanks | Up to about 750k barrels crude/products depending vessel | Crude, condensate, fuel oil, naphtha, diesel/jet/gasoil | Classify as large tanker ambiguous unless registry and route support crude/product split. |
| Product tankers MR/LR1/Handy | AIS tanker + product/chemical tanker registry, roughly 10k-80k DWT | EIA-style ranges: GP/MR/LR1 from tens to hundreds of thousands of barrels | Gasoline, diesel/gasoil, jet/kerosene, naphtha, clean condensate | AIS cannot identify product; use terminal, draught, fixtures/cargo data. |
| Chemical/parcel tankers | AIS tanker/cargo + chemical/oil-chemical registry | Capacity varies by tank segmentation | Methanol, aromatics, base oils, acids, petrochemicals, some refined products | Defer specific chemical to registry subtype and cargo data. |
| LNG carriers | Gas/LNG carrier registry | Conventional LNGC and Q-Flex/Q-Max capacity in cubic meters | LNG, mainly Qatar/UAE flows | High confidence if registry says LNG carrier; commodity volume still needs capacity/load factor. |
| LPG/liquefied gas carriers | LPG/VLGC/LGC/MGC/ammonia-capable registry | Capacity in cubic meters, not DWT | Propane, butane, possible ammonia/ethylene/VCM | Do not assume all gas carriers are LPG. Use cargo-capability and trade data. |
| Dry bulkers | AIS cargo + bulker registry; Handysize through Capesize | Cargo tonnes constrained by DWT, actual cargo by density/draught | Sulfur, urea, DAP/phosphates, petcoke, cement/clinker, aggregates, steel, grain, coal/ore inbound | Vessel type only says dry bulk. Commodity requires port-pair/cargo data. |
| Container ships | AIS cargo + container registry | TEU capacity | Containerized manufactured goods, machinery, food, chemicals | Do not map to commodity tonnage without manifests/customs data. |
| General cargo/MPP/ro-ro/car carriers | AIS cargo + registry subtype | Lane meters, units, DWT, or hold capacity | Vehicles, project cargo, breakbulk steel, bagged cargo, construction inputs | Keep as broad general/breakbulk/ro-ro unless matched. |
| Naval/coast guard/tug/offshore/support/service | AIS military/other/special craft/tug/offshore supply | Not commodity carriers | Security, escort, offshore-energy support | Exclude from commodity throughput. |

### Working Principle For Publication

Publish daily ship counts by vessel bucket. Publish commodity exposure only where confidence is supported by port-call/cargo/trade data. AIS alone is credible for "what kind of hull crossed Hormuz," not "what product was onboard."

### Closeout

- For the public tracker, use PortWatch's broad class fields directly: `n_tanker`, `n_container`, `n_dry_bulk`, `n_general_cargo`, `n_roro`, `n_cargo`, `n_total`.
- Do not infer specific cargo/product from these classes. Use RQ2 commodity-flow sources for oil/LNG/products/fertilizer/etc.
