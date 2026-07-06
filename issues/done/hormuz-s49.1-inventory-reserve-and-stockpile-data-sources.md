---
id: "hormuz-s49.1"
title: "Inventory reserve and stockpile data sources"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-s49"
labels:
  - "energy-security"
  - "inventories"
  - "sources"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-s49.2"
  - "hormuz-s49.3"
  - "hormuz-s49.4"
  - "hormuz-s49.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:50Z"
updated_at: "2026-07-06T07:35:00Z"
---

# Inventory reserve and stockpile data sources

## Description

Identify official and market sources for SPR, commercial crude/product inventories, LNG storage, gas inventories, coal stockpiles, and strategic reserves by major importer.

## Acceptance Criteria

Source inventory covers frequency, lag, units, public availability, revisions, and comparability limits.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Unblocked: `hormuz-fyp.1` is done; use `docs/foundation-research-standards.md` as the citation/source-quality rubric.
- Blocks: `hormuz-s49.2` - Quantify OECD and US reserve response
- Blocks: `hormuz-s49.3` - Evaluate China SPR release claims
- Blocks: `hormuz-s49.4` - Assess LNG and gas storage buffering
- Blocks: `hormuz-s49.5` - Assess fertilizer and chemical inventory buffers

## Work Notes

- 2026-07-06: Claimed for current work. Dedicated subagent assigned to inventory reserve/stockpile data sources and optionally append durable public datasets to `data/manifest.csv`. Required output fields: source, frequency, lag, units, geography, public availability, comparability/revision caveats, and confidence.
- 2026-07-06 research pass, access date 2026-07-06:
  - U.S. petroleum: EIA Weekly Petroleum Status Report is the live weekly series; release is Wednesday 10:30 a.m. ET; Table 4 carries crude and product stocks; Petroleum Supply Monthly/Annual is the final revision path for inventories. Sources: https://www.eia.gov/petroleum/supply/weekly/ and https://www.eia.gov/petroleum/supply/monthly/
  - U.S. SPR: EIA's Weekly U.S. Ending Stocks of Crude Oil in SPR series is weekly and runs back to 1982. Source: https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
  - U.S. gas storage: EIA Weekly Natural Gas Storage Report is weekly Thursday 10:30 a.m. ET; it covers Lower 48 working gas storage and the methodology page says the survey covers about 95% of working capacity. Historical weekly series begin in 1994. Sources: https://www.eia.gov/naturalgas/storage/ and https://ir.eia.gov/ngs/methodology.html
  - OECD/IEA oil stocks: IEA Monthly Oil Statistics is a free product with monthly OECD stocks; IEA MODS Stocks is more complete but licensed; Oil Stocks of IEA Countries is public and expresses stockholding in days of net imports, updated with the Oil Market Report. Sources: https://www.iea.org/data-and-statistics/data-product/monthly-oil-statistics ; https://www.iea.org/data-and-statistics/data-product/monthly-oil-data-service-mods-supply-demand-balances-and-stocks ; https://www.iea.org/data-and-statistics/data-tools/oil-stocks-of-iea-countries
  - JODI oil/gas: JODI-Oil is monthly with April 2026 data updated 25 June 2026; JODI-Gas is monthly around the 20th and includes closing stocks and LNG trade. JODI's country note says China still cannot provide stock levels, so China inventory work needs inference inputs rather than a direct public stock series. Sources: https://www.jodidata.org/oil/ ; https://www.jodidata.org/gas/database/overview.aspx ; https://www.jodidata.org/_resources/files/downloads/oil-data/jodi-oil-country-note.xlsx
  - Europe gas/LNG storage: GIE AGSI+ and ALSI are daily public platforms; the API docs say data are published daily for the previous gas day and updated at 19:30 CET and again later the same day. Sources: https://www.gie.eu/press/gie-eus-partner-for-gas-market-transparency/ and https://www.gie.eu/transparency-platform/GIE_API_documentation_v006.pdf
  - India coal stockpiles: Central Electricity Authority daily coal reporting is the main public stockpile source I found for coal; the dashboard includes opening and closing stock views for all India. Sources: https://cea.nic.in/fuel-management-division/?lang=en and https://cea.nic.in/dashboard/?lang=en
  - China inferred crude stocks: no direct public stock series; use monthly NBS crude production and crude processing plus GACC monthly crude import tables as the apparent-balance proxy stack. Sources: https://www.stats.gov.cn/english/ and https://english.customs.gov.cn/Statistics/Statistics?ColumnId=1
  - Fertilizer and chemicals: USDA AgTransport provides a public fertilizer inventory dashboard for primary nutrients N/P/K; Census M3 is the public broad chemical-products inventory proxy and is benchmark revised. Sources: https://agtransport.usda.gov/Fertilizer/Fertilizer-Production-Inventory-and-Disappearance/qize-x4xc and https://www.census.gov/manufacturing/m3
  - Gap note: I did not find a durable public global fertilizer stock series or a comparably clean global chemical stock series. Outside the U.S. the practical path is usually trade and production balances plus company or country disclosures.
- 2026-07-06: Acceptance criteria met for initial source inventory. Durable public and licensed source rows were added to `data/manifest.csv`; downstream tasks can now use this file as the reference source inventory, while preserving caveats around China stocks and fertilizer/chemical inventories.
