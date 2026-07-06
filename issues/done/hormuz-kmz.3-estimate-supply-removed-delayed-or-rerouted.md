---
id: "hormuz-kmz.3"
title: "Estimate supply removed, delayed, or rerouted"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "disruption"
  - "supply"
blocked_by: []
blocks:
  - "hormuz-f6r.2"
  - "hormuz-f6r.3"
  - "hormuz-kmz.6"
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:35Z"
updated_at: "2026-07-06T07:03:00Z"
---

# Estimate supply removed, delayed, or rerouted

## Description

Combine baseline flows, ship tracker evidence, and bypass capacity to estimate how much supply is off market versus delayed, stored, or rerouted.

## Acceptance Criteria

Scenario table reports low/base/high disrupted volumes by product and country, with uncertainty and double-counting notes.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Former blocker resolved: `hormuz-2y7.3` - Map vessel classes to commodity categories
- Former blocker resolved: `hormuz-2y7.4` - Prototype daily transit count pipeline
- Former blocker resolved: `hormuz-fyp.2` - Build canonical disruption chronology
- Former blocker resolved: `hormuz-fyp.3` - Define baseline periods and scenario taxonomy
- Blocks: `hormuz-f6r.2` - Analyze China exposure and substitution behavior
- Blocks: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Blocks: `hormuz-kmz.6` - Reconcile disrupted volumes with global market balances
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Started before blockers are fully resolved. Initial tracker validation was a material blocker for observed vessel/cargo loss, but not for a preliminary scenario table based on public EIA/IEA energy-market anchors.
- 2026-07-06: Created `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv` and registered it in `data/manifest.csv`. Treat it as a modeled bridge table, not final observed disruption data.
- 2026-07-06: Integrated `hormuz-kmz.2` bypass-capacity findings. Keep EIA's 2.6 mb/d Saudi/UAE spare bypass estimate as the conservative base-case offset, but run a sensitivity using IEA's 3.5-5.5 mb/d available-capacity range. Nameplate capacity is much higher than spare capacity, and Saudi East-West utilization may already be high.
- 2026-07-06: Integrated `hormuz-kmz.1` baseline-flow findings. Updated derived table to EIA figure-data total oil flow of 20.26 mb/d in 2024 and IEA/kmz.6 crude-flow denominator of about 14.95 mb/d in 2025.
- 2026-07-06: Rechecked blockers after the 2Y7 coordination pass. `hormuz-2y7.3`, `hormuz-2y7.4`, `hormuz-2y7.5`, `hormuz-fyp.2`, `hormuz-fyp.3`, `hormuz-kmz.1`, and `hormuz-kmz.2` are now done. Remaining cargo/country uncertainty is handled as modeled uncertainty, not a blocking dependency.
- 2026-07-06: Added `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv` and registered it in `data/manifest.csv`. This is the final current-stage low/base/high country-product table.

### Preliminary Source Anchors

| Claim | Source | Confidence | Use |
|---|---|---|---|
| 2024 oil flow through Hormuz averaged 20.26 million b/d in EIA figure data, about 20% of global petroleum liquids consumption; 1Q25 was 20.10 million b/d. | EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint," 2025-06-16, https://www.eia.gov/todayinenergy/detail.php?id=65504 and linked figure data | high | Baseline oil-flow denominator. |
| Saudi crude/condensate through Hormuz was 5.5 million b/d in 2024 and 38% of total Hormuz crude flows. | Same EIA Today in Energy article. | high for cited values; medium for inferred total | Implies total Hormuz crude/condensate of about 14.5 million b/d. |
| EIA estimates about 2.6 million b/d of Saudi/UAE spare pipeline capacity could bypass Hormuz. | Same EIA Today in Energy article. | high | Conservative bypass offset for base scenario. |
| IEA estimates 3.5-5.5 million b/d of available oil-bypass capacity through Saudi/UAE operational crude pipelines; `hormuz-kmz.2` notes Saudi East-West, UAE ADCOP, and utilization constraints. | IEA, "The Middle East and Global Energy Markets," accessed 2026-07-06, https://www.iea.org/topics/the-middle-east-and-global-energy-markets; `hormuz-kmz.2` Work Notes. | medium-high | Wider bypass sensitivity. |
| EIA STEO assumes Hormuz remains effectively closed in the near term, oil shipments resume in 3Q26, and pre-conflict traffic does not return until early 2027. It reports May Middle East crude production more than 11 million b/d below pre-conflict levels. | EIA Short-Term Energy Outlook forecast overview, accessed 2026-07-06, https://www.eia.gov/outlooks/steo/ | high for EIA forecast/assumption; medium for real-time magnitude | Low-end observed/supply-loss anchor and timing frame. |
| IEA says Gulf producers exported 3.3 million b/d of refined products and 1.5 million b/d of LPG in 2025; nearly 3 million b/d of regional refining capacity has been shut. | IEA, "The Middle East and Global Energy Markets," accessed 2026-07-06, https://www.iea.org/topics/the-middle-east-and-global-energy-markets | medium-high | Product and LPG disruption frame. |
| IEA says >110 bcm LNG passed through Hormuz in 2025, representing almost one-fifth of global LNG trade; Qatar/UAE LNG has no alternative route, and supply losses have exceeded 300 mcm/d since 2026-03-01. | Same IEA topic page. | high | LNG disruption anchor. |
| IEA says observed global oil stocks have declined by 3.8 million b/d on average since war start; EIA forecasts global inventory draws of 6.3 mb/d in 2Q26 and 7.6 mb/d in 3Q26. | IEA topic page and EIA STEO forecast overview, accessed 2026-07-06. | medium | Market-balance consistency check, not product-specific loss. |

### Working Scenario Logic

| Product | Low | Base | High | Notes |
|---|---:|---:|---:|---|
| Oil and petroleum liquids | 11.0 mb/d | 15.06 mb/d | 20.26 mb/d | Low uses EIA May production reduction; base subtracts 2.6 mb/d spare bypass and a provisional 2.6 mb/d delayed/priority-flow allowance from 20.26 mb/d baseline; high is full 2024 exposure. |
| Saudi/UAE bypass offset sensitivity | 2.6 mb/d | 3.5 mb/d | 5.5 mb/d | Offset only, not disrupted supply. Low uses EIA spare-capacity estimate; base/high use IEA range. |
| Crude/condensate | 8.0 mb/d | 12.35 mb/d | 14.95 mb/d | Crude baseline uses IEA/kmz.6 2025 denominator. Base subtracts EIA spare bypass. |
| Refined products | 1.5 mb/d | 2.4 mb/d | 3.3 mb/d | IEA denominator is Gulf exports, not necessarily all Hormuz-routed. |
| LPG | 0.8 mb/d | 1.2 mb/d | 1.5 mb/d | Keep separate until LPG definition is reconciled with petroleum liquids totals. |
| LNG | 0.25 bcm/d | 0.30 bcm/d | 0.33 bcm/d | Base uses IEA reported >300 mcm/d supply loss and no-bypass constraint. |

### Open Questions

- Replace modeled disruption ranges with observed cargo/vessel evidence once `hormuz-2y7.3` and `hormuz-2y7.4` can allocate validated transits into usable product/country classes.
- Reconcile EIA's 2.6 mb/d spare bypass estimate with IEA's broader 3.5-5.5 mb/d available-capacity range once `hormuz-kmz.2` finishes.
- Confirm whether IEA's refined-products and LPG export numbers are strictly Hormuz-exposed or Gulf-wide exports with mixed route options.
- Decide whether the blog headline should use "barrels removed from production," "exports stranded," or "delivered supply delayed"; those are not interchangeable.

### Blocker Note

- 2026-07-06: `hormuz-2y7.5` is now done after a KMZ support pass validated the public PortWatch tracker against external benchmarks. That removes the aggregate-count validation blocker.
- 2026-07-06: Former blocker resolved for current project stage. Licensed cargo-flow data would improve precision, but the public-source table now satisfies the task acceptance criteria by reporting low/base/high disrupted volumes by product and country, with uncertainty and double-counting notes.

### Country/Product Estimate Method

- Use `hormuz-kmz.1` as the normal-flow baseline and `hormuz-kmz.2` as the bypass constraint layer.
- Use `hormuz-2y7.5` only as a public traffic-severity proxy: PortWatch tanker counts fell 96.0% in the acute 2026-03-01 to 2026-03-07 window and remained 78.1% below baseline by 2026-06-28. PortWatch does not reveal direction, exact cargo, country, or AIS-dark movements.
- Treat LNG as the cleanest removed-supply row because `hormuz-kmz.2` finds no practical Qatar/UAE LNG bypass and IEA reports >300 mcm/d regional LNG supply loss.
- Treat oil rows as removed/delayed/rerouted depending on bypass optionality: Saudi/UAE get lower base disruption than Iraq/Kuwait/Qatar because Saudi East-West and UAE ADCOP/Fujairah can offset part of the loss.
- Treat fertilizer, sulphur, and aluminium rows as annualized disrupted export availability, not observed daily cargo counts.

### Final Current-Stage Deliverable

| Output | Path | Status |
|---|---|---|
| Scenario bridge table | `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv` | complete |
| Country/product low-base-high table | `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv` | complete |

### Completion Note

- 2026-07-06: Acceptance criteria met for current project stage. The table reports low/base/high disrupted volumes by product and country, with classification, source basis, uncertainty, and double-counting notes. Future licensed AIS/Kpler/Vortexa cargo data should refresh the estimates, but no active local dependency remains.
