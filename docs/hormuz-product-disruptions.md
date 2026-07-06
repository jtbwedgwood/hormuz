# Hormuz Product Disruptions

Last updated: 2026-07-06.

## Bottom Line

The Strait of Hormuz shock is not just an oil story. Oil is the largest barrel exposure, but the more interesting result is that several harder-to-substitute markets are also routed through the same narrow lane: LNG, LPG, sulphur, urea, ammonia, phosphate fertilizers, aluminium, and petrochemical feedstocks.

The cleanest blog framing is:

- Oil sets the macro scale: roughly 20 mb/d of oil and oil products moved through Hormuz in 2024, with about 15 mb/d of crude through the Strait in 2025.
- LNG is the hard constraint: more than 110 bcm/year moved through Hormuz in 2025, mostly Qatar and UAE LNG, with no practical bypass.
- The surprising industrial choke points are real: about half of global seaborne sulphur trade, about 5 Mt/year of aluminium shipments, 34% of global urea trade, 23% of ammonia trade, and 18% of MAP/DAP trade are tied to Hormuz-adjacent flows.
- Freight and war-risk insurance are not side effects. They turn a physical chokepoint into a delivered-cost shock even for cargoes that still move.

This epic is complete for the current public-source stage. The estimates should be refreshed if licensed cargo-flow data, Kpler/Vortexa extracts, or vessel-level AIS become available.

## Coolest Results

| Result | Why It Matters | Best Current Number | Confidence |
|---|---|---:|---|
| Hormuz is still a one-line macro shock. | Even before product detail, this is a large share of the world oil system. | 20.26 mb/d oil and oil products in 2024; about 14.95 mb/d crude in 2025. | High for baseline; medium for disrupted volume. |
| Qatar/UAE LNG is the cleanest no-bypass case. | Oil has Saudi/UAE bypass pipelines; Qatar LNG does not have an equivalent. | >110 bcm/year through Hormuz in 2025; modeled base disruption 10.7 Bcf/d across Qatar/UAE. | High. |
| Sulphur is the best non-obvious commodity. | Sulphur feeds sulphuric acid, phosphate fertilizers, refining, and parts of the critical-minerals chain. | About half of global seaborne sulphur trade moves through Hormuz; modeled base disrupted availability: 6.15 Mt/year across Qatar/UAE/Saudi rows. | High for market share; medium for disrupted country tonnage. |
| Fertilizer exposure is broad, not just a footnote. | Urea/ammonia/phosphates connect the Strait to food costs and farm input prices. | Hormuz-adjacent countries account for 34% of global urea trade, 23% of ammonia trade, and 18% of MAP/DAP trade. | High for shares. |
| Aluminium belongs in the story. | Gulf smelters are a material source of primary aluminium, which matters for manufacturing, construction, power systems, and packaging. | IEA/World Bank evidence supports about 5 Mt/year shipped through Hormuz and about 8% Gulf share of global supply. | High for scale; medium for disrupted volume. |
| LPG/naphtha is the bridge from energy to plastics. | It connects the Strait to petrochemical feedstock and polymer production rather than only fuels. | IEA says 30% of seaborne LPG exports crossed Hormuz in 2025; modeled base disruption: 1.2 mb/d. | High for share; medium for modeled disruption. |
| Insurance/freight amplifies every row. | A ship can be physically able to move while commercially uneconomic or unavailable. | War-risk premium moved from roughly 0.1%-0.15% pre-war to 1%-3% in cited crisis windows; VLCC freight quotes reached hundreds of thousands of dollars/day. | Medium-high. |

## The Core Supply Picture

Use three layers, not one blended number.

1. Baseline exposure: what normally uses Hormuz.
2. Physical/logistical offset: what can bypass, reroute, store, or wait.
3. Market impact: what the world cannot easily replace, even if the absolute tonnage is smaller.

### Baseline Exposure

The strongest baseline anchors are:

| Product | Normal Hormuz Exposure | Source/Notes |
|---|---:|---|
| Oil and oil products | 20.26 mb/d in 2024; 20.10 mb/d in 1Q25. | EIA figure data based on Vortexa, recorded in `hormuz-kmz.1`. |
| Crude oil | About 14.95 mb/d through Hormuz in 2025. | IEA denominator used in `hormuz-kmz.6`. |
| Qatar LNG | 9.28 Bcf/d in 2024; 10.65 Bcf/d in 1Q25. | EIA LNG figure data. |
| UAE LNG | 0.70 Bcf/d in 2024; 0.78 Bcf/d in 1Q25. | EIA LNG figure data. |
| Gulf refined products | 3.3 mb/d in 2025. | IEA Middle East markets page. |
| Gulf LPG | 1.5 mb/d in 2025. | IEA Middle East markets page. |
| Qatar sulphur | 3.13 Mt/year in 2024. | WITS/UN Comtrade. |
| UAE sulphur | 5.1 Mt/year in 2024. | USGS UAE country note. |
| Saudi urea | 4.44 Mt/year in 2024. | WITS/UN Comtrade. |
| Qatar urea proxy | 5.82 Mt/year in 2024 production. | QAFCO report; production proxy, not pure exports. |
| Bahrain unwrought alloyed aluminium | 0.968 Mt/year in 2024. | WITS/UN Comtrade. |

### Bypass And Reroute Limits

Saudi Arabia and the UAE have the only serious crude bypass options.

| Route | What It Can Do | Constraint |
|---|---|---|
| Saudi East-West / Petroline | Main Saudi crude route to the Red Sea; nameplate or maximum cited around 7.0 mb/d. | Spare usable capacity is much lower than nameplate when already heavily used. |
| UAE ADCOP / Habshan-Fujairah | Moves UAE crude to Fujairah outside Hormuz; current capacity around 1.5-1.8 mb/d, with about 0.7 mb/d additional room in the IEA framing. | Helps UAE crude, not Qatar/Kuwait/Bahrain/LNG. |
| Iraq-Turkey / Ceyhan | Helps only northern Iraqi crude, with practical current flow around 0.25-0.4 mb/d in the research notes. | Does not solve southern Iraq exports, which remain Hormuz-linked. |
| Oman storage/ports | Useful for Omani volumes and staging. | Not a Gulf-system substitute at Saudi/UAE scale. |
| Qatar/UAE LNG | No practical seaborne bypass. | This is the strongest hard constraint in the whole epic. |
| Kuwait/Bahrain | No meaningful bypass. | Storage can delay pain, but it is not a true alternate export route. |

Use EIA's 2.6 mb/d Saudi/UAE spare bypass estimate as the conservative base offset. Use IEA's 3.5-5.5 mb/d available bypass range as a sensitivity.

## Disruption Estimates

The current country/product estimates live in `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`.

These are modeled low/base/high values. They use public PortWatch traffic severity as a traffic proxy, `hormuz-kmz.1` as the baseline flow table, and `hormuz-kmz.2` as the bypass constraint layer. They are not vessel-manifest truth.

### Base Case By Unit

| Unit Group | Mechanical Base Sum | How To Read It |
|---|---:|---|
| Oil/products rows | 10.8 mb/d | Useful as a severity proxy, but not a final additive headline because some crude/product/LPG rows overlap and route splits are imperfect. |
| LNG rows | 10.7 Bcf/d | The most robust removed-supply estimate because Qatar/UAE LNG has no practical bypass. |
| Fertilizer/sulphur/aluminium rows | 19.5 Mt/year | Annualized disrupted export availability; not one comparable commodity market. |

### Largest Base-Case Rows

| Country | Product | Baseline | Base Disruption | Classification | Confidence |
|---|---:|---:|---:|---|---|
| Qatar | LNG | 10.65 Bcf/d | 10.00 Bcf/d | removed | High |
| UAE | LNG | 0.78 Bcf/d | 0.70 Bcf/d | removed | High |
| Iraq | Crude oil and condensate | 3.20 mb/d | 2.40 mb/d | removed or delayed | Medium |
| Saudi Arabia | Crude oil and condensate | 5.48 mb/d | 1.50 mb/d | rerouted or removed | Medium |
| Iran | Crude oil and condensate | 1.40 mb/d | 1.10 mb/d | removed or delayed | Medium-low |
| Kuwait | Crude/products | 1.33 mb/d | 1.00 mb/d | removed or delayed | Medium-low |
| Saudi Arabia | Refined products | 1.30 mb/d | 0.90 mb/d | removed, delayed, or rerouted | Medium-low |
| UAE | Refined products | 1.50 mb/d | 0.90 mb/d | rerouted or removed | Medium-low |
| Qatar | Urea proxy | 5.82 Mt/year | 4.40 Mt/year | delayed or removed | Medium-low |
| UAE | Sulphur | 5.10 Mt/year | 3.50 Mt/year | rerouted or removed | Medium |
| Saudi Arabia | Urea | 4.44 Mt/year | 3.30 Mt/year | delayed or removed | Medium |
| Qatar | Ammonia proxy | 3.71 Mt/year | 2.80 Mt/year | delayed or removed | Medium-low |
| Qatar | Sulphur | 3.13 Mt/year | 2.40 Mt/year | delayed or removed | Medium |
| Bahrain | Aluminium | 0.968 Mt/year | 0.75 Mt/year | delayed or removed | Medium |

The absolute oil rows are important, but the blog should not stop there. LNG, sulphur, fertilizer, and aluminium are where the story becomes less obvious and more defensible as a supply-chain shock rather than just another crude-price spike.

## Why Price Response Is Not Proportional To Barrels

Oil has the largest headline volume, but it also has the richest offset system: spare capacity, inventories, strategic reserves, demand destruction, and partial Saudi/UAE bypass capacity. That does not make the oil shock small, but it means the price response is mediated by buffers.

LNG has much less route flexibility. Qatar and UAE LNG exports depend on LNG trains and seaborne cargoes through Hormuz. If the Strait is commercially shut, LNG cannot simply move to the Red Sea by pipeline.

Fertilizer and sulphur are smaller by weight than oil, but less substitutable in the near term. A disruption to sulphur can propagate into sulphuric acid and phosphate fertilizer chains. A disruption to ammonia or urea can show up in planting-season fertilizer availability, not just energy balances.

Freight and insurance make the whole system nonlinear. In the crisis evidence, war-risk premiums moved from roughly 0.1%-0.15% of hull value pre-war to 1%-3% in cited crisis windows, and freight quotes for large tankers reached extreme levels. Even when cargo moves, the landed price can change sharply.

## What We Know Versus What We Are Modeling

| Claim Type | Status |
|---|---|
| Normal oil/LNG flows through Hormuz | Strong. EIA/IEA provide public baselines. |
| Broad daily traffic collapse and partial recovery | Strong for aggregate public counts. IMF PortWatch is validated against annual scale and independent crisis-collapse evidence. |
| LNG removed supply | Strongest product-specific disruption claim because no practical bypass exists and IEA reports >300 mcm/d regional LNG supply loss. |
| Oil removed vs delayed vs rerouted by country | Modeled. Baselines and bypass constraints are strong, but cargo-level classification needs licensed flow data to tighten. |
| Fertilizer, sulphur, aluminium disruption volumes | Modeled from trade/production baselines and route dependence. Good enough for ranking and narrative, not final market-clearing losses. |
| Actual cargo onboard each vessel | Not available from public PortWatch. Requires vessel-level AIS plus cargo/fixture data. |
| AIS-dark or sanctioned flows | Material uncertainty, especially for Iran and shadow-fleet oil movements. |

## How To Use This In The Blog

Strong wording:

- "Hormuz is not just an oil chokepoint; it is also a gas, fertilizer, sulphur, aluminium, and petrochemical feedstock chokepoint."
- "The cleanest hard-stop case is LNG, because Qatar and UAE LNG have no practical bypass route."
- "Sulphur is the best surprising industrial input: roughly half of global seaborne sulphur trade moves through Hormuz."
- "Freight and insurance turn a physical disruption into a delivered-cost shock, even when some cargoes still move."

Careful wording:

- "Our base modeled country/product table estimates..." rather than "we observed..."
- "Removed, delayed, or rerouted" rather than only "removed from the market" for oil and refined products.
- "Annualized disrupted export availability" for fertilizer/sulphur/aluminium rows.

Avoid:

- Summing all rows into one grand total.
- Treating PortWatch tanker counts as barrels.
- Treating product tanker movements as proof of specific diesel, naphtha, or LPG cargoes.
- Equating nameplate pipeline capacity with immediately available bypass capacity.

## Files

- Epic: `issues/done/hormuz-kmz-rq2-quantify-products-and-supply-disrupted.md`
- Baseline flows: `issues/done/hormuz-kmz.1-estimate-normal-hormuz-export-flows-by-country-and-product.md`
- Bypass capacity: `issues/done/hormuz-kmz.2-map-bypass-routes-and-non-hormuz-export-capacity.md`
- Disruption estimates: `issues/done/hormuz-kmz.3-estimate-supply-removed-delayed-or-rerouted.md`
- Non-obvious products: `issues/done/hormuz-kmz.4-investigate-non-obvious-disrupted-products.md`
- Freight/insurance: `issues/done/hormuz-kmz.5-quantify-freight-insurance-and-war-risk-disruption.md`
- Market balances: `issues/done/hormuz-kmz.6-reconcile-disrupted-volumes-with-global-market-balances.md`
- Master table: `issues/done/hormuz-kmz.7-produce-product-disruption-master-table.md`
- Country/product estimates: `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`
- Product master table: `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`

## Key Sources

- EIA, Strait of Hormuz remains critical oil chokepoint: https://www.eia.gov/todayinenergy/detail.php?id=65504
- EIA, World Oil Transit Chokepoints: https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints
- EIA, STEO: https://www.eia.gov/outlooks/steo/
- IEA, The Middle East and Global Energy Markets: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- IEA, Strait of Hormuz: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- IMF PortWatch methodology/data: https://portwatch.imf.org/pages/data-and-methodology
- IFASTAT: https://ifastat.org/
- World Bank commodity markets blog: https://blogs.worldbank.org/en/developmenttalk/five-questions-on-how-the-war-in-the-middle-east-is-affecting-commodity-markets
- UNCTAD logistics disruption note: https://unctad.org/system/files/non-official-document/myem_tlb_12th_session_p4_tokuda_en.pdf
