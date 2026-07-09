---
id: "hormuz-ccx.8"
title: "Build global accounting of lost supply, new supply, inventories, and demand destruction"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-ccx"
labels:
  - "balances"
  - "global"
  - "synthesis"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "codex"
created_at: "2026-07-06T00:00:00Z"
updated_at: "2026-07-07T00:45:00Z"
---

# Build global accounting of lost supply, new supply, inventories, and demand destruction

## Description

Estimate how the gross Hormuz energy shock clears globally: genuinely new supply, inventory draw, demand destruction, delayed cargoes, and displaced consumption by third countries. The key blog question is whether rich/directly exposed countries were cushioned by new supply or by outbidding poorer indirect consumers.

## Acceptance Criteria

- Start with oil, LNG, and LPG before attempting fertilizers or metals.
- Reconcile gross supply loss against observed or modeled inventory draw, demand reduction, new non-Hormuz output, and redirected cargoes.
- Explicitly identify double-counting risks between importer adjustment rows.
- Produce a concise global-balance table and a blog-ready caveat paragraph.

## Work Notes

- 2026-07-06: Filed from follow-up synthesis. Current repo tables are importer scenario allocations and should not be summed into a de-duplicated world balance without additional reconciliation.
- 2026-07-07: Claimed. Scope is a first-pass global accounting frame for oil, LNG, and LPG using existing KMZ/F6R/S49 outputs, not a new cargo-level reconstruction.
- 2026-07-07: Built `scripts/build_ccx_global_energy_accounting.py`, which reads `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv` and `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, then writes `data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv` and `docs/hormuz-global-energy-shock-accounting.md`.
- 2026-07-07: Registered the new derived CSV in `data/manifest.csv`.

### Final Outputs

| Output | Path | Status |
|---|---|---|
| Global energy shock accounting table | `data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv` | complete |
| Short synthesis doc | `docs/hormuz-global-energy-shock-accounting.md` | complete |
| Builder script | `scripts/build_ccx_global_energy_accounting.py` | complete |
| Manifest row | `data/manifest.csv` | complete |

### Key Assumptions

- The table starts with oil/petroleum liquids, LNG, and LPG/NGL feedstocks only. Fertilizers, sulfur, petrochemicals, and metals remain outside this accounting pass because their units and supply-chain overlaps need separate de-duplication.
- Oil uses the KMZ modeled gross loss of 15.06 mb/d against a 20.26 mb/d 2024 EIA/Vortexa baseline, with IEA's 2025 19.87 mb/d total as a consistency check. The oil row deliberately does not claim that the 5.15 mb/d replacement-supply bridge is new production; it is mostly replacement/redirection and may represent another buyer's displaced consumption.
- LNG uses the KMZ 0.30 bcm/d base loss and F6R Asia aggregate adjustment bridge. This is the cleanest physical loss because Qatar/UAE LNG has no practical seaborne bypass.
- LPG uses the KMZ 1.2 mb/d base loss and the India-visible LPG/NGL F6R row only. The remaining 0.78 mb/d base residual is unallocated by public global evidence, not assumed to vanish.

### Double-Counting Notes

- Do not add the F6R importer rows as if they are independent world totals. They are scenario bridges for major importers.
- Oil replacement supply, global stock draw, and country inventory draw overlap. A barrel counted as an importer replacement may be a redirected cargo from another buyer; a country inventory draw can also be part of the global stock-draw check.
- LPG overlaps with petroleum liquids/product aggregates and petrochemical feedstock rows. LNG country rows overlap with the Asia aggregate row.

### Source Breadcrumbs

- EIA Hormuz oil/Vortexa route data: https://www.eia.gov/todayinenergy/detail.php?id=65504
- EIA Hormuz LNG/Vortexa route data: https://www.eia.gov/todayinenergy/detail.php?id=65584
- IEA Strait of Hormuz factsheet: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- IEA Middle East and global energy markets: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- Local inputs: `data/derived/hormuz_kmz_3_preliminary_disruption_scenarios.csv`, `data/derived/hormuz_f6r_5_replacement_demand_response.csv`, `data/derived/hormuz_s49_6_stockpile_buffer_duration.csv`, `docs/hormuz-energy-shock-followups.md`, `docs/hormuz-importer-adjustment.md`, and `docs/hormuz-stockpile-buffers.md`.

### Validation

- 2026-07-07: Ran `.venv/bin/python scripts/build_ccx_global_energy_accounting.py`; generated 3 product rows.
- 2026-07-07: Ran a repo-local Python validation that parsed `data/derived/hormuz_ccx_8_global_energy_shock_accounting.csv` and `data/manifest.csv`, checked required fields, confirmed oil/LNG/LPG coverage, and confirmed the manifest row. Validation passed.

### Completion Note

- Acceptance criteria met for the current public-source stage. The deliverable is a defensible accounting frame with explicit confidence and double-counting warnings, not a closed cargo-level global balance.
