# Hormuz Energy Shock Follow-Up Questions

Last updated: 2026-07-06.

## Short Version

Oil is the macro shock; LNG is the hard physical constraint. Oil is larger in energy and dollar terms, but it has more buffers: strategic stocks, spare production, demand response, and limited Saudi/UAE bypass pipelines. LNG is smaller in total global-energy terms, but Qatar/UAE LNG has no practical bypass and therefore creates a sharper regional gas-price shock.

LPG/NGLs are relevant. They are smaller than crude and LNG, but not negligible: IEA says Gulf producers exported 1.5 mb/d of LPG in 2025, and the repo's base disruption estimate is 1.2 mb/d. The main reason to include them is not total energy share; it is the link to petrochemicals, household cooking fuel, and India/Asia rationing.

The big unresolved question is global accounting: how much of the "replacement supply" was genuinely new supply versus energy redirected away from poorer or less price-insensitive buyers. Existing repo work strongly suggests displacement matters, but it does not yet support a clean global balance sheet.

## Oil Versus LNG

| Question | Answer |
|---|---|
| Main difference | Oil is liquid, storable, globally benchmarked, and mostly used in transport, refining, petrochemicals, and industrial fuels. LNG is natural gas chilled for shipping; it needs liquefaction plants, LNG tankers, regasification terminals, and usually long-term contracts. |
| Fungibility | They are not generally fungible. Oil can sometimes substitute into power or industry, and gas can sometimes displace oil products, but most end uses are locked into equipment, infrastructure, and fuel specs. A jet cannot burn LNG; a gas-fired power plant cannot burn crude without dual-fuel capability. |
| Crisis relevance | Oil has broader macro pass-through. LNG has tighter infrastructure constraints and therefore sharper regional price effects. |
| Price globalization | Oil is more globally integrated because barrels can move, store, blend, and price off Brent/Dubai/WTI-like benchmarks. LNG is globalizing but still regionally segmented by terminal capacity, shipping, contract terms, and pipeline competition. |

The LNG price split is real. EIA reported that after the February 28 closure, TTF rose 35% and JKM rose 51% by the week ending April 24, while U.S. Henry Hub fell 9%. EIA's explanation is straightforward: U.S. LNG export terminals were already near capacity, so the international LNG shock could not immediately pull much more U.S. gas into export markets. See EIA, ["International LNG prices rise amid Strait of Hormuz closure"](https://www.eia.gov/todayinenergy/detail.php?id=67604).

## Scale And Unit Intuition

| Metric | Best Current Number | Intuition |
|---|---:|---|
| Oil through Hormuz before the war | About 20 mb/d in 2024; about 20% of global petroleum liquids consumption. | 1 mb/d is 365 million barrels per year. At $75/bbl, that is about $27 billion/year of gross oil value. |
| Oil share of seaborne trade | More than one-quarter of global seaborne oil trade in 2024/1Q25; IEA says around 25% in 2025. | This is why the route matters even when global consumption share sounds "only" one-fifth. |
| LNG through Hormuz before the war | About 20% of global LNG trade in 2024; over 110 bcm in 2025. | 1 Bcf/d is about 0.38 quads/year. At $12/MMBtu, 1 Bcf/d is roughly $4.5 billion/year. |
| Total global energy share | Oil through Hormuz is roughly 6%-7% of world primary energy on a heat-content basis; Hormuz LNG is roughly 0.6%-0.8%. | This is a denominator check, not a market-impact model. Small shares can still be systemically important if they are hard to replace. |

Sources: EIA says 2024 Hormuz oil flows averaged about 20 mb/d and about 20% of global petroleum liquids consumption; it also says about one-fifth of global LNG trade moved through Hormuz in 2024, primarily from Qatar. IEA says over 110 bcm of LNG moved through Hormuz in 2025 and that there are no alternative routes for those LNG volumes. See EIA oil chokepoint article, EIA LNG article, and IEA Middle East/Hormuz topic pages.

## Supply Side

These are rough exposure estimates from `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`, not observed customs truth. GDP shares use World Bank nominal GDP and simple gross export-value assumptions: oil at $75/bbl and LNG at $12/MMBtu. That means they are useful for scale, not national-accounts accounting.

| Supplier | What Is Cut Off? | What Has A Bypass? | Rough GDP Scale |
|---|---|---|---:|
| Saudi Arabia | Base modeled disruption: 1.5 mb/d crude plus 0.9 mb/d refined products. That is about 35% of the repo's Saudi crude-plus-product exposed baseline, or 27% for crude alone. | Saudi has the main crude bypass, the East-West pipeline to Yanbu. In the base case, most exposed crude is rerouted or preserved, but product flows are less clean. | Base disrupted oil/product gross value is about $66B/year, roughly 5% of 2024 GDP. Crude-only is about 3%. |
| UAE | Base modeled disruption: 0.8 mb/d mixed crude/condensate/products and 0.9 mb/d refined products, plus 0.7 Bcf/d LNG. The oil rows have double-counting risk. | UAE has ADCOP/Habshan-Fujairah for crude, with limited spare room. That helps crude but not LNG. | If the oil rows are read as a broad stress range, gross annual value is roughly 4%-8% of 2024 GDP. LNG is small by UAE GDP scale. |
| Iraq | Base modeled disruption: 2.4 mb/d crude and 0.35 mb/d products, roughly three-quarters of the repo's southern/seaborne exposed oil baseline. | Iraq-Turkey/Ceyhan helps only northern Iraq at limited practical volumes. Southern exports remain Hormuz-linked. | About $75B/year gross value at $75/bbl, roughly 27% of 2024 GDP. This is the most severe oil-exporter macro exposure among the listed countries. |
| Qatar | Base modeled disruption: 10.0 Bcf/d LNG, 0.5 mb/d crude/condensate, and 0.6 mb/d petroleum products. LNG is the core. | No practical seaborne bypass for LNG. | LNG at $12/MMBtu is about $45B/year, or about 21% of 2024 GDP. Oil/product rows add material exposure but should not be mixed with LNG without a macro model. |

The Qatar GDP puzzle is mostly denominator confusion. "LNG exports are 60% of GDP" is too high if interpreted as current gross LNG sales divided by nominal GDP under ordinary prices; a 10 Bcf/d LNG stream is closer to 20%-30% of GDP at $12-$15/MMBtu. It can look much larger if someone uses peak spot prices, hydrocarbon export revenue, government revenue, or export share rather than value added. A 2026 GDP contraction under 10% can coexist with a large LNG export shock because prices rise, outages may not last all year, GDP is value added rather than gross cargo value, and government/non-hydrocarbon activity cushions the headline economy.

## Demand Side

China is the biggest and least transparent adjustment case. Known: China had large Hormuz-linked crude and LNG exposure; public data show lower refinery runs, import timing changes, product export controls, and commercial/operational stock flexibility. Unknown: exact replacement barrels by origin and the split between government SPR, commercial tanks, bonded Iranian barrels, and floating storage. The repo's best wording remains: China appears to be using commercial and operational stock flexibility, not a publicly confirmed large SPR release.

India's rationing references are real, but they are mostly gas/LPG, not crude. That is why the crude demand-reduction bar is small. India reported crude diversification from about 55% non-Hormuz sourcing before the crisis to about 70% during the crisis, while gas and LPG policy orders protected households/CNG first and cut or allocated industrial, fertilizer, refinery, petrochemical, restaurant, and commercial LPG demand.

Japan's replacement supply is the cleanest public case: METI named Yanbu, Fujairah, increased U.S. procurement, and possible Central Asia/South America supply, then estimated alternative procurement around 60% of May would-have-been Hormuz crude and 70%+ for June. Reserves bridged much of the residual.

South Korea's public record is thinner. The visible response is supplier diplomacy, Qatar priority assurances for LNG/condensate, and known oil/LNG reserve frameworks. Treat Korea's replacement and inventory-draw split as modeled, not proven cargo accounting.

The U.S. and Europe can show "cushion" larger than direct exposure because these rows are not measuring only physical replacement of their own imports. They include market-stabilizing releases, product-market support, and global price insulation. That is a real policy technique, but it should be described as market cushioning rather than "they replaced more than they lost."

## Global Price Exposure

Countries are exposed even without direct Hormuz imports because oil, LNG, refined products, fertilizer, sulphur, aluminium, freight, and war-risk insurance are globally or regionally priced. A country can import no Qatari LNG and still pay more if Europe or Asia bids away spot cargoes. A food importer can be hit through urea, ammonia, sulphur, and DAP prices without importing Gulf energy directly. A manufacturer can be hit through aluminium, plastics, diesel, jet fuel, insurance, and freight.

The most important caution: "replacement supply" is often not new supply. It can be diverted cargoes, reserve draw, lower refinery runs, demand destruction, product export curbs, or poorer buyers getting outbid. The repo has country bridge estimates, but it does not yet have a de-duplicated global accounting in which gross lost supply equals new supply plus inventory draw plus global demand reduction plus displaced third-country consumption. That needs a dedicated task.

## Filed Follow-Up Work

The following questions need more work before they should become blog claims:

- Supplier-side cushioning diagram: filed as `hormuz-ccx.7`.
- Exact China/India/Japan/Korea replacement-origin breakdown: filed as `hormuz-f6r.7`.
- Rough global accounting of new supply versus inventory draw, demand destruction, and displaced consumption: filed as `hormuz-ccx.8`.

## Main Sources

- EIA, ["Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint"](https://www.eia.gov/todayinenergy/detail.php?id=65504).
- EIA, ["About one-fifth of global liquefied natural gas trade flows through the Strait of Hormuz"](https://www.eia.gov/todayinenergy/detail.php?id=65584).
- EIA, ["International LNG prices rise amid Strait of Hormuz closure"](https://www.eia.gov/todayinenergy/detail.php?id=67604).
- IEA, ["The Middle East and Global Energy Markets"](https://www.iea.org/topics/the-middle-east-and-global-energy-markets).
- World Bank API, GDP current US dollars, `NY.GDP.MKTP.CD`, accessed 2026-07-06.
- Local anchors: `docs/hormuz-product-disruptions.md`, `docs/hormuz-importer-adjustment.md`, `docs/hormuz-stockpile-buffers.md`, `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`, `data/derived/hormuz_f6r_5_replacement_demand_response.csv`.
