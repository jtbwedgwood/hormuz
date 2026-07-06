---
id: "hormuz-l8m.3"
title: "Estimate US power-price implications for data centers"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "datacenters"
  - "electricity"
  - "prices"
  - "us-business"
blocked_by:
  - "hormuz-l8m.1"
blocks:
  - "hormuz-l8m.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:01Z"
updated_at: "2026-07-06T17:35:00Z"
---

# Estimate US power-price implications for data centers

## Description

Assess how oil/LNG/gas price shocks feed into US electricity prices by region, with attention to gas marginal generation and grid mix near AI data center hubs.

## Acceptance Criteria

Regional sensitivity table links fuel price changes to power cost changes with caveats on market structure.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-l8m.1` - Define commodity price shock scenarios
- `hormuz-s49.6` remains relevant to broader stockpile-buffer interpretation, but is not a blocker for this power-price sensitivity table.
- Blocks: `hormuz-l8m.4` - Estimate AI cost-per-token sensitivity

## Work Notes

- 2026-07-06T16:35Z: Built a scenario-ready regional framework rather than a single-point estimate.
- Regional grouping: use EIA's six RTO markets for the core table - ISO-NE, NYISO, PJM, MISO, ERCOT, CAISO - plus the EIA trading-hub proxies for Louisiana/Entergy, Southwest/Palo Verde, and Northwest/Mid-Columbia where the grid is not neatly captured by an RTO frame. EIA notes wholesale electricity prices are shown for those six RTOs and the three extra hubs, and that wholesale prices are closely tied to wholesale natural gas prices in all but the center of the country. Sources: EIA Electricity Monthly Update - Regional Wholesale Markets (accessed 2026-07-06) https://www.eia.gov/electricity/monthly/update/wholesale-markets.php ; EIA wholesale electricity and natural gas market data (accessed 2026-07-06) https://www.eia.gov/electricity/wholesale/.
- Marginal-generation sensitivity method: start with `Δ power price ($/MWh) ≈ marginal heat rate (MMBtu/MWh) × Δ gas price ($/MMBtu)` and then add congestion / losses / ancillary / retail lag separately. EIA defines implied heat rate as day-ahead power price divided by day-ahead gas price, and defines heat rate as Btu per kWh. For an anchored marginal unit, EIA reports modern CCGT plants at 6,960 Btu/kWh on average (2010-2022 vintage), i.e. about 6.96 MMBtu/MWh; EIA also shows the broader natural-gas fleet is technology-dependent, so peaker-heavy or constrained regions should use a higher stress heat rate. Sources: EIA glossary on implied heat rate and heat rate (accessed 2026-07-06) https://www.eia.gov/tools/glossary/index.php?id=I and https://www.eia.gov/tools/glossary/index.php?id=Heat+rate ; EIA CCGT heat-rate article (accessed 2026-07-06) https://www.eia.gov/todayinenergy/detail.php?id=60984.
- Provisional working assumption for the table: use 7.0 MMBtu/MWh as the base marginal gas heat rate, 8.5-10.5 MMBtu/MWh as a peak/stress band, and treat retail pass-through as partial and lagged outside competitive wholesale markets. Quick read-through: a $1/MMBtu gas shock implies about +$7/MWh at the wholesale margin under the base case, before transmission and retail adjustments.
- Current price anchors: EIA's April 2026 Electricity Monthly Update shows Henry Hub at $2.79/MMBtu and notes that Texas (ERCOT) daily peak demand was at the upper end of its 12-month range while ERCOT wholesale prices ranged from $22/MWh to $87/MWh in April 2026. EIA's STEO natural gas outlook currently projects Henry Hub at $3.60/MMBtu for 2026 and $3.46/MMBtu for 2027. Sources: EIA Electricity Monthly Update (accessed 2026-07-06) https://www.eia.gov/electricity/monthly/update/print-version.php ; EIA STEO natural gas outlook (accessed 2026-07-06) https://www.eia.gov/outlooks/steo/report/natgas.php.
- Data-center hub exposure notes: current U.S. concentration is still centered on Northern Virginia, Dallas-Fort Worth, New York/Northern New Jersey, Chicago, Phoenix, and a growing set of frontier markets. Credible market lists and concentration notes from Cushman & Wakefield and JLL place Atlanta, Austin/San Antonio, Chicago, Columbus, Dallas-Fort Worth, Houston, New York/Northern New Jersey, Northern Virginia, Phoenix, Salt Lake City, West Texas, Oregon, and Central Washington among key U.S. markets; JLL says 64% of North American capacity under construction is in frontier markets including West Texas, Tennessee, Wisconsin, and Ohio, and that Texas could overtake Northern Virginia by 2030. Sources: Cushman & Wakefield Americas Data Center Update H2 2025 (accessed 2026-07-06) https://www.cushmanwakefield.com/en/insights/americas-data-center-update ; JLL North America Data Center Report Year-end 2025 (accessed 2026-07-06) https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers ; EIA on Texas data-center-driven load growth (accessed 2026-07-06) https://www.eia.gov/todayinenergy/detail.php?id=63344 ; EIA AEO2026 narrative on data-center electricity growth (accessed 2026-07-06) https://www.eia.gov/outlooks/aeo/narrative/.
- Regional exposure mapping to use in the next pass:
  - Northern Virginia, Pennsylvania, New York/NJ, Boston corridor: PJM / NYISO / ISO-NE, with strong gas marginal exposure but more retail lag outside wholesale customers.
  - Dallas-Fort Worth, Austin/San Antonio, Houston, West Texas: ERCOT, highest near-term sensitivity because ERCOT power prices are very gas-linked and load growth is already sharp.
  - Chicago, Columbus, Iowa, Kansas City, Minneapolis: MISO / SPP overlap, likely moderate-to-high gas pass-through depending on local congestion and coal retirements.
  - Phoenix, Salt Lake City, Reno, Central Washington, Oregon: Southwest / West / Palo Verde / Mid-C proxies, with more hydro/solar influence and more location-specific congestion.
  - Los Angeles / Northern California: CAISO, where EIA's 2026 data show solar often displacing gas on the margin; gas sensitivity is still material in evenings and winter shoulder periods.
  - Atlanta and much of the Southeast: not a clean RTO pass-through case; treat as utility-regulated retail with slower and partial fuel-cost transmission.
- Open blockers: still need `hormuz-l8m.1` shock magnitudes and a separate demand-charge treatment for large data-center tariffs before turning this into a full bill model. `hormuz-s49.6` remains relevant for the broader stockpile-buffer narrative, but it is not a blocker for this regional power-price sensitivity work.

### Regional sensitivity table

Indicative conversion from fuel shock to power-cost change, using the base `+$7/MWh` wholesale rule of thumb for a `+$1/MMBtu` gas move and then adjusting for market structure.

| Region / market | Structure | Indicative power-cost change for `+$1/MMBtu` gas | Interpretation |
|---|---|---:|---|
| ERCOT (Texas) | Competitive wholesale, scarce reserve margin, fast scarcity pricing | `+$7 to +$10/MWh` | Highest short-run sensitivity; data-center loads in Dallas, Houston, and West Texas see the quickest wholesale repricing. |
| PJM / NYISO / ISO-NE | RTO wholesale with congestion and capacity constructs | `+$6 to +$9/MWh` | Strong gas linkage, but nodal congestion and retail lag mute end-user bill changes relative to the wholesale market. |
| MISO / SPP | Mixed fuel stack, congestion, lower average gas dependence than ERCOT/PJM | `+$5 to +$8/MWh` | Sensitivity is meaningful but more location-specific; coal retirements can make marginal gas exposure jump by node. |
| CAISO | Gas still marginal in evening and winter periods, but solar/hydro suppress daytime gas pricing | `+$4 to +$8/MWh` | Daytime power is less gas-sensitive than evening peak; local congestion can dominate the delivered price. |
| Hydro-rich Northwest / Mid-Columbia | Hydro-heavy, transmission-constrained, gas less often marginal | `+$2 to +$5/MWh` | Gas shocks still matter at the margin, but hydrology and transmission constraints often set the price path. |
| Southeast regulated utilities | Vertically integrated or regulated retail recovery | `+$2 to +$6/MWh` at retail, with lag | Fuel-cost changes are usually passed through slowly and incompletely; large-customer tariffs can differ from residential bills. |

- Caveats on market structure:
  - Wholesale markets in ERCOT and the RTOs transmit gas shocks quickly, but retail customers usually see a damped and delayed effect.
  - Regulated utilities recover fuel cost through rate cases and riders, so near-term retail changes are smaller than wholesale moves.
  - Data-center tariffs can add demand charges, coincident-peak charges, and contract-specific hedges, so the table is a power-market sensitivity, not a full site bill model.
- 2026-07-06T17:35Z: Acceptance criteria met. The issue now carries a regional sensitivity table that links gas-price shocks to power-cost changes and states the relevant market-structure caveats. `hormuz-s49.6` remains a caveat for the broader stockpile-buffer narrative, but it is not a blocker for this power-price sensitivity work.
- 2026-07-06 cleanup: removed stale `hormuz-s49.6` blocker from frontmatter to match the issue conclusion above.
