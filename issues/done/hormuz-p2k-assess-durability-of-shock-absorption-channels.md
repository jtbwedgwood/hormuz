---
id: "hormuz-p2k"
title: "Assess the durability of each shock-absorption channel"
type: "epic"
status: "done"
priority: "P0"
parent: ""
labels:
  - "oil"
  - "projection"
  - "durability"
  - "buffers"
blocked_by: []
blocks: []
children:
  - "hormuz-p2k.1"
  - "hormuz-p2k.2"
  - "hormuz-p2k.3"
  - "hormuz-p2k.4"
  - "hormuz-p2k.5"
  - "hormuz-p2k.6"
  - "hormuz-p2k.7"
  - "hormuz-p2k.8"
  - "hormuz-p2k.9"
  - "hormuz-p2k.10"
  - "hormuz-p2k.11"
  - "hormuz-p2k.12"
  - "hormuz-p2k.13"
owner: "jtbwedgwood@gmail.com"
created_at: "2026-08-05T00:00:00Z"
updated_at: "2026-08-06T23:59:00Z"
---

# Assess the durability of each shock-absorption channel

## Description

Forward-looking workstream, deliberately framed to avoid the standard public format of
"if Hormuz stays closed until X, oil hits $Y." That format requires jointly predicting
demand elasticity, political decisions and risk premium, and is not defensible.

This epic asks a different and answerable question: **the shock has been absorbed through
several channels; how sustainable is each, and what happens as the cheap ones exhaust?**
Buffers have levels and burn rates, so exhaustion arithmetic is mechanical rather than
predictive. Capacity ceilings are engineering facts. Statutory stock floors are published.

### Core reframe

Do not model a "break point" at which prices spike. Price is continuous and already
responded to expectations. What actually happens as buffers deplete is a **composition
shift in which channel absorbs the marginal barrel**, along an implicit cost ordering:

> stocks (cheap, fast) → rerouting (cheap, capped) → voluntary conservation (moderate)
> → forced demand destruction (expensive, welfare-destroying)

The defensible forward claim is therefore about the **rising marginal cost of absorption**,
conditional on closure duration as a scenario switch, not a prediction.

### The channels have qualitatively different failure modes

This is the main analytical trap to avoid. Do not assign a duration to each channel and
compare them; they are not commensurable.

| Channel | Mar-Jun mb | Time signature | What "breaking" means |
|---|---:|---|---|
| Bypass rerouting | 362 | Step change, does not decay | Capacity ceiling (largely reached) or catastrophic single-point failure |
| Non-Gulf production | 57 net | Improves slowly | Nothing breaks; grows on 6-36 month lags |
| Inventory draw | 298 | Genuinely exhaustible | Hits statutory/operational floors, not zero |
| Foregone build | 396 | Already fully spent | Cannot contribute again |
| Demand reduction | 439 | Bifurcated by cost tier | Depends entirely on composition |

Two consequences worth stating up front:

- **Foregone build is structurally exhausted.** Roughly 27% of absorption to date came from
  an expected surplus failing to materialize. That flexibility does not recur. See `p2k.5`.
- **Bypass is the most durable channel in normal operation and the most dangerous in the
  tail.** Its analysis should be a vulnerability assessment, not a depletion curve.

## Acceptance Criteria

- A buffer balance sheet covering every absorption channel with level, floor or ceiling,
  burn rate, headroom and confidence tier.
- A marginal-absorber timeline at 6, 12 and 18 months of continued closure.
- Demand reduction classified by economic cost tier, qualitatively and by country.
- No price forecast anywhere in the output.
- Uncertainty from the historical accounting propagated forward rather than silently
  resolved: roughly 29% of historical absorption is tier T4, and the durability of a buffer
  that could not be measured cannot be asserted.

## Work Notes

- 2026-08-05: Opened following a consultant discussion. Children `.1` to `.7` scoped below.
  `.2` and `.5` are the highest-value entry points: the June partial reopening is a natural
  experiment on the cost ordering, and the forward expected-build path is already sitting in
  the frozen February STEO.
- 2026-08-05: `.4` is a correctness check on the historical accounting rather than a forward
  question, but it is filed here because it materially changes the durability picture. If
  part of the demand slice is destocking, that portion is exhaustible rather than
  indefinitely sustainable.
- 2026-08-05: Claimed for parallel execution. First wave assigns `.2`, `.4`, and `.5` to
  independent research agents while the parent builds the `.1` integration scaffold. Price
  forecasts remain explicitly out of scope; all forward results are conditional buffer and
  composition scenarios.
- 2026-08-05: Completed all seven children. The central 19-row buffer ledger is
  `data/derived/hormuz_p2k_1_absorption_buffer_balance_sheet.csv`; the reader synthesis is
  `docs/hormuz-shock-absorption-durability.md`. Child artifacts cover the June reopening,
  country/mechanism economic-cost tiers, China apparent-demand versus opaque destocking,
  foregone-build exhaustion, historical-parameter transferability and bypass-route
  vulnerability. No price forecast was produced.
- 2026-08-06: Completed follow-ups `.8`-`.11`. They add explicit stock bounds, separate the
  July STEO reopening branch from a bounded no-reopening balance, resolve the March-June
  demand denominator to country scaffolds, and quantify 1.25x/1.5x/2x demand-adjustment
  scenarios with country-sector landing evidence. The synthesis now distinguishes existing
  absorber flows from genuinely incremental headroom and refuses a false single stock-
  exhaustion date.
- 2026-08-06: Completed `.12`-.13. March global oil on water is corrected to -117 mb; the
  regional +100 mb Gulf build is explicitly nested and the crude 568 mb onshore arithmetic
  is retired. Onshore-accessible draw is 316/351/386 mb, but reclassifying only the observed
  side closes zero of the 308.171 mb same-bound residual. The causal audit separates
  57/91/125 mb of persistent longer-route float from 66/111.6/151.8 mb of ordinary June
  system refill; all voyage float receives zero usable-headroom credit.

### Epic verdict

- The historical cheap cushion is less repeatable than headline shares imply: 396.078 mb of
  foregone build is fully spent, bypass is continuing but almost capped, and the genuinely
  exhaustible global inventory channel lacks a public usable-headroom-above-floor measure.
- The 308.171 mb implied-versus-observed stock residual remains a material measurement and
  mechanism uncertainty, not a normal or projectable buffer. All T4 absorption remains
  explicit at 422.284 mb base, 29.3% of the market-clearing bridge.
- China product destocking is plausible but unproven; the only defensible treatment is a
  0/14.972/29.943 mb zero-sum sensitivity from demand-side T4 into opaque inventory T4.
- At longer horizons the marginal barrel shifts toward demand adjustment. The country matrix
  makes the welfare ordering explicit: tier-2 industrial and mobility drag dominates the
  broad six-month margin, while tier-3 essential-service and livelihood failures become more
  prevalent in fragile importers by 12-18 months.
