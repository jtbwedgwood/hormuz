# Country GDP impact under two Hormuz scenarios

The producer and consumer numbers below answer different questions and should not be compared as though they came from one model. Producer entries are **real GDP level declines against a no-shut-in 2026 counterfactual**. Consumer entries are **real GDP growth rates and growth revisions** from ADB, with a narrow price-path re-timing. Neither is a central estimate.

## Scenarios

- **A: full reopening on 30 September 2026.** Each country's July crude shut-in rate is held through September, then declines linearly. The headline uses a three-month restart (October factor 5/6, November 1/2, December 1/6); one- and six-month ramps form the range.
- **B: no reopening during 2026.** Each country's July crude shut-in rate is held from August through December. This represents continued managed partial closure, not a return to the March-May trough.

The exact monthly factors are in `data/derived/hormuz_k4w_scenarios.csv`. Reopening is not a production switch: wells, export chains, insurance and tanker positioning recover with lags. This is consistent with EIA's August baseline, which assumes flows improve slowly from September and most production returns only in early 2027 ([EIA August STEO, Table 1 and pp. 5-6](https://www.eia.gov/outlooks/steo/archives/aug26.pdf)).

## Gulf producers: direct hydrocarbon calculation

| Producer | Annual crude-output loss, A base | Real hydrocarbon VA share | Direct real GDP level decline, A base (1-6 month range) | Direct real GDP level decline, B |
|---|---:|---:|---:|---:|
| Saudi Arabia | 15.5% | 27.3% | -4.2 pp (-4.6 to -3.8) | -4.9 pp |
| Iraq | 36.9% | 52.7% | -19.4 pp (-20.8 to -17.6) | -22.2 pp |
| Kuwait | 31.8% | 47.9% | -15.2 pp (-16.4 to -13.8) | -17.5 pp |
| United Arab Emirates | 10.2% | 24.5% | -2.5 pp (-2.5 to -2.5) | -2.5 pp |
| Qatar | 50.3% | 35.5% | -17.9 pp (-19.3 to -16.0) | -20.7 pp |
| Bahrain | 47.5% | 14.7% | -7.0 pp (-7.6 to -6.2) | -8.2 pp |
| Iran | 3.3% | 12.6% | -0.4 pp (-0.4 to -0.4) | -0.5 pp |

Method: calendar-weighted annual crude-output loss equals modeled 2026 shut-in barrels divided by February output times 365; the GDP proxy multiplies that loss by the real hydrocarbon value-added share. EIA's displayed country rows sum to 1,207.9 million shut-in barrels in March-July, while its published total is 1,318.3 million. The unexplained 110.4 million-barrel gap is preserved and not allocated to countries.

The national-accounts inputs are: Saudi GASTAT's implied real oil-activity weight ([2024 annual accounts](https://www.stats.gov.sa/documents/20117/2435267/Annual_National_Accounts_Publication_2024_EN.pdf_fixed_8631783/770f9e7b-444a-5d5e-5b75-f6825f2668d0)); Iraq's 52.7% constant-price oil-sector share ([Central Bank of Iraq annual report](https://cbi.iq/static/uploads/up/file-177269103623349.pdf)); [Kuwait CSB constant-price accounts](https://www.csb.gov.kw/Pages/Statistics_en?ID=80&ParentCatID=3); the UAE's 24.5% constant-price oil-and-gas share ([FCSC Unified Numbers](https://fcsc.gov.ae/wp-content/uploads/2025/12/UAE-Unified-Numbers-En.pdf)); Qatar's QAR256.737 billion mining value added over QAR723.553 billion GDP at constant 2018 prices ([National Planning Council](https://www.npc.qa/en/statistics/Statistical%20Releases/Economic/National%20Accounts/GDP/Qatar%20Annual%20Gross%20Domestic%20Product%20by%20Economic%20Activity%20En%20V5.pdf)); Bahrain's constant-price oil GDP ([Bahrain Open Data Portal](https://www.data.gov.bh/explore/dataset/02-annually-general-economic-indicators-by-constant-prices/table/)); and an implied Iranian real-oil weight from the IMF regional appendix ([May 2025](https://www.imf.org/-/media/Files/Publications/REO/MCD-CCA/2025/May/English/regional-economic-outlook-middle-east-central-asia-may-2025-statistical-appendix.ashx)). Iran is low-confidence because production, exports and national accounts are unusually uncertain.

“Floor” needs two qualifications. First, it excludes tourism and aviation, trade and logistics, domestic energy-infrastructure outages, war-risk insurance and freight, construction and FDI, and the fiscal multiplier from lost government revenue. Sovereign-wealth drawdowns can offset some fiscal contraction. Second, the available UAE and Qatar real shares combine oil and gas while the monthly shut-in series covers crude only. With no defensible monthly realized LNG shut-in series, those two entries are **mechanical mixed-sector proxies, not clean lower bounds**; applying crude losses to gas value added can overstate the oil-only channel even while omitted LNG losses work in the other direction.

## Asian consumers: audited forecast and narrow re-timing

| Economy | ADB July 2026 real growth | Revision from ADB April | Re-timed A base (1-6 month range) | Re-timed B |
|---|---:|---:|---:|---:|
| China | 4.6% | 0.0 pp | 4.60% (4.59%-4.61%) | 4.58% |
| India | 6.6% | -0.3 pp | 6.59% (6.56%-6.62%) | 6.53% |
| Indonesia | 5.2% | 0.0 pp | 5.19% (5.17%-5.22%) | 5.15% |
| Thailand | 1.8% | 0.0 pp | 1.79% (1.77%-1.82%) | 1.75% |
| Vietnam | 7.2% | 0.0 pp | 7.19% (7.17%-7.22%) | 7.15% |
| Philippines | 3.8% | -0.6 pp | 3.79% (3.77%-3.82%) | 3.75% |
| Malaysia | 4.6% | 0.0 pp | 4.59% (4.57%-4.62%) | 4.55% |
| Singapore | 3.2% | +0.2 pp | 3.19% (3.15%-3.23%) | 3.12% |
| Japan | 0.7% | 0.0 pp | 0.69% (0.66%-0.73%) | 0.62% |
| South Korea | 2.6% | +0.7 pp | 2.59% (2.56%-2.63%) | 2.52% |

These are real growth rates, not contractions. India is fiscal-year 2026; the rest are calendar-year. China, India, Thailand, the Philippines, Japan and Korea are straightforward oil-importer cases. Indonesia is a net oil importer but exports LNG and coal; Malaysia is a net oil user on a production-consumption basis but a major LNG exporter. Their broader energy terms of trade are therefore mixed. Singapore is a crude-importing refining and product-export hub, not an upstream windfall economy; Viet Nam also combines domestic crude production and trade with net petroleum-import dependence. Country classifications and source links are retained in the audit CSV rather than forcing all ten into a binary label.

[ADB's 8 July outlook](https://www.adb.org/sites/default/files/publication/1155601/asian-development-outlook-july-2026.pdf) already incorporates the war, assumes only partial normalization and uses $87 average Brent in 2026. Our transparent price bridge—observed monthly Brent through July, the 1-11 August mean held for August, then the scenario premium over the prewar mean—produces $87.58 in A base and $90.18 in B. That explains why price-only re-timing is small: most of the 2026 price shock is already realized and already in ADB's forecast.

ADB does not publish country oil-price elasticities. To avoid inventing them, the table uses current regional **bundled scenario slopes**, not structural elasticities: [ADB's April early-stabilization case](https://www.adb.org/sites/default/files/publication/1135881/ado-april-2026.pdf) used $72 Brent, while [ADB Brief 388](https://www.adb.org/sites/default/files/publication/1142926/adb-brief-388-middle-east-conflict-updated-analysis.pdf) used $96 plus higher gas, fertilizer, supply-chain and financial stress. The associated 2026 growth changes imply -0.06 pp per 10% for developing East Asia, -0.18 for South Asia, -0.15 for developing Southeast Asia and -0.21 for advanced Asia. Treat the re-timing as sensitivity arithmetic around ADB—not a new forecast and not an oil-only causal estimate.

Most importantly, price models miss physical rationing. The repo already measures March-July oil-demand revisions of 136.4 million barrels in China, 64.9 in India, 22.0 in Japan and a bounded 30.6 in Korea, plus 92.2 for other Asia/Oceania excluding Korea. China suffered refinery and petrochemical run cuts; India faced LPG and industrial-feedstock allocation; Japan and Korea curtailed refining and naphtha-linked activity; Thailand and the Philippines cut travel or working patterns, with reported livelihood loss among some Philippine fishers. Subsidies, price caps, stock releases and export controls suppress observed retail-price pass-through while shifting costs to budgets or physical availability. ADB itself warns that interrupted imports can produce materially larger short-run effects than its price-centered simulations. The small re-timed numbers therefore do **not** reconcile away the large observed volume adjustment; they demonstrate the model's blind spot.
