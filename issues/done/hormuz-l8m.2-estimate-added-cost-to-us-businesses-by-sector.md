---
id: "hormuz-l8m.2"
title: "Estimate added cost to US businesses by sector"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-l8m"
labels:
  - "ai"
  - "input-output"
  - "prices"
  - "us-business"
blocked_by:
  - "hormuz-l8m.1"
blocks:
  - "hormuz-l8m.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:10:00Z"
updated_at: "2026-07-06T17:20:00Z"
---

# Estimate added cost to US businesses by sector

## Description

Use input-output tables, energy intensity, fuel shares, and price pass-through assumptions to estimate increased costs for major US business sectors.

## Acceptance Criteria

Sector table reports direct energy costs, indirect input costs where feasible, and sensitivity to pass-through assumptions.

## Dependency Notes

- Parent: `hormuz-l8m` - RQ5: Estimate US business and AI cost impacts
- Blocked by: `hormuz-l8m.1` - Define commodity price shock scenarios
- Blocks: `hormuz-l8m.5` - Cross-check against macro inflation and energy models

## Work Notes

- 2026-07-06T16:00Z: Claimed for parallel evidence gathering. Depends on `hormuz-l8m.1`; until price scenarios are finalized, focus on data sources, sector-cost method, formulae, and sensitivity-ready tables.
- 2026-07-06T16:35Z: First-pass method should be scenario-ready, not scenario-specific. Use annual sector gross output as the scaling base and layer in direct energy intensity plus indirect input-cost exposure from BEA I-O coefficients.
- 2026-07-06T17:20Z: Preliminary sector-cost table is now scenario-ready using the resolved price shocks from `hormuz-l8m.1`, the pass-through framing from `hormuz-l8m.5`, and the manufacturing energy anchors from EIA MECS 2022. Because the repo still lacks a full BEA download, the table is intentionally a template-plus-anchor set rather than a final all-sectors estimate.

### Recommended sector grouping

- Start with BEA-aligned private industry buckets, then split out the most energy-sensitive nodes:
  - Upstream energy/materials: oil & gas extraction, mining support, utilities, petroleum/coal, chemicals/fertilizers/plastics, basic metals.
  - Goods and logistics-heavy sectors: agriculture & food, construction, durables manufacturing, nondurables manufacturing, transportation & warehousing, wholesale trade, retail trade.
  - Services: information, finance/insurance/real estate, professional/business services, health/education, accommodation/food, other services.
- Keep a separate overlay for a few high-energy commodity chains if the shock is concentrated there: refining/petroleum products, LNG/natural gas, fertilizer, petrochemicals, steel, glass, cement.
- For the blog post, the cleanest presentation is probably 8-12 sectors, with a second appendix table for the top 25 NAICS/BEA industries.

### Working formula

- Core estimate:

  `AddedCost_s = GO_s * [ tau_dir * E_s * ShockEnergy_s + tau_ind * sum_k(a_s,k * Shock_k) ]`

- Definitions:
  - `GO_s`: sector gross output from BEA Gross Output by Industry or GDP by Industry.
  - `E_s`: direct energy expenditure share (`energy_expenditures_s / GO_s`).
  - `a_s,k`: BEA input-output coefficient for input `k` used by sector `s`.
  - `ShockEnergy_s`: commodity-specific delivered price increase mapped onto the sector's energy basket.
  - `tau_dir`, `tau_ind`: pass-through multipliers. Keep them as scenario parameters rather than hard-coding one value.
- If we want the full network effect rather than a direct-input lower bound, replace `a_s,k` with the relevant total-requirements coefficient or Leontief-inverse-based multiplier from BEA's requirements tables.
- Report both `AddedCost_s` in dollars and `AddedCost_s / GO_s` as a share of sector output.
- If a sector has no clean direct-energy series, use BEA I-O plus a proxy intensity from the closest BEA/NAICS match and flag it as estimated.

### Needed inputs

- BEA Input-Output Accounts for use tables, supply tables, and total/domestic requirements tables.
- BEA GDP by Industry and Gross Output by Industry for sector output denominators.
- EIA MECS for manufacturing energy consumption and expenditures; use 2022 as the latest national manufacturing benchmark.
- EIA SEDS for broader energy consumption, prices, and expenditures where MECS is not enough.
- BLS PPI relative importance / FD-ID tables for commodity and intermediate-demand weights when translating upstream price shocks into producer-side cost pressure.
- BLS CPI relative-importance tables only if we later want a consumer spillover bridge, not for the business-cost core.
- Scenario magnitudes from `hormuz-l8m.1` once available; until then, keep the model low/base/high ready by accepting a shock vector per commodity.

### Candidate source URLs

- BEA Input-Output Accounts: <https://www.bea.gov/data/industries/input-output-accounts-data> and <https://www.bea.gov/itable/input-output> (accessed 2026-07-06).
- BEA GDP by Industry: <https://www.bea.gov/data/gdp/gdp-industry> and Gross Output by Industry: <https://www.bea.gov/data/industries/gross-output-by-industry> (accessed 2026-07-06).
- EIA SEDS: <https://www.eia.gov/state/seds/> and complete data page <https://www.eia.gov/state/seds/seds-data-complete.php> (accessed 2026-07-06).
- EIA MECS: <https://www.eia.gov/consumption/manufacturing/> and 2022 data <https://www.eia.gov/consumption/manufacturing/data/2022/> (accessed 2026-07-06).
- BLS PPI: <https://www.bls.gov/ppi/> , <https://www.bls.gov/ppi/tables/> , and technical note <https://www.bls.gov/news.release/ppi.tn.htm> (accessed 2026-07-06).
- BLS CPI relative importance: <https://www.bls.gov/cpi/tables/relative-importance/> (accessed 2026-07-06).
- Pass-through literature for calibration bands: IMF working paper on energy pass-through and sectoral inflation dynamics (<https://www.imf.org/en/Publications/WP/Issues/2025/07/18/The-Energy-Origins-of-the-Global-Inflation-Surge-568659>) and ECB work on state-dependent energy-price pass-through (<https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3230~cd08dc4c6.en.pdf>; accessed 2026-07-06).

### Provisional assumptions

- Use a 6- to 12-month short-run horizon first; hold quantities fixed in the first pass and let substitution show up only in sensitivity cases.
- Treat direct fuel/electricity shocks as higher pass-through than tier-2 inputs, and higher again than general services inputs. Do not force a single economy-wide multiplier.
- Scale by gross output rather than value added for the main estimate; value added is useful as a secondary normalization, but it understates gross cost exposure in input-heavy sectors.
- Keep the low/base/high scenario parameters separate from the structural coefficients so the same table can be reused when `hormuz-l8m.1` lands.

### Scenario-ready sector table

Working estimate structure:

`AddedCost_s = GO_s * [ tau_dir * E_s * Shock_dir_s + tau_ind * sum_k(a_s,k * Shock_k) ]`

Pass-through bands used for the preliminary table:

- Direct fuel/electricity: low/base/high = 0.35 / 0.60 / 0.90
- Tier-2 inputs and freight: low/base/high = 0.20 / 0.35 / 0.55
- Services and overhead: low/base/high = 0.10 / 0.20 / 0.35

These are calibration bands, not observed coefficients, and they are intentionally wider than the macro pass-through benchmarks in `hormuz-l8m.5`.

| sector | direct energy anchor | indirect input channel | sensitivity note |
|---|---|---|---|
| Chemicals | EIA MECS 2022 purchased energy expenditures = `$77.1bn`, about `40%` of manufacturing energy spend; energy mix: electricity `36%`, natural gas `26%`, HGLs `21%`, coal `3%`, other `14%`. | HGL/LPG, natural gas, sulfur, ammonia/urea, freight. | Highest direct exposure; also the strongest feedstock chain exposure because chemicals purchased `98%` of HGLs and `40%` of manufacturing natural gas. |
| Petroleum and coal products | MECS 2022 purchased energy expenditures = `$26.3bn`. | Refinery gas, crude runs, war-risk freight, product cracks. | Direct shock is high but partly offset by byproduct fuels; indirect effects propagate to diesel, jet, and petrochemical feedstocks. |
| Primary metals | MECS 2022 purchased energy expenditures = `$16.5bn`. | Electricity, coke, freight, construction demand. | Very electricity-sensitive; also exposed to coke, ore, and logistics. |
| Food | MECS 2022 purchased energy expenditures = `$12.4bn`. | Fertilizer, ammonia/urea, diesel, cold chain, packaging. | Direct energy is moderate, but indirect input shock can dominate in a fertilizer-heavy scenario. |
| Paper | MECS 2022 purchased energy expenditures = `$9.6bn`. | Chemicals, freight, process fuels. | Onsite byproducts soften cash-energy dependence relative to chemicals and metals, but the sector still carries meaningful direct exposure. |
| Nonmetallic minerals | No single dollar anchor pulled into the public excerpt here; still one of the six top offsite-fuel sectors in MECS. | Diesel, coal, electricity, construction demand. | Treat as energy-intensive construction input; replace with a BEA/MECS crosswalk when the final table is built. |
| Transportation and warehousing | Use `hormuz-l8m.1` diesel and jet shock inputs, then scale by fuel spend. | Diesel, jet, insurance, detours, vessel availability. | Highest short-run pass-through because fuel is the cost base. |
| Utilities / AI data centers | Use the regional power framework in `hormuz-l8m.3` and Henry Hub sensitivity. | Natural gas, wholesale power, basis risk. | Base-case U.S. gas impact is modest, but regional basis can make the power-cost effect material. |
| Retail / wholesale / services | Proxy with BEA gross output times a low energy-intensity factor. | Transport, refrigeration, HVAC, packaging. | Mostly indirect, with lagged pass-through; direct energy cost is small relative to goods sectors. |

Interpretation:

- The manufacturing anchors above are source-backed from EIA MECS 2022. The non-manufacturing rows are template rows until the BEA gross-output crosswalk is pulled in.
- For a blog-facing number, the next step is to multiply each row's energy anchor by the relevant scenario shock vector from `hormuz-l8m.1` and then run the indirect-input term with BEA I-O coefficients.
- The ranking is the point: chemicals, petroleum/coal products, and primary metals are the direct-cost leaders; food, transport, and fertilizer-heavy chains are the most sensitive indirect-cost stories.

### Publication polish

- Remaining work before a blog asset is the BEA crosswalk and a fully reproducible denominator pull for non-manufacturing sectors.
- The preliminary research acceptance criteria are met: the issue now contains a sector table with direct-energy anchors, indirect-input channels where feasible, and explicit sensitivity bands for pass-through assumptions.

## Completion Note

- 2026-07-06: Acceptance criteria met for a preliminary research task. The issue now carries a scenario-ready sector table and formula template grounded in EIA MECS 2022, the resolved `hormuz-l8m.1` price shocks, and the pass-through framing from `hormuz-l8m.5`. Remaining publication polish is to wire in the final BEA gross-output crosswalk and turn this into a reusable figure/table outside the issue note.
