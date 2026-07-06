---
id: "hormuz-s49.2"
title: "Quantify OECD and US reserve response"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-s49"
labels:
  - "energy-security"
  - "oecd"
  - "spr"
  - "stockpiles"
blocked_by: []
blocks:
  - "hormuz-s49.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:51Z"
updated_at: "2026-07-06T09:10:00Z"
---

# Quantify OECD and US reserve response

## Description

Track SPR and commercial inventory changes for the US, IEA/OECD members, Japan, Korea, and Europe relative to baseline and policy announcements.

## Acceptance Criteria

Tables distinguish strategic releases, commercial draws, seasonal changes, and reporting lags.

## Dependency Notes

- Parent: `hormuz-s49` - RQ4: Assess strategic stockpiles and reserve releases
- Unblocked: `hormuz-s49.1` - Inventory reserve and stockpile data sources
- Blocks: `hormuz-s49.6` - Estimate stockpile buffer duration by country/product

## Work Notes

- 2026-07-06: Started preliminary research despite formal dependency on `hormuz-s49.1`. This note captures the best immediately available official evidence and a method skeleton; final quantification remains blocked until source inventory is reconciled.
- Access date for sources below: 2026-07-06.

- U.S. SPR: EIA weekly series shows the Strategic Petroleum Reserve at 415.441 million barrels on 2026-02-27 and 325.655 million barrels on 2026-06-26, a visible draw of 89.786 million barrels in the weekly stock series. EIA also reported that DOE had released 17.5 million barrels between the week ending 2026-03-20 and 2026-04-24, with SPR stocks at 397.9 million barrels on 2026-04-24. Important caveat: EIA says the U.S. release is structured as an exchange, so gross SPR withdrawals are not the same as net permanent market supply.
- U.S. commercial inventories: WPSR / Today in Energy show commercial crude oil inventories excluding SPR at 408.4 million barrels on 2026-06-26, down 3.8 million barrels w/w and about 7% below the five-year average. Keep this separate from SPR draws; it is mostly commercial/seasonal movement, not strategic release.
- IEA collective action: on 2026-03-11 IEA members agreed to make 400 million barrels available; on 2026-03-19 IEA published the country split. The table is the key decomposition source for this task: U.S. 172.2 mb all public stocks; Japan 79.8 mb total, split 54.0 public / 25.8 obligated industry stocks; Korea 22.5 mb; Europe largely refined products; Canada includes production increase. IEA explicitly says the detailed split remains subject to change.
- IEA market context: the May and June 2026 Oil Market Reports are useful for framing response and lag. June OMR says OECD government inventories fell 163 mb over Mar-May and emergency stock releases accelerated; May OMR says global observed inventories drew 129 mb in March and 117 mb in April, with OECD on-land stocks down 146 mb in April. Use these as the broader observed-stock backdrop, not as reserve releases.
- Europe: European Commission said on 2026-03-31 that EU countries are contributing about 20% to the IEA release and should coordinate any emergency stock use with demand restraint; on 2026-05-18 it said jet fuel is the main near-term constraint and any emergency release should be paired with fuel-saving measures. Eurostat's public article is lagged (May 2025 aggregate emergency stocks = 108.6 Mt), so for anything post-shock we need the databrowser or Commission/IEA proxies rather than the article alone.
- Japan: METI's petroleum statistics page was updated 2026-06-30 for May 2026. METI pressers show Japan's IEA allocation is 79.8 million barrels, with national reserves scheduled to start releasing on 2026-03-26 after private reserves; a 2026-05-15 METI release says the third national stockpile release was canceled because alternative procurement had improved and the 15-day private stockholding obligation reduction was maintained through 2026-06-15. This matters because Japan's response mixes public reserve drawdown with private-obligation relief.
- Korea: KNOC's official stockpiling pages / ESG materials say Korea operates nine stockpile bases with 146 million barrels of capacity and held about 100 million barrels of reserves in 2026 (99.49 million barrels at end-2024 in the ESG report). I could not find a public weekly release series like EIA's; for now Korea will likely be a snapshot endpoint unless MOTIE/KNOC publish a release announcement.
- Method skeleton:
  - Anchor on 2026-02-28 as the shock date and compare against the nearest pre-shock weekly/monthly observations.
  - Separate public strategic stocks, obligated industry stocks, and commercial stocks into different series; do not mix them.
  - For the U.S., use EIA weekly SPR plus WPSR commercial crude/products. For Japan, use METI monthly petroleum statistics plus release announcements. For Europe, use Eurostat emergency oil stock series / Commission notes. For Korea, use KNOC stockpile snapshots and any release notices.
  - Classify weekly/monthly moves as strategic release, commercial draw, or seasonal drift by comparing to same-week/month prior-year levels and the five-year average, then overlay policy announcements and stock-release dates.
  - Treat reporting lags explicitly: EIA weekly is near-real-time; METI is monthly with end-of-month publication; Eurostat article is lagged relative to the databrowser; IEA OMR is monthly and preliminary.

- Source breadcrumbs:
  - https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1
  - https://www.eia.gov/todayinenergy/detail.php?id=67625
  - https://ir.eia.gov/wpsr/wpsrsummary.pdf
  - https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict
  - https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
  - https://www.iea.org/reports/oil-market-report-march-2026
  - https://www.iea.org/reports/oil-market-report-may-2026
  - https://www.iea.org/reports/oil-market-report-june-2026
  - https://energy.ec.europa.eu/news/commission-calls-eu-countries-coordinate-measures-ensure-oil-security-supply-amid-middle-east-energy-disruption-2026-03-31_en
  - https://energy.ec.europa.eu/news/eu-continues-monitor-oil-market-situation-and-prepares-coordinated-response-address-jet-fuel-supply-2026-05-18_en
  - https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Emergency_oil_stocks_statistics
  - https://www.meti.go.jp/english/statistics/tyo/sekiyuso/index.html
  - https://www.meti.go.jp/english/speeches/press_conferences/2026/0313001.html
  - https://www.meti.go.jp/english/speeches/press_conferences/2026/0324001.html
  - https://www.meti.go.jp/english/press/2026/0515_003.html
  - https://www.knoc.co.kr/ENG/sub04/sub04_2_4.jsp
  - https://www.knoc.co.kr/ENG/sub03/sub03_3_3.jsp
  - https://www.knoc.co.kr/sub13/downloads/2025_esg_en_summary.pdf

- 2026-07-06: Finalized a compact table-ready CSV at `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv` that separates strategic releases, obligated/private stock relief, commercial draws, seasonal or baseline change, and reporting lags across the U.S., IEA/OECD collective action, EU, Japan, and Korea. The table uses only official or primary sources and carries explicit caveats where public reporting is partial:
  - U.S.: EIA weekly SPR series shows 415.441 mb on 2026-02-27 and 325.655 mb on 2026-06-26; Today in Energy says DOE released 17.5 mb between 2026-03-20 and 2026-04-24, and that the SPR release is structured as an exchange rather than a permanent supply addition. EIA WPSR says commercial crude inventories were 408.4 mb on 2026-06-26, down 3.8 mb w/w and about 7% below the five-year average.
  - IEA/OECD collective action: IEA announced 400 mb on 2026-03-11, then published a provisional country split on 2026-03-19 showing 280 mb public stocks, 119 mb obligated industry stocks, and 28 mb production increase, with the detailed split explicitly subject to change. IEA OMRs show observed stock draws of 129 mb in March, 117 mb in April, and 143 mb in May, plus OECD government inventories down 163 mb over Mar-May.
  - EU/Europe: European Commission said EU countries are contributing about 20% of the IEA release and that emergency stock releases, if needed, should be paired with fuel-saving measures. Eurostat's public explainer is lagged to May 2025, when EU emergency oil stocks were 108.6 Mt and commercial stocks were 45.7 Mt, down from 52.6 Mt in May 2024.
  - Japan: METI said Japan's allocation is 79.8 mb; private reserves began releasing on 2026-03-16, national reserves on 2026-03-26, and the 15-day private stockpiling obligation reduction (70 days to 55 days) was maintained through 2026-06-15. METI later canceled the third national stockpile release on 2026-05-15 because alternative procurement had improved.
  - Korea: IEA allocates 22.5 mb, but the public IEA table does not yet finalize the public/obligated split. KNOC's latest public ESG material says Korea held about 99.49 mb of strategic reserves at end-2024, across nine sites with 146 mb of capacity; no public weekly release series was found.
  - Acceptance criteria met: the output now distinguishes strategic releases, obligated/private relief, commercial draws, seasonal/baseline change, and reporting lag, and each row carries source URLs plus the 2026-07-06 access date.
- 2026-07-06: Marked done after local review. `data/derived/hormuz_s49_2_oecd_us_reserve_response.csv` parses cleanly and satisfies the requested distinction between strategic releases, commercial draws, seasonal/baseline changes, and reporting lags.
