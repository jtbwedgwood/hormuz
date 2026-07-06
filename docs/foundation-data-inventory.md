# Foundation Data Inventory

Last updated: 2026-07-06. Scope: `hormuz-fyp.4`, `hormuz-fyp.5`, and `hormuz-fyp.6`.

## Data Layout

Use this structure:

| Path | Purpose | Commit rule |
|---|---|---|
| `data/manifest.csv` | One row per dataset/source extract. | Commit. |
| `data/raw/` | Public raw downloads small enough to version. | Commit only public/licensed-permitted extracts. |
| `data/external/` | Local pointers or cached pulls from APIs/vendor tools. | Commit metadata, not restricted payloads. |
| `data/derived/` | Clean outputs used by charts/tables. | Commit if reproducible and not restricted. |
| `notebooks/` | Exploratory analysis with named inputs/outputs. | Keep only useful notebooks. |
| `scripts/` | Reproducible loaders/cleaners/chart builders. | Commit. |
| `figures/` | Publication charts/maps plus machine-readable figure data. | Commit final/reusable outputs. |

Manifest fields are defined in `data/manifest.csv`: `dataset_id`, `title`, `provider`, `url`, `access_type`, `frequency`, `geography`, `unit`, `coverage_start`, `coverage_end`, `license_or_terms`, `local_path`, `refresh_rule`, `confidence`, `notes`.

Licensed AIS/commercial data rule: do not commit restricted raw data, screenshots, or derived tables that violate provider terms. Keep only provider name, module, query parameters, retrieval date, allowed summary fields, and notes needed to reproduce inside the licensed environment.

## Commodity Taxonomy

| Commodity | Unit | Vessel/data proxy | Exporters exposed through Hormuz | Main exposed destinations | Priority |
|---|---|---|---|---|---|
| Crude oil and condensate | b/d, barrels | Crude tankers; EIA/Vortexa/Kpler | Saudi Arabia, Iraq, UAE, Kuwait, Iran, Qatar | China, India, Japan, South Korea | P0 |
| Refined oil products | b/d, barrels | Product tankers; refinery exports; EIA/IEA | Saudi Arabia, UAE, Kuwait, Qatar, Bahrain | Asia, Europe, East Africa | P0 |
| LNG | bcm, bcf/d, tonnes | LNG carriers; EIA/IEA/Kpler | Qatar, UAE | China, India, South Korea, Japan, Europe | P0 |
| LPG/NGLs | b/d, tonnes | LPG carriers; IEA/customs | Qatar, UAE, Saudi Arabia, Kuwait | Asia petrochemicals, India, East Asia | P1 |
| Fertilizer: urea, ammonia, phosphate, DAP | tonnes | Bulk/liquid gas/chemical vessels; World Bank/FAO/customs | Qatar, Saudi Arabia, Oman, UAE, Iran | India, Brazil, Asia, Africa | P0 |
| Sulphur | tonnes | Dry bulk; customs/IEA | Qatar, UAE, Saudi Arabia, Kuwait | Fertilizer, sulphuric acid, mining/refining users | P1 |
| Aluminium | tonnes | Bulk/general cargo; producer/customs data | UAE, Bahrain, Qatar, Saudi Arabia | Asia, Europe, U.S. | P1 |
| Petrochemicals/plastics | tonnes | Chemical/product tankers, containers; ICIS/Argus/customs | Saudi Arabia, Qatar, UAE, Kuwait | Asia, Europe | P1 |
| Containers/general cargo | TEU, tonnes | Container AIS/port calls; IMF PortWatch, port stats | Jebel Ali/Gulf ports | Regional Gulf economies and transshipment partners | P2 |

Inclusion rationale:

- Energy is the core price and supply shock.
- Fertilizer, sulphur, aluminium, LPG, and petrochemicals are the best "beyond oil" candidates because the Gulf has material export share and disruption channels are plausible.
- General container cargo belongs in the logistics section, not the headline supply-removal table, unless port-call data show a measurable Gulf trade freeze.

## Price-Series Inventory

| Series | Source | Access/frequency | Unit | Comparison method |
|---|---|---|---|---|
| Brent spot | EIA/FRED `DCOILBRENTEU` | Public daily | $/bbl | Percent and dollar change vs 2026-01-01 to 2026-02-27 average; also 2025 average. |
| WTI spot | EIA/FRED `DCOILWTICO` | Public daily | $/bbl | Same; use Brent-WTI spread for international vs U.S. tightness. |
| Dubai/Oman sour crude | CME/DME, Platts, Argus | Mixed, daily | $/bbl | Use if available for Asian refinery exposure; label licensed if from Platts/Argus. |
| U.S. gasoline/diesel/jet fuel spot | EIA petroleum spot prices | Public daily/weekly/monthly | $/gal or $/bbl | Compare product cracks vs Brent/WTI to isolate refining/product scarcity. |
| Henry Hub gas | EIA/FRED | Public daily/weekly | $/MMBtu | U.S. power/data-center channel; separate from LNG-exposed Europe/Asia. |
| Dutch TTF gas | ICE/CME/market data vendors | Mixed daily | EUR/MWh | Europe gas shock and LNG competition proxy. |
| JKM LNG | Platts/ICE/CME/vendor | Mostly licensed daily | $/MMBtu | Asia LNG scarcity proxy. |
| World Bank fertilizer prices/index | World Bank Pink Sheet | Public monthly | $/mt or index | Fertilizer cost channel; use monthly because public daily data are limited. |
| Aluminium | LME/World Bank | Public/mixed daily/monthly | $/mt | Manufacturing/input-cost channel. |
| Freight and war risk | Baltic Exchange, Drewry, Lloyd's List, broker notes | Mixed daily/weekly | index, $/day, % hull value | Keep separate from commodity prices; often lower confidence if quote-based. |

## Source Anchors

- EIA World Oil Transit Chokepoints: https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints
- EIA Hormuz critical chokepoint note: https://www.eia.gov/todayinenergy/detail.php?id=65504
- IEA Middle East and Global Energy Markets: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- IMF PortWatch methodology: https://portwatch.imf.org/pages/data-and-methodology
- UN AIS Task Team: https://unstats.un.org/bigdata/task-teams/ais/index.cshtml
- EIA petroleum spot prices: https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm
- FRED Brent/WTI graph: https://fred.stlouisfed.org/graph/?id=DCOILWTICO,DCOILBRENTEU
- World Bank Commodity Markets: https://www.worldbank.org/en/research/commodity-markets
