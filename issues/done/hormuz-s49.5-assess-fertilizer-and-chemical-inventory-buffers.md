---
id: "hormuz-s49.5"
title: "Assess fertilizer and chemical inventory buffers"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-s49"
labels:
  - "energy-security"
  - "fertilizer"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:55Z"
updated_at: "2026-07-06T10:05:00Z"
---

# Assess fertilizer and chemical inventory buffers

## Description

Investigate whether fertilizer, ammonia, urea, sulfur, and petrochemical inventories can cushion supply disruptions and for how long.

## Acceptance Criteria

Findings include whether data are strong enough for quantitative claims or only qualitative treatment.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Unblocked: `hormuz-fyp.5` - Create Hormuz commodity taxonomy
- Unblocked: `hormuz-kmz.4` - Investigate non-obvious disrupted products
- Unblocked: `hormuz-s49.1` - Inventory reserve and stockpile data sources
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Started preliminary research despite formal dependencies on `hormuz-fyp.5`, `hormuz-kmz.4`, and `hormuz-s49.1`. Dedicated subagent assigned to determine whether fertilizer/chemical inventory buffering can support quantitative days-of-cover claims or only qualitative treatment.
- Preliminary verdict: public evidence is strong on trade exposure and price shock, but weak on true inventories. The best-supported global claim is that fertilizer markets do not have coordinated strategic reserves, so buffer analysis mostly has to be local and approximate rather than global and exact.
- FAO Director-General statement (26 Mar 2026) says the Strait of Hormuz normally carries between 20% and 30% of globally traded fertilizers, that "no strategic reserves exist for fertilizers," and that an estimated 1.5 to 3 million tons of fertilizer trade per month has been delayed. It also notes rapid price spikes in urea in the US and Brazil. Source: https://www.fao.org/director-general/speeches/details/180th-session-of-the-council--implications-for-world-food-security-and-agriculture-arising-from-disruptions-of-supply-chains-in-the-gulf-region--including-the-closure-of-key-maritime-routes--opening-statement/en (accessed 2026-07-06).
- IFA Medium-Term Fertilizer Outlook 2026-2030 (6 May 2026) is the strongest public exposure map: the Strait of Hormuz accounts for 34% of global urea trade, 23% of ammonia trade, and 49% of sulfur trade. It also says that by end-April 2026 about 800 kt of urea on 17 ships and 400 kt of sulfur on 10 ships remained blocked west of Hormuz. This is good shock-size evidence, but it is not an inventory series. Source: https://www.fertilizer.org/wp-content/uploads/2026/05/2026_IFA_Medium_Term_Outlook_Report_English.pdf (accessed 2026-07-06).
- World Bank Commodity Markets Outlook (Apr 2026) reinforces that the market is price-sensitive and input-cost-driven rather than stock-buffered: fertilizer prices rose in 2026Q1, mostly because of urea, and the index was projected to rise by more than 30% in 2026 under ongoing Middle East disruption. Earlier World Bank fertilizer commentary says the global market was still fairly well supplied in 2025, but trade restrictions and input costs were pushing prices higher. Sources: https://thedocs.worldbank.org/en/doc/f3138644a1e8e2bb631399ae11d6c408-0050012026/original/CMO-April-2026.pdf and https://thedocs.worldbank.org/en/doc/1b388949805c9a0ae3736bdacb32ea94-0050012025/original/CMO-April-2025.pdf (accessed 2026-07-06).
- FAO Food Outlook (Nov 2025) is useful background on structural balance: global fertilizer utilization rose to 200 Mt nutrients in 2024, nitrogen use hit 115 Mt, and nutrient capacity growth was expected to run around 2% annually through 2030. That supports a capacity-and-trade-rerouting story, not a hard inventory-buffer story. Source: https://openknowledge.fao.org/server/api/core/bitstreams/11877910-a587-4202-b22d-d66e498d76b0/content (accessed 2026-07-06).
- India is the best public national-stock case study found so far. Parliamentary answers from the Ministry of Chemicals & Fertilizers provide opening stock and season-to-date sales/closing stock for urea, DAP, MOP, and NPKS. On 5 Mar 2026 the all-India closing stocks were 49.01 LMT urea, 21.61 LMT DAP, 8.00 LMT MOP, and 45.51 LMT NPKS; on 27 Nov 2025 they were 50.02, 17.36, 6.53, and 35.17 LMT; on 15 Jul 2025 Kharif closing stocks were 51.29, 13.11, 7.10, and 38.76 LMT. Sources: https://sansad.in/getFile/annex/270/AS191_na9na4.pdf?source=pqars, https://sansad.in/getFile/annex/269/AU199_V91D1h.pdf?source=pqars, and https://sansad.in/getFile/annex/268/AU179_Fqpcb7.pdf?source=pqars (accessed 2026-07-06).
- Rough days-of-cover is feasible only as a back-of-envelope for India using closing stock divided by average daily sales over the reported season. For Rabi 2025-26 as of 5 Mar 2026, that gives about 41 days for urea, 67 days for DAP, 123 days for MOP, and 113 days for NPKS. Caveat: this is only a proxy because the government data are seasonal cumulative sales, not a true daily inventory ledger, and fertilizer demand is highly seasonal.
- India's official answers also show the government leaning on allocation, iFMS monitoring, and import diversification rather than reserve drawdown. For Rabi 2025-26 the Ministry cited LTAs/MoUs for DAP/NPKS supply of 31 lakh tonnes from Saudi Arabia, 30.10 lakh tonnes from Russia, and 25 lakh tonnes from Morocco, saying those arrangements helped mitigate supply risks.
- Petrochemicals remain the weakest part of this task. I did not find a comparable open, official inventory series for petrochemical stocks that would support a credible days-of-cover estimate. For now this should stay qualitative unless a proprietary tank/terminal dataset or a country-specific inventory release turns up.
- Working conclusion: quantitative days-of-cover is defensible only for a few jurisdictions with public stock/sales data, especially India. For the broader Gulf/Hormuz shock, the rigorous treatment is likely qualitative with one or two country case studies translated into approximate cover bands rather than a claimed global inventory metric.
- 2026-07-06: Table-ready assessment, organized by product group.

| Product/group | Days-of-cover support? | Public source that exists | Likely blog treatment | Key exposure / disruption figures | Confidence |
| --- | --- | --- | --- | --- | --- |
| Urea | Yes, but only as a country-specific seasonal proxy; no public global daily stock ledger found. | India parliamentary opening/closing stock answers; USDA AgTransport Fertilizer Dashboard has public U.S. annual nutrient inventory/disappearance and commodity-level fertilizer price indicators. | Quantitative India case study plus global qualitative framing. | IFA says 34% of global urea trade moves via Hormuz; end-April AIS implied 800 kt on 17 ships remained blocked west of Hormuz; IFA says only 2 urea vessels carrying about 85 kt exited between late Feb and end-Apr. | High on exposure, medium on buffer math. |
| Ammonia | Partial at best; U.S. public data exist only at aggregate nitrogen-nutrient level, not a clean ammonia stock ledger. | USDA AgTransport annual nitrogen inventory/disappearance; no comparable public ammonia inventory series found for Hormuz-exposed exporters/importers. | Mostly qualitative mechanism story, with any quantitative case limited to a jurisdiction-specific proxy. | IFA says 23% of global ammonia trade moves via Hormuz; end-April AIS implied 60 kt on 3 ships blocked west of Hormuz; World Bank says Iran halted ammonia production, Qatar suspended ammonia output, and India cut ammonia output because of lower LNG supplies. | Medium on exposure, low on buffer. |
| Sulfur | No reliable public inventory series found for a credible days-of-cover claim. | Exposure and blocked-shipment evidence are public; true stock data are not. | Qualitative only, unless a proprietary terminal/tank dataset appears. | IFA says about 49% of global seaborne sulfur trade moves via Hormuz; about 400 kt on 10 ships remained blocked west of Hormuz at end-April; only 4 sulfur vessels carrying about 200 kt exited between late Feb and end-Apr. | High on exposure, low on buffer. |
| DAP / phosphates | Yes, but mainly for India; U.S. public phosphorus-nutrient inventory/disappearance exists as a secondary reference point. | India parliamentary opening/closing stock answers for DAP; USDA AgTransport dashboard for U.S. phosphorus nutrient inventory/disappearance. | Quantitative India case study plus global qualitative framing. | IFA says 18% of global MAP+DAP trade moves via Hormuz; end-April AIS implied 150 kt of phosphate fertilizers on 3 ships blocked west of Hormuz; India closing stock was 21.61 LMT on 5 Mar 2026 and 13.11 LMT on 15 Jul 2025; DAP imports from China fell from 22.28 LMT in 2023-24 to 8.47 LMT in 2024-25. | Medium-high on exposure, medium on buffer. |
| MOP / potash | Yes, but it looks like a control case rather than a Hormuz-sensitive buffer story. | India parliamentary stock answers for MOP; USDA AgTransport dashboard for U.S. potash inventory/disappearance. | Brief comparative/control row, not a main quantitative claim. | World Bank says MOP prices rose more than 5% in 2026Q1 and were nearly 17% higher y/y, but the market is becoming better supplied and is less exposed to Middle East disruptions; India closing stock was 8.00 LMT on 5 Mar 2026 and 7.10 LMT on 15 Jul 2025. | Medium on inventory data, medium-low on Hormuz relevance. |
| Petrochemicals | No public inventory series found. | Public sources cover feedstock exposure and price effects, not inventories. | Qualitative only unless a proprietary stock dataset becomes available. | IEA says the steepest losses have occurred in the petrochemical sector because feedstock availability is constrained; it also says 30% of all LPG exported by sea transited Hormuz in 2025, and the Strait carries over 110 bcm of LNG with no alternative routes. World Bank says the crisis affects petrochemicals, chemicals, and heavy manufacturing. | Low. |

Source breadcrumbs, all accessed 2026-07-06:

- IFA Medium-Term Fertilizer Outlook 2026-2030: https://www.fertilizer.org/wp-content/uploads/2026/05/2026_IFA_Medium_Term_Outlook_Report_English.pdf
- USDA AMS announcement for the Fertilizer Transportation Dashboard: https://www.ams.usda.gov/content/usda-announces-availability-new-agricultural-transportation-data
- USDA AgTransport Fertilizer Transportation Dashboard: https://agtransport.usda.gov/stories/s/Fertilizer-Transportation-Dashboard/dtqv-e4ux/
- India Rajya Sabha response, 10 Mar 2026: https://sansad.in/getFile/annex/270/AS191_na9na4.pdf?source=pqars
- India Rajya Sabha response, 15 Jul 2025: https://sansad.in/getFile/annex/268/AU179_Fqpcb7.pdf?source=pqars
- World Bank fertilizer market blog: https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten-
- IEA Middle East and Global Energy Markets topic page: https://www.iea.org/topics/the-middle-east-and-global-energy-markets
- IEA petrochemicals/LPG podcast page: https://www.iea.org/podcasts/everything-energy/how-petrochemicals-are-reshaping-oil-markets
- World Bank policy brief on the global shock: https://documents1.worldbank.org/curated/en/099137106232625656/pdf/IDU-204de921-282f-4016-a1e5-2bb9d9d9f4ad.pdf

- 2026-07-06: Marked done after blocker review. `hormuz-fyp.5` and `hormuz-kmz.4` are done, and this issue's acceptance criterion is met: the notes and `data/derived/hormuz_s49_5_fertilizer_chemical_buffer_table.csv` state where data support quantitative claims versus qualitative treatment. The universal country/product buffer table belongs to downstream `hormuz-s49.6`, not this issue.
