---
id: "hormuz-r3v.2"
title: "Period-match observed national emergency-stock series to March-June"
type: "task"
status: "done"
priority: "P0"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "stocks"
  - "observed-data"
blocked_by: []
blocks: []
children: []
owner: "codex-subagent"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-05T19:00:00Z"
---

# Period-match observed national emergency-stock series to March-June

## Description

The r3v.1 tier tally puts only **157.1 mb (10.9%)** of the 1,441.48 mb net global supply
loss in tier T1 "directly observed," and all of it is U.S. weekly data: an 89.786 mb SPR
draw and a 67.317 mb commercial petroleum draw.

That understates what is actually observed. Other countries have real national stock
observations, but they are recorded over mismatched windows and so currently sit inside the
T3 "rest of world" residual of 140.897 mb:

- **Japan:** 58.75 mb combined national, private and producer-joint net draw, but measured
  through 30 April rather than 30 June.
- **Italy:** 12.09 mb Eurostat net emergency-stock decline, measured February-May.
- **Germany:** 2.70 mb Eurostat net decline, February-May.
- **France and Spain:** net emergency stocks *rose* through May, which is a real observation
  and not a zero.

Converting these to a clean March-June basis would move barrels from estimate to observation
without any new modelling assumption. This is the cheapest available reduction in the
unknown bucket.

## Acceptance Criteria

- A March-June observed national stock change for each IEA member with a published series,
  on a consistent month-end basis.
- Explicit handling of the gross-versus-net problem: a country can deliver emergency barrels
  while net national stocks rise, so net decline is a floor on delivery, not a measure of it.
- Recomputed T1/T3 totals in `hormuz_r3v_1_confidence_tiered_ledger.csv`, with the expected
  T1 rising from 157.1 mb toward roughly 228 mb (about 16%) if Japan and Italy alone are
  matched.
- Preserved distinction between government emergency stocks, obligated industry stocks and
  ordinary commercial stocks.
- No double counting against the ~290 mb IEA collective-release aggregate.

## Source Leads

- Japan METI emergency-release portal: https://www.enecho.meti.go.jp/category/others/energysecurity/
- Eurostat monthly emergency oil stocks: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_stk_oilm
- IEA 19 March country contribution table: https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions
- IEA 21 July execution statement: https://www.iea.org/news/iea-executive-director-statement-on-oil-markets
- Existing project ledger: `data/derived/hormuz_m8q_10_emergency_release_execution.csv`

## Work Notes

- 2026-08-05: Claimed for parallel work. Use exact March-June endpoints where published;
  distinguish primary government, obligated industry, and ordinary commercial stocks, and
  do not treat net change as gross emergency-program delivery.
- 2026-08-05: Added `scripts/build_r3v_2_period_matched_national_stocks.py`, producing
  `data/derived/hormuz_r3v_2_period_matched_national_stocks.csv` with 32 rows. The script
  freezes the official Eurostat `nrg_stk_oilm` response extracted on 5 August (API update
  timestamp 4 August 23:00 CEST), records `None` as missing rather than zero, and applies the
  existing project conversion of 7.33 barrels per tonne only after preserving native
  thousand-tonne endpoints.
- 2026-08-05: The strict public-data result is much thinner than the issue's expected
  roughly 70 mb T1 upgrade. Only Austria, Belgium, Czechia and Finland had February and June
  values in the Eurostat closing-emergency-stock series. Their signed net changes are
  +0.508, -1.388, +12.710 and +0.022 mb respectively; a negative draw is an observed build.
  Czechia is retained but held out of T1 because the June level falls 79.5% month on month,
  implying a 12.71 mb draw (5.8 times its 2.2 mb programme allocation) without national
  corroboration. The three continuity-passing observations net to **-0.859 mb**, i.e. a
  small observed build rather than a new draw.
- 2026-08-05: Germany (+2.696 mb draw), Italy (+12.087 mb draw), France (-0.132 mb draw/
  build), Spain (-6.360 mb draw/build) and most other Eurostat IEA members still stop at
  May or earlier. They remain useful partial observations in the new ledger but are not
  period-matched March-June measurements and therefore are not T1 inputs.
- 2026-08-05: Japan's official monthly quantity series now reaches May: national 30.67,
  private 26.01 and producer-country joint 0.76 million kl, versus 41.11, 25.73 and 1.79
  million kl in February. A late-June METI preliminary release reports 106, 94 and 3 days
  on 26 June. Scaling each May category volume by its June-days/May-days ratio gives a
  **provisional 72.136 mb signed net draw** through 26 June (national +70.975, private
  -5.318, joint +6.479 mb). This agrees closely with Kpler's earlier “more than 70 mb”
  estimate, but it is explicitly **not T1**: the endpoint is four days short of month-end
  and the June volume is derived from days of cover rather than directly reported tank
  quantities. The exact June monthly quantity release is scheduled after this audit's
  5 August cutoff.
- 2026-08-05: Korea is not assigned a stock draw. Yonhap quoted the deputy minister on
  26 May saying Seoul was still deciding the timing of its 22.46 mb release and regarded it
  as a final card. That is evidence against treating the allocation as delivered by May,
  but it is a dated execution statement, not a June tank series, and says nothing definitive
  about action after 26 May. It is therefore context only and excluded from T1.
- 2026-08-05: Preserved the ownership distinction. U.S. SPR is government stock; U.S.
  commercial petroleum is ordinary commercial inventory; Japan is split into national,
  obligated private-industry and producer-country joint stocks. The selected Eurostat
  aggregate covers all holders and does not expose ownership, so it is labelled mixed rather
  than assigned to government or industry.
- 2026-08-05: No national net change is equated with gross collective-action delivery.
  A country can release emergency barrels and replenish or reclassify stocks during the same
  interval; conversely an ordinary stock draw need not be an IEA action. Every row is marked
  as nested within the project's 298 mb IEA observed-stock composite and must not be added
  to the roughly 290 mb collective-release headline.

### Conservative handoff to r3v.1

Do not automatically promote the 72.136 mb Japan estimate or the 12.710 mb Czech observation.
The only new exact-window, continuity-passing public series are Austria, Belgium and Finland,
whose signed total is -0.859 mb. A presentation can show Japan's 72.1 mb as a high-quality
provisional cross-check, but calling it directly observed T1 would erase the distinction this
task was designed to enforce. Germany, France, Italy, Spain, Korea and the other incomplete
series stay inside the mixed-vintage rest-of-world observed residual until June endpoints are
published.

### Source breadcrumbs

- Eurostat monthly emergency stocks (`nrg_stk_oilm`, `STKCL_EUE`, `O4000`):
  https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_stk_oilm
- Japan METI February monthly quantities:
  https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260415oil.pdf
- Japan METI May monthly quantities (July publication):
  https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf/2026/260715oil.pdf
- Public mirror exposing the METI monthly series and 2026-05 quantities:
  https://opengov.jp/economy/energy/petroleum-reserves/
- Industry mirror of METI's 29 June preliminary release, with 26 June days of cover:
  https://www.mie-sekiyu.or.jp/wp-content/uploads/2026/07/123.pdf
- Korea deputy-minister execution statement, 26 May:
  https://en.yna.co.kr/view/AEN20260526010800320

### Validation

- `.venv/bin/python scripts/build_r3v_2_period_matched_national_stocks.py` passes its guards:
  32 unique row IDs; four Eurostat June endpoints; Czechia excluded by a deterministic
  continuity check; signed promoted total -0.858695 mb; and at least one observed build
  retained as negative rather than converted to zero.
