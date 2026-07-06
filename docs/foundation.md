# Hormuz Foundation

As of 2026-07-06, treat the Strait of Hormuz shock as an **effective disruption with partial recovery**, not a simple open/closed binary. The working narrative should track three separate things: physical transits, insurable/commercially viable transits, and commodity supply reaching end markets.

## Source Standard

Use four confidence labels:

| Label | Use when | Blog wording |
|---|---|---|
| High | Official statistics, primary legal/policy text, exchange data, or reproducible AIS/price data; method is visible. | "shows", "reported" |
| Medium | Reputable news, named analyst data, think-tank work with visible sourcing, or commercial estimates with partial method. | "estimates", "indicates" |
| Low | Single-source claims, social media, unattributed industry chatter, or paywalled summaries without visible method. | "suggests", "reportedly" |
| Excluded | No date, no origin, circular citation, or claim cannot be tied to a primary observation. | Do not use except as rumor context. |

Every cited claim needs: source name, URL, publication/access date, event/observation date, geography, commodity/vessel scope, unit, method note, confidence label, and archive path if saved. For paywalled sources, record only what is visible or independently verified elsewhere; never let a paywalled claim be the sole support for a key number.

## Canonical Dates

| Date | Event | Why it matters | Confidence |
|---|---|---|---|
| 2024 | Normal oil flow through Hormuz averaged about 20 million b/d, about 20% of global petroleum liquids consumption. | Best public prewar oil-flow anchor. | High |
| 2024 | About one-fifth of global LNG trade moved through Hormuz, mostly from Qatar. | Best public LNG-flow anchor. | High |
| 2025 | IEA says about 25% of world seaborne oil trade and more than 110 bcm of LNG transited Hormuz. | Stronger 2025 baseline for scenario models if IEA tables are used. | High |
| 2026-02-28 | U.S. and Israeli strikes on Iran preceded the acute Hormuz disruption, per Brookings' June account. | Shock onset marker for event-study charts. | Medium |
| 2026-03-01 | IEA says LNG supply losses from Qatar/UAE began on March 1, exceeding 300 million cubic metres per day. | Gas-market disruption start date. | High |
| 2026-03-02 | CSIS says the waterway was effectively closed from March 2; Brookings describes insurance/crew risk making transit commercially unviable. | Primary closure start for traffic tracker. | Medium |
| 2026-04-17 to 2026-04-20 | CSIS reports a failed reopening attempt: at least 13 tankers got through after Iran said the strait was open, but many reversed. | Shows why "announced open" and "traffic normalized" are different. | Medium |
| 2026-06-17 | Reported interim U.S.-Iran arrangement began partial recovery in traffic. | Use as recovery/regime-change marker, but verify with primary text if available. | Medium-Low |
| 2026-07-05 | OPEC+ reportedly agreed to raise August output by 188,000 b/d while Hormuz traffic was recovering but still risky. | Market expectation/current-status marker. | Medium-Low |

## Baselines And Scenarios

Use these baseline windows unless a downstream task has a better reason:

| Domain | Baseline | Reason |
|---|---|---|
| Daily ship transits | 2025-01-01 to 2026-02-27, with 2024 as cross-check | Captures recent post-Red Sea routing behavior before the acute war shock. |
| Oil/LNG/product flows | 2024 and 2025 annual averages | EIA has 2024/1Q25 public numbers; IEA has 2025 crisis factsheet numbers. |
| Prices | 60 trading days before 2026-02-28 plus 2025 average | Separates immediate event shock from preexisting volatility. |
| Inventories/reserves | Latest pre-shock weekly/monthly value before 2026-02-28 | Avoids mixing policy response into starting buffer. |
| Historical comparisons | Normalize to share of global consumption/trade, days of inventory cover, price move vs trailing 60-day average, and duration. | Avoids dumb barrel-only comparisons. |

Scenario taxonomy:

| Scenario | Definition | Key metrics |
|---|---|---|
| S0: Baseline | No acute Hormuz disruption; normal insurance and routing. | Transits/day, flows/day, price spread vs 2025 average. |
| S1: Insurance shock | Strait physically passable, but insurance/crew risk reduces willing traffic. | War-risk premium, failed/reversed voyages, dark AIS share. |
| S2: Partial closure | Some escorted/toll/dark traffic gets through; traffic materially below baseline. | Daily crossings, commodity throughput, queue length. |
| S3: Effective closure | Commercial traffic near zero or economically unviable for most operators. | Missed b/d, LNG bcm/week, stranded vessels. |
| S4: Reroute/bypass | Saudi/UAE pipelines and non-Gulf supply offset part of the loss. | Bypass b/d, replacement origin, extra freight/time. |
| S5: Recovery | Transit counts rise but remain below baseline until queues, insurance, repairs, and inventories normalize. | Recovery slope, inventory rebuild, price reversion. |

## Commodity Taxonomy

| Commodity | Unit | Vessels/data proxy | Main Gulf exporters | Main exposed importers | Include? |
|---|---|---|---|---|---|
| Crude oil/condensate | b/d, barrels | Crude/product tankers, Kpler/Vortexa/EIA | Saudi Arabia, Iraq, UAE, Kuwait, Iran, Qatar | China, India, Japan, South Korea | Yes: core shock. |
| Refined products | b/d, barrels | Product tankers, refinery runs | Gulf refiners | Asia, Europe, East Africa | Yes: diesel/jet fuel inflation channel. |
| LNG | bcm, bcf/d, tonnes | LNG carriers, IEA/EIA/Kpler | Qatar, UAE | China, India, South Korea, Japan, Europe | Yes: no practical bypass. |
| LPG/NGLs | b/d, tonnes | LPG carriers | Qatar, UAE, Saudi Arabia, Kuwait | Asia petrochemicals/residential LPG | Yes: petrochemical and household-fuel channel. |
| Fertilizer: urea/ammonia/phosphate/DAP | tonnes | Bulk carriers, customs, IEA/FAO/World Bank prices | Qatar, Saudi Arabia, Oman, UAE, Iran | India, Brazil, Asia, Africa | Yes: food-cost channel. |
| Sulphur | tonnes | Dry bulk, customs | Qatar, UAE, Saudi Arabia, Kuwait | Fertilizer/acid users | Yes: non-obvious, high share of seaborne trade. |
| Aluminium | tonnes | Bulk/general cargo, producer exports | UAE, Bahrain, Qatar, Saudi Arabia | Asia, Europe, U.S. | Yes: manufacturing/electrification input. |
| Petrochemicals/plastics | tonnes | Chemical/product tankers, container/bulk | Saudi Arabia, Qatar, UAE, Kuwait | Asia, Europe | Yes, but expect weaker public data. |
| Containers/general cargo | TEU, tonnes | Container AIS/port calls | Jebel Ali/Gulf ports | Regional importers/exporters | Include as secondary logistics effect. |

## Data Inventory

Use `data/manifest.csv` as the control file. Store licensed/raw extracts under `data/raw/` only when license permits; otherwise keep metadata and retrieval notes in the manifest. Put cleaned reproducible outputs in `data/derived/`, notebooks in `notebooks/`, scripts in `scripts/`, and publication assets in `figures/`.

Minimum manifest fields: `dataset_id`, `title`, `provider`, `url`, `access_type`, `frequency`, `geography`, `unit`, `coverage_start`, `coverage_end`, `license_or_terms`, `local_path`, `refresh_rule`, `confidence`, `notes`.

## Price Series

| Series | Source | Frequency/access | Unit | Use |
|---|---|---|---|---|
| Brent spot | EIA/FRED `DCOILBRENTEU` | Daily, public | $/bbl | Global oil shock anchor. |
| WTI spot | EIA/FRED `DCOILWTICO` | Daily, public | $/bbl | U.S. pass-through and Brent-WTI spread. |
| Dubai/Oman crude | CME/DME/Platts/Argus | Daily, partly licensed | $/bbl | Asia sour-crude benchmark. |
| EIA petroleum product spot prices | EIA | Daily/weekly/monthly, public | $/gal or $/bbl | Gasoline, diesel, jet fuel pass-through. |
| Henry Hub | EIA/FRED | Daily/weekly, public | $/MMBtu | U.S. gas/power cost channel. |
| Dutch TTF, JKM LNG | ICE/CME/Platts/Argus | Daily, often licensed | EUR/MWh, $/MMBtu | LNG scarcity and Europe/Asia gas effects. |
| Fertilizer prices | World Bank Pink Sheet | Monthly, public | $/mt | Urea/DAP/phosphate stress. |
| Aluminium/sulphur/petrochemicals | LME, World Bank, ICIS/Argus | Daily/monthly, mixed | $/mt | Non-obvious industrial exposures. |
| Freight/war risk | Baltic Exchange, Drewry, Lloyd's/List, broker quotes | Daily/weekly, mixed | index, $/day, % hull value | Separates commodity price from shipping-risk premium. |

## Chart And Map Standards

Charts should always show: baseline window, event markers, latest observation date, unit, source footnote, and uncertainty/confidence label. Use ribbons for modeled ranges; use points or hatching for sparse/unverified observations; never interpolate missing AIS days without marking them.

Maps should use WGS84 data, label the strait, Gulf of Oman, Persian Gulf, UAE/Oman/Iran coastlines, and relevant bypass routes. Use arrows only for measured or clearly modeled flows. Export final figures as SVG plus 2x PNG; keep the script/notebook able to regenerate each figure from manifest-listed inputs.

## Key Sources

- EIA, "World Oil Transit Chokepoints": https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints
- EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint": https://www.eia.gov/todayinenergy/detail.php?id=65504
- IEA, "The Middle East and Global Energy Markets": https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- CSIS, "The Strait of Hormuz in 8 Charts": https://www.csis.org/analysis/strait-hormuz-8-charts
- Brookings, "From chokepoint to crisis": https://www.brookings.edu/articles/from-chokepoint-to-crisis-the-strait-of-hormuz-and-global-oil-markets/
- IMF PortWatch: https://portwatch.imf.org/pages/data-and-methodology
- UN AIS Task Team: https://unstats.un.org/bigdata/task-teams/ais/index.cshtml
- EIA petroleum spot prices: https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm
- FRED Brent/WTI: https://fred.stlouisfed.org/graph/?id=DCOILWTICO,DCOILBRENTEU
- World Bank Commodity Markets/Pink Sheet: https://www.worldbank.org/en/research/commodity-markets
