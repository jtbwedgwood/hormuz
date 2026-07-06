---
id: "hormuz-f6r.1"
title: "Build importer exposure matrix"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "importers"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-f6r.2"
  - "hormuz-f6r.3"
  - "hormuz-f6r.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:42Z"
updated_at: "2026-07-06T18:25:00Z"
---

# Build importer exposure matrix

## Description

For each major Hormuz-linked product, identify top destination countries and regions before the disruption and their dependence on affected flows.

## Acceptance Criteria

Matrix includes product, exporter, importer, volume/value, share of importer demand, baseline period, and source confidence.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Cleared dependency: `hormuz-fyp.1` - Define citation and source-quality rubric
- Cleared dependency: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Cleared dependency: `hormuz-kmz.1` - Estimate normal Hormuz export flows by country and product
- Blocks: `hormuz-f6r.2` - Analyze China exposure and substitution behavior
- Blocks: `hormuz-f6r.3` - Analyze Japan, Korea, India, and Southeast Asia adjustment
- Blocks: `hormuz-f6r.4` - Assess Europe and Mediterranean exposure

## Work Notes

- 2026-07-06: Claimed for exposure-matrix build using completed KMZ product-flow tables, public IEA/EIA anchors, and region/country trade-source notes. Output target: `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv`.
- 2026-07-06: Built `data/derived/hormuz_f6r_1_importer_exposure_matrix.csv` as a table-ready public-source exposure matrix with the requested columns: `product`, `exporter_or_origin_region`, `importer_or_region`, `baseline_period`, `baseline_volume`, `unit`, `importer_demand_or_import_share`, `direct_exposure_category`, `substitution_notes`, `confidence`, `source_urls`, and `caveats`. I added `row_id` for stable references.
- 2026-07-06: Method notes:
  - Oil/crude destination rows use EIA/Vortexa public figure data from `fig3.xlsx` for 2024 destination volumes. These are route/destination estimates, not importer customs records. They are the highest-confidence numeric importer rows.
  - LNG rows use IEA's 2025 public Hormuz LNG anchors: over 110 bcm through Hormuz, almost 90% to Asia, just over 10% to Europe, and more than one-quarter of Asia LNG imports. I encoded regional volumes as approximate shares of 110 bcm/year rather than false country precision.
  - LPG rows use IEA's public LPG commentary: 30% of seaborne LPG exports transited Hormuz in 2025; Hormuz LPG exports fell from about 1.5 mb/d to 0.3 mb/d in March 2026; almost all Middle East LPG exports went to Asia; India consumed LPG with around two-thirds transiting Hormuz and lost about 430 kb/d of imports early in the conflict.
  - Fertilizer rows use IFASTAT public shares for upstream Hormuz countries in global trade: ammonia 23%, urea 34%, sulfur 49%, MAP/DAP 18%. Exporter baseline volumes are drawn from `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv` where the repo already has country-product rows. These are not bilateral importer volumes.
  - Sulfur importer rows use IEA/IFA for global Hormuz exposure and NDSU Agricultural Trade Monitor as a clearly secondary but useful importer-specific source for China, Morocco, and Indonesia. These rows should be tightened with customs data before final publication.
  - Aluminium uses IEA's public statement that about 5 Mt/year of aluminium is shipped through Hormuz and the Gulf is about 8% of global supply; importer split remains global/industrial rather than bilateral.
- 2026-07-06: Sources accessed 2026-07-06:
  - EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint" and linked figure data: `https://www.eia.gov/todayinenergy/detail.php?id=65504`, `https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx`.
  - EIA, "China's crude oil imports decreased from a record as refinery activity slowed": `https://www.eia.gov/todayinenergy/detail.php?id=64544`.
  - IEA, "The Middle East and Global Energy Markets": `https://www.iea.org/topics/the-middle-east-and-global-energy-markets`.
  - IEA, "Energy crisis threatens world's most vulnerable as cooking fuel shortages grow": `https://www.iea.org/commentaries/energy-crisis-threatens-world-s-most-vulnerable-as-cooking-fuel-shortages-grow`.
  - IFASTAT homepage / Strait of Hormuz disruption spotlight: `https://ifastat.org/`.
  - PPAC Government of India import/export page, used as primary breadcrumb for later India harmonization: `https://ppac.gov.in/import-export`.
  - Japan Agency for Natural Resources and Energy, "10 questions for understanding the current energy situation": `https://www.enecho.meti.go.jp/en/category/brochures/pdf/japan_energy_2023.pdf`.
  - NDSU Agricultural Trade Monitor, "Strait of Hormuz Closure and Global Fertilizer Trade Disruptions" PDF via AgEcon Search: `https://ageconsearch.umn.edu/record/396250/files/NDSU%20Agricultural%20Trade%20Monitor%202026-03%20%281%29.pdf`.
  - CSIS, "The Impact of the Iran Conflict on South Korea: By the Numbers": `https://www.csis.org/analysis/impact-iran-conflict-south-korea-numbers`.
  - IFPRI, "How fertilizer policies could exacerbate Hormuz price shocks": `https://www.ifpri.org/blog/how-fertilizer-policies-could-exacerbate-hormuz-price-shocks/`.
  - Existing repo inputs: `data/derived/hormuz_kmz_3_country_product_disruption_estimates.csv`, `data/derived/hormuz_kmz_7_product_disruption_master_table_prelim.csv`, `docs/hormuz-product-disruptions.md`, and `data/manifest.csv`.
- 2026-07-06: Acceptance criteria met for the public-source stage. The matrix includes product, exporter/origin, importer/region, volume or explicit `not_available`, demand/import-share or route-share notes, baseline period, and source confidence. Remaining limitations are captured in `caveats`; they are refinement targets for `hormuz-f6r.2`, `hormuz-f6r.3`, and `hormuz-f6r.4`, not blockers for this task.
