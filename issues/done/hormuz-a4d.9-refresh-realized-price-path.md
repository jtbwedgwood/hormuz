---
id: "hormuz-a4d.9"
title: "Refresh the realized price and spread path through mid-August"
type: "task"
status: "done"
priority: "P2"
parent: "hormuz-a4d"
labels:
  - "prices"
  - "context"
  - "blog"
blocked_by: []
blocks: []
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-18T00:00:00Z"
updated_at: "2026-08-18T23:00:00Z"
---

# Refresh the realized price and spread path through mid-August

## Description

The draft explicitly declines to forecast prices, which is the right call, but it also omits
the **realized** path entirely — and that path is a large part of the answer to its own
framing question, "how is business continuing as usual?" Brent went $61/b at the start of
2026, $72 pre-shock, above $100 on 12 March, peaked at $138 on 7 April, then averaged $85 in
June and $82 through 27 July. A reader told only about 1.4 billion missing barrels and no
price relief will not understand why the world looks calm.

1. Extend `hormuz_r3v_3_price_context_summary.csv` (Brent, WTI, Brent-WTI spread) through the
   publication date, and check whether the July re-closure moved prices at all — a
   near-non-response would itself be the story.
2. Extend `hormuz_r3v_3_time_spread_summary.csv`. July vintage: WTI front-minus-December was
   backwardated on all 84 March-June observations and Brent on 82 of 84, which is the
   project's evidence against profit-seeking carry storage. Confirm the structure holds.
3. Refresh product cracks / retail pass-through where already collected, since the US section
   claims "elevated gas prices but no demand reduction" and North America revised **up** by
   16.6 mb — the fiscal-shielding story needs a current price anchor.

## Acceptance Criteria

- Price and spread series extended to the publication date.
- A short, blog-usable price chronology paragraph that stays diagnostic and makes no
  barrels-from-prices inference, consistent with the project's existing rule.
- Explicit note on whether the July re-closure produced a price response.

## Dependency Notes

- Parent: `hormuz-a4d`

## Work Notes

- 2026-08-18: Claimed for extension through the publication cutoff. Scope includes realized
  Brent/WTI spot prices, prompt/deferred curve structure, and already-collected U.S. product
  or retail pass-through anchors. Prices remain descriptive chronology and a storage-regime
  discriminator only; no price-to-barrels inference or forward price path will be made.
- 2026-08-18: Extended `scripts/build_r3v_3_price_context.py` to the 18 August publication
  cutoff. Official EIA spot observations transported by FRED currently end 11 August
  (**156 daily rows**); exchange-listed futures closes transported by Yahoo reach the latest
  completed 17 August session (**156 rows**); official weekly EIA retail observations reach
  17 August. The date differences are source reporting frequency/lag, not silently filled
  days.
- 2026-08-18: Regenerated `hormuz_r3v_3_price_context_summary.csv` with explicit July
  re-closure, August-to-publication, and post-reclosure windows. The re-closure was **not** a
  near-non-response: Brent moved from **$69.56/b on 6 July** to **$76.50 on 8 July** and
  **$105.32 on 23 July**, then stood at **$93.26 on 11 August**. WTI moved from **$69.60**
  to **$93.08** by 23 July and **$84.77** on 11 August. This sequencing is descriptive;
  security news, reopening expectations, policy, macro demand, other supply and positioning
  remain concurrent drivers.
- 2026-08-18: Regenerated `hormuz_r3v_3_time_spread_summary.csv`. The original matched-frame
  results are unchanged: WTI front-minus-December backwardated on **84/84** March-June
  observations and Brent on **82/84**. From 8 July through 17 August both front-minus-
  December measures were backwardated on **every observed session**. August means were
  **+$3.96/b WTI** and **+$3.77/b Brent**. This weighs against voluntary carry storage after
  freight/insurance/financing, but not against blocked cargoes, congestion, sanctioned dwell
  or longer voyage float. Historical closes remain a Yahoo transport of exchange-listed
  contracts, not certified settlements; the expired Brent September contract is preserved
  from the prior capture only through 31 July.
- 2026-08-18: Added official EIA product/retail artifacts:
  `data/external/prices/hormuz_a4d_9_product_retail_prices.csv` and
  `data/derived/hormuz_a4d_9_product_retail_price_summary.csv`. They contain U.S. Gulf Coast
  regular gasoline, ULSD and jet-fuel spot prices; U.S. regular-gasoline and on-highway-
  diesel retail prices; and transparent product-spot-minus-Brent/42 gross crack proxies.
  Those proxies are **not refinery margins**: they omit yields, fuel/losses, basis, logistics,
  compliance, finance and taxes.
- 2026-08-18: On 17 August U.S. regular gasoline was **$4.049/gal** and on-highway diesel
  **$5.454/gal**, respectively **41.7% and 50.6% above** their January-February means. On the
  latest daily product observation, 11 August, Gulf Coast gasoline/diesel/jet were
  **$3.214/$4.248/$3.814 per gallon**. These are strong realized pass-through anchors, but
  prices alone do not establish U.S. demand reduction.
- 2026-08-18: Added a blog-ready chronology paragraph to
  `docs/hormuz-what-happened-to-the-barrels.md`, updated the six price/product manifest rows,
  and preserved the project's no-price-to-barrels rule. No forward price path was added.
- 2026-08-18: Validation passed in `.venv`: compilation; two consecutive deterministic
  builds with identical SHA-256 outputs; sorted unique daily dates; unique summary IDs;
  exact futures-spread arithmetic; expected March-June and post-reclosure backwardation
  guards; endpoint guards for 11/17 August reporting dates; CSV parsing; and unique manifest
  IDs. No dependency or `requirements.txt` change was needed.
