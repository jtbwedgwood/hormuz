---
id: "hormuz-r3v.3"
title: "Add the realized price path as a shortage-severity diagnostic"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-r3v"
labels:
  - "oil"
  - "prices"
  - "cross-check"
blocked_by: []
blocks: []
children: []
owner: "codex"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T21:20:00Z"
---

# Add the realized price path as a shortage-severity diagnostic

## Description

The historical accounting was deliberately volume-only and contained no realized benchmark
series. Add a compact price context as one market outcome, without treating price as a
sufficient statistic for whether the measured volume loss was a binding physical shortage.

Price mixes physical balance with news, expectations, risk premia, policy, macro demand and
financial positioning. The diagnostic value is therefore limited to context:

- If Brent and regional differentials moved **far less** than a 1.44 bn bbl supply loss would
  imply, that is independent evidence that a large part of the February-to-July revision is
  soft — ordinary forecast revision, demand-side weakness, or supply that was never really
  lost — which would corroborate a large T4 bucket.
- If prices moved **more** than the volumes imply, that points the other way: toward genuine
  scarcity plus risk premium, and toward the residual containing real unobserved draws.

This is explicitly **not** a price forecast and must not become one. It is a consistency
check on the volume reconstruction.

## Acceptance Criteria

- Daily or monthly Brent and WTI spot series covering at least January 2026 to date, stored
  under `data/external/` and registered in `data/manifest.csv`.
- Time-spread structure (prompt versus deferred) where available, since backwardation is the
  cleaner scarcity signal than flat price.
- A short comparison of the realized price response against historical supply-shock
  elasticities, reusing the historical comparison work in `hormuz-4j7` where possible.
- An explicit statement of what the observed price response implies about the plausible size
  of the 308.171 mb unreconciled residual, in both directions.
- No forward price path, and no attribution of price moves to Hormuz without noting the
  concurrent Russia-Ukraine and macro drivers.

## Source Leads

- EIA spot price series (Brent, WTI): https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm
- EIA STEO price tables in the existing February and July workbooks already in the manifest
- Project historical shock comparison: `data/derived/hormuz_4j7_3_historical_comparison_metric_panel.csv`

## Work Notes

- 2026-08-05: Claimed with reduced evidentiary weight per user direction. The realized flat
  price and time spread will be reported as contextual market outcomes only. No inference
  that price is a sufficient statistic for physical scarcity is permitted; contemporaneous
  news, geopolitical risk, expectations of reopening, emergency releases, macro demand,
  positioning, and unrelated supply events must be acknowledged.
- 2026-08-05: Added `scripts/build_r3v_3_price_context.py`, which downloads the public
  EIA/FRED daily Brent and WTI spot series and writes 145 observations from 1 January through
  the latest common observation on 27 July to
  `data/external/prices/hormuz_r3v_3_daily_price_context.csv`. It also generates 24 period
  summaries in `data/derived/hormuz_r3v_3_price_context_summary.csv`. Added `xlrd==2.0.2`
  to `requirements.txt` while checking EIA's public WTI futures workbooks; those contract-1
  and contract-2 histories end on 5 April 2024, so no current time-spread series is presented.
- 2026-08-05: Descriptive result: Brent averaged $68.69/b in the 1 January-27 February
  baseline, $103.13 in March, $117.29 in April, $107.14 in May, $85.40 in June and $82.11
  in July through the available observations. It peaked at $138.21 on 7 April and ended the
  current file at $91.82 on 27 July. The Brent-WTI spread is included as geographic context.
- 2026-08-05: Interpretation: this path confirms a large and volatile market response but
  does **not** bound the 308.171 mb residual in either direction. The April peak can reflect
  perceived tail risk and news; the June decline can reflect reopening expectations,
  emergency releases and lower demand without proving the physical shortage was small.
  Historical elasticities are not applied because duration, policy buffers, expectations and
  shock definitions are not comparable. This implements the user's reduced-weight framing.
- 2026-08-05: Validation passed: script compilation and regeneration, unique date rows,
  unique summary row IDs, chronological ordering, and `git diff --check`.
- 2026-08-06: Reopened as a narrow follow-up for `hormuz-p2k.13`. The extension will recover
  a current prompt-versus-deferred futures structure where public access permits and use it
  only to discriminate discretionary storage from mechanically required voyage float. It
  will not treat the curve as a shortage-severity sufficient statistic or forecast prices.
- 2026-08-06: Extended `scripts/build_r3v_3_price_context.py` to download eight public daily
  futures-close histories from Yahoo Finance's chart endpoint: rolling front, September 2026,
  October 2026 and December 2026 contracts for WTI (`CL`) and CME Brent Last Day financial
  futures (`BZ`). The builder writes 148 daily rows through 5 August to
  `data/external/prices/hormuz_r3v_3_daily_time_spreads.csv` and 32 period summaries to
  `data/derived/hormuz_r3v_3_time_spread_summary.csv`. The daily file contains both rolling
  front-minus-December and fixed September-minus-October measures, always using
  `near - deferred`, so positive values mean backwardation.
- 2026-08-06: Data limitation is explicit. Yahoo's public close histories are a convenient
  transport layer, not an exchange-certified historical-settlement archive. The continuous
  front series also stitches and rolls contracts. The fixed September-October pair avoids
  stitching but was not the actual prompt pair in March-June. EIA's free first- and
  second-contract histories still stop on 5 April 2024, while CME directs historical daily
  bulletin users to DataMine. The new series is therefore **medium-weight regime evidence**,
  not a tick-accurate official settlement dataset.
- 2026-08-06: Three primary cross-checks support the regime classification. CME's 23 March
  commentary reported May 2026 WTI about **$12/b above September** and called the
  backwardation extreme:
  https://www.cmegroup.com/newsletters/fresh-from-the-trading-room/2026-03-23.html . CME's
  April research said December WTI had traded as much as **$40/b below May or June**:
  https://www.cmegroup.com/insights/economic-research/2026/implications-of-wti-oil-futures-in-backwardation-amid-the-supply-crunch.html . Finally,
  CME's official 5 August energy bulletin reports Micro WTI September at **$75.22/b** and
  October at **$74.05/b**, an exact **+$1.17/b** match to the convenience series:
  https://www.cmegroup.com/daily_bulletin/current/Section61_Energy_Futures_Products.pdf .
- 2026-08-06: March-June result: WTI rolling-front minus December averaged **+$15.943/b**
  (range +$1.150 to +$39.430) and was backwardated on **84/84** observed days. Fixed WTI
  September-minus-October averaged **+$2.183/b** (range +$0.290 to +$4.140), also 84/84.
  Brent front-minus-December averaged **+$15.037/b** (range -$0.170 to +$38.730) and was
  backwardated on **82/84** days. Fixed Brent September-minus-October averaged **+$2.226/b**
  (range -$0.080 to +$4.510), backwardated on **83/84** days. Front-December monthly means
  declined from WTI/Brent +$17.665/+20.186 in March and +$22.179/+19.968 in April to
  +$6.450/+4.121 in June, but the dominant regime remained backwardation.
- 2026-08-06: Interpretation for `hormuz-p2k.13`: the very strong March-May backwardation
  makes **profit-seeking carry storage** an implausible main explanation for rising oil on
  water, because a holder was accepting a large prompt-to-deferred price penalty even before
  freight, insurance and financing. It does **not** exclude involuntarily blocked or stranded
  Gulf cargoes, port congestion, sanctioned-fleet dwell, classification effects, or the
  mechanically larger voyage float created by longer routes. Nor does it establish how many
  barrels belong to any mechanism. June flattening weakens the discriminator at the margin;
  the handful of shallow Brent contango observations cannot explain the earlier large build.
- 2026-08-06: Updated the two original price-context manifest endpoints through 3 August and
  registered both time-spread outputs. Validation passed: compilation and clean regeneration;
  148 unique chronological daily rows; 32 unique summary IDs; all March-June WTI observations
  positive under both spread definitions; exact agreement of the 5 August WTI Sep-Oct close
  pair with the CME bulletin; and CSV widths consistent.
