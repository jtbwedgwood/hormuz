---
id: "hormuz-a4d.5"
title: "Refresh the strategic and commercial stock ledger through mid-August"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-a4d"
labels:
  - "spr"
  - "inventories"
  - "durability"
  - "blog"
blocked_by: []
blocks:
  - "hormuz-a4d.6"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T19:00:00Z"
---

# Refresh the strategic and commercial stock ledger through mid-August

## Description

The draft's US section is an outline placeholder, but its two stated deliverables ("SPR drawn
down, talk about rates and how long it could last for") and its cited 90 mb SPR / 67 mb
commercial figures both need August data. The IEA collective release total is also stale, and
that release is arguably the single most important institutional response of the whole shock.

1. **US SPR weekly series** through the latest release. July vintage: 304.809 mb on 31 July,
   the lowest since 18 February 1983; 20.846 mb drawn from 26 June (0.5956 mb/d); March-June
   calendar rate 0.736 mb/d; 89.786 mb drawn in the matched March-June frame.
2. **US total commercial petroleum stocks** weekly. July vintage: 1,220.730 mb on 31 July,
   **built** 19.160 mb since 26 June — a reversal worth checking, because it is the draft's
   best evidence that the US is not on a fixed burn rate.
3. Recompute the days-to-physical-zero bounds (511.8 days at the July rate, 414.2 at the
   March-June rate) on August rates, keeping the GAO caveat that effective draw capability
   was 2.700 mb/d against 4.415 mb/d design and that >25% of the December 2025 inventory
   snapshot was unavailable.
4. **IEA collective emergency release delivered** beyond the ~290 mb reported through 21 July,
   and **member government-controlled stocks** beyond the ">1 billion barrels" 21 July figure.
   Refresh the 400-455 day arithmetic and restate it as the lower-bound calculation it is.
5. Any newly published national endpoints that could upgrade evidence tier: Japan METI June/
   July tank quantities (currently a provisional 72.1 mb draw derived from days of cover),
   Korea's release execution, and the missing Eurostat June months for Germany, France,
   Italy, Spain.

## Acceptance Criteria

- US SPR and commercial series extended to the latest weekly observation with restated rates.
- Updated collective-release-delivered total and remaining member holdings, with the
  as-of date stated.
- Recomputed runway bounds, still labelled as permissive physical-zero arithmetic.
- `hormuz_r3v_2_period_matched_national_stocks.csv` updated if any T1 upgrade is now possible.

## Dependency Notes

- Parent: `hormuz-a4d`
- Blocks: `hormuz-a4d.6`

## Work Notes

- 2026-08-18: Claimed for the August-vintage refresh. Scope is the latest published U.S.
  weekly SPR and total-commercial-petroleum endpoints, rate/runway calculations, IEA
  collective-action delivery and remaining controlled-stock statements, plus newly
  available exact national endpoints. Net stock changes will remain distinct from gross
  emergency-program delivery, and physical-zero arithmetic will retain operational caveats.
- 2026-08-18: Added `scripts/build_a4d_5_us_weekly_stocks.py` and its 24-row output
  `data/derived/hormuz_a4d_5_us_weekly_stocks.csv`. The 12 August EIA release ends on
  7 August: SPR **298.694 mb**, down **26.961 mb** from 26 June (**0.6419 mb/d**), and
  commercial petroleum excluding SPR **1,236.468 mb**, a **34.898 mb build** from
  26 June (**0.8309 mb/d build**). The latter strengthens the conclusion that ordinary
  commercial inventories do not follow a fixed crisis burn rate.
- 2026-08-18: Refreshed `hormuz_p2k_8_stock_exhaustion_bounds.csv`. At the latest six-week
  rate, permissive physical-zero arithmetic is **465.3 days** (15 November 2027); at the
  March-June calendar rate it is **405.9 days** (16 September 2027). These are not usable
  reserve horizons. GAO's December 2025 snapshot remains the best operational caveat:
  2.700 mb/d effective versus 4.415 mb/d design, with more than 25% of the then-413 mb
  inventory unavailable. The 298.694 mb level is the lowest since 28 January 1983.
- 2026-08-18: The public 12 August OMR says the pace of IEA emergency releases slowed in
  July, but gives no newer cumulative delivery or remaining government-stock quantity.
  Accordingly, the latest public quantified endpoints remain **around 290 mb delivered**
  and **more than 1 billion barrels of government-controlled stocks**, both as of 21 July.
  The 400/455-day divisions remain lower-bound hypothetical-zero calculations, not usable
  headroom or strict duration bounds.
- 2026-08-18: METI's 17 August monthly report supplies the exact June endpoint missing from
  the prior audit. February-to-June product-equivalent changes are a **71.955 mb public
  national draw**, **6.793 mb obligated-private build**, and **6.479 mb producer-country
  joint draw**, net **71.641 mb drawn**. Updated
  `hormuz_r3v_2_period_matched_national_stocks.csv` and promoted these exact rows to T1;
  with the signed Austria/Belgium/Finland total, newly promoted national observations net
  to **70.782 mb**. Source: https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040491305&fileKind=2
- 2026-08-18: Korea's ministry reported **21 mb** of gross strategic-crude swaps to refiners
  through 2 June, with later replenishment required; the measure wound down at end-June.
  This is real gross execution evidence but not a net tank endpoint and is not publicly
  reconciled to Korea's 22.5 mb IEA allocation, so it is retained outside T1 and outside the
  IEA aggregate. Sources: https://en.yna.co.kr/view/AEN20260602006300320 and
  https://en.yna.co.kr/view/AEN20260630004352320
- 2026-08-18: Eurostat `nrg_stk_oilm`, updated 13 August, still stops at May for Germany,
  France, Italy and Spain. No T1 upgrade is possible for those four. The frozen public API
  observations for countries already reporting June are unchanged from the 5 August audit.
- 2026-08-18: Updated `docs/hormuz-shock-absorption-durability.md` and `data/manifest.csv`.
  Validation passed in `.venv`: all three builders run cleanly, `py_compile` passes, CSVs
  parse with unique row IDs, and endpoint/rate/Japan/Korea guards pass. No dependency change.

### Handoff to a4d.6

Use **71.641 mb** rather than the provisional 72.136 mb for Japan. The exact signed national
T1 upgrade is **70.782 mb** after including Austria, Belgium and Finland. Preserve nesting:
these national net changes are already inside the August OMR observed-stock aggregate and
must not be added to the IEA collective-release total. Korea's 21 mb is a gross swap flow,
not a net endpoint. The IEA 290 mb / >1 billion barrel figures have not received a newer
public numeric update.
