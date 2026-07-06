---
id: "hormuz-kmz.1"
title: "Estimate normal Hormuz export flows by country and product"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-kmz"
labels:
  - "commodities"
  - "energy"
  - "exports"
  - "supply"
blocked_by:
  - "hormuz-fyp.1"
  - "hormuz-fyp.5"
blocks:
  - "hormuz-f6r.1"
  - "hormuz-kmz.3"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:32Z"
updated_at: "2026-07-06T06:51:34Z"
---

# Estimate normal Hormuz export flows by country and product

## Description

Quantify baseline exports through Hormuz by exporter and product, separating crude, condensate, refined products, LNG, LPG, fertilizer, petrochemicals, and other material categories.

## Acceptance Criteria

Baseline table includes units, dates, source citations, confidence, and whether volumes physically require Hormuz.

## Dependency Notes

- Parent: `hormuz-kmz` - RQ2: Quantify products and supply disrupted
- Blocked by: `hormuz-fyp.1` - Define citation and source-quality rubric
- Blocked by: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Blocks: `hormuz-f6r.1` - Build importer exposure matrix
- Blocks: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted

## Work Notes

- Add research notes, source links, decisions, and open questions here as work progresses.

### Candidate baseline table

Working rule: use the most recent route-specific annual average where available. For oil, the cleanest source is EIA/Vortexa Hormuz flow data; for fertilizers, sulfur, aluminum, and plastics, use trade-data or national/company proxies and treat them as approximate through-Hormuz baselines, not exact tanker-flow series.

| product | exporter/country | baseline volume | unit | period | physically_requires_hormuz | source | confidence | notes |
|---|---:|---:|---|---|---|---|---|---|
| crude oil + condensate + petroleum products | all exporters | 20.26 | million b/d | 2024 annual avg | yes | EIA fig1.xlsx (`https://www.eia.gov/todayinenergy/images/2025.06.16/fig1.xlsx`) | high | Anchor total for all Hormuz oil traffic. 1Q25 was 20.10 mb/d, so the 2025 run-rate stayed close to 2024. |
| crude oil + condensate | Saudi Arabia | 5.48 | million b/d | 2024 annual avg | yes | EIA Hormuz article (`https://www.eia.gov/todayinenergy/detail.php?id=65504`) | high | Route-specific Hormuz crude flow; Saudi remains the biggest single origin. |
| crude oil + condensate | Iraq | 3.2 | million b/d | 2024 annual avg | yes | EIA Iraq CAB (`https://www.eia.gov/international/analysis/country/irq`) | high | EIA says Iraq's total seaborne crude exports averaged more than 3.2 mb/d in 2024; southern exports are Hormuz-linked. |
| crude oil + condensate | UAE | 1.89 | million b/d | 2024 annual avg | yes | EIA fig3.xlsx (`https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx`) | medium | Combined crude+product origin flow through Hormuz; UAE pipeline to Fujairah means this is not the UAE's total oil export volume. |
| crude oil + condensate | Kuwait | 1.33 | million b/d | 2024 annual avg | yes | EIA fig3.xlsx (`https://www.eia.gov/todayinenergy/images/2025.06.16/fig3.xlsx`) | medium | Combined crude+product origin flow through Hormuz; not a pure crude series. |
| crude oil + condensate | Qatar | 0.65 | million b/d | 2024 annual avg | yes | EIA fig3.xlsx + Qatar page (`https://www.eia.gov/international/analysis/country/QAT`) | medium | Qatar's crude/condensate exports have been around 0.7 mb/d since 2021; route is Hormuz-dependent. |
| crude oil + condensate | Iran | 1.40 | million b/d | 2024 annual avg | mostly yes | EIA fig3.xlsx + Iran CAB (`https://www.eia.gov/international/content/analysis/countries_long/Iran/pdf/Iran%20CAB%202024.pdf`) | medium | Includes sanctioned exports tracked by tanker data; Jask bypass exists but was <70 kb/d in summer 2024 and then stopped. |
| petroleum products | Qatar | 805,000 | b/d | 2024 annual avg | yes | EIA Qatar page (`https://www.eia.gov/international/analysis/country/QAT`) | high | EIA says most went to Asia; this basket includes LPG, diesel, naphtha, etc. |
| petroleum products | Iraq | 479,000 | b/d | 2024 annual avg | yes | EIA Iraq page (`https://www.eia.gov/international/analysis/country/irq`) | high | High-sulfur fuel oil is a key component. |
| petroleum products | Saudi Arabia | 1.3 | million b/d | 2023 annual avg | yes | EIA Saudi page (`https://www.eia.gov/international/analysis/country/SAU`) | medium | 2024 not isolated in the official Hormuz source; use as the latest clean Saudi product export baseline. |
| petroleum products | UAE | 1.5 | million b/d | 2023 annual avg | yes | EIA UAE CAB 2023 (`https://www.eia.gov/international/content/analysis/countries_long/United_Arab_Emirates/uae_2023.pdf`) | medium | Proxy for UAE refined-product exports; not route-isolated. |
| petroleum products | Iran | >1.0 | million b/d | 2023 annual avg | yes | EIA Iran CAB 2024 (`https://www.eia.gov/international/content/analysis/countries_long/Iran/pdf/Iran%20CAB%202024.pdf`) | medium | LPG, fuel oil, and diesel were >70% of product exports. |
| LNG | Qatar | 9.28 | Bcf/d | 2024 annual avg | yes | EIA fig2.xlsx (`https://www.eia.gov/todayinenergy/images/2025.06.24/fig2.xlsx`) | high | This is the most important non-oil Hormuz flow. 1Q25 was 10.65 Bcf/d. |
| LNG | UAE | 0.70 | Bcf/d | 2024 annual avg | yes | EIA fig2.xlsx (`https://www.eia.gov/todayinenergy/images/2025.06.24/fig2.xlsx`) | high | Nearly all UAE LNG exports transited Hormuz. 1Q25 was 0.78 Bcf/d. |
| fertilizer / urea | Saudi Arabia | 4.44 | billion kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/SAU/year/2024/tradeflow/Exports/partner/ALL/product/310210`) | high | Saudi urea exports are large and Hormuz-linked for eastern Gulf shipments. |
| fertilizer / ammonia | Saudi Arabia | 2.19 | billion kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/SAU/year/2024/tradeflow/Exports/partner/ALL/product/281410`) | high | Direct export series; major markets include India, Morocco, and Korea. |
| fertilizer / urea | Qatar (QAFCO production proxy) | 5.82 | million metric tons | 2024 | yes | QAFCO 2024 ESG Report (`https://www.qafco.qa/wp-content/uploads/2025/07/QAFCO-2024-ESG-Report.pdf`) | medium | Company production is export-oriented, but some ammonia is internally consumed for urea; use as proxy until a clean customs export series is pulled. |
| fertilizer / ammonia | Qatar (QAFCO production proxy) | 3.71 | million metric tons | 2024 | yes | QAFCO 2024 ESG Report (`https://www.qafco.qa/wp-content/uploads/2025/07/QAFCO-2024-ESG-Report.pdf`) | medium | Production proxy, not a pure export number. |
| fertilizer / urea | Bahrain | 679.1 | million kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/BHR/year/2024/tradeflow/Exports/partner/ALL/product/310210`) | high | Bahrain is small in absolute terms but relevant on the Hormuz route. |
| fertilizer / ammonia | Bahrain | 7.7 | million kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/BHR/year/2024/tradeflow/Exports/partner/ALL/product/281410`) | high | Single-market concentration to Korea, Rep. |
| sulphur | Qatar | 3.13 | billion kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/QAT/year/2024/tradeflow/Exports/partner/ALL/product/250310`) | high | Major sulfur exporter; Singapore and Switzerland are the biggest destinations. |
| sulphur | UAE | 5.1 | million metric tons | 2024 | yes | USGS UAE country note (`https://www.usgs.gov/centers/national-minerals-information-center/united-arab-emirates`) | high | USGS says UAE was the world's leading sulfur exporter in 2024. |
| sulphur | Saudi Arabia | 393.0 | million kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/SAU/year/2024/tradeflow/Exports/partner/ALL/product/250310`) | high | Smaller than Qatar/UAE but still material. |
| aluminum (unwrought, alloyed) | Bahrain | 967.6 | million kg | 2024 annual avg | yes | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/BHR/year/2024/tradeflow/Exports/partner/ALL/product/760120`) | high | Bahrain's aluminum exports are a clean Hormuz-dependent industrial flow. |
| petrochemicals / plastics proxy (polyethylene <0.94) | Saudi Arabia | 4.58 | billion kg | 2024 annual avg | partial | WITS/UN Comtrade (`https://wits.worldbank.org/trade/comtrade/en/country/SAU/year/2024/tradeflow/Exports/partner/ALL/product/390110`) | medium-low | Good proxy for Gulf petrochem intensity, but not a route-isolated Hormuz series and some Saudi petrochemicals can move via Red Sea outlets. |

### Open questions

- I still need a clean 2024/2025 route-specific series for LPG/NGLs. EIA gives baskets and country totals, but not a standalone Hormuz-linked annual export series by origin.
- Kuwait's refined-product baseline is still only cleanly visible in 2022/2023 EIA material; I have not yet pulled a 2024 annual average.
- UAE and Saudi oil/product split needs a better allocation between Hormuz and non-Hormuz routes. The bypass pipelines make this a routing problem, not just a production problem.
- Qatar fertilizers are the most valuable non-oil item, but QAFCO data are production-oriented. We should pull a customs mirror series next if we want a tighter export-only number.

### Double-counting risks

- Do not sum the `all exporters` total with the country rows; the country rows are components of the total.
- Do not add the crude/condensate origin rows to the petroleum-product rows without tracking overlaps by source and year; EIA's origin table is a combined oil basket.
- QAFCO urea and ammonia numbers are production proxies and ammonia feeds urea internally, so the two rows are not independent exports.
- WITS mirror trade data can differ from reporter data and may include confidentiality or re-export artifacts; use it as a best-available baseline, not a census.
- Oman and some UAE exports can bypass Hormuz, so they should be excluded from the "physically requires Hormuz" subtotal even when they are Gulf exports.

### Completion Note

- 2026-07-06: Acceptance criteria met for current project stage. The baseline table includes product/country, volume, unit, period, physical Hormuz dependence, source, confidence, and notes. Remaining open questions are refinement targets, not blockers for downstream analysis.
